"""
FILE: frequency_analysis.py
DESCRIPTION:
    ANALYSIS & RESULT -> Frequency Analysis
    Frequency Analysis UI component using ttkbootstrap and matplotlib.
FUNCTIONS:
    create_frequency_analysis_ui(root):
        Render the frequency analysis page UI in the provided root window.
"""

'''IMPORT STATEMENTS'''
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk
from tkinter import Canvas
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import numpy as np
import sys
import os
import importlib.util

# Add middleware paths - use absolute paths
current_dir = os.path.dirname(os.path.abspath(__file__))
# Go up from: ui/components/analysis/analysis_freq/ to project root
project_root = os.path.abspath(os.path.join(current_dir, '../../../..'))

# Add frequency analysis middleware path (needed for frequency_database import)
freq_analysis_path = os.path.join(project_root, 'middleware/analysis/frequency')
if freq_analysis_path not in sys.path:
    sys.path.insert(0, freq_analysis_path)

# Add database path (needed for supabase_connect import)
db_path = os.path.join(project_root, 'database')
if db_path not in sys.path:
    sys.path.insert(0, db_path)

# Load calculate_freq module using importlib
calculate_freq_path = os.path.join(project_root, 'middleware/analysis/frequency/calculate_freq.py')
print(f"Looking for calculate_freq at: {calculate_freq_path}")
print(f"File exists: {os.path.exists(calculate_freq_path)}")

try:
    spec = importlib.util.spec_from_file_location("calculate_freq", calculate_freq_path)
    calculate_freq_module = importlib.util.module_from_spec(spec)
    sys.modules['calculate_freq'] = calculate_freq_module
    spec.loader.exec_module(calculate_freq_module)
    calculate_all_group_frequencies = calculate_freq_module.calculate_all_group_frequencies
    print(f"Successfully loaded calculate_freq from {calculate_freq_path}")
except Exception as e:
    print(f"Warning: Could not import calculate_freq: {e}")
    import traceback
    traceback.print_exc()
    # Define a fallback function
    def calculate_all_group_frequencies():
        return {}

'''FUNCTION: create_frequency_analysis_ui(root)'''
def create_frequency_analysis_ui(root):
    """Create the frequency analysis UI in the provided root window."""
    
    # Create main container frame
    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill="both", expand=True)
    
    # Storage for widgets that need to be updated
    plot_widgets = {'canvas': None, 'fig': None, 'ax': None}
    table_widgets = {'tree': None}
    legend_widgets = {'frame': None}
    
    def load_frequency_data():
        """Load frequency calculation results"""
        try:
            print("Attempting to load frequency data...")
            frequencies = calculate_all_group_frequencies()
            print(f"Loaded {len(frequencies)} groups")
            if frequencies:
                for group_num, data in frequencies.items():
                    print(f"Group {group_num}: {len(data['equipments'])} equipment(s)")
            return frequencies
        except Exception as e:
            print(f"Error loading frequency data: {str(e)}")
            import traceback
            traceback.print_exc()
            return {}
    
    def update_graph(group_frequencies):
        """Update the graph with new data"""
        if plot_widgets['ax'] is None or plot_widgets['canvas'] is None:
            return
        
        ax = plot_widgets['ax']
        canvas = plot_widgets['canvas']
        
        # Clear the plot
        ax.clear()
        
        # Define leak size categories and their midpoints for plotting
        leak_categories = {
            '1-3mm': 2.0,
            '3-10mm': 6.5,
            '10-50mm': 30.0,
            '50-150mm': 100.0,
            '>150mm': 175.0
        }
        
        # Define colors and styles for each group
        colors = ['black', 'red', 'blue', 'magenta', 'green', 'orange', 'purple', 'brown']
        styles = ['-', '--', '-.', ':', '-', '--', '-.', ':']
        markers = ['x', 's', 'o', 'v', 'd', '^', 'p', '*']
        
        # Plot each group with real data
        if group_frequencies:
            for i, (group_num, data) in enumerate(sorted(group_frequencies.items())):
                color = colors[i % len(colors)]
                style = styles[i % len(styles)]
                marker = markers[i % len(markers)]
                
                group_name = f'Group {group_num}'
                
                # Extract frequency data for each leak size category
                x_values = []
                y_values = []
                
                for category, x_pos in leak_categories.items():
                    if category in data['frequencies']:
                        x_values.append(x_pos)
                        y_values.append(data['frequencies'][category]['total'])
                
                # Plot the group data
                if x_values and y_values:
                    ax.plot(x_values, y_values,
                            color=color,
                            linestyle=style,
                            marker=marker,
                            markersize=6,
                            label=group_name,
                            linewidth=1.5)
        else:
            # Fallback to no data
            leak_sizes = np.linspace(0, 200, 100)
            ax.plot(leak_sizes, np.zeros_like(leak_sizes),
                    color='gray', linestyle='-', marker='x', label='No Data')
        
        # Configure the plot
        ax.set_xlabel('Leak Size (mm)')
        ax.set_ylabel('Leak Freq. (/year)')
        ax.set_yscale('log')
        
        # Set appropriate y-axis limits based on data
        if group_frequencies:
            all_values = []
            for data in group_frequencies.values():
                for rates in data['frequencies'].values():
                    if rates['total'] > 0:
                        all_values.append(rates['total'])
            if all_values:
                min_val = min(all_values)
                max_val = max(all_values)
                ax.set_ylim(min_val * 0.5, max_val * 2)
            else:
                ax.set_ylim(1e-6, 1e-1)
        else:
            ax.set_ylim(1e-6, 1e-1)
        
        ax.set_xlim(0, 150)
        ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
        ax.set_facecolor('#f0f0f0')
        
        canvas.draw()
        return group_frequencies
    
    def update_table(group_frequencies):
        """Update the table with new data"""
        if table_widgets['tree'] is None:
            return
        
        tree = table_widgets['tree']
        
        # Clear existing data
        for item in tree.get_children():
            tree.delete(item)
        
        # Populate table with real data
        total_by_category = {
            '1-3mm': 0.0,
            '3-10mm': 0.0,
            '10-50mm': 0.0,
            '50-150mm': 0.0,
            '>150mm': 0.0,
            'Total': 0.0
        }
        
        if group_frequencies:
            for group_num in sorted(group_frequencies.keys()):
                data = group_frequencies[group_num]
                frequencies = data['frequencies']
                
                row_data = [str(group_num)]
                group_total = 0.0
                
                for category in ['1-3mm', '3-10mm', '10-50mm', '50-150mm', '>150mm']:
                    if category in frequencies:
                        freq = frequencies[category]['total']
                        row_data.append(f"{freq:.6f}")
                        total_by_category[category] += freq
                        group_total += freq
                    else:
                        row_data.append("0.000000")
                
                row_data.append(f"{group_total:.6f}")
                total_by_category['Total'] += group_total
                tree.insert("", "end", values=row_data)
            
            # Add total row
            total_row = ["Total"]
            for category in ['1-3mm', '3-10mm', '10-50mm', '50-150mm', '>150mm', 'Total']:
                total_row.append(f"{total_by_category[category]:.6f}")
            tree.insert("", "end", values=total_row, tags=("total",))
        else:
            # Show "No Data" message if no groups found
            tree.insert("", "end", values=("No Data", "0.000000", "0.000000", "0.000000", "0.000000", "0.000000", "0.000000"))
    
    def update_legend(group_frequencies):
        """Update the legend with new group data"""
        if legend_widgets['frame'] is None:
            return
        
        legend_frame = legend_widgets['frame']
        
        # Clear existing legend items
        for widget in legend_frame.winfo_children():
            widget.destroy()
        
        # Define colors and styles for each group
        colors = ['black', 'red', 'blue', 'magenta', 'green', 'orange', 'purple', 'brown']
        styles = ['-', '--', '-.', ':', '-', '--', '-.', ':']
        markers = ['x', 's', 'o', 'v', 'd', '^', 'p', '*']
        
        if group_frequencies:
            for i, group_num in enumerate(sorted(group_frequencies.keys())):
                color = colors[i % len(colors)]
                style = styles[i % len(styles)]
                marker = markers[i % len(markers)]
                group_name = f'Group {group_num}'
                
                row_frame = ttk.Frame(legend_frame)
                row_frame.pack(fill="x", pady=2)
                
                # Create a small canvas for the line indicator
                indicator = Canvas(row_frame, width=30, height=15, bg='white', highlightthickness=0)
                indicator.pack(side="left", padx=5)
                
                # Draw the line style
                if style == '-':
                    indicator.create_line(5, 8, 25, 8, fill=color, width=2)
                elif style == '--':
                    indicator.create_line(5, 8, 25, 8, fill=color, width=2, dash=(4, 2))
                elif style == '-.':
                    indicator.create_line(5, 8, 25, 8, fill=color, width=2, dash=(6, 2, 2, 2))
                elif style == ':':
                    indicator.create_line(5, 8, 25, 8, fill=color, width=2, dash=(2, 2))
                
                # Draw marker
                marker_x, marker_y = 15, 8
                if marker == 'x':
                    indicator.create_line(marker_x-3, marker_y-3, marker_x+3, marker_y+3, fill=color, width=2)
                    indicator.create_line(marker_x-3, marker_y+3, marker_x+3, marker_y-3, fill=color, width=2)
                elif marker == 's':
                    indicator.create_rectangle(marker_x-3, marker_y-3, marker_x+3, marker_y+3, outline=color, width=2)
                elif marker == 'o':
                    indicator.create_oval(marker_x-3, marker_y-3, marker_x+3, marker_y+3, outline=color, width=2)
                elif marker == 'v':
                    indicator.create_polygon(marker_x, marker_y+3, marker_x-3, marker_y-3, marker_x+3, marker_y-3, 
                                           outline=color, fill='', width=2)
                elif marker == 'd':
                    indicator.create_polygon(marker_x, marker_y-3, marker_x+3, marker_y, marker_x, marker_y+3, marker_x-3, marker_y,
                                           outline=color, fill='', width=2)
                elif marker == '^':
                    indicator.create_polygon(marker_x, marker_y-3, marker_x-3, marker_y+3, marker_x+3, marker_y+3,
                                           outline=color, fill='', width=2)
                elif marker == 'p':
                    # Pentagon
                    pts = [(marker_x, marker_y-3), (marker_x+3, marker_y-1), (marker_x+2, marker_y+3),
                           (marker_x-2, marker_y+3), (marker_x-3, marker_y-1)]
                    indicator.create_polygon(*[c for pt in pts for c in pt], outline=color, fill='', width=2)
                elif marker == '*':
                    # Star
                    for angle in range(0, 360, 72):
                        rad = np.radians(angle)
                        x1, y1 = marker_x + 3*np.cos(rad), marker_y + 3*np.sin(rad)
                        indicator.create_line(marker_x, marker_y, x1, y1, fill=color, width=2)
                
                # Add label
                ttk.Label(row_frame, text=group_name).pack(side="left")
        else:
            ttk.Label(legend_frame, text="No Data").pack()
    
    def refresh_analysis():
        """Refresh the analysis by reloading data and updating all visualizations"""
        print("Refreshing frequency analysis...")
        group_frequencies = load_frequency_data()
        update_graph(group_frequencies)
        update_table(group_frequencies)
        update_legend(group_frequencies)
        print("Refresh complete!")
    
    # Initial load
    group_frequencies = load_frequency_data()
    
    # Configure grid - add row for refresh button
    main_frame.grid_columnconfigure(0, weight=3)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=0)  # Refresh button row
    main_frame.grid_rowconfigure(1, weight=3)  # Graph row
    main_frame.grid_rowconfigure(2, weight=1)  # Table row
    
    # Add refresh button at the top
    button_frame = ttk.Frame(main_frame)
    button_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=5, pady=5)
    
    refresh_btn = tb.Button(
        button_frame,
        text="🔄 Refresh Analysis",
        bootstyle="success",
        command=refresh_analysis
    )
    refresh_btn.pack(side="right", padx=5)
    
    # Create the graph frame (top left)
    graph_frame = ttk.LabelFrame(main_frame, text="Frequency Analysis Graph", padding=10)
    graph_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    # Create matplotlib figure
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Store references for updates
    plot_widgets['fig'] = fig
    plot_widgets['ax'] = ax
    
    # Create canvas and embed in tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.get_tk_widget().pack(fill="both", expand=True)
    plot_widgets['canvas'] = canvas
    
    # Initial plot rendering
    update_graph(group_frequencies)
    
    # Create legend frame (top right)
    legend_frame = ttk.LabelFrame(main_frame, text="Sub Groups", padding=10)
    legend_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    legend_widgets['frame'] = legend_frame
    
    # Initial legend rendering
    update_legend(group_frequencies)
    
    # Create data table frame (bottom left)
    table_frame = ttk.LabelFrame(main_frame, text="Frequency Data Table", padding=10)
    table_frame.grid(row=2, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    
    # Create Treeview for the table
    columns = ("Group", "1-3mm", "3-10mm", "10-50mm", "50-150mm", ">150mm", "Total")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
    
    # Configure column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    # Configure tag for total row
    tree.tag_configure("total", background="#e0e0e0", font=("TkDefaultFont", 9, "bold"))
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack the table and scrollbar
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    # Store reference for updates
    table_widgets['tree'] = tree
    
    # Initial table rendering
    update_table(group_frequencies)
    
    return main_frame


if __name__ == "__main__":
    root = tb.Window(themename="pulse")
    root.geometry("1000x700")
    root.title("Frequency Analysis")
    create_frequency_analysis_ui(root)
    root.mainloop()
