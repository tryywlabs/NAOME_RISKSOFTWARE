import ttkbootstrap as tkbs
from ttkbootstrap.constants import LEFT, RIGHT, X
import tkinter as tk

class TabBar(tk.Frame):
    def __init__(self, master, switch_callback, **kw):
        super().__init__(master, **kw)
        self.switch_callback = switch_callback
        self.tabs = []
        self.active_tab = None

        # Left/back button (optional)
        self.left_btn = tk.Button(self, text='◀', width=2, command=self.scroll_left)

        # Canvas that holds the tab frames so we can scroll horizontally
        self.canvas = tk.Canvas(self, height=34, bd=0, highlightthickness=0)

        # Right/forward button (optional)
        self.right_btn = tk.Button(self, text='▶', width=2, command=self.scroll_right)

        # Layout using grid so the canvas (column 1) expands to fill available width.
        # This is more robust than pack for making the tab row span the full window.
        self.grid_columnconfigure(1, weight=1)
        self.left_btn.grid(row=0, column=0, sticky='w', padx=(2,0), pady=2)
        self.canvas.grid(row=0, column=1, sticky='ew')
        self.right_btn.grid(row=0, column=2, sticky='e', padx=(0,2), pady=2)

        # create an interior frame to put tab widgets inside the canvas
        self.inner = tk.Frame(self.canvas)
        self.inner_id = self.canvas.create_window((0,0), window=self.inner, anchor='nw')

        # new tab button (unused for fixed tabs)
        # self.new_tab_btn = tk.Button(self, text='+', width=3, command=self.add_new_tab)
        # self.new_tab_btn.pack(side=RIGHT, padx=4)

        # scrolling bindings
        self.inner.bind('<Configure>', lambda e: self._on_inner_configure())
        self.canvas.bind('<Configure>', lambda e: self._on_canvas_configure())
        self.canvas.bind_all('<Shift-MouseWheel>', self._on_shiftwheel)  # horizontal wheel

    def _on_inner_configure(self):
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self):
        # keep inner window width to canvas width when there are few tabs
        canvas_w = self.canvas.winfo_width()
        inner_w = self.inner.winfo_reqwidth()
        if inner_w < canvas_w:
            self.canvas.itemconfig(self.inner_id, width=canvas_w)

    def _on_shiftwheel(self, event):
        # shift+wheel scrolls horizontally inside canvas
        # positive delta -> scroll left
        self.canvas.xview_scroll(int(-1*(event.delta/120)), 'units')

    def add_tab(self, tab_id, title):
        # create a tab widget: small frame with label (fixed, non-closable)
        index = len(self.tabs)
        tab_frame = tk.Frame(self.inner, bd=0, relief='flat', padx=6, pady=4)

        # place tab frames in a grid so we can give each column equal weight;
        # this allows the tabs to expand and collectively fill the full width.
        tab_frame.grid(row=0, column=index, sticky='nsew')
        self.inner.grid_columnconfigure(index, weight=1)

        lbl = tk.Label(tab_frame, text=title, padx=4)
        # make the label expand to fill its tab frame so the tab looks like a
        # stretchable button
        lbl.pack(fill='both', expand=True)

        # clicking the tab
        tab_frame.bind('<Button-1>', lambda e, tid=tab_id: self.activate_tab(tid))
        lbl.bind('<Button-1>', lambda e, tid=tab_id: self.activate_tab(tid))

        # record the tab and refresh the canvas scrollregion
        self.tabs.append((tab_id, tab_frame, title))
        self._on_inner_configure()
        # Do not auto-activate here; caller may choose which tab to activate.

    # def add_tab(self, tab_id, title):
    #     # create a tab widget: small frame with label and close button
    #     tab_frame = tk.Frame(self.inner, bd=0, relief='flat', padx=6, pady=4)
    #     lbl = tk.Label(tab_frame, text=title, padx=4)
    #     lbl.pack(side=LEFT)

    #     # clicking the tab
    #     tab_frame.bind('<Button-1>', lambda e, tid=tab_id: self.activate_tab(tid))
    #     lbl.bind('<Button-1>', lambda e, tid=tab_id: self.activate_tab(tid))

    #     # layout
    #     tab_frame.pack(side=LEFT, padx=(0,4))
    #     self.tabs.append((tab_id, tab_frame, title))
    #     self._on_inner_configure()
    #     self.activate_tab(tab_id)

    # def add_new_tab(self):
    #     # convenience: create a new tab with incremental id
    #     n = len(self.tabs) + 1
    #     tab_id = f"tab-{n}"
    #     self.master.create_tab_content(tab_id, f"Tab {n}")
    #     self.add_tab(tab_id, f"Tab {n}")

    def activate_tab(self, tab_id):
        # visually mark the active tab and call callback to show content
        for tid, widget, _ in self.tabs:
            if tid == tab_id:
                widget.configure(bg='white')
                for child in widget.winfo_children():
                    child.configure(bg='white')
                self.active_tab = tab_id
            else:
                widget.configure(bg=self.master.cget('bg'))
                for child in widget.winfo_children():
                    child.configure(bg=self.master.cget('bg'))
        # ensure the active tab is visible: scroll if needed
        self._ensure_visible(tab_id)
        # callback to show content
        self.switch_callback(tab_id)

    def _ensure_visible(self, tab_id):
        # ensure tab widget sits within visible canvas area; adjust canvas.xview if needed.
        for tid, widget, _ in self.tabs:
            if tid == tab_id:
                x1 = widget.winfo_rootx()
                x2 = x1 + widget.winfo_width()
                canvas_x1 = self.canvas.winfo_rootx()
                canvas_x2 = canvas_x1 + self.canvas.winfo_width()
                # scroll left
                if x1 < canvas_x1:
                    delta = canvas_x1 - x1 + 10
                    self.canvas.xview_scroll(int(-1 * (delta / 10)), 'units')
                # scroll right
                elif x2 > canvas_x2:
                    delta = x2 - canvas_x2 + 10
                    self.canvas.xview_scroll(int(delta / 10), 'units')
                break

    def scroll_left(self):
        self.canvas.xview_scroll(-3, 'units')

    def scroll_right(self):
        self.canvas.xview_scroll(3, 'units')
