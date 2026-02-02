"""Lightweight interface for leak calculators."""
from abc import ABC, abstractmethod


class PhaseModule(ABC):
    """Base interface implemented by phase-specific leak calculators."""

    @abstractmethod
    def calculate_leak(self, *args, **kwargs):
        """Return leak rate in kg/s for the given phase-specific inputs."""
        raise NotImplementedError