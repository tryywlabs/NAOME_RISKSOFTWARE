"""Gas leak calculation utilities (UI-free)."""
import math

from PhaseModule import PhaseModule


class GasLeakCalculator(PhaseModule):
    """Calculates initial gas leak rate (kg/s)."""

    def calculate_leak(self, diameter_mm: float, gas_density: float, pressure_bar_g: float) -> float:
        """Compute Q_g using hole diameter (mm), density (kg/m^3), and gauge pressure (bar).
        Formula: Q_g = 1.4e-4 * d^2 * sqrt(rho_g * P_g)
        """
        return 1.4e-4 * diameter_mm ** 2 * math.sqrt(gas_density * pressure_bar_g)
