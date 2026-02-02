"""
    Docstring for middleware.analysis.consequence.models.IQRAModeling.IQRA_software.GasDispersion.dispersion_calculations
    Contains all functions required to perform dispersion calculations
    - Gas: Gaussian Plume Model
    - Gas: Gaussian Puff Model
    TODO:
    - Liquid Models
"""

import math
from typing import Tuple


_PG_PARAMS = {
    "A": {"a_xy": 0.18, "b_xy": 0.92, "a_z": 0.60, "b_z": 0.75},
    "B": {"a_xy": 0.14, "b_xy": 0.92, "a_z": 0.53, "b_z": 0.73},
    "C": {"a_xy": 0.10, "b_xy": 0.92, "a_z": 0.34, "b_z": 0.71},
    "D": {"a_xy": 0.06, "b_xy": 0.92, "a_z": 0.15, "b_z": 0.70},
    "E": {"a_xy": 0.04, "b_xy": 0.92, "a_z": 0.10, "b_z": 0.65},
    "F": {"a_xy": 0.02, "b_xy": 0.89, "a_z": 0.05, "b_z": 0.61},
}


def sigma_yz_plume(x: float, stability_class: str) -> Tuple[float, float]:
    """Return plume sigma_y, sigma_z from CCPS/ALCHe correlations."""
    if stability_class == "A":
        sigma_y = 0.22 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.20 * x
    elif stability_class == "B":
        sigma_y = 0.16 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.12 * x
    elif stability_class == "C":
        sigma_y = 0.11 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.08 * x * (1 + 0.0002 * x) ** -0.5
    elif stability_class == "D":
        sigma_y = 0.08 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.06 * x * (1 + 0.0015 * x) ** -0.5
    elif stability_class == "E":
        sigma_y = 0.06 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.03 * x * (1 + 0.0003 * x) ** -1
    elif stability_class == "F":
        sigma_y = 0.04 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.016 * x * (1 + 0.0003 * x) ** -1
    else:
        raise ValueError("Invalid stability class")

    return sigma_y, sigma_z


def gaussian_plume_concentration(
    q_evap_kg_s: float,
    wind_speed_m_s: float,
    effective_height_m: float,
    x_m: float,
    y_m: float,
    z_m: float,
    stability_class: str,
) -> float:
    """Return Gaussian plume concentration (kg/m^3) at a point."""
    if x_m <= 0 or wind_speed_m_s <= 0:
        return 0.0
    sigma_y, sigma_z = sigma_yz_plume(x_m, stability_class)
    term1 = q_evap_kg_s / (2 * math.pi * wind_speed_m_s * sigma_y * sigma_z)
    term2 = math.exp(-(y_m**2) / (2 * sigma_y**2))
    term3 = math.exp(-((effective_height_m - z_m) ** 2) / (2 * sigma_z**2))
    term4 = math.exp(-((effective_height_m + z_m) ** 2) / (2 * sigma_z**2))
    return term1 * term2 * (term3 + term4)


def gaussian_puff_concentration(
    mass_kg: float,
    wind_speed_m_s: float,
    effective_height_m: float,
    x_m: float,
    y_m: float,
    z_m: float,
    time_s: float,
    stability_class: str,
) -> float:
    """Return Gaussian puff concentration (kg/m^3) at a point."""
    if time_s <= 0:
        return 0.0
    stability_class = stability_class.upper()
    if stability_class not in _PG_PARAMS:
        raise ValueError("Invalid stability class")

    params = _PG_PARAMS[stability_class]
    sigma_x = params["a_xy"] * (wind_speed_m_s * time_s) ** params["b_xy"]
    sigma_y = params["a_xy"] * (wind_speed_m_s * time_s) ** params["b_xy"]
    sigma_z = params["a_z"] * (wind_speed_m_s * time_s) ** params["b_z"]

    term_exp = math.exp(-((x_m - wind_speed_m_s * time_s) ** 2) / (2 * sigma_x**2))
    term_exp *= math.exp(-(y_m**2) / (2 * sigma_y**2))
    term_z = math.exp(-((z_m - effective_height_m) ** 2) / (2 * sigma_z**2))
    term_z += math.exp(-((z_m + effective_height_m) ** 2) / (2 * sigma_z**2))

    return mass_kg / ((2 * math.pi) ** 1.5 * sigma_x * sigma_y * sigma_z) * term_exp * term_z
