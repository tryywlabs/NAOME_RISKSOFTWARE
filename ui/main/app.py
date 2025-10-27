'''
FILE: ui/main/app.py
DESCRIPTION: Main loop of the interface application.
AUTHOR: Yongwoo Hur
'''

import os, sys
from pathlib import Path
#add ui directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]) )

import ttkbootstrap as tkbs
import tkinter as tk
from components.main_panels.TabBar import TabBar

# import ui.components.loginpage as loginpage


def main():
  # Allow selecting a ttkbootstrap theme via the TTK_THEME environment variable.
  # If not set, default to a light, neutral theme.
  theme = os.getenv("TTK_THEME", "litera")
  root = tkbs.Window(themename=theme)
  root.title("Maritime Risk Assessment")
  root.geometry("1024x768")
  root.eval('tk::PlaceWindow . center')

  # Create topbar and content area
  topbar = tk.Frame(root, height=36, bg='#e9e9e9')
  # Make the topbar stretch across the full window width and keep its fixed height
  topbar.pack(side='top', fill='x')
  # Prevent the frame from shrinking to fit its children so the height stays as set
  topbar.pack_propagate(False)

  content_area = tk.Frame(root)
  content_area.pack(fill='both', expand=True)

  # store content frames by id
  contents = {}

  def create_tab_content(tab_id, title):
    frame = tk.Frame(content_area, bg='white')
    tk.Label(frame, text=title, font=('Helvetica', 18)).pack(padx=20, pady=20)
    frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    frame.lower()
    contents[tab_id] = frame

  def show_tab(tab_id):
    for tid, frame in contents.items():
      if tid == tab_id:
        frame.lift()
      else:
        frame.lower()

  # Instantiate the TabBar and pack it
  tabbar = TabBar(topbar, switch_callback=show_tab)
  # Pack the TabBar to fill the full width of the topbar. Remove horizontal
  # padding so it aligns with the window edges.
  tabbar.pack(side='top', fill='x', expand=True, padx=0, pady=4)

  # TODO: Rename tabs according to the application
  tabs = [
    ('dashboard', 'Dashboard'),
    ('riskcalc', 'Risk Calculator'),
    ('reports', 'Reports'),
    ('analytics', 'Analytics'),
    ('repercussions', 'Repercussions'),
    ('settings', 'Settings'),
  ]

  for tid, title in tabs:
    create_tab_content(tid, title)
    tabbar.add_tab(tid, title)

  # Activate the first tab by default
  if tabs:
    tabbar.activate_tab(tabs[0][0])

  root.mainloop()


if __name__ == "__main__":
  main()