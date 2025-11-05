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
from frequency_data import create_group_ui

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
        style.configure('TNotebook', tabposition='n')
        style.configure('TFrame', background=background_color)
        style.configure('TLabel', background=background_color, foreground=text_color)

    # Main Tab Container
    outer = tb.Notebook(root) if TB_AVAILABLE else ttk.Notebook(root)
    outer.pack(fill='both', expand=True)

    # Data Input tab with inner notebook
    data_frame = tb.Frame(outer) if TB_AVAILABLE else ttk.Frame(outer)
    outer.add(data_frame, text='Data Input')

    inner = tb.Notebook(data_frame) if TB_AVAILABLE else ttk.Notebook(data_frame)
    inner.pack(fill='both', expand=True, padx=6, pady=6)

    param = tb.Frame(inner) if TB_AVAILABLE else ttk.Frame(inner)
    freq = tb.Frame(inner) if TB_AVAILABLE else ttk.Frame(inner)
    cons = tb.Frame(inner) if TB_AVAILABLE else ttk.Frame(inner)
    safety = tb.Frame(inner) if TB_AVAILABLE else ttk.Frame(inner)

    inner.add(param, text='Parameter Input')
    inner.add(freq, text='Frequency Data')
    inner.add(cons, text='Consequence Data')
    inner.add(safety, text='Safety system & Human factor')

    # Outer tabs
    outer.add(tb.Frame(outer) if TB_AVAILABLE else ttk.Frame(outer), text='Analysis & Result')
    outer.add(tb.Frame(outer) if TB_AVAILABLE else ttk.Frame(outer), text='Extra')

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
    root.mainloop()


if __name__ == '__main__':
    main()
