'''Simple demo of tableview widget: NOT for production use'''

import ttkbootstrap as ttk
from ttkbootstrap.widgets.tableview import Tableview
from ttkbootstrap.constants import *

app = ttk.Window()
colors = app.style.colors

coldata = [
    {"text": "LicenseNumber", "stretch": False},
    "CompanyName",
    {"text": "UserCount", "stretch": False},
]

rowdata = [
    ('A123', 'IzzyCo', 12),
    ('A136', 'Kimdee Inc.', 45),
    ('A158', 'Farmadding Co.', 36)
]

dt = Tableview(
  master=app,
  coldata=coldata,
  rowdata=rowdata,
  paginated=True,
  searchable=True,
  bootstyle="primary",
  stripecolor=(colors.dark(0.05), colors.light(0.05)),
)