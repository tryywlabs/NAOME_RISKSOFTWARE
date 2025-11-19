"""
FILE: frequency_data.py
DESCRIPTION:
    DATA INPUT -> Frequency Data (2nd tab)
    Frequency Data UI component using ttkbootstrap.
FUNCTIONS:
    create_group_ui(root):
        Render the frequency data page UI in the provided root window.
        
        INNER FUNCTIONS:
            configure_scroll_region(event):
                Configure the scroll region of the canvas.
            configure_inner_scroll_region(event):
                Configure the scroll region of the inner canvas.
            set_fuel_phase(value):
                Set the selected fuel phase in the menu.
"""

'''IMPORT STATEMENTS'''
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from ttkbootstrap.widgets.tableview import Tableview
from tkinter import ttk
from tkinter import Canvas
from tkinter import StringVar
from tkinter.font import Font
from tkinter import messagebox
import sys
import os

'''Middleware API IMPORT'''
sys.path.append(os.path.join(os.path.dirname(__file__), '../../../middleware/data-input/frequency'))
from frequency_group import FrequencyGroupManager, FrequencyGroup, OperationalConditions, FrequencyEquipment

'''FUNCTION: create_group_ui(root)'''
def create_group_ui(root):
    """Create the group UI in the provided root window."""

    # Initialize the group manager
    group_manager = FrequencyGroupManager()
    
    # Track the current staging group number
    current_staging_group = {'number': None}

    # Create a canvas and scrollbar for scrolling
    canvas = Canvas(root)
    scrollbar = ttk.Scrollbar(root, orient="vertical", command=canvas.yview)
    canvas.configure(yscrollcommand=scrollbar.set)

    # Pack the canvas and scrollbar
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    # Create a frame inside the canvas
    main_frame = ttk.Frame(canvas, padding=10)

    # Add the frame to the canvas
    canvas.create_window((0, 0), window=main_frame, anchor="nw")

    '''INNER FUNCTION: enable scrolling region'''
    def configure_scroll_region(event):
        canvas.configure(scrollregion=canvas.bbox("all"))

    main_frame.bind("<Configure>", configure_scroll_region)

    # Configure the column width for the grouping_frame
    main_frame.grid_columnconfigure(0, weight=1, minsize=100)

    # Create bold font for LabelFrame labels
    bold_font = Font(family="Helvetica", size=10, weight="bold")

    # Grouping Section
    grouping_frame = ttk.LabelFrame(main_frame, text="Grouping", padding=10)
    grouping_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)
    # Apply bold font to the label
    grouping_label = ttk.Label(grouping_frame.winfo_toplevel(), text="Grouping", font=bold_font)
    grouping_frame.configure(labelwidget=grouping_label)
    
    # Configure grid columns - 2 column layout
    grouping_frame.grid_columnconfigure(0, weight=0, minsize=200)  # Left panel (controls)
    grouping_frame.grid_columnconfigure(1, weight=1)  # Right panel (view of all groups)
    grouping_frame.grid_rowconfigure(0, weight=1)  # Single row that expands
    
    # Left panel - Group controls (save, operation hours, reset)
    controls_frame = ttk.LabelFrame(grouping_frame, text="Group Controls", padding=10)
    controls_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    controls_label = ttk.Label(controls_frame.winfo_toplevel(), text="Group Controls", font=bold_font)
    controls_frame.configure(labelwidget=controls_label)
    
    # Operation hours input
    ttk.Label(controls_frame, text="Operation hours ( /year)").pack(anchor=W, pady=(5, 5))
    operation_hours_spinbox = ttk.Spinbox(controls_frame, from_=0, to=10000, increment=1, width=15)
    operation_hours_spinbox.pack(fill=X, pady=(0, 15))
    operation_hours_spinbox.set(0)  # Default value
    
    # Save button
    # Saves to the following location: RISKSOFTWARE/middleware/data-input/frequency/group_cache.csv
    # The CSV file is effectively acting as a simple cache, where it is created if not exists & updated when a group is added
    # The CSV file is deleted when "Reset" is clicked
    ttk.Label(controls_frame, text="Save Groups").pack(anchor=W, pady=(5, 5))
    ttk.Button(controls_frame, text="Save", bootstyle=INFO, width=15).pack(fill=X, pady=(0, 15))
    
    '''FUNCTION: reset_groups() wipes the group cache and staging area'''
    def reset_groups():
        """Reset all groups - clear cache and staging area"""
        result = messagebox.askyesno("Confirm Reset", 
            "This will delete all groups and clear the cache. Are you sure?")
        if result:
            # Clear groups from manager
            group_manager.groups = []
            group_manager.current_group_number = 1
            
            # Clear staging area
            group_manager.staging_equipments = []
            group_manager.staging_operational_conditions.fuel_phase = None
            group_manager.staging_operational_conditions.pressure = None
            group_manager.staging_operational_conditions.temperature = None
            group_manager.staging_operational_conditions.size = None
            
            # Delete cache file
            import os
            # Relative cache routing
            cache_file = os.path.join(os.path.dirname(__file__), '../../../middleware/data-input/frequency/group_cache.csv')
            if os.path.exists(cache_file):
                os.remove(cache_file)
            
            # Update display
            update_groups_display()
            messagebox.showinfo("Success", "All groups have been reset!")
    
    # Reset button
    ttk.Label(controls_frame, text="Reset All Groups").pack(anchor=W, pady=(5, 5))
    ttk.Button(controls_frame, text="Reset", bootstyle=DANGER, width=15, command=reset_groups).pack(fill=X, pady=(0, 5))
    
    # Create a labeled frame to group row headers and groups view
    view_all_frame = ttk.LabelFrame(grouping_frame, text="View of All Groups", padding=5)
    view_all_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    view_all_label = ttk.Label(view_all_frame.winfo_toplevel(), text="View of All Groups", font=bold_font)
    view_all_frame.configure(labelwidget=view_all_label)
    
    # Configure columns within the view_all_frame
    view_all_frame.grid_columnconfigure(0, weight=0, minsize=200)  # Headers column
    view_all_frame.grid_columnconfigure(1, weight=1)  # Groups view column (expandable)
    
    # Row headers in left column
    headers_frame = ttk.Frame(view_all_frame, padding=5)
    headers_frame.grid(row=0, column=0, sticky="nsw", padx=(5, 10), pady=5)
    
    # Add spacing for header alignment (to match button row)
    ttk.Label(headers_frame, text=" ").grid(row=0, column=0, sticky="ew", pady=(0, 5))
    
    # Add row header labels with consistent spacing
    ttk.Label(headers_frame, text="Phase", width=20, anchor=W).grid(row=1, column=0, sticky="ew", pady=3)
    ttk.Label(headers_frame, text="Working Press. (bar)", width=20, anchor=W).grid(row=2, column=0, sticky="ew", pady=3)
    ttk.Label(headers_frame, text="Working Temp. (°C)", width=20, anchor=W).grid(row=3, column=0, sticky="ew", pady=3)
    ttk.Label(headers_frame, text="System Size (mm)", width=20, anchor=W).grid(row=4, column=0, sticky="ew", pady=3)
    
    # Create container for groups with canvas in right column
    groups_container = ttk.Frame(view_all_frame, padding=5)
    groups_container.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    
    # Create canvas for horizontal scrolling of groups
    groups_canvas = Canvas(groups_container)
    h_scrollbar = ttk.Scrollbar(groups_container, orient="horizontal", command=groups_canvas.xview)
    groups_canvas.configure(xscrollcommand=h_scrollbar.set)
    
    groups_canvas.pack(side=TOP, fill=BOTH, expand=True)
    h_scrollbar.pack(side=BOTTOM, fill=X)
    
    # Create frame for groups inside canvas
    groups_scrollable_frame = ttk.Frame(groups_canvas)
    groups_canvas.create_window((0, 0), window=groups_scrollable_frame, anchor="nw")
    
    '''INNER FUNCTION: enable inner scrolling region'''
    def configure_groups_scroll_region(event):
        groups_canvas.configure(scrollregion=groups_canvas.bbox("all"))
    
    groups_scrollable_frame.bind("<Configure>", configure_groups_scroll_region)
    
    '''INNER FUNCTION: update_groups_display() renders all groups'''
    def update_groups_display():
        """Update the View of All Groups display with current groups"""
        # Clear existing group cards
        for widget in groups_scrollable_frame.winfo_children():
            widget.destroy()
        
        # Check if there are any groups
        all_groups = group_manager.get_all_groups()
        if len(all_groups) == 0:
            # Display placeholder when no groups exist
            placeholder = ttk.Label(
                groups_scrollable_frame, 
                foreground="gray"
            )
            placeholder.grid(row=0, column=0, padx=20, pady=20)
            return
        
        # Display each group
        for idx, group in enumerate(all_groups):
            # Create group card
            group_card = ttk.Frame(groups_scrollable_frame, relief="ridge", borderwidth=2, padding=5)
            group_card.grid(row=0, column=idx, padx=5, pady=0, sticky="nsew")
            
            # Group header
            header_label = ttk.Label(
                group_card, 
                text=f"Group {group.group_number}",
                font=("Helvetica", 10, "bold"),
                anchor=CENTER
            )
            header_label.grid(row=0, column=0, sticky="ew", pady=(0, 5))
            
            # Group data labels with consistent height to match headers
            ttk.Label(group_card, text=str(group.operational_conditions.fuel_phase or ""), width=15, anchor=CENTER).grid(row=1, column=0, sticky="ew", pady=3)
            ttk.Label(group_card, text=str(group.operational_conditions.pressure or "0"), width=15, anchor=CENTER).grid(row=2, column=0, sticky="ew", pady=3)
            ttk.Label(group_card, text=str(group.operational_conditions.temperature or "0"), width=15, anchor=CENTER).grid(row=3, column=0, sticky="ew", pady=3)
            ttk.Label(group_card, text=str(group.operational_conditions.size or "0"), width=15, anchor=CENTER).grid(row=4, column=0, sticky="ew", pady=3)
    
    # Initial display
    update_groups_display()

    # Create a container frame for Operational Conditions, Equipment List-Up, and Add Group
    conditions_equipment_container = ttk.Frame(main_frame, padding=10)
    conditions_equipment_container.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)
    conditions_equipment_container.grid_columnconfigure(0, weight=3)
    conditions_equipment_container.grid_columnconfigure(1, weight=1)
    conditions_equipment_container.grid_rowconfigure(0, weight=1)
    conditions_equipment_container.grid_rowconfigure(1, weight=1)

    # Operational Conditions (top left)
    operational_frame = ttk.LabelFrame(conditions_equipment_container, text="Operational Conditions", padding=10, bootstyle="info")
    operational_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    operational_label = ttk.Label(operational_frame.winfo_toplevel(), text="Operational Conditions", font=bold_font)
    operational_frame.configure(labelwidget=operational_label)

    ttk.Label(operational_frame, text="Fuel Phase:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    fuel_phase_var = StringVar(value="Select Fuel Phase")
    fuel_phase_menu = ttk.Menubutton(operational_frame, textvariable=fuel_phase_var, width=15)
    fuel_phase_menu.grid(row=1, column=0, sticky=W, padx=5, pady=5)
    fuel_phase_menu.menu = tb.Menu(fuel_phase_menu, tearoff=0)
    fuel_phase_menu["menu"] = fuel_phase_menu.menu

    def set_fuel_phase(value):
        fuel_phase_var.set(value)

    fuel_phase_menu.menu.add_command(label="Liquid", command=lambda: set_fuel_phase("Liquid"))
    fuel_phase_menu.menu.add_command(label="Gas", command=lambda: set_fuel_phase("Gas"))

    ttk.Label(operational_frame, text="Pressure (Bar):").grid(row=0, column=1, sticky=W, padx=5, pady=5)
    ttk.Label(operational_frame, text="Temperature (°C):").grid(row=0, column=2, sticky=W, padx=5, pady=5)
    ttk.Label(operational_frame, text="Size (mm):").grid(row=0, column=3, sticky=W, padx=5, pady=5)

    '''INNER FUNCTION: confirm_operational_conditions() validates & saves staging data and creates group'''
    def confirm_operational_conditions():
        try:
            # Get values from widgets
            fuel_phase = fuel_phase_var.get()
            if fuel_phase == "Select Fuel Phase":
                raise ValueError("Please select a fuel phase")
            
            pressure = float(pressure_spinbox.get())
            temperature = float(temperature_spinbox.get())
            size = float(size_spinbox.get())
            
            # Update staging area
            group_manager.set_staging_fuel_phase(fuel_phase)
            group_manager.set_staging_pressure(pressure)
            group_manager.set_staging_temperature(temperature)
            group_manager.set_staging_size(size)
            
            # Create a new group immediately with these conditions
            op_conditions = OperationalConditions(fuel_phase, pressure, temperature, size)
            new_group = FrequencyGroup(group_manager.current_group_number, op_conditions)
            group_manager.groups.append(new_group)
            current_staging_group['number'] = new_group.group_number
            group_manager.current_group_number += 1
            
            # Update displays
            update_groups_display()
            update_group_specifics_for_group(current_staging_group)
            
            messagebox.showinfo("Success", f"Group {current_staging_group['number']} created! Now add equipment to this group.")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    # Store spinbox references
    pressure_spinbox = ttk.Spinbox(operational_frame, from_=0, to=1000, increment=1)
    temperature_spinbox = ttk.Spinbox(operational_frame, from_=-2, to=30, increment=0.1)
    size_spinbox = ttk.Spinbox(operational_frame, from_=0, to=500, increment=0.1)
    
    pressure_spinbox.grid(row=1, column=1, sticky=W, padx=5, pady=5)
    temperature_spinbox.grid(row=1, column=2, sticky=W, padx=5, pady=5)
    size_spinbox.grid(row=1, column=3, sticky=W, padx=5, pady=5)
    
    # Add "Confirm" label and button in a frame for proper alignment
    confirm_frame = ttk.Frame(operational_frame)
    confirm_frame.grid(row=0, column=4, rowspan=2, sticky="nsew", padx=5, pady=5)
    ttk.Label(confirm_frame, text="Confirm").pack(pady=(0, 5))
    ttk.Button(confirm_frame, text="OK", bootstyle=SUCCESS, command=confirm_operational_conditions).pack(fill="both", expand=True)

    # Equipment List-Up (bottom left)
    equipments = ['1. Centrifugal Compressor', '2. Reciprocating Compressor', '3. Filter', '4. Flange', '5. Fin Fan Heat Exchanger', '6. Plate Heat Exchanger', '7. Shell Side Heat Exchanger', '8. Tube Side Heat Exchanger', '9. Pig Trap', '10. Process Pipe', '11. Centrifugal Pump', '12. Reciprocating Pump', '13. Small Bore Fitting', '14. Actuated Valve', '15. Manual Valve', '16. Process Vessel', '17. Atmospheric Storage Vessel']
    
    # Define size ranges for each equipment type
    equipment_sizes = {
        '1. Centrifugal Compressor': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '2. Reciprocating Compressor': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '3. Filter': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '4. Flange': ['12.5mm', '25mm', '50mm', '100mm', '125mm', '250mm', '350mm', '500mm'],
        '5. Fin Fan Heat Exchanger': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '6. Plate Heat Exchanger': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '7. Shell Side Heat Exchanger': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '8. Tube Side Heat Exchanger': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '9. Pig Trap': ['12.5mm', '25mm', '50mm', '100mm', '125mm', '250mm', '350mm', '500mm'],
        '10. Process Pipe': ['12.5mm', '25mm', '50mm', '100mm', '125mm', '250mm', '350mm', '500mm'],
        '11. Centrifugal Pump': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '12. Reciprocating Pump': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '13. Small Bore Fitting': ['12.5mm', '25mm', '50mm'],
        '14. Actuated Valve': ['12.5mm', '25mm', '50mm', '100mm', '125mm', '250mm', '350mm', '500mm'],
        '15. Manual Valve': ['12.5mm', '25mm', '50mm', '100mm', '125mm', '250mm', '350mm', '500mm'],
        '16. Process Vessel': ['12.5mm', '25mm', '50mm', '100mm', '125mm'],
        '17. Atmospheric Storage Vessel': ['12.5mm', '25mm', '50mm', '100mm', '125mm']
    }
    
    equipment_frame = ttk.LabelFrame(conditions_equipment_container, text="Equipment List-Up", padding=10)
    equipment_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    equipment_label = ttk.Label(equipment_frame.winfo_toplevel(), text="Equipment List-Up", font=bold_font)
    equipment_frame.configure(labelwidget=equipment_label)

    ttk.Label(equipment_frame, text="Name of Equipment:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    equipment_combobox = ttk.Combobox(equipment_frame, values=equipments, state="readonly")
    equipment_combobox.grid(row=1, column=0, sticky=W, padx=5, pady=5)


    # NOTE: Alternative using Menubutton for equipment selection

    # equipment_menu = ttk.Menubutton(equipment_frame, textvariable=equipments , width=15)
    # equipment_menu.grid(row=1, column=0, sticky=W, padx=5, pady=5)
    # equipment_menu.menu = tb.Menu(equipment_menu, tearoff=0)
    # equipment_menu["menu"] = equipment_menu.menu

    # fuel_phase_menu = ttk.Menubutton(operational_frame, textvariable=fuel_phase_var, width=15)
    # fuel_phase_menu.grid(row=1, column=0, sticky=W, padx=5, pady=5)
    # fuel_phase_menu.menu = tb.Menu(fuel_phase_menu, tearoff=0)
    # fuel_phase_menu["menu"] = fuel_phase_menu.menu

    ttk.Label(equipment_frame, text="Size:").grid(row=0, column=1, sticky=W, padx=5, pady=5)
    size_combobox = ttk.Combobox(equipment_frame, values=[], state="readonly")
    size_combobox.grid(row=1, column=1, sticky=W, padx=5, pady=5)

    ttk.Label(equipment_frame, text="EA:").grid(row=0, column=2, sticky=W, padx=5, pady=5)
    ea_spinbox = ttk.Spinbox(equipment_frame, from_=1, to=100, increment=1)
    ea_spinbox.grid(row=1, column=2, sticky=W, padx=5, pady=5)
    
    '''INNER FUNCTION: update_size_options() updates size combobox based on selected equipment'''
    def update_size_options(event=None):
        """Update size combobox values based on selected equipment"""
        selected_equipment = equipment_combobox.get()
        if selected_equipment in equipment_sizes:
            size_combobox['values'] = equipment_sizes[selected_equipment]
            size_combobox.set('')  # Clear current selection
        else:
            size_combobox['values'] = []
            size_combobox.set('')
    
    # Bind equipment selection to update size options
    equipment_combobox.bind('<<ComboboxSelected>>', update_size_options)

    # Staging equipment list to display current equipments
    staging_equipment_listbox = []
    
    def update_staging_display():
        """Update the display of staging equipments and groups"""
        update_groups_display()
    
    def add_equipment():
        """Add equipment to the current staging group"""
        try:
            # Check if a group has been created
            if current_staging_group['number'] is None:
                raise ValueError("Please confirm operational conditions first to create a group")
            
            equipment_name = equipment_combobox.get()
            if not equipment_name:
                raise ValueError("Please select an equipment")
            
            size = size_combobox.get()
            if not size:
                raise ValueError("Please select a size")
            
            ea = int(ea_spinbox.get())
            if ea <= 0:
                raise ValueError("EA must be greater than 0")
            
            # Add equipment directly to the current staging group
            equipment = FrequencyEquipment(equipment_name, size, ea)
            
            # Find the current staging group and add equipment
            for group in group_manager.groups:
                if group.group_number == current_staging_group['number']:
                    group.add_equipment(equipment)
                    break
            
            # Save to cache after adding equipment
            group_manager.save_to_cache()
            
            # Clear inputs
            equipment_combobox.set('')
            size_combobox.set('')
            ea_spinbox.set('0')
            
            # Update group specifics display
            update_group_specifics_for_group(current_staging_group)
            
            messagebox.showinfo("Success", f"Added {equipment_name} to Group {current_staging_group['number']}")
        except ValueError as e:
            messagebox.showerror("Error", f"Invalid input: {str(e)}")
    
    def remove_equipment():
        """Remove last equipment from staging area"""
        if len(group_manager.staging_equipments) > 0:
            group_manager.remove_staging_equipment(len(group_manager.staging_equipments) - 1)
            messagebox.showinfo("Success", "Removed last equipment from staging area")
            update_staging_display()
        else:
            messagebox.showwarning("Warning", "No equipment to remove")
    
    # Add/Remove/Confirm buttons column
    ttk.Label(equipment_frame, text="Add").grid(row=0, column=3, sticky=W, padx=5, pady=5)
    ttk.Button(equipment_frame, text="✓", bootstyle=SUCCESS, width=5, command=add_equipment).grid(row=1, column=3, sticky=W, padx=5, pady=5)
    
    ttk.Label(equipment_frame, text="Remove").grid(row=0, column=4, sticky=W, padx=5, pady=5)
    ttk.Button(equipment_frame, text="−", bootstyle=INFO, width=5, command=remove_equipment).grid(row=1, column=4, sticky=W, padx=5, pady=5)

    # Add Group Frame (right side, spanning 2 rows)
    add_group_frame = ttk.LabelFrame(conditions_equipment_container, text="Add Group", padding=10)
    add_group_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
    add_group_label = ttk.Label(add_group_frame.winfo_toplevel(), text="Add Group", font=bold_font)
    add_group_frame.configure(labelwidget=add_group_label)

    '''INNER FUNCTION: add_group() validates staging data and adds a new group'''
    def add_group():
        """Add group from staging area"""
        try:
            if not group_manager.can_add_group():
                missing = []
                if not group_manager.staging_operational_conditions.is_complete():
                    missing.append("operational conditions not complete")
                if len(group_manager.staging_equipments) == 0:
                    missing.append("no equipment added")
                raise ValueError(f"Cannot add group: {', '.join(missing)}")
            
            group = group_manager.add_group()
            
            # Save to cache file
            if group_manager.save_to_cache():
                messagebox.showinfo("Success", 
                    f"Group {group.group_number} created with {len(group.equipments)} equipment(s) and saved to cache!")
            else:
                messagebox.showwarning("Warning", 
                    f"Group {group.group_number} created but failed to save to cache")
            
            update_staging_display()
        except ValueError as e:
            messagebox.showerror("Error", str(e))
    
    def finish_groups():
        """Finish creating groups"""
        if len(group_manager.groups) == 0:
            messagebox.showwarning("Warning", "No groups have been created yet")
            return
        
        result = messagebox.askyesno("Confirm", 
            f"You have created {len(group_manager.groups)} group(s). Finish and proceed?")
        if result:
            messagebox.showinfo("Success", "Groups finalized!")
            # TODO: Proceed to next step or save groups
    
    # Add Group content
    add_button_frame = ttk.Frame(add_group_frame)
    add_button_frame.pack(pady=20, fill="both", expand=True)
    ttk.Button(add_button_frame, text="Add", bootstyle=INFO, width=15, command=add_group).pack(pady=10)
    
    finish_label = ttk.Label(add_group_frame, text="Finish", font=bold_font)
    finish_label.pack(pady=(20, 5))
    
    finish_button_frame = ttk.Frame(add_group_frame)
    finish_button_frame.pack(pady=10, fill="both", expand=True)
    ttk.Button(finish_button_frame, text="STOP", bootstyle=DANGER, width=15, command=finish_groups).pack(pady=10)

    # Group List
    group_list_frame = ttk.LabelFrame(main_frame, text="Group Specifics", padding=10)
    group_list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    group_specifics_label = ttk.Label(group_list_frame.winfo_toplevel(), text="Group Specifics", font=bold_font)
    group_list_frame.configure(labelwidget=group_specifics_label)

    columns = ("No.", "Equip. List", "Size", "EA")
    group_list_frame.grid_columnconfigure(0, weight=0)
    group_list_frame.grid_columnconfigure(1, weight=1)

    # Storage for table widget and spinbox (initialize early)
    table_widget = {'table': None}
    group_spinbox_widget = {}
    
    # Add the spinbox section to the left - select which group to view
    spinbox_label = ttk.Labelframe(group_list_frame, text="Select Group")
    spinbox_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    # Create a spinbox to select which group to view
    ttk.Label(spinbox_label, text="Group Number:").grid(row=0, column=0, sticky=W, padx=5, pady=(5, 2))
    
    def on_group_selection_change():
        """Called when user changes the spinbox value"""
        try:
            selected_group = int(group_select_spinbox.get())
            # Check if this group exists
            group_exists = any(g.group_number == selected_group for g in group_manager.groups)
            if group_exists:
                # Update the view to show this group
                temp_group = {'number': selected_group}
                update_group_specifics_for_group(temp_group)
        except (ValueError, TypeError):
            pass
    
    group_select_spinbox = ttk.Spinbox(
        spinbox_label, 
        from_=1, 
        to=100, 
        increment=1, 
        width=15,
        command=on_group_selection_change
    )
    group_select_spinbox.grid(row=1, column=0, sticky="ew", padx=5, pady=(0, 5))
    group_select_spinbox.set(1)
    
    # Bind to handle manual entry
    group_select_spinbox.bind('<Return>', lambda e: on_group_selection_change())
    group_select_spinbox.bind('<FocusOut>', lambda e: on_group_selection_change())
    
    # Store spinbox reference
    group_spinbox_widget['spinbox'] = group_select_spinbox

    # # Add the second table section to the right
    # specifics_table = ttk.Treeview(group_list_frame, columns=("Item No.", "Equip. List", "Size", "EA"), show="headings")
    # specifics_table.heading("Item No.", text="Item No.")
    # specifics_table.heading("Equip. List", text="Equip. List")
    # specifics_table.heading("Size", text="Size")
    # specifics_table.heading("EA", text="EA")

    # specifics_table.column("Item No.", width=100, anchor="center")
    # specifics_table.column("Equip. List", width=150, anchor="center")
    # specifics_table.column("Size", width=100, anchor="center")
    # specifics_table.column("EA", width=100, anchor="center")

    # specifics_table.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=5, pady=5)

    # # Embed the spinbox inside the 0th column of the Treeview in the second table
    # for i in range(3):
    #     item_id = specifics_table.insert("", "end", values=("", "Equip. List", "Size", "EA"))
    #     bbox = specifics_table.bbox(item_id, column="Item No.")
    #     if bbox:  # Ensure the bounding box is valid
    #         spinbox = ttk.Spinbox(group_list_frame, from_=0, to=100, increment=1, width=5)
    #         spinbox.place(x=bbox[0] + specifics_table.winfo_rootx(), y=bbox[1] + specifics_table.winfo_rooty(), width=bbox[2], height=bbox[3])

    # Using Tableview for better functionality
    coldata = [
        {"text": "No.", "width": 50, "anchor": "center"},
        {"text": "Equip. List", "width": 200, "anchor": "center"},
        {"text": "Size", "width": 100, "anchor": "center"},
        {"text": "EA", "width": 50, "anchor": "center"},
    ]

    # Initial empty data
    rowdata = []

    '''INNER FUNCTION: update_group_specifics_for_group() updates the group specifics table'''
    def update_group_specifics_for_group(group_dict):
        """Update the group specifics table to show the specified group"""
        if group_dict['number'] is None:
            # No group selected, show empty
            new_rowdata = []
        else:
            # Find the specified group
            current_group = None
            for group in group_manager.groups:
                if group.group_number == group_dict['number']:
                    current_group = group
                    break
            
            if current_group and len(current_group.equipments) > 0:
                # Build row data from equipment list
                new_rowdata = []
                for idx, equip in enumerate(current_group.equipments, 1):
                    new_rowdata.append((idx, equip.name, equip.size, equip.ea))
            else:
                new_rowdata = []
        
        # Update the table by accessing the internal treeview
        if table_widget['table'] is not None:
            try:
                # Access the internal treeview
                tree = table_widget['table'].view
                # Clear existing rows
                for item in tree.get_children():
                    tree.delete(item)
                # Insert new rows
                for row in new_rowdata:
                    tree.insert("", "end", values=row)
            except AttributeError:
                # Fallback: try the Tableview methods
                table_widget['table'].delete_rows()
                table_widget['table'].load_table_data(new_rowdata)
        
        # Update the spinbox if this is the current staging group
        if 'spinbox' in group_spinbox_widget and group_dict is current_staging_group:
            if current_staging_group['number'] is not None:
                group_spinbox_widget['spinbox'].set(current_staging_group['number'])

    table = Tableview(
        master=group_list_frame,
        coldata=coldata,
        rowdata=rowdata,
        paginated=True,
        searchable=True,
        bootstyle="primary",
        autofit=False,
        autoalign=True,
        stripecolor=(None, None),
    )

    # Store table reference for updates
    table_widget['table'] = table
    
    # Adjust the Tableview to stretch fully within its grid cell
    table.grid(row=0, column=1, rowspan=4, sticky="nsew", padx=0, pady=0)
    
    # Make the table's internal treeview stretch columns to fill available width
    try:
        # Access the internal treeview and make columns stretch
        tree = table.view
        for col in tree['columns']:
            tree.column(col, stretch=True)
    except AttributeError:
        pass  # Fallback if attribute name is different
    
    # Initial update of group specifics
    update_group_specifics_for_group(current_staging_group)
    
    # Prevent scrolling the entire window when interacting with a Combobox
    def disable_scroll(event):
        canvas.unbind_all("<MouseWheel>")

    def enable_scroll(event):
        canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Bind focus events for all Combobox widgets explicitly
    def bind_combobox_events(frame):
        for child in frame.winfo_children():
            if isinstance(child, ttk.Combobox):
                child.bind("<Enter>", disable_scroll)
                child.bind("<Leave>", enable_scroll)
            elif isinstance(child, ttk.Frame) or isinstance(child, ttk.LabelFrame):
                bind_combobox_events(child)  # Recursively bind events in nested frames

    bind_combobox_events(main_frame)

    # Bind mouse wheel scrolling to the canvas
    # Adjust mouse wheel scrolling to handle both directions
    def on_mouse_wheel(event):
        direction = -1 if event.delta > 0 else 1
        canvas.yview_scroll(direction, "units")

    canvas.bind_all("<MouseWheel>", on_mouse_wheel)

    # Allow clicking on empty space to clear focus
    def clear_focus(event):
        root.focus_set()

    canvas.bind("<Button-1>", clear_focus)

if __name__ == "__main__":
    root = tb.Window(themename="pulse")
    root.geometry("1100x760")
    create_group_ui(root)
    root.mainloop()