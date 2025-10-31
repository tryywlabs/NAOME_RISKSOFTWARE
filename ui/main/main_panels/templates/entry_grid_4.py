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
    def __init__(self, parent, placeholders=None, action_text="Action", fixed_width=None, entry_width=20, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        placeholders = placeholders or ["A1", "A2", "A3", "A4"]

        # If fixed_width is provided (pixels), request that width and disable
        # geometry propagation so the component keeps a stable size when the
        # parent resizes. Entry widths are specified in characters via
        # `entry_width`.
        if fixed_width is not None:
            try:
                # Request a preferred width but keep geometry propagation
                # enabled so the frame's height is determined by its children.
                # Disabling propagation can collapse the frame if a height
                # isn't also requested.
                self.configure(width=fixed_width)
            except Exception:
                # If configure/grid_propagate are not applicable in some
                # contexts, ignore silently and continue.
                pass

        # Use fixed internal column weights so the component doesn't expand
        # entries/display when the external layout stretches. This keeps the
        # component dimensions stable; use `fixed_width` above for outer
        # constraint.
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=0)
        self.grid_columnconfigure(2, weight=0)
        self.grid_columnconfigure(3, weight=0)

        # Display area: set a fixed character width so its horizontal size is
        # controlled by the component. We use anchor='w' so overflow text is
        # clipped on the right instead of centered-expanding the widget.
        self.display = tk.Label(self, text="Display", relief="sunken", anchor="center", justify="center", bg="white")
        # If fixed_width is provided, set a label wraplength (pixels) so
        # long text will wrap into multiple lines instead of forcing the
        # component to expand horizontally. Also set a minimum column size
        # so the display column width remains stable.
        if fixed_width is not None:
            try:
                # reserve a portion of the fixed width for the display column
                display_px = max(80, int(fixed_width * 0.28))
                self.grid_columnconfigure(0, minsize=display_px, maxsize=display_px)
                self.display.config(wraplength=display_px - 8, justify='left', width=int(display_px / 8))
            except Exception:
                pass
        else:
            # Heuristic default wrap width (approx pixels per character)
            self.display.config(width=20, wraplength=160, justify='left')

        # Place the display; use vertical sticky so it won't stretch the
        # component horizontally when grid_propagate is disabled.
        self.display.grid(row=0, column=0, rowspan=4, sticky="ns", padx=(0,6), pady=4)

        self.entries = []
        self.selected = []

        # NOTE: Use instead of Entry widgets when dropdowns are needed
        self.dropdowns = ["Option1", "Option2", "Option3", "Option4", "Option5", "Option6"]

        for i in range(4):
            cb = ttk.Combobox(self, values=self.dropdowns, width=entry_width)
            # Do not make the combobox expand to fill available horizontal
            # space; we want a stable size.
            cb.grid(row=i, column=1, sticky="w", padx=4, pady=4)
            self._attach_placeholder(cb, placeholders[i])
            self.entries.append(cb)
            # ent = tk.Entry(self)
            # ent.grid(row=i, column=1, sticky="ew", padx=4, pady=4)
            # self._attach_placeholder(ent, placeholders[i])
            # self.entries.append(ent)

            var = tk.BooleanVar(value=False)
            cb = ttk.Checkbutton(self, variable=var)
            cb.grid(row=i, column=2, padx=4)
            self.selected.append(var)

        self.action_btn = ttk.Button(self, text=action_text, command=self._on_action)
        self.action_btn.grid(row=0, column=3, rowspan=4, sticky="nsew", padx=(6,0), pady=4)

    def _attach_placeholder(self, entry, placeholder):
        # Support both regular Entry and ttk.Combobox. For Combobox prefer
        # using set()/get() so the displayed value updates correctly.
        is_combo = isinstance(entry, ttk.Combobox)

        if is_combo:
            entry.set(placeholder)
        else:
            entry.insert(0, placeholder)

        entry._placeholder = placeholder
        entry._is_placeholder = True

        def on_focus_in(event):
            if getattr(entry, "_is_placeholder", False):
                if is_combo:
                    entry.set("")
                else:
                    entry.delete(0, "end")
                entry._is_placeholder = False

        def on_focus_out(event):
            # If the widget is empty, restore the placeholder
            if (is_combo and entry.get() == "") or (not is_combo and entry.get() == ""):
                if is_combo:
                    entry.set(entry._placeholder)
                else:
                    entry.insert(0, entry._placeholder)
                entry._is_placeholder = True

        entry.bind("<FocusIn>", on_focus_in)
        entry.bind("<FocusOut>", on_focus_out)

        # For Combobox, also clear the placeholder flag when the user selects
        # an item from the dropdown so subsequent reads return the real value.
        if is_combo:
            def on_combo_selected(event):
                entry._is_placeholder = False

            entry.bind('<<ComboboxSelected>>', on_combo_selected)

    def _on_action(self):
        vals = []
        for ent, var in zip(self.entries, self.selected):
            if var.get():
                v = ent.get()
                if getattr(ent, "_is_placeholder", False):
                    v = ""
                vals.append(v)
        self.set_display(', '.join(filter(None, vals)) or ' No selection')

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

# ----------------- demo / test -----------------
if __name__ == "__main__":
    root = tk.Tk()
    root.title("EntryGridComponent Demo")
    root.geometry("600x240")
    comp = EntryGridComponent(root, placeholders=["Val 1", "Val 2", "Val 3", "Val 4"], action_text="Apply")
    comp.pack(fill="both", expand=True, padx=12, pady=12)
    root.mainloop()
