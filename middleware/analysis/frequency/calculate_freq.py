"""
Frequency Calculation Module
Calculates total frequencies for each group by aggregating equipment failure rates
"""
import os
import sys
import csv
from dataclasses import dataclass
from typing import Dict, Any, Optional, List
from collections import defaultdict

from frequency_database import get_equipment_failure_rates

# Leak adapter import (used only when enriching with leak profiles)
_LEAK_ADAPTER_PATH = os.path.abspath(
    os.path.join(
        os.path.dirname(__file__),
        "../consequence/models/IQRAModeling/IQRA_software/LeakModel/LeakCalculations",
    )
)
if _LEAK_ADAPTER_PATH not in sys.path:
    sys.path.insert(0, _LEAK_ADAPTER_PATH)
try:
    from leak_scenario_adapter import attach_leak_profiles, DEFAULT_HOLE_DIAMETERS_MM as ADAPTER_DEFAULT_HOLES
except Exception:
    attach_leak_profiles = None
    ADAPTER_DEFAULT_HOLES = None


_FALLBACK_HOLE_MAP = {
    "1-3mm": 3.0,
    "3-10mm": 10.0,
    "10-50mm": 50.0,
    "50-150mm": 150.0,
    ">150mm": 175.0,
}


@dataclass
class LeakScenario:
    """Represents a single leak size scenario for a group."""

    category: str
    hole_diameter_mm: Optional[float]
    frequency_total: float
    frequency_full_pressure: float
    frequency_zero_pressure: float
    leak_rate_kg_s: Optional[float] = None


@dataclass
class GroupScenarioSet:
    """Holds all leak-size scenarios for a group."""

    group_number: int
    operational_conditions: Dict[str, Any]
    equipments: List[Dict[str, Any]]
    scenarios: List[LeakScenario]


def load_groups_from_cache(cache_file_path: str = None):
    """
    Load all groups from the cache CSV file
    
    Args:
        cache_file_path: Optional path to cache file. If None, uses default location.
    
    Returns:
        Dictionary with group numbers as keys, each containing:
        {
            'operational_conditions': {
                'fuel_phase': str,
                'pressure': float,
                'temperature': float,
                'size': float
            },
            'equipments': [
                {
                    'name': str,
                    'size': str,
                    'ea': int
                },
                ...
            ]
        }
    """
    if cache_file_path is None:
        cache_file_path = os.path.join(
            os.path.dirname(__file__), 
            '../../data-input/frequency/group_cache.csv'
        )
    
    if not os.path.exists(cache_file_path):
        return {}
    
    groups = defaultdict(lambda: {
        'operational_conditions': {},
        'equipments': []
    })
    
    with open(cache_file_path, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            group_num = int(row['Group_Number'])
            
            # Set operational conditions (same for all equipment in group)
            if not groups[group_num]['operational_conditions']:
                groups[group_num]['operational_conditions'] = {
                    'fuel_phase': row['Fuel_Phase'],
                    'pressure': float(row['Pressure_Bar']),
                    'temperature': float(row['Temperature_K']),
                    'size': float(row['Size_mm'])
                }
            
            # Add equipment
            groups[group_num]['equipments'].append({
                'name': row['Equipment_Name'],
                'size': row['Equipment_Size'],
                'ea': int(row['Equipment_EA'])
            })
    
    return dict(groups)


def load_groups_from_manager(group_manager) -> dict:
    """Load group data from an in-memory FrequencyGroupManager."""
    if group_manager is None:
        return {}
    try:
        group_data = group_manager.get_all_group_data()
        return dict(group_data)
    except Exception:
        return {}


def calculate_group_frequencies(group_data: dict):
    """
    Calculate total frequencies for a single group by summing all equipment failure rates
    
    Args:
        group_data: Dictionary containing:
            - operational_conditions: dict with fuel_phase, pressure, temperature, size
            - equipments: list of equipment dicts with name, size, ea
    
    Returns:
        Dictionary with aggregated failure rates by category:
        {
            'category_name': {
                'total': float,
                'full_pressure': float,
                'zero_pressure': float
            },
            ...
        }
    """
    # Initialize aggregated results
    aggregated_rates = defaultdict(lambda: {
        'total': 0.0,
        'full_pressure': 0.0,
        'zero_pressure': 0.0
    })
    
    # Process each equipment in the group
    for equipment in group_data['equipments']:
        try:
            # Get failure rates from database
            failure_rates = get_equipment_failure_rates(
                equipment['name'],
                equipment['size']
            )
            
            # Multiply by EA and add to aggregated rates
            ea = equipment['ea']
            for rate in failure_rates:
                category = rate['category']
                aggregated_rates[category]['total'] += float(rate['total']) * ea
                aggregated_rates[category]['full_pressure'] += float(rate['full_pressure']) * ea
                aggregated_rates[category]['zero_pressure'] += float(rate['zero_pressure']) * ea
        
        except Exception as e:
            print(f"Error processing equipment {equipment['name']}: {str(e)}")
            continue
    
    return dict(aggregated_rates)


def calculate_all_group_frequencies(
    cache_file_path: str = None,
    group_manager=None,
    groups: Optional[Dict[int, Dict[str, Any]]] = None,
):
    """
    Calculate frequencies for all groups in the cache
    
    Args:
        cache_file_path: Optional path to cache file
    
    Returns:
        Dictionary with group numbers as keys:
        {
            group_number: {
                'operational_conditions': {...},
                'equipments': [...],
                'frequencies': {
                    'category_name': {
                        'total': float,
                        'full_pressure': float,
                        'zero_pressure': float
                    },
                    ...
                }
            },
            ...
        }
    """
    # Load all groups: prefer in-memory objects when provided.
    if groups is None:
        groups = load_groups_from_manager(group_manager)
    if not groups:
        groups = load_groups_from_cache(cache_file_path)
    
    # Calculate frequencies for each group
    results = {}
    for group_num, group_data in groups.items():
        frequencies = calculate_group_frequencies(group_data)
        results[group_num] = {
            'operational_conditions': group_data['operational_conditions'],
            'equipments': group_data['equipments'],
            'frequencies': frequencies
        }
    
    return results


def calculate_all_group_frequencies_with_leaks(
    cache_file_path: str = None,
    density_overrides: dict | None = None,
    hole_diameters_mm: dict | None = None,
):
    """Calculate frequencies and attach leak profiles per leak-size bin.

    Returns the same structure as calculate_all_group_frequencies but with an
    additional `leak_profiles` key per group. If the leak adapter is unavailable,
    this raises RuntimeError to make the failure obvious to callers.
    """
    base = calculate_all_group_frequencies(cache_file_path)

    if attach_leak_profiles is None:
        raise RuntimeError("leak_scenario_adapter is not available on PYTHONPATH")

    return attach_leak_profiles(
        base,
        density_overrides=density_overrides,
        hole_diameters_mm=hole_diameters_mm,
    )


def _resolve_hole_map(custom_map: Optional[Dict[str, float]]) -> Dict[str, float]:
    base = dict(ADAPTER_DEFAULT_HOLES) if ADAPTER_DEFAULT_HOLES else dict(_FALLBACK_HOLE_MAP)
    if custom_map:
        base.update({k: float(v) for k, v in custom_map.items()})
    return base


def build_group_scenarios(
    group_results: Dict[int, Dict[str, Any]],
    hole_diameters_mm: Optional[Dict[str, float]] = None,
) -> Dict[int, GroupScenarioSet]:
    """Convert raw frequency (and optional leak profile) data into scenario objects."""
    hole_map = _resolve_hole_map(hole_diameters_mm)
    out: Dict[int, GroupScenarioSet] = {}

    for group_num, group_data in group_results.items():
        freqs = group_data.get("frequencies", {})
        leak_profiles = group_data.get("leak_profiles", {}).get("categories", {}) if group_data.get("leak_profiles") else {}

        scenarios: List[LeakScenario] = []
        for category, rates in freqs.items():
            if category == "Total":
                continue
            hole_d = hole_map.get(category)
            leak_rate = None
            if category in leak_profiles:
                leak_rate = leak_profiles[category].get("leak_rate_kg_s")

            scenarios.append(
                LeakScenario(
                    category=category,
                    hole_diameter_mm=hole_d,
                    frequency_total=float(rates.get("total", 0.0)),
                    frequency_full_pressure=float(rates.get("full_pressure", 0.0)),
                    frequency_zero_pressure=float(rates.get("zero_pressure", 0.0)),
                    leak_rate_kg_s=leak_rate,
                )
            )

        out[group_num] = GroupScenarioSet(
            group_number=group_num,
            operational_conditions=group_data.get("operational_conditions", {}),
            equipments=group_data.get("equipments", []),
            scenarios=scenarios,
        )

    return out


def calculate_group_scenarios(
    cache_file_path: str = None,
    hole_diameters_mm: Optional[Dict[str, float]] = None,
) -> Dict[int, GroupScenarioSet]:
    """Return object model of groups with 5 leak-size scenarios each (no leak rates)."""
    base = calculate_all_group_frequencies(cache_file_path)
    return build_group_scenarios(base, hole_diameters_mm=hole_diameters_mm)


def calculate_group_scenarios_with_leaks(
    cache_file_path: str = None,
    density_overrides: dict | None = None,
    hole_diameters_mm: dict | None = None,
) -> Dict[int, GroupScenarioSet]:
    """Return object model with leak rates attached (via leak_scenario_adapter)."""
    enriched = calculate_all_group_frequencies_with_leaks(
        cache_file_path=cache_file_path,
        density_overrides=density_overrides,
        hole_diameters_mm=hole_diameters_mm,
    )
    return build_group_scenarios(enriched, hole_diameters_mm=hole_diameters_mm)


def get_frequency_summary(group_frequencies: dict):
    """
    Generate a summary of frequencies across all groups
    
    Args:
        group_frequencies: Output from calculate_all_group_frequencies()
    
    Returns:
        List of dictionaries suitable for display:
        [
            {
                'group_number': int,
                'fuel_phase': str,
                'pressure': float,
                'temperature': float,
                'size': float,
                'equipment_count': int,
                'total_frequency': float  # Sum of all 'total' values
            },
            ...
        ]
    """
    summary = []
    
    for group_num, data in group_frequencies.items():
        ops = data['operational_conditions']
        
        # Calculate total frequency (sum of all leak categories)
        total_freq = sum(
            freq_data['total'] 
            for freq_data in data['frequencies'].values()
        )
        
        summary.append({
            'group_number': group_num,
            'fuel_phase': ops['fuel_phase'],
            'pressure': ops['pressure'],
            'temperature': ops['temperature'],
            'size': ops['size'],
            'equipment_count': len(data['equipments']),
            'total_frequency': total_freq
        })
    
    return sorted(summary, key=lambda x: x['group_number'])


if __name__ == "__main__":
    print("Calculating frequencies for all groups...\n")
    
    try:
        # Calculate frequencies for all groups
        results = calculate_all_group_frequencies()
        
        if not results:
            print("No groups found in cache.")
        else:
            # Display results for each group
            for group_num in sorted(results.keys()):
                data = results[group_num]
                ops = data['operational_conditions']
                
                print(f"=== Group {group_num} ===")
                print(f"Operational Conditions:")
                print(f"  Fuel Phase: {ops['fuel_phase']}")
                print(f"  Pressure: {ops['pressure']} bar")
                print(f"  Temperature: {ops['temperature']} K")
                print(f"  Size: {ops['size']} mm")
                print(f"\nEquipment ({len(data['equipments'])} items):")
                for eq in data['equipments']:
                    print(f"  - {eq['name']} ({eq['size']}) x {eq['ea']}")
                
                print(f"\nAggregated Frequencies by Leak Size Category:")
                for category, rates in sorted(data['frequencies'].items()):
                    if category != 'Total':  # Skip total for now
                        print(f"  {category}:")
                        print(f"    Total: {rates['total']:.6f}")
                        print(f"    Full Pressure: {rates['full_pressure']:.6f}")
                        print(f"    Zero Pressure: {rates['zero_pressure']:.6f}")
                
                # Show total if available
                if 'Total' in data['frequencies']:
                    rates = data['frequencies']['Total']
                    print(f"  Total (All Categories):")
                    print(f"    Total: {rates['total']:.6f}")
                    print(f"    Full Pressure: {rates['full_pressure']:.6f}")
                    print(f"    Zero Pressure: {rates['zero_pressure']:.6f}")
                
                print("\n" + "="*50 + "\n")
            
            # Display summary
            print("\n=== SUMMARY ===")
            summary = get_frequency_summary(results)
            print(f"{'Group':<8} {'Phase':<10} {'Press.':<8} {'Temp.':<8} {'Size':<8} {'Equip.':<8} {'Total Freq.':<12}")
            print("-" * 80)
            for item in summary:
                print(f"{item['group_number']:<8} {item['fuel_phase']:<10} "
                      f"{item['pressure']:<8.1f} {item['temperature']:<8.1f} "
                      f"{item['size']:<8.1f} {item['equipment_count']:<8} "
                      f"{item['total_frequency']:<12.6f}")
    
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
