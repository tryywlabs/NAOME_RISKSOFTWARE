"""4_entry_calc component

Provides EntryGridComponent: a 4x4 layout component intended for embedding in
calculation panels. The layout is:

  - Col 0: display Label spanning 4 rows
  - Col 1: four Entry widgets with placeholder text
  - Col 2: four Checkbuttons to select each entry
  - Col 3: an Action button spanning 4 rows

The component is importable and can be instantiated as:
  from ui.main.main_panels.templates.4_entry_calc import EntryGridComponent
  comp = EntryGridComponent(parent)

Running this file directly launches a small demo window.
"""

import tkinter as tk
from tkinter import ttk

__all__ = ["EntryGridComponent"]


class EntryGridComponent(tk.Frame):
    """A reusable 4x4 component with placeholders and selection.

    Methods
    -------
    get_values()
        Returns a list of (value, selected_bool) for each row.

    set_display(text)
        Set the left display label text.
    """

    def __init__(self, parent, placeholders=None, action_text="Action", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        placeholders = placeholders or ["A1", "A2", "A3", "A4"]

        # Configure column weights: column 0 (display) a bit larger,
        # column 1 entries flexible, column 3 action button flexible too.
        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        # Column 0: display label spanning 4 rows
        self.display = tk.Label(self, text="Display", relief="sunken", anchor="center", bg="white")
        self.display.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=(0,6), pady=4)

        # Column 1: entries with placeholders
        self.entries = []
        # Column 2: selection variables
        self.selected = []

        for i in range(4):
            ent = tk.Entry(self)
            ent.grid(row=i, column=1, sticky="ew", padx=4, pady=4)
            self._attach_placeholder(ent, placeholders[i])
            self.entries.append(ent)

            var = tk.BooleanVar(value=False)
            cb = ttk.Checkbutton(self, variable=var)
            cb.grid(row=i, column=2, padx=4)
            self.selected.append(var)

        # Column 3: action button spanning 4 rows
        self.action_btn = ttk.Button(self, text=action_text, command=self._on_action)
        self.action_btn.grid(row=0, column=3, rowspan=4, sticky="nsew", padx=(6,0), pady=4)

    # ----------------- placeholder support -----------------
    def _attach_placeholder(self, entry, placeholder):
        """Add placeholder behavior to a tk.Entry widget."""
        entry.insert(0, placeholder)
        entry._placeholder = placeholder
        entry._is_placeholder = True

        def on_focus_in(event):
            if getattr(entry, "_is_placeholder", False):
                entry.delete(0, "end")
                entry._is_placeholder = False

        def on_focus_out(event):
            if entry.get() == "":
                entry.insert(0, entry._placeholder)
                entry._is_placeholder = True

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

    # ----------------- actions / helpers -----------------
    def _on_action(self):
        # default action: show selected values in the display
        vals = []
        for ent, var in zip(self.entries, self.selected):
            if var.get():
                v = ent.get()
                if getattr(ent, "_is_placeholder", False):
                    v = ""
                vals.append(v)
        self.set_display(', '.join(filter(None, vals)) or 'No selection')

    def get_values(self):
        """Return list of (value, selected_bool) for each row."""
        out = []
        for ent, var in zip(self.entries, self.selected):
            v = ent.get()
            if getattr(ent, "_is_placeholder", False):
                v = ""
            out.append((v, bool(var.get())))
        return out

    def set_display(self, text):
        """Set the left display label text."""
        self.display.config(text=text)


if __name__ == "__main__":
    # Simple demo when run directly
    demo_root = tk.Tk()
    demo_root.title("EntryGridComponent Demo")
    demo_root.geometry("600x240")

    comp = EntryGridComponent(demo_root, placeholders=["Val 1", "Val 2", "Val 3", "Val 4"], action_text="Apply")
    comp.pack(fill="both", expand=True, padx=12, pady=12)

    demo_root.mainloop()
