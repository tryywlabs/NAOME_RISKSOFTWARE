"""
Frequency Calculation Module
Calculates total frequencies for each group by aggregating equipment failure rates
"""
import os
import csv
from collections import defaultdict

from frequency_database import get_equipment_failure_rates, convert_equipment_size_to_db_format


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


def calculate_all_group_frequencies(cache_file_path: str = None):
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
    # Load all groups
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
