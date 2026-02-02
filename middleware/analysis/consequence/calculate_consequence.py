"""Consequence calculation pipeline tying frequency, leak, and dispersion models."""
from __future__ import annotations

import os
import sys
from typing import Any, Dict, Optional


def _ensure_path(path: str) -> None:
    if path not in sys.path:
        sys.path.insert(0, path)


_BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Frequency calculation module
_FREQ_PATH = os.path.abspath(os.path.join(_BASE_DIR, "../frequency"))
_ensure_path(_FREQ_PATH)

# Leak adapter module
_LEAK_PATH = os.path.abspath(
    os.path.join(
        _BASE_DIR,
        "models/IQRAModeling/IQRA_software/LeakModel/LeakCalculations",
    )
)
_ensure_path(_LEAK_PATH)

# Dispersion calculations
_DISPERSION_PATH = os.path.abspath(
    os.path.join(
        _BASE_DIR,
        "models/IQRAModeling/IQRA_software/GasDispersion",
    )
)
_ensure_path(_DISPERSION_PATH)

from calculate_freq import calculate_all_group_frequencies
from leak_scenario_adapter import compute_leak_profiles
from dispersion_calculations import (
    gaussian_plume_concentration,
    gaussian_puff_concentration,
)

# Calculate leak rates and dispersion per each group
# Returns: dict keyed by group number, with operational conditions, leak categories, operational dispersion results
def calculate_group_consequence(
    *,
    cache_file_path: Optional[str] = None,
    group_manager=None,
    density_overrides: Optional[Dict[int, Dict[str, Any]]] = None,
    dispersion_params: Optional[Dict[str, Any]] = None,
    hole_diametres_mm: Optional[Dict[str, float]] = None,
) -> Dict[int, Dict[str, Any]]:
    
    group_results = calculate_all_group_frequencies(
        cache_file_path=cache_file_path,
        group_manager=group_manager,
    )

    if not group_results:
        return {}

    leak_profiles = compute_leak_profiles(
        group_results,
        density_overrides=density_overrides,
        hole_diametres_mm=hole_diametres_mm,
    )

    for group_num, group_data in leak_profiles.items():
        phase = group_data.get("phase", "")
        if phase != "gas" or not dispersion_params:
            continue

        model = str(dispersion_params.get("model", "plume")).lower()
        wind = float(dispersion_params.get("wind_speed_m_s", 0.0))
        height = float(dispersion_params.get("release_height_m", 0.0))
        stability = str(dispersion_params.get("stability_class", "D")).upper()
        x_m = float(dispersion_params.get("x_m", 0.0))
        y_m = float(dispersion_params.get("y_m", 0.0))
        z_m = float(dispersion_params.get("z_m", 0.0))
        puff_time = float(dispersion_params.get("puff_time_s", 0.0))
        duration = float(dispersion_params.get("release_duration_s", 0.0))

        for category, cat_data in group_data.get("categories", {}).items():
            leak_rate = float(cat_data.get("leak_rate_kg_s") or 0.0)
            dispersion = None
            if model == "plume":
                concentration = gaussian_plume_concentration(
                    leak_rate,
                    wind,
                    height,
                    x_m,
                    y_m,
                    z_m,
                    stability,
                )
                dispersion = {
                    "model": "plume",
                    "concentration_kg_m3": concentration,
                }
            elif model == "puff":
                mass_kg = leak_rate * max(duration, 0.0)
                concentration = gaussian_puff_concentration(
                    mass_kg,
                    wind,
                    height,
                    x_m,
                    y_m,
                    z_m,
                    puff_time,
                    stability,
                )
                dispersion = {
                    "model": "puff",
                    "concentration_kg_m3": concentration,
                }

            if dispersion is not None:
                cat_data["dispersion"] = dispersion

    return leak_profiles
