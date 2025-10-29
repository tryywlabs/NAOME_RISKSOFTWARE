"""Entry grid component (renamed to a valid module name).

Contains EntryGridComponent which provides the 4x4 layout described by the
project: display (col0, rowspan 4), entries with placeholders (col1),
checkboxes (col2), and action button (col3, rowspan 4).
"""

import tkinter as tk
from tkinter import ttk

__all__ = ["EntryGridComponent"]


class EntryGridComponent(tk.Frame):
    def __init__(self, parent, placeholders=None, action_text="Action", *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        placeholders = placeholders or ["A1", "A2", "A3", "A4"]

        self.grid_columnconfigure(0, weight=2)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=1)

        self.display = tk.Label(self, text="Display", relief="sunken", anchor="center", bg="white")
        self.display.grid(row=0, column=0, rowspan=4, sticky="nsew", padx=(0,6), pady=4)

        self.entries = []
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

        self.action_btn = ttk.Button(self, text=action_text, command=self._on_action)
        self.action_btn.grid(row=0, column=3, rowspan=4, sticky="nsew", padx=(6,0), pady=4)

    def _attach_placeholder(self, entry, placeholder):
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

    def _on_action(self):
        vals = []
        for ent, var in zip(self.entries, self.selected):
            if var.get():
                v = ent.get()
                if getattr(ent, "_is_placeholder", False):
                    v = ""
                vals.append(v)
        self.set_display(', '.join(filter(None, vals)) or 'No selection')

    def get_values(self):
        out = []
        for ent, var in zip(self.entries, self.selected):
            v = ent.get()
            if getattr(ent, "_is_placeholder", False):
                v = ""
            out.append((v, bool(var.get())))
        return out

    def set_display(self, text):
        self.display.config(text=text)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("EntryGridComponent Demo")
    root.geometry("600x240")
    comp = EntryGridComponent(root, placeholders=["Val 1", "Val 2", "Val 3", "Val 4"], action_text="Apply")
    comp.pack(fill="both", expand=True, padx=12, pady=12)
    root.mainloop()
