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
