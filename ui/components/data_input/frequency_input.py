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

'''FUNCTION: create_group_ui(root)'''
def create_group_ui(root):
    """Create the group UI in the provided root window."""

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

    # Configure the canvas to scroll
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

    ttk.Label(grouping_frame, text="Operation hours (/ year):").grid(row=1, column=0, sticky=W, padx=5, pady=5)
    ttk.Spinbox(grouping_frame, from_=0, to=10000, increment=1).grid(row=1, column=1, sticky=W, padx=5, pady=5)

    ttk.Label(grouping_frame, text="Phase:").grid(row=2, column=0, sticky=W, padx=5, pady=5)
    ttk.Combobox(grouping_frame, values=["Liquid", "Gas"], state="readonly").grid(row=2, column=1, sticky=W, padx=5, pady=5)

    ttk.Label(grouping_frame, text="Working Press. (Bar):").grid(row=3, column=0, sticky=W, padx=5, pady=5)
    ttk.Spinbox(grouping_frame, from_=0, to=10000, increment=1).grid(row=3, column=1, sticky=W, padx=5, pady=5)

    ttk.Label(grouping_frame, text="Working Temp. (K):").grid(row=4, column=0, sticky=W, padx=5, pady=5)
    ttk.Spinbox(grouping_frame, from_=270, to=310, increment=1).grid(row=4, column=1, sticky=W, padx=5, pady=5)

    ttk.Label(grouping_frame, text="System Size (mm):").grid(row=5, column=0, sticky=W, padx=5, pady=5)
    ttk.Spinbox(grouping_frame, from_=0, to=10000, increment=0.1).grid(row=5, column=1, sticky=W, padx=5, pady=5)

    group_save_frame = ttk.LabelFrame(grouping_frame, text="Save Group Results", padding=10)
    group_save_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    save_label = ttk.Label(group_save_frame.winfo_toplevel(), text="Save Group Results", font=bold_font)
    group_save_frame.configure(labelwidget=save_label)

    ttk.Button(group_save_frame, text="Save", bootstyle=SUCCESS).grid(row=0, column=1, sticky=NSEW, padx=5, pady=5)

    # Add a scrollable inner box inside the grouping section
    inner_group_frame = ttk.LabelFrame(grouping_frame, text="View of All Groups ", padding=10)
    inner_group_frame.grid(row=0, column=2, columnspan=2, rowspan=6, sticky="nsew", padx=10, pady=5)
    view_label = ttk.Label(inner_group_frame.winfo_toplevel(), text="View of All Groups ", font=bold_font)
    inner_group_frame.configure(labelwidget=view_label)

    # Create a canvas and scrollbar for horizontal scrolling
    inner_canvas = Canvas(inner_group_frame)
    h_scrollbar = ttk.Scrollbar(inner_group_frame, orient="horizontal", command=inner_canvas.xview)
    inner_canvas.configure(xscrollcommand=h_scrollbar.set)

    # Pack the canvas and scrollbar
    inner_canvas.pack(side="top", fill="both", expand=True)
    h_scrollbar.pack(side="bottom", fill="x")

    # Create a frame inside the canvas
    scrollable_frame = ttk.Frame(inner_canvas)
    inner_canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

    # Configure the canvas to scroll horizontally
    def configure_inner_scroll_region(event):
        inner_canvas.configure(scrollregion=inner_canvas.bbox("all"))

    scrollable_frame.bind("<Configure>", configure_inner_scroll_region)

    # Add placeholder content to the scrollable frame
    # TODO: Replace with group data display
    for i in range(20):
        # NOTE: Needlessly complicated... this is placeholder data anyways, but find a way to efficiently label each column per group
        ttk.Label(scrollable_frame, text=f"Item {int(i/2+1-0.5)}").grid(row=0, column=i, columnspan=2, padx=5, pady=5)

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
    ttk.Spinbox(operational_frame, from_=0, to=1000, increment=1).grid(row=1, column=1, sticky=W, padx=5, pady=5)

    ttk.Label(operational_frame, text="Temperature (K):").grid(row=0, column=2, sticky=W, padx=5, pady=5)
    ttk.Spinbox(operational_frame, from_=270, to=310, increment=1).grid(row=1, column=2, sticky=W, padx=5, pady=5)

    ttk.Label(operational_frame, text="Size (mm):").grid(row=0, column=3, sticky=W, padx=5, pady=5)
    ttk.Spinbox(operational_frame, from_=0, to=500, increment=0.1).grid(row=1, column=3, sticky=W, padx=5, pady=5)

    # Add "Confirm" label and button in a frame for proper alignment
    confirm_frame = ttk.Frame(operational_frame)
    confirm_frame.grid(row=0, column=4, rowspan=2, sticky="nsew", padx=5, pady=5)
    ttk.Label(confirm_frame, text="Confirm").pack(pady=(0, 5))
    ttk.Button(confirm_frame, text="OK", bootstyle=SUCCESS).pack(fill="both", expand=True)

    # Equipment List-Up (bottom left)
    equipments = ['1. Centrifugal Compressor', '2. Reciprocating Compressor', '3. Filter', '4. Flange', '5. Fin Fan Head Exchanger', '6. Plate Heat Exchanger', '7. Shell Side Head Exchanger', '8. Tube Side Head Exchanger', '9. Pig Trap', '10. Process Pipe', '11. Centrifugal Pump', '12. Reciprocating Pump', '13. Small Bore Fitting', '14. Actuated Valve', '15. Manual Valve', '16. Process Vessel', '17. Atmospheric Storage Vessel']
    
    equipment_frame = ttk.LabelFrame(conditions_equipment_container, text="Equipment List-Up", padding=10)
    equipment_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    equipment_label = ttk.Label(equipment_frame.winfo_toplevel(), text="Equipment List-Up", font=bold_font)
    equipment_frame.configure(labelwidget=equipment_label)

    ttk.Label(equipment_frame, text="Name of Equipment:").grid(row=0, column=0, sticky=W, padx=5, pady=5)
    ttk.Combobox(equipment_frame, values=equipments, state="readonly").grid(row=1, column=0, sticky=W, padx=5, pady=5)


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
    ttk.Combobox(equipment_frame, values=["≥12.5mm", "≥25mm", "≥50mm", "≥100mm", "≥150mm", "≥250mm", "≥350mm", "500mm"], state="readonly").grid(row=1, column=1, sticky=W, padx=5, pady=5)

    ttk.Label(equipment_frame, text="EA:").grid(row=0, column=2, sticky=W, padx=5, pady=5)
    ttk.Spinbox(equipment_frame, from_=0, to=100, increment=1).grid(row=1, column=2, sticky=W, padx=5, pady=5)

    # Add/Remove/Confirm buttons column
    ttk.Label(equipment_frame, text="Add").grid(row=0, column=3, sticky=W, padx=5, pady=5)
    ttk.Button(equipment_frame, text="✓", bootstyle=SUCCESS, width=5).grid(row=1, column=3, sticky=W, padx=5, pady=5)
    
    ttk.Label(equipment_frame, text="Remove").grid(row=0, column=4, sticky=W, padx=5, pady=5)
    ttk.Button(equipment_frame, text="−", bootstyle=INFO, width=5).grid(row=1, column=4, sticky=W, padx=5, pady=5)
    
    # Add "Confirm" label and button in a frame
    confirm_equip_frame = ttk.Frame(equipment_frame)
    confirm_equip_frame.grid(row=0, column=5, rowspan=2, sticky="nsew", padx=5, pady=5)
    ttk.Label(confirm_equip_frame, text="Confirm").pack(pady=(0, 5))
    ttk.Button(confirm_equip_frame, text="OK", bootstyle=SUCCESS).pack(fill="both", expand=True)

    # Add Group Frame (right side, spanning 2 rows)
    add_group_frame = ttk.LabelFrame(conditions_equipment_container, text="Add Group", padding=10)
    add_group_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
    add_group_label = ttk.Label(add_group_frame.winfo_toplevel(), text="Add Group", font=bold_font)
    add_group_frame.configure(labelwidget=add_group_label)

    # Add Group content
    add_button_frame = ttk.Frame(add_group_frame)
    add_button_frame.pack(pady=20, fill="both", expand=True)
    ttk.Button(add_button_frame, text="Add", bootstyle=INFO, width=15).pack(pady=10)
    
    finish_label = ttk.Label(add_group_frame, text="Finish", font=bold_font)
    finish_label.pack(pady=(20, 5))
    
    finish_button_frame = ttk.Frame(add_group_frame)
    finish_button_frame.pack(pady=10, fill="both", expand=True)
    ttk.Button(finish_button_frame, text="STOP", bootstyle=DANGER, width=15).pack(pady=10)

    # Group List
    group_list_frame = ttk.LabelFrame(main_frame, text="Group Specifics", padding=10)
    group_list_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)
    group_specifics_label = ttk.Label(group_list_frame.winfo_toplevel(), text="Group Specifics", font=bold_font)
    group_list_frame.configure(labelwidget=group_specifics_label)

    columns = ("No.", "Equip. List", "Size", "EA")
    group_list_frame.grid_columnconfigure(0, weight=0)
    group_list_frame.grid_columnconfigure(1, weight=1)

    # Add the spinbox section to the left
    spinbox_label = ttk.Labelframe(group_list_frame, text="Group No.")
    spinbox_label.grid(row=0, column=0, sticky="ew", padx=5, pady=5)

    # NOTE: PLACEHOLDER FOR MAX GROUP.
    # NOTE: In production, this value should be dynamically fetched from the middleware or database.
    max_group_no = 100
    # spinbox for group selection to view specifics
    for i in range(3):
        spinbox = ttk.Spinbox(spinbox_label, from_=1, to=max_group_no, increment=1, width=10)
        spinbox.grid(row=i + 1, column=0, sticky="ew", padx=5, pady=5)

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

    # NOTE: Placeholder data for the rows
    # TODO: Replace by linking with the actual group data stored in memory or db
    # (memory more likely unless user saves the current group data as CSV or to db)
    # Would need to think about what storage mechanisms should be implemented (either one or both)
    rowdata = [
        (1, 'Centrifugal Compressor', '≥100mm', 5),
        (2, 'Reciprocating Compressor', '≥50mm', 3),
        (3, 'Filter', '≥25mm', 10),
        (4, 'Flange', '≥12.5mm', 20),
        (5, 'Fin Fan Head Exchanger', '≥150mm', 2),
        (6, 'Plate Heat Exchanger', '≥100mm', 4),
        (7, 'Shell Side Head Exchanger', '≥250mm', 1),
        (8, 'Tube Side Head Exchanger', '≥250mm', 1),
        (9, 'Pig Trap', '≥100mm', 2),
        (10, 'Process Pipe', '≥50mm', 15),
    ]

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

    # Ensure only the column for "View of All Groups" expands
    grouping_frame.grid_columnconfigure(0, weight=0)
    grouping_frame.grid_columnconfigure(1, weight=0)
    grouping_frame.grid_columnconfigure(2, weight=1)

if __name__ == "__main__":
    root = tb.Window(themename="pulse")
    root.geometry("1100x760")
    create_group_ui(root)
    root.mainloop()