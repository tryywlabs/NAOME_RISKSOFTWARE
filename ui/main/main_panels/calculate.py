'''
FILE: calculate.py
DESCRIPTION: Labview calculation panel copy for risk factors.
NOTE: Might become boilerplate template for other tabs as well.
'''

import sys
import pathlib
import tkinter as tk
from tkinter import ttk

# Try absolute package import first. If the script is being run directly from
# a subdirectory (for example `ui/main/main_panels`), `ui` won't be on
# sys.path and the import will fail. In that case add the project root to
# sys.path and retry so this module can be executed directly for quick
# debugging.
try:
    from ui.main.main_panels.templates.entry_grid_4 import EntryGridComponent
except ModuleNotFoundError:
    # repo root is two levels up from ui/main/main_panels (i.e. RISKSOFTWARE)
    repo_root = pathlib.Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(repo_root))
    from ui.main.main_panels.templates.entry_grid_4 import EntryGridComponent


class CalculateFrame(tk.Frame):
    def __init__(self, container, *args, **kwargs):
        super().__init__(container, *args, **kwargs)
        # Use grid layout so multiple components can be arranged neatly.
        self.columnconfigure(0, weight=1)
        self.rowconfigure(1, weight=1)

        label = ttk.Label(self, text="Calculation Panel", font=("Helvetica", 16))
        label.grid(row=0, column=0, sticky='w', padx=12, pady=(12, 6))
        self.configure(bg='LightCyan3')
        # Content area where multiple EntryGridComponents can be arranged in a grid
        self.content = ttk.Frame(self)
        self.content.grid(row=1, column=0, sticky='nsew', padx=12, pady=8)
        # make a 2x2 grid by default (you can change sizes as needed)
        for c in range(2):
            self.content.columnconfigure(c, weight=1)
        for r in range(2):
            self.content.rowconfigure(r, weight=1)
        # Create and place four EntryGridComponents in a 2x2 arrangement
        self.entry_grids = []
        for r in range(2):
            for c in range(2):
                comp = EntryGridComponent(self.content,
                                          placeholders=[f'R{r+1}C{c+1}-1', f'R{r+1}C{c+1}-2', f'R{r+1}C{c+1}-3', f'R{r+1}C{c+1}-4'],
                                          action_text='Apply')
                comp.grid(row=r, column=c, sticky='nsew', padx=6, pady=6)
                self.entry_grids.append(comp)

    def add_component(self, comp, row, column):
        """Add an EntryGridComponent instance at given grid position inside the panel."""
        comp.grid(in_=self.content, row=row, column=column, sticky='nsew', padx=6, pady=6)
        self.entry_grids.append(comp)
    

if __name__ == "__main__":
  root = tk.Tk()
  root.title("Calculation Panel Test")
  root.geometry("800x600")
  calc_frame = CalculateFrame(root)
  calc_frame.pack(fill='both', expand=True)
  root.mainloop()
