"""
FILE: frequency_database.py
DESCRIPTION:
    Frequency Database Module
    Handles database queries for equipment failure rate data

FUNCTIONS:
    - convert_equipment_name_to_table(equipment_name: str) -> str (Converts the app's equipment name to the matching database table name)
    - convert_equipment_size_to_db_format(equipment_size: str) -> str (Converts the app's equipment size format to the database's format mm -> A)
    - get_equipment_failure_rates(equipment_name: str, equipment_size: str) -> list
    - get_group_failure_rates(group_data: dict) -> dict
    - calculate_adjusted_failure_rates(failure_rates_data: dict) -> dict
"""
import sys
import os

# Add database module to path
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../database'))
from supabase_connect import supabase

def convert_equipment_name_to_table(equipment_name: str) -> str:
    """
    Convert equipment name to database table name format
    Example: '8. Tube Side Heat Exchanger' -> '8_Tube_Side_Heat_Exchanger'
    Note: Database tables use underscores with each word capitalized
    """
    # Remove number prefix and clean the name
    parts = equipment_name.split('.', 1)
    if len(parts) > 1:
        number = parts[0].strip()
        name = parts[1].strip()
    else:
        number = ""
        name = equipment_name.strip()
    
    # Handle special cases and replacements for exact database table names
    name_mapping = {
        "Tube Side Heat Exchanger": "Tube_Side_Heat_Exchanger",
        "Shell Side Heat Exchanger": "Shell_Side_Heat_Exchanger",
        "Fin Fan Heat Exchanger": "Fin_Fan_Heat_Exchanger",
        "Plate Heat Exchanger": "Plate_Heat_Exchanger",
        "Centrifugal Compressor": "Centrifugal_Compressors",
        "Reciprocating Compressor": "Reciprocating_Compressors",
        "Centrifugal Pump": "Centrifugal_Pump",
        "Reciprocating Pump": "Reciprocating_Pump",
        "Process Pipe": "Process_Pipe",
        "Process Vessel": "Process_Vessel",
        "Atmospheric Storage Vessel": "Atmospheric_Storage_Vessel",
        "Small Bore Fitting": "Small_Bore_Fittings",
        "Actuated Valve": "Actuated_Valves",
        "Manual Valve": "Manual_Valves",
        "Pig Trap": "Pig_Trap",
        "Flange": "Flange",
        "Filter": "Filters"
    }
    
    # Apply mapping (convert spaces to underscores, capitalize each word)
    table_name = name_mapping.get(name, name.replace(" ", "_"))
    
    # Add number prefix if present
    if number:
        table_name = f"{number}_{table_name}"
    
    return table_name


def convert_equipment_size_to_db_format(equipment_size: str) -> str:
    """
    Convert equipment size from UI format to database format
    Example: '≥100mm' -> '100A'
    """
    # Remove '≥' and 'mm' from the size string
    size = equipment_size.replace('≥', '').replace('mm', '').strip()
    
    # Add 'A' suffix for database format
    return f"{size}A"


def get_equipment_failure_rates(equipment_name: str, equipment_size: str):
    """
    Retrieve failure rate data for a specific equipment and size from the database
    
    Args:
        equipment_name: Name of the equipment (e.g., '8. Tube Side Heat Exchanger')
        equipment_size: Size of the equipment (e.g., '≥100mm')
    
    Returns:
        List of dictionaries containing failure rate data with keys:
        - category: Leak size category
        - total: Total failure rate
        - full_pressure: Full pressure failure rate
        - zero_pressure: Zero pressure failure rate
    
    Raises:
        Exception: If database query fails
    """
    try:
        # 1. First, parse the user inputs into DB-compatible formats

        # Convert equipment name to table name
        table_name = convert_equipment_name_to_table(equipment_name)
        
        # Convert equipment size to database format
        db_size = convert_equipment_size_to_db_format(equipment_size)
        
        # 2. Second, query the database using the Supabase python client functions
          # Supabase functions used:
          # .select()
          # .eq()
          # .execute()

        # Query the database
        response = supabase.table(table_name).select(
            "category, total, full_pressure, zero_pressure"
        ).eq("equipment_size", db_size).execute()
        
        return response.data
    
    except Exception as e:
        print(f"Error retrieving failure rates for {equipment_name} (size: {equipment_size}): {str(e)}")
        raise


# NOTE: The main function to be used by other modules
def get_group_failure_rates(group_data: dict):
    """
    Retrieve failure rates for all equipment in a group
    
    Args:
        group_data: Dictionary containing group information with keys:
            - Group_Number: Group identifier
            - Equipment_Name: Name of the equipment
            - Equipment_Size: Size of the equipment
            - Equipment_EA: Number of equipment units
    
    Returns:
        Dictionary with structure:
        {
            'group_number': int,
            'equipment_name': str,
            'equipment_size': str,
            'equipment_ea': int,
            'failure_rates': [
                {
                    'category': str,
                    'total': float,
                    'full_pressure': float,
                    'zero_pressure': float
                },
                ...
            ]
        }
    """
    try:
        equipment_name = group_data['Equipment_Name']
        equipment_size = group_data['Equipment_Size']
        equipment_ea = group_data['Equipment_EA']
        group_number = group_data['Group_Number']
        
        # Get failure rates from database
        failure_rates = get_equipment_failure_rates(equipment_name, equipment_size)
        
        return {
            'group_number': group_number,
            'equipment_name': equipment_name,
            'equipment_size': equipment_size,
            'equipment_ea': equipment_ea,
            'failure_rates': failure_rates
        }
    
    except Exception as e:
        print(f"Error processing group data: {str(e)}")
        raise


def calculate_adjusted_failure_rates(failure_rates_data: dict):
    """
    Calculate failure rates adjusted by equipment count (EA)
    
    Args:
        failure_rates_data: Dictionary from get_group_failure_rates()
    
    Returns:
        Dictionary with adjusted failure rates multiplied by EA
    """
    ea = failure_rates_data['equipment_ea']
    adjusted_rates = []
    
    for rate in failure_rates_data['failure_rates']:
        adjusted_rates.append({
            'category': rate['category'],
            'total': float(rate['total']) * ea,
            'full_pressure': float(rate['full_pressure']) * ea,
            'zero_pressure': float(rate['zero_pressure']) * ea
        })
    
    return {
        **failure_rates_data,
        'adjusted_failure_rates': adjusted_rates
    }


if __name__ == "__main__":
    # Test the functions
    test_equipment = {
        'Group_Number': 1,
        'Equipment_Name': '8. Tube Side Heat Exchanger',
        'Equipment_Size': '≥100mm',
        'Equipment_EA': 3
    }
    
    print("Testing equipment failure rate retrieval...")
    print(f"Equipment: {test_equipment['Equipment_Name']}")
    print(f"Size: {test_equipment['Equipment_Size']}")
    print(f"EA: {test_equipment['Equipment_EA']}")
    print()
    
    # Test table name conversion
    table_name = convert_equipment_name_to_table(test_equipment['Equipment_Name'])
    print(f"Converted table name: {table_name}")
    
    # Test size conversion
    db_size = convert_equipment_size_to_db_format(test_equipment['Equipment_Size'])
    print(f"Converted size: {db_size}")
    print()
    
    # Test database query
    try:
        result = get_group_failure_rates(test_equipment)
        # print("Retrieved failure rates:")
        # for rate in result['failure_rates']:
        #     print(f"  Category: {rate['category']}")
        #     print(f"    Total: {rate['total']}")
        #     print(f"    Full Pressure: {rate['full_pressure']}")
        #     print(f"    Zero Pressure: {rate['zero_pressure']}")
        #     print()
        
        # Test adjusted rates
        adjusted = calculate_adjusted_failure_rates(result)
        print(f"\nAdjusted failure rates (multiplied by EA={test_equipment['Equipment_EA']}):")
        for rate in adjusted['adjusted_failure_rates']:
            print(f"  Category: {rate['category']}")
            print(f"    Total: {rate['total']}")
            print(f"    Full Pressure: {rate['full_pressure']}")
            print(f"    Zero Pressure: {rate['zero_pressure']}")
            print()
            
    except Exception as e:
        print(f"Error: {str(e)}")
