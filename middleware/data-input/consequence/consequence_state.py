"""Shared consequence input state between UI and analysis."""
from dataclasses import dataclass


@dataclass
class ConsequenceParams:
    gas_density_kg_m3: float = 1.2
    liquid_density_kg_m3: float = 800.0
    gor: float = 5.0
    wind_speed_m_s: float = 3.0
    release_height_m: float = 10.0
    stability_class: str = "D"
    model: str = "plume"
    x_m: float = 50.0
    y_m: float = 0.0
    z_m: float = 0.0
    puff_time_s: float = 30.0
    release_duration_s: float = 60.0
    critical_concentration_kg_m3: float = 0.0
    explosion_eta: float = 0.01
    explosion_mass_kg: float = 1.0
    explosion_heat_combustion_kj_kg: float = 0.0
    explosion_tnt_heat_combustion_kj_kg: float = 4680.0
    explosion_distance_m: float = 10.0
    explosion_ambient_pressure_bar: float = 1.013
    pool_fire_heat_release_rate_kw: float = 1000.0
    pool_fire_diameter_m: float = 5.0
    pool_fire_distance_m: float = 20.0
    pool_fire_radiative_fraction: float = 0.35
    pool_fire_atmospheric_transmissivity: float = 1.0


_PARAMS = ConsequenceParams()


def get_params() -> ConsequenceParams:
    """Return current consequence parameters."""
    return _PARAMS


def update_params(**kwargs) -> ConsequenceParams:
    """Update consequence parameters with validated values."""
    for key, value in kwargs.items():
        if hasattr(_PARAMS, key):
            setattr(_PARAMS, key, value)
    return _PARAMS
