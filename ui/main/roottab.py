'''
FILE: roottab.py
DESCRIPTION: Sample code to create a tabbed interface using tkinter's Notebook widget. Direct integration might actually be better.
NOTE: Might use instead of the current TabBar + app.py structure.
'''

import tkinter as tk
from tkinter import ttk

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

  frame1.pack(fill='both', expand=True)
  frame2.pack(fill='both', expand=True)
  frame3.pack(fill='both', expand=True)

  tabs.add(frame1, text='Tab 1')
  tabs.add(frame2, text='Tab 2')
  tabs.add(frame3, text='Tab 3')

  root.mainloop()

if __name__ == "__main__":
  main()