'''
FILE: roottab.py
DESCRIPTION: Sample code to create a tabbed interface using tkinter's Notebook widget. Direct integration might actually be better.
NOTE: Might use instead of the current TabBar + app.py structure.
'''

import tkinter as tk
from tkinter import ttk
import pathlib
import sys

try:
    from ui.main.main_panels.calculate import CalculateFrame
except ModuleNotFoundError:
    # repo root is two levels up from ui/main/ (i.e. RISKSOFTWARE)
    repo_root = pathlib.Path(__file__).resolve().parents[2]
    sys.path.insert(0, str(repo_root))
    from ui.main.main_panels.calculate import CalculateFrame

# from main_panels.calculate import CalculateFrame

def main():
  root = tk.Tk()
  root.title("Sample tab substitution")
  root.geometry("1082x768")
  root.columnconfigure(0, weight=1)
  root.rowconfigure(0, weight=1)

  style = ttk.Style(root)
  style.configure('TNotebook.Tab', width=root.winfo_screenwidth())

  tabs = ttk.Notebook(root)
  tabs.grid(row=0, column=0, sticky='nsew')

  frame1 = tk.Frame(tabs, width=400, height=200, bg='LightCyan3')
  frame2 = tk.Frame(tabs, width=400, height=200, bg='LightCyan3')
  frame3 = tk.Frame(tabs, width=400, height=200, bg='LightCyan3')
  frame4 = tk.Frame(tabs, width=400, height=200, bg='LightCyan3')
  frame5 = tk.Frame(tabs, width=400, height=200, bg='LightCyan3')
  frame6 = tk.Frame(tabs, width=400, height=200, bg='LightCyan3')
  # Create the CalculateFrame as a child of the Notebook so it becomes a
  # proper tab page. CalculateFrame requires a container argument.
  calculateTab = CalculateFrame(tabs)

  label1 = tk.Label(frame1, text="This is Tab 1")
  label1.pack()
  label2 = tk.Label(frame2, text="This is Tab 2")
  label2.pack()

  button2 = tk.Button(frame2, text="Tab 2 Button")
  button2.pack()

  entry1 = tk.Entry(frame1)
  entry1.pack()

  label3 = tk.Label(frame3, text="This is Tab 3")
  label3.pack()

  # Do not pack the tab pages — the Notebook will manage their geometry when
  # they are added with `tabs.add(...)`.

  tabs.add(calculateTab, text='Calculate')
  tabs.add(frame1, text='Tab 1')
  tabs.add(frame2, text='Tab 2')
  tabs.add(frame3, text='Tab 3')
  tabs.add(frame4, text='Tab 4')
  tabs.add(frame5, text='Tab 5')

  root.mainloop()

if __name__ == "__main__":
  main()