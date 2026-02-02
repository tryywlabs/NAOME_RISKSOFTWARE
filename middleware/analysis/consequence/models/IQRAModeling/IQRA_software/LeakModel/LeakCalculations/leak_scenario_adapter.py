"""
Bridge frequency leak-size categories to consequence leak calculations.

Inputs:
    frequency_results: output of calculate_all_group_frequencies()
        {
            group_number: {
                'operational_conditions': { fuel_phase, pressure, temperature, size },
                'equipments': [...],
                'frequencies': {
                    '1-3mm': { 'total': float, ... },
                    ...
                }
            },
            ...
        }
    density_overrides: optional per-group overrides
        { group_number: { 'gas_density': float, 'liquid_density': float, 'gor': float } }
    hole_diametres_mm: optional mapping of category -> representative hole diametre (mm)
        defaults use midpoints consistent with UI plots.

Returns:
    { group_number: { 'phase': str, 'categories': { cat: { 'hole_diametre_mm', 'leak_rate_kg_s', 'frequency_total' } } } }
Assumptions:
    - Pressure is gauge (bar) as used in Gas/Liquid calculators.
    - Gas/leak densities and GOR must be supplied either in density_overrides or group env.
"""
from typing import Dict, Any, Optional

from GasLeak import GasLeakCalculator
from LiquidLeak import LiquidLeakCalculator
from TwoPhaseLeak import TwoPhaseLeakCalculator

# Label to map each diamitre scenario to hole in diametre (mm)
DEFAULT_HOLE_DIAMETRES_MM = {
    "1-3mm": 3.0,
    "3-10mm": 10.0,
    "10-50mm": 50.0,
    "50-150mm": 150.0,
    # Arbitrary hole size for > 150mm
    ">150mm": 175.0,
}

def _resolve_hole_diametre(category: str, custom_map: Optional[Dict[str, float]]) -> float:
    if custom_map and category in custom_map:
        return float(custom_map[category])
    if category not in DEFAULT_HOLE_DIAMETRES_MM:
        raise ValueError(f"Unknown leak category '{category}'")
    return DEFAULT_HOLE_DIAMETRES_MM[category]


def _resolve_density(group_number: int, key: str, env: Dict[str, Any], overrides: Optional[Dict[int, Dict[str, Any]]]):
    if overrides and group_number in overrides and overrides[group_number].get(key) is not None:
        return overrides[group_number][key]
    return env.get(key)


def compute_leak_profiles(
    frequency_results: Dict[int, Dict[str, Any]],
    density_overrides: Optional[Dict[int, Dict[str, Any]]] = None,
    hole_diametres_mm: Optional[Dict[str, float]] = None,
) -> Dict[int, Dict[str, Any]]:
    """For each group and leak category, compute leak rates using derived hole diametre."""
    gas_calc = GasLeakCalculator()
    liq_calc = LiquidLeakCalculator()
    two_calc = TwoPhaseLeakCalculator()

    results: Dict[int, Dict[str, Any]] = {}

    for group_num, group_data in frequency_results.items():
        env = group_data.get("operational_conditions", {})
        phase = str(env.get("fuel_phase", "")).lower()
        pressure = float(env.get("pressure", env.get("pressure_bar_g", 0.0)))

        gas_density = _resolve_density(group_num, "gas_density", env, density_overrides)
        liquid_density = _resolve_density(group_num, "liquid_density", env, density_overrides)
        gor = _resolve_density(group_num, "gor", env, density_overrides)

        categories = {}
        for category, freq_data in group_data.get("frequencies", {}).items():
            if category == "Total":
                continue
            hole_d = _resolve_hole_diametre(category, hole_diametres_mm)

            if phase == "gas":
                if gas_density is None:
                    raise ValueError(f"gas_density missing for group {group_num}")
                leak_rate = gas_calc.calculate_leak(hole_d, float(gas_density), pressure)
            elif phase == "liquid":
                if liquid_density is None:
                    raise ValueError(f"liquid_density missing for group {group_num}")
                leak_rate = liq_calc.calculate_leak(hole_d, float(liquid_density), pressure)
            else:
                if gor is None:
                    raise ValueError(f"gor missing for two-phase calculation in group {group_num}")
                if gas_density is None or liquid_density is None:
                    raise ValueError(f"gas_density/liquid_density missing for two-phase calculation in group {group_num}")
                q_g = gas_calc.calculate_leak(hole_d, float(gas_density), pressure)
                q_l = liq_calc.calculate_leak(hole_d, float(liquid_density), pressure)
                leak_rate = two_calc.calculate_leak(float(gor), q_g, q_l)

            categories[category] = {
                "hole_diametre_mm": hole_d,
                "leak_rate_kg_s": leak_rate,
                "frequency_total": freq_data.get("total", 0.0),
                "frequency_full_pressure": freq_data.get("full_pressure", 0.0),
                "frequency_zero_pressure": freq_data.get("zero_pressure", 0.0),
            }

        results[group_num] = {
            "phase": phase or "unknown",
            "operational_conditions": env,
            "categories": categories,
        }

    return results


def attach_leak_profiles(
    frequency_results: Dict[int, Dict[str, Any]],
    density_overrides: Optional[Dict[int, Dict[str, Any]]] = None,
    hole_diametres_mm: Optional[Dict[str, float]] = None,
) -> Dict[int, Dict[str, Any]]:

    leak_profiles = compute_leak_profiles(
        frequency_results,
        density_overrides=density_overrides,
        hole_diametres_mm=hole_diametres_mm,
    )

    merged: Dict[int, Dict[str, Any]] = {}
    for group_num, group_data in frequency_results.items():
        merged[group_num] = {**group_data}
        merged[group_num]["leak_profiles"] = leak_profiles.get(group_num, {})
    return merged
