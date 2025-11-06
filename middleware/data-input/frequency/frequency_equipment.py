__package____ = "middleware.data_input.frequency.group"

from frequency_equipment import FrequencyEquipment

# DB Integration needed for storing/retrieving frequency groups

class FrequencyGroup:
  def __init__(self, name: str, equipments: list[FrequencyEquipment]):
      self.name = name
      self.equipments = equipments

class FrequencyEquipment:
  def __init__(self, name: str, size: float, ea: int):
    self.name = name
    self.size = size
    self.ea = ea

  def __getattribute__(self, name):
    if name == "failure_rate":
      return self.fetch_failure_rate()
    else:
      return super().__getattribute__(name)

  def add_equipment(self, equipment):
    pass

  def remove_equipment(self, equipment):
    pass
  
  def fetch_failure_rate(self):
    pass
"""middleware.data_input.frequency.equipment package init"""
