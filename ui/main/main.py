"""
FILE: nested_notebook_demo.py

DESCRIPTION:
    Nested notebook demo using ttkbootstrap.

    Creates a top-level window with an outer Notebook (3 tabs) and an inner
    Notebook inside the Data Input tab with 4 tabs. This file is intended as a
    drop-in runnable demo and will fall back to standard ttk if ttkbootstrap is
    not available.

FUNCTIONS:
    1. build(root, style=None):
        Build the nested notebook UI into the provided `root` window. If
        `style` is provided (ttkbootstrap Style), apply the theme to the UI.
    2. main():
        Create the main application window, set up ttkbootstrap if available,
        and launch the nested notebook demo.
"""

'''IMPORT STATEMENTS'''

# Debug block for ttkbootstrap availability check
import ttkbootstrap as tb
try:
    from ttkbootstrap.constants import *
    # Boolean flag for indicating ttkbootstrap availability
    TB_AVAILABLE = True
except Exception:
    import tkinter as tk
    from tkinter import ttk
    # Boolean flag for indicating ttkbootstrap availability
    TB_AVAILABLE = False
import tkinter as tk
from tkinter import ttk
import pathlib
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../components/data_input')))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../components/analysis/frequency')))
from frequency_input import create_group_ui
from frequency_analysis import create_frequency_analysis_ui

'''build(root, style=None): FUNCTION'''

def build(root, style=None):
    '''Build UI into `root`. `style` should be created before calling this
    function so widgets pick up the theme immediately.
    '''

    # Apply the theme if ttkbootstrap is available and a style is provided
    if TB_AVAILABLE and style:
        style.theme_use(style.theme.name)
        # Use valid attributes from style.colors
        background_color = style.colors.bg
        text_color = style.colors.fg
        # Configure outer notebook with tabs on left side
        style.configure('Outer.TNotebook', tabposition='wn')
        # Configure inner notebooks with tabs on top
        style.configure('Inner.TNotebook', tabposition='n')
        style.configure('TFrame', background=background_color)
        style.configure('TLabel', background=background_color, foreground=text_color)

    # Create top frame for theme toggle button
    top_frame = tb.Frame(root) if TB_AVAILABLE else ttk.Frame(root)
    top_frame.pack(side='top', fill='x', padx=10, pady=5)
    
    # Add theme toggle button
    current_theme = {'name': style.theme.name if TB_AVAILABLE and style else 'pulse'}
    
    def toggle_theme():
        if TB_AVAILABLE and style:
            if current_theme['name'] == 'pulse':
                new_theme = 'solar'
                button_text = '☀️ Light Mode'
            else:
                new_theme = 'pulse'
                button_text = '🌙 Dark Mode'
            
            style.theme_use(new_theme)
            current_theme['name'] = new_theme
            theme_button.configure(text=button_text)
            
            # Reapply notebook configuration after theme change
            style.configure('Outer.TNotebook', tabposition='wn')
            style.configure('Outer.TNotebook.Tab', padding=[20, 10], width=15)
            style.configure('Inner.TNotebook', tabposition='n')
            background_color = style.colors.bg
            text_color = style.colors.fg
            style.configure('TFrame', background=background_color)
            style.configure('TLabel', background=background_color, foreground=text_color)
    
    # Set initial button text based on current theme
    initial_button_text = '🌙 Dark Mode' if current_theme['name'] == 'pulse' else '☀️ Light Mode'
    theme_button = tb.Button(top_frame, text=initial_button_text, command=toggle_theme, bootstyle='secondary-outline') if TB_AVAILABLE else ttk.Button(top_frame, text=initial_button_text, command=toggle_theme)
    theme_button.pack(side='right', padx=5)

    # Main Tab Container with tabs on the left
    if TB_AVAILABLE:
        outer = tb.Notebook(root, style='Outer.TNotebook')
    else:
        outer = ttk.Notebook(root, style='Outer.TNotebook')
    outer.pack(fill='both', expand=True)
    
    # Configure outer notebook tab width to stretch horizontally
    if TB_AVAILABLE and style:
        style.configure('Outer.TNotebook.Tab', padding=[20, 10], width=15)

    # Data Input tab with inner notebook
    data_frame = tb.Frame(outer) if TB_AVAILABLE else ttk.Frame(outer)
    outer.add(data_frame, text='📝 Data Input')

    if TB_AVAILABLE:
        inner = tb.Notebook(data_frame, style='Inner.TNotebook')
    else:
        inner = ttk.Notebook(data_frame, style='Inner.TNotebook')
    inner.pack(fill='both', expand=True, padx=6, pady=6)

    param = tb.Frame(inner) if TB_AVAILABLE else ttk.Frame(inner)
    freq = tb.Frame(inner) if TB_AVAILABLE else ttk.Frame(inner)
    cons = tb.Frame(inner) if TB_AVAILABLE else ttk.Frame(inner)
    safety = tb.Frame(inner) if TB_AVAILABLE else ttk.Frame(inner)

    inner.add(param, text='Parameter Input')
    inner.add(freq, text='Frequency Data')
    inner.add(cons, text='Consequence Data')
    inner.add(safety, text='Safety system & Human factor')

    # Analysis & Result tab with inner notebook
    analysis_frame = tb.Frame(outer) if TB_AVAILABLE else ttk.Frame(outer)
    outer.add(analysis_frame, text='📊 Analysis & Result')
    
    if TB_AVAILABLE:
        analysis_inner = tb.Notebook(analysis_frame, style='Inner.TNotebook')
    else:
        analysis_inner = ttk.Notebook(analysis_frame, style='Inner.TNotebook')
    analysis_inner.pack(fill='both', expand=True, padx=6, pady=6)
    
    freq_analysis = tb.Frame(analysis_inner) if TB_AVAILABLE else ttk.Frame(analysis_inner)
    cons_analysis = tb.Frame(analysis_inner) if TB_AVAILABLE else ttk.Frame(analysis_inner)
    risk_assessment = tb.Frame(analysis_inner) if TB_AVAILABLE else ttk.Frame(analysis_inner)
    
    analysis_inner.add(freq_analysis, text='Frequency Analysis')
    analysis_inner.add(cons_analysis, text='Consequence Analysis')
    analysis_inner.add(risk_assessment, text='Risk Assessment')
    
    # Extra tab
    outer.add(tb.Frame(outer) if TB_AVAILABLE else ttk.Frame(outer), text='⚙️ Extra')

    # Put placeholder content in the parameter tab replicating the wireframe
    lbl = tb.Label(param, text='Parameter Input area — add widgets here', anchor='center') if TB_AVAILABLE else ttk.Label(param, text='Parameter Input area — add widgets here', anchor='center')
    lbl.pack(fill='both', expand=True, padx=12, pady=12)

    # Replace placeholder content in the Frequency Data tab with the frame from frequency_data.py
    for widget in freq.winfo_children():
        widget.destroy()  # Clear placeholder content
    create_group_ui(freq)

    lbl3 = tb.Label(cons, text='Consequence Data area — add widgets here', anchor='center') if TB_AVAILABLE else ttk.Label(cons, text='Consequence Data area — add widgets here', anchor='center')
    lbl3.pack(fill='both', expand=True, padx=12, pady=12)

    lbl4 = tb.Label(safety, text='Safety system & Human factor area — add widgets here', anchor='center') if TB_AVAILABLE else ttk.Label(safety, text='Safety system & Human factor area — add widgets here', anchor='center')
    lbl4.pack(fill='both', expand=True, padx=12, pady=12)

    # Add frequency analysis UI to Frequency Analysis tab
    create_frequency_analysis_ui(freq_analysis)
    
    # Add placeholder content for other analysis tabs
    lbl_cons_analysis = tb.Label(cons_analysis, text='Consequence Analysis area — add widgets here', anchor='center') if TB_AVAILABLE else ttk.Label(cons_analysis, text='Consequence Analysis area — add widgets here', anchor='center')
    lbl_cons_analysis.pack(fill='both', expand=True, padx=12, pady=12)
    
    lbl_risk = tb.Label(risk_assessment, text='Risk Assessment area — add widgets here', anchor='center') if TB_AVAILABLE else ttk.Label(risk_assessment, text='Risk Assessment area — add widgets here', anchor='center')
    lbl_risk.pack(fill='both', expand=True, padx=12, pady=12)

    return root

'''main(): FUNCTION'''

def main():
    if TB_AVAILABLE:
        thistheme = "pulse"
        root = tb.Window(themename=thistheme)
        style = tb.Style(theme=thistheme)
        print("ttkbootstrap available — using theme:", thistheme)
    else:
        root = tk.Tk()
        root.title('Main Page')
        style = ttk.Style(root)
        print("ttkbootstrap not available — using default ttk style")

    root.geometry('1100x760')
    build(root, style=style)
    root.title('NAOME Risk Assessment Software')
    root.mainloop()


if __name__ == '__main__':
    main()
