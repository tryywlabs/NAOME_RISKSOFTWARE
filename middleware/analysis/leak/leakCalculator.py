class LeakCalculator:
  def __init__(self):
    return LeakCalculator
  
  def calculate_leak(self, diameter_mm: float, density: float, pressure_bar_g: float) -> float:
    raise NotImplementedError("This method should be implemented by subclasses.")
    pass