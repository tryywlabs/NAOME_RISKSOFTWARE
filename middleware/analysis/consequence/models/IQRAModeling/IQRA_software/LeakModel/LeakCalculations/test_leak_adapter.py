"""
Ad-hoc test driver for leak_scenario_adapter.
Run: python test_leak_adapter.py
"""
import os
import sys
from pprint import pprint

# Ensure local imports work when executed directly
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
if CURRENT_DIR not in sys.path:
    sys.path.insert(0, CURRENT_DIR)

from leak_scenario_adapter import attach_leak_profiles


def build_mock_frequency_results():
    """Minimal mock of calculate_all_group_frequencies output."""
    return {
        1: {
            "operational_conditions": {
                "fuel_phase": "Gas",
                "pressure": 12.0,  # bar gauge
                # Optional: could include gas_density here instead of overrides
            },
            "frequencies": {
                "1-3mm": {"total": 7.95e-6, "full_pressure": 7.95e-6, "zero_pressure": 0.0},
                "3-10mm": {"total": 1.06e-4, "full_pressure": 1.06e-4, "zero_pressure": 0.0},
            },
            "equipments": [],
        },
        2: {
            "operational_conditions": {
                "fuel_phase": "Liquid",
                "pressure": 8.0,  # bar gauge
            },
            "frequencies": {
                "1-3mm": {"total": 1.18e-4, "full_pressure": 1.18e-4, "zero_pressure": 0.0},
                "3-10mm": {"total": 1.57e-3, "full_pressure": 1.57e-3, "zero_pressure": 0.0},
            },
            "equipments": [],
        },
        3: {
            "operational_conditions": {
                "fuel_phase": "TwoPhase",
                "pressure": 10.0,  # bar gauge
            },
            "frequencies": {
                "1-3mm": {"total": 2.0e-5, "full_pressure": 2.0e-5, "zero_pressure": 0.0},
                "3-10mm": {"total": 5.0e-4, "full_pressure": 5.0e-4, "zero_pressure": 0.0},
            },
            "equipments": [],
        },
    }


def main():
    frequency_results = build_mock_frequency_results()

    # Provide densities/GOR here (if not embedded in operational_conditions)
    density_overrides = {
        1: {"gas_density": 8.5},
        2: {"liquid_density": 850.0},
        3: {"gas_density": 8.5, "liquid_density": 850.0, "gor": 50},
    }

    merged = attach_leak_profiles(
        frequency_results,
        density_overrides=density_overrides,
        hole_diameters_mm=None,  # use defaults; override with a dict if needed
    )

    print("=== Leak profiles attached to frequency results ===")
    for group_num, data in merged.items():
        print(f"\nGroup {group_num} (phase={data['leak_profiles'].get('phase')}):")
        for cat, payload in data["leak_profiles"]["categories"].items():
            print(
                f"  {cat}: hole={payload['hole_diameter_mm']} mm, "
                f"leak_rate={payload['leak_rate_kg_s']:.6e} kg/s, "
                f"freq_total={payload['frequency_total']:.6e}"
            )

    # Pretty-print full structure if needed
    # pprint(merged)


if __name__ == "__main__":
    main()
