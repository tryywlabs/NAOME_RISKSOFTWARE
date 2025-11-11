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

'''FUNCTION: create_frequency_analysis_ui(root)'''
def create_frequency_analysis_ui(root):
    """Create the frequency analysis UI in the provided root window."""
    
    # Create main container frame
    main_frame = ttk.Frame(root, padding=10)
    main_frame.pack(fill="both", expand=True)
    
    # Configure grid
    main_frame.grid_columnconfigure(0, weight=3)
    main_frame.grid_columnconfigure(1, weight=1)
    main_frame.grid_rowconfigure(0, weight=3)
    main_frame.grid_rowconfigure(1, weight=1)
    
    # Create the graph frame (top left)
    graph_frame = ttk.LabelFrame(main_frame, text="Frequency Analysis Graph", padding=10)
    graph_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    # Create matplotlib figure
    fig = Figure(figsize=(6, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Sample data for sub-groups (you'll replace this with actual data)
    leak_sizes = np.linspace(0, 200, 100)
    
    # Define colors and styles for each sub-group
    subgroup_data = {
        'Sub_Group 1': {'color': 'black', 'style': '-', 'marker': 'x'},
        'Sub_Group 2': {'color': 'red', 'style': '--', 'marker': 's'},
        'Sub_Group 3': {'color': 'black', 'style': '-.', 'marker': 'x'},
        'Sub_Group 4': {'color': 'magenta', 'style': '--', 'marker': 'v'},
        'Sub_Group 5': {'color': 'black', 'style': ':', 'marker': 'x'},
        'Sub_Group 6': {'color': 'blue', 'style': '-.', 'marker': 'd'},
    }
    
    # Plot each sub-group with different curves
    for i, (name, style) in enumerate(subgroup_data.items()):
        # Generate sample frequency data (replace with actual calculations)
        # Exponential decay with different rates for each group
        leak_freq = 6e-3 * np.exp(-leak_sizes / (50 + i * 10))
        ax.plot(leak_sizes, leak_freq, 
                color=style['color'], 
                linestyle=style['style'],
                marker=style['marker'],
                markevery=10,
                markersize=4,
                label=name,
                linewidth=1.5)
    
    # Configure the plot
    ax.set_xlabel('Leak Size (mm)')
    ax.set_ylabel('Leak Freq. (/year)')
    ax.set_yscale('log')
    ax.set_ylim(1e-1, 1e-2)
    ax.set_xlim(0, 200)
    ax.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)
    ax.set_facecolor('#f0f0f0')
    
    # Adjust layout to prevent label cutoff
    fig.tight_layout()
    
    # Embed the plot in tkinter
    canvas = FigureCanvasTkAgg(fig, master=graph_frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill="both", expand=True)
    
    # Create legend frame (top right)
    legend_frame = ttk.LabelFrame(main_frame, text="Sub Groups", padding=10)
    legend_frame.grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
    
    # Add checkboxes for each sub-group with colored indicators
    for i, (name, style) in enumerate(subgroup_data.items()):
        row_frame = ttk.Frame(legend_frame)
        row_frame.pack(fill="x", pady=2)
        
        # Create a small canvas for the line indicator
        indicator = Canvas(row_frame, width=30, height=15, bg='white', highlightthickness=0)
        indicator.pack(side="left", padx=5)
        
        # Draw the line style
        if style['style'] == '-':
            indicator.create_line(5, 8, 25, 8, fill=style['color'], width=2)
        elif style['style'] == '--':
            indicator.create_line(5, 8, 25, 8, fill=style['color'], width=2, dash=(4, 2))
        elif style['style'] == '-.':
            indicator.create_line(5, 8, 25, 8, fill=style['color'], width=2, dash=(6, 2, 2, 2))
        elif style['style'] == ':':
            indicator.create_line(5, 8, 25, 8, fill=style['color'], width=2, dash=(2, 2))
        
        # Draw marker
        marker_x, marker_y = 15, 8
        if style['marker'] == 'x':
            indicator.create_line(marker_x-3, marker_y-3, marker_x+3, marker_y+3, fill=style['color'], width=2)
            indicator.create_line(marker_x-3, marker_y+3, marker_x+3, marker_y-3, fill=style['color'], width=2)
        elif style['marker'] == 's':
            indicator.create_rectangle(marker_x-3, marker_y-3, marker_x+3, marker_y+3, outline=style['color'], width=2)
        elif style['marker'] == 'v':
            indicator.create_polygon(marker_x, marker_y+3, marker_x-3, marker_y-3, marker_x+3, marker_y-3, 
                                   outline=style['color'], fill='', width=2)
        elif style['marker'] == 'd':
            indicator.create_polygon(marker_x, marker_y-3, marker_x+3, marker_y, marker_x, marker_y+3, marker_x-3, marker_y,
                                   outline=style['color'], fill='', width=2)
        
        # Add label
        ttk.Label(row_frame, text=name).pack(side="left")
    
    # Create data table frame (bottom left)
    table_frame = ttk.LabelFrame(main_frame, text="Frequency Data Table", padding=10)
    table_frame.grid(row=1, column=0, columnspan=2, sticky="nsew", padx=5, pady=5)
    
    # Create Treeview for the table
    columns = ("Sub Group", "<=3mm", "<=10mm", "<=50mm", "<150mm", ">=150mm")
    tree = ttk.Treeview(table_frame, columns=columns, show="headings", height=6)
    
    # Configure column headings
    for col in columns:
        tree.heading(col, text=col)
        tree.column(col, width=100, anchor="center")
    
    # Sample data (replace with actual calculations)
    sample_data = [
        ("1", "0.001927", "0.000704", "0.000307", "0.000035", "0.000102"),
        ("2", "0.004271", "0.001788", "0.001029", "0.000035", "0.000106"),
        ("3", "0.003238", "0.001306", "0.000713", "0.000127", "0.000000"),
        ("4", "0.002718", "0.001252", "0.000797", "0.000070", "0.000188"),
        ("Total", "0.012154", "0.005050", "0.002846", "0.000267", "0.000396"),
    ]
    
    # Insert data
    for i, row in enumerate(sample_data):
        if row[0] == "Total":
            # Highlight total row
            tree.insert("", "end", values=row, tags=("total",))
        else:
            tree.insert("", "end", values=row)
    
    # Configure tag for total row
    tree.tag_configure("total", background="#e0e0e0", font=("TkDefaultFont", 9, "bold"))
    
    # Add scrollbar
    scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=tree.yview)
    tree.configure(yscrollcommand=scrollbar.set)
    
    # Pack the table and scrollbar
    tree.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    return main_frame


if __name__ == "__main__":
    root = tb.Window(themename="pulse")
    root.geometry("1000x700")
    root.title("Frequency Analysis")
    create_frequency_analysis_ui(root)
    root.mainloop()
