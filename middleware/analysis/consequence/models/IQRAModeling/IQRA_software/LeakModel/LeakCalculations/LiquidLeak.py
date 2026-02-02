"""Liquid leak calculation utilities (UI-free)."""
import math

from PhaseModule import PhaseModule


class LiquidLeakCalculator(PhaseModule):
    """Calculates initial liquid leak rate (kg/s)."""

    def calculate_leak(self, diameter_mm: float, liquid_density: float, pressure_bar_g: float) -> float:
        """Compute Q_L using hole diameter (mm), density (kg/m^3), and gauge pressure (bar).
        Formula: Q_L = 2.1e-4 * d^2 * sqrt(rho_L * P_L)
        """
        return 2.1e-4 * diameter_mm ** 2 * math.sqrt(liquid_density * pressure_bar_g)
