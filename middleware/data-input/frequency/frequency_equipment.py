"""
Frequency Equipment Module
Re-exports from frequency_group for backward compatibility
"""
from frequency_group import (
    FrequencyEquipment,
    OperationalConditions,
    FrequencyGroup,
    FrequencyGroupManager,
)

__all__ = [
    "FrequencyEquipment",
    "OperationalConditions",
    "FrequencyGroup",
    "FrequencyGroupManager",
]