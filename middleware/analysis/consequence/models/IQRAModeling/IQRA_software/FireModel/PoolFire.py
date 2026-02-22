"""Pool fire radiant heat flux calculation utilities."""
from __future__ import annotations

import math


def calculate_radiant_heat_flux(
    heat_release_rate_kw: float,
    pool_diameter_m: float,
    distance_m: float,
    radiative_fraction: float,
    atmospheric_transmissivity: float,
) -> float:
    """Return radiant heat flux q'' (kW/m^2) from a pool fire."""
    q_kw = float(heat_release_rate_kw)
    d_m = float(pool_diameter_m)
    x_m = float(distance_m)
    f = float(radiative_fraction)
    tau = float(atmospheric_transmissivity)

    if q_kw <= 0:
        raise ValueError("Heat release rate must be > 0.")
    if d_m <= 0:
        raise ValueError("Pool diameter must be > 0.")
    if x_m < 0:
        raise ValueError("Distance must be >= 0.")
    if not 0 <= f <= 1:
        raise ValueError("Radiative fraction must be between 0 and 1.")
    if not 0 <= tau <= 1:
        raise ValueError("Atmospheric transmissivity must be between 0 and 1.")

    # Effective distance from fire center to target.
    r_m = math.sqrt((x_m**2) + ((d_m / 2.0) ** 2))
    return (tau * f * q_kw) / (math.pi * (r_m**2))
