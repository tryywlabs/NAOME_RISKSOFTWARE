'''
FILE: loginpage.py
DESCRIPTION: Login page for the risk assessment software.
FUNCTIONS: login_window, user_entry, login_verify
'''


from tkinter import *
import ttkbootstrap as tkbs

def login_window():
  login = tkbs.Window(themename="yeti")

  login.title("Risk Software Login")
  login.geometry("400x300")
  login.resizable(False, False)
  login.eval('tk::PlaceWindow . center')

  #Layout Frame
  pane = Frame(login)
  pane.pack(pady=20)

  # Page Components
  username_entry = tkbs.Entry(pane, width=30)
  pw_entry = tkbs.Entry(pane, width=30)
  login_button = tkbs.Button(pane, text="Login", bootstyle="secondary", command=login_attempt)

  # Placeholder helper: sets placeholder text that clears on focus and restores on focus-out if empty.
  def add_placeholder(entry, placeholder, is_password=False):
    # initialize with placeholder
    entry.insert(0, placeholder)
    entry._placeholder = placeholder
    entry._is_placeholder = True

    # If it's a password field, don't mask placeholder
    if is_password:
      try:
        entry.configure(show='')
      except Exception:
        pass

    def on_focus_in(event):
      if getattr(entry, '_is_placeholder', False):
        entry.delete(0, 'end')
        entry._is_placeholder = False
        if is_password:
          try:
            entry.configure(show='*')
          except Exception:
            pass

    def on_focus_out(event):
      if entry.get() == '':
        entry.insert(0, entry._placeholder)
        entry._is_placeholder = True
        if is_password:
          try:
            entry.configure(show='')
          except Exception:
            pass

    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)

  # Attach placeholders
  add_placeholder(username_entry, 'Username', is_password=False)
  add_placeholder(pw_entry, 'Password', is_password=True)
  
  #Pack components
  username_entry.pack(fill = Y,expand = False, pady = 10)
  pw_entry.pack(expand = False, pady = 10)
  login_button.pack(expand = False, pady = 10)
  
  #Loop
  login.mainloop()
    

  if(login_verify(username_entry.get(), pw_entry.get())):
    login.quit()
    return True


# TODO: Implement actual login verification with backend and DB
def login_verify(username, password):
  # Placeholder function for login success handling
  if username == "user" and password == "pass":
    return True
  else:
    return False

def login_attempt():
  pass

if __name__ == "__main__":
  login_window()