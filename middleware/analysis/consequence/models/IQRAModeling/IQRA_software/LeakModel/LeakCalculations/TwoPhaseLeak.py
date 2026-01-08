"""Two-phase (gas + liquid) leak calculation utilities."""
from PhaseModule import PhaseModule


class TwoPhaseLeakCalculator(PhaseModule):
    """Combines gas and liquid leak rates using GOR."""

    def calculate_leak(self, gor: float, gas_rate: float, liquid_rate: float) -> float:
        """Return combined rate Q_o (kg/s) given GOR and component rates."""
        return (gor / (gor + 1)) * gas_rate + (1 / (gor + 1)) * liquid_rate
