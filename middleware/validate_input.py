"""
FILE: middleware/validate_input.py
DESCRIPTION: Functions to validate user input data before database insertion or processing.
WHERE TO USE: All components that handle user input (this would be all tabs in the data entry notebook tab)
TODO: Import inputs from frequency_data.py for validation routines.
"""


def validate_group_numbers(group_numbers, max_group_no):
    """Validate that group numbers are within the allowed range."""
    for num in group_numbers:
        if not (1 <= num <= max_group_no):
            return False
    return True

def validate_equipment_selection(equipment, valid_equipments):
    """Validate that the selected equipment is in the list of valid equipments."""
    return equipment in valid_equipments

def validate_frequency_data(frequency_data):
    """Validate the frequency data structure."""
    # Placeholder for actual validation logic
    if not isinstance(frequency_data, dict):
        return False
    for key, value in frequency_data.items():
        if not isinstance(key, str) or not isinstance(value, (int, float)):
            return False
    return True

# TODO: Additional validation functions can be added as needed.