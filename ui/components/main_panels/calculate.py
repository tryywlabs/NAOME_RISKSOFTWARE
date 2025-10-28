'''
FILE: calculate.py
DESCRIPTION: Labview calculation panel copy for risk factors.
'''

import tkinter as tk
from tkinter import ttk

class CalculateFrame(ttk.Frame):
  def __init__(self, container, *args, **kwargs):
    super().__init__(container, *args, **kwargs)
    label = ttk.Label(self, text="Calculation Panel - Under Construction", font=("Helvetica", 16))
    label.pack(pady=20, padx=20)

#class CalculatePanel(tk.Frame):
  