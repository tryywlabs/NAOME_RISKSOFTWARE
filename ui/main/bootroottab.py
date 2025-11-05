"""
For root tab in ttkbootstrap styled version
NOTE: DEPRECATED; Use main.py for the main program body
"""

import ttkbootstrap as ttkb
from ttkbootstrap.constraints import *
import pathlib
import sys

def main():
  nb = ttkb.Notebook()
  frame = ttkb.Frame(nb)
  nb.add(frame, text='Sample Tab')

if __name__ == "__main__":
  main().mainloop()