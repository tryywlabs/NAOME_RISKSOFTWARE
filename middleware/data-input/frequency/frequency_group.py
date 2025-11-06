__package____ = "middleware.data_input.frequency.group"
from frequency_equipment import FrequencyEquipment

class FrequencyGroup:
  def __init__(self, name: str, equipments: list[FrequencyEquipment]):
      self.name = name
      self.equipments = equipments
"""middleware.data_input.frequency.group package init"""