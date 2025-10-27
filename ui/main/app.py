'''
FILE: ui/main/app.py
DESCRIPTION: Main loop of the interface application.
AUTHOR: Yongwoo Hur
'''

import os
import sys
from tkinter import Tk
import ttkbootstrap as tkbs

# import ui.components.loginpage as loginpage


def main():
  # Allow selecting a ttkbootstrap theme via the TTK_THEME environment variable.
  # If not set, default to a light, neutral theme.
  theme = os.getenv("TTK_THEME", "litera")
  root = tkbs.Window(themename=theme)
  root.title("Maritime Risk Assessment")
  root.geometry("1024x768")
  # loginpage.login_window()
  root.mainloop()


if __name__ == "__main__":
  main()