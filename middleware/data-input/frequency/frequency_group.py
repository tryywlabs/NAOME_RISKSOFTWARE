"""
Frequency Group Management
Manages groups of equipment with operational conditions
"""
import csv
import os

class FrequencyEquipment:
    """Represents a single equipment item"""
    def __init__(self, name: str, size: str, ea: int):
        self.name = name
        self.size = size
        self.ea = ea

class OperationalConditions:
    """Stores operational conditions for a group"""
    def __init__(self, fuel_phase: str = None, pressure: float = None, temperature: float = None, size: float = None):
        self.fuel_phase = fuel_phase
        self.pressure = pressure
        self.temperature = temperature
        self.size = size
    
    def is_complete(self) -> bool:
        """Check if all operational conditions are set"""
        return all([
            self.fuel_phase is not None,
            self.pressure is not None,
            self.temperature is not None,
            self.size is not None
        ])

class FrequencyGroup:
    """Represents a group of equipment with operational conditions"""
    def __init__(self, group_number: int, operational_conditions: OperationalConditions):
        self.group_number = group_number
        self.operational_conditions = operational_conditions
        self.equipments = []
    
    def add_equipment(self, equipment: FrequencyEquipment):
        """Add equipment to the group"""
        self.equipments.append(equipment)
    
    def remove_equipment(self, index: int):
        """Remove equipment by index"""
        if 0 <= index < len(self.equipments):
            del self.equipments[index]
    
    def has_equipment(self) -> bool:
        """Check if group has at least one equipment"""
        return len(self.equipments) > 0
    
    def is_valid(self) -> bool:
        """Check if group is valid (has complete conditions and at least one equipment)"""
        return self.operational_conditions.is_complete() and self.has_equipment()

class FrequencyGroupManager:
    """Manages multiple frequency groups"""
    def __init__(self, cache_file_path=None):
        self.groups = []
        self.current_group_number = 1
        # Staging area for current group being created
        self.staging_operational_conditions = OperationalConditions()
        self.staging_equipments = []
        
        # Set cache file path
        if cache_file_path is None:
            # Default to group_cache.csv in the same directory
            self.cache_file_path = os.path.join(os.path.dirname(__file__), 'group_cache.csv')
        else:
            self.cache_file_path = cache_file_path
        
        # Load existing groups from cache
        self.load_from_cache()
    
    def set_staging_fuel_phase(self, fuel_phase: str):
        """Set fuel phase in staging area"""
        self.staging_operational_conditions.fuel_phase = fuel_phase
    
    def set_staging_pressure(self, pressure: float):
        """Set pressure in staging area"""
        self.staging_operational_conditions.pressure = pressure
    
    def set_staging_temperature(self, temperature: float):
        """Set temperature in staging area"""
        self.staging_operational_conditions.temperature = temperature
    
    def set_staging_size(self, size: float):
        """Set size in staging area"""
        self.staging_operational_conditions.size = size
    
    def add_staging_equipment(self, name: str, size: str, ea: int):
        """Add equipment to staging area"""
        equipment = FrequencyEquipment(name, size, ea)
        self.staging_equipments.append(equipment)
        return equipment
    
    def remove_staging_equipment(self, index: int):
        """Remove equipment from staging area by index"""
        if 0 <= index < len(self.staging_equipments):
            del self.staging_equipments[index]
    
    def clear_staging(self):
        """Clear the staging area"""
        self.staging_operational_conditions = OperationalConditions()
        self.staging_equipments = []
    
    def can_add_group(self) -> bool:
        """Check if staging area is ready to create a group"""
        return (self.staging_operational_conditions.is_complete() and 
                len(self.staging_equipments) > 0)
    
    def add_group(self) -> FrequencyGroup:
        """Create group from staging area and add to groups list"""
        if not self.can_add_group():
            raise ValueError("Cannot add group: operational conditions incomplete or no equipment added")
        
        # Create new group with staging data
        group = FrequencyGroup(self.current_group_number, self.staging_operational_conditions)
        group.equipments = self.staging_equipments.copy()
        
        # Add to groups list
        self.groups.append(group)
        self.current_group_number += 1
        
        # Clear staging area for next group
        self.clear_staging()
        
        return group
    
    def get_group(self, group_number: int) -> FrequencyGroup:
        """Get group by group number"""
        for group in self.groups:
            if group.group_number == group_number:
                return group
        return None
    
    def get_all_groups(self) -> list:
        """Get all groups"""
        return self.groups
    
    def save_to_cache(self):
        """Save all groups to CSV cache file"""
        try:
            with open(self.cache_file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                
                # Write header
                writer.writerow([
                    'Group_Number',
                    'Fuel_Phase',
                    'Pressure_Bar',
                    'Temperature_K',
                    'Size_mm',
                    'Equipment_Name',
                    'Equipment_Size',
                    'Equipment_EA'
                ])
                
                # Write each group with its equipment
                for group in self.groups:
                    if len(group.equipments) == 0:
                        # Write group info even if no equipment (shouldn't happen with validation)
                        writer.writerow([
                            group.group_number,
                            group.operational_conditions.fuel_phase,
                            group.operational_conditions.pressure,
                            group.operational_conditions.temperature,
                            group.operational_conditions.size,
                            '',
                            '',
                            ''
                        ])
                    else:
                        # Write one row per equipment
                        for equipment in group.equipments:
                            writer.writerow([
                                group.group_number,
                                group.operational_conditions.fuel_phase,
                                group.operational_conditions.pressure,
                                group.operational_conditions.temperature,
                                group.operational_conditions.size,
                                equipment.name,
                                equipment.size,
                                equipment.ea
                            ])
            return True
        except Exception as e:
            print(f"Error saving to cache: {e}")
            return False
    
    def load_from_cache(self):
        """Load groups from CSV cache file"""
        if not os.path.exists(self.cache_file_path):
            # No cache file exists yet
            return
        
        try:
            with open(self.cache_file_path, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                
                current_group_dict = {}
                
                for row in reader:
                    group_number = int(row['Group_Number'])
                    
                    # Check if we need to create a new group
                    if group_number not in current_group_dict:
                        # Create operational conditions
                        op_conditions = OperationalConditions(
                            fuel_phase=row['Fuel_Phase'],
                            pressure=float(row['Pressure_Bar']) if row['Pressure_Bar'] else None,
                            temperature=float(row['Temperature_K']) if row['Temperature_K'] else None,
                            size=float(row['Size_mm']) if row['Size_mm'] else None
                        )
                        
                        # Create group
                        group = FrequencyGroup(group_number, op_conditions)
                        current_group_dict[group_number] = group
                        self.groups.append(group)
                    
                    # Add equipment if present
                    if row['Equipment_Name']:
                        equipment = FrequencyEquipment(
                            name=row['Equipment_Name'],
                            size=row['Equipment_Size'],
                            ea=int(row['Equipment_EA'])
                        )
                        current_group_dict[group_number].add_equipment(equipment)
                
                # Update current group number to be one more than the highest
                if self.groups:
                    self.current_group_number = max(g.group_number for g in self.groups) + 1
                    
        except Exception as e:
            print(f"Error loading from cache: {e}")
    
    def clear_cache(self):
        """Clear the cache file"""
        try:
            if os.path.exists(self.cache_file_path):
                os.remove(self.cache_file_path)
            self.groups = []
            self.current_group_number = 1
            return True
        except Exception as e:
            print(f"Error clearing cache: {e}")
            return False