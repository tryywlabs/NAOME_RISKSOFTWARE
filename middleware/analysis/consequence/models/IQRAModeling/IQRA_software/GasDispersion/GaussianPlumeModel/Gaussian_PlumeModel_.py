import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# -----------------------------
# Gaussian plume model functions
# -----------------------------
def sigma_yz(x, stability_class):
    """Compute dispersion coefficients σy and σz based on stability class (ALCHe/CCPS, 1996)"""
    if stability_class == 'A':
        sigma_y = 0.22 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.20 * x
    elif stability_class == 'B':
        sigma_y = 0.16 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.12 * x
    elif stability_class == 'C':
        sigma_y = 0.11 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.08 * x * (1 + 0.0002 * x) ** -0.5
    elif stability_class == 'D':
        sigma_y = 0.08 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.06 * x * (1 + 0.0015 * x) ** -0.5
    elif stability_class == 'E':
        sigma_y = 0.06 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.03 * x * (1 + 0.0003 * x) ** -1
    elif stability_class == 'F':
        sigma_y = 0.04 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.016 * x * (1 + 0.0003 * x) ** -1
    else:
        raise ValueError("Invalid stability class")
    return sigma_y, sigma_z


def gaussian_plume(Qevp, u_wind, H_E, x, y, z, stability_class):
    """Calculate Gaussian plume concentration C(x,y,z;H_E)"""
    sigma_y, sigma_z = sigma_yz(x, stability_class)
    term1 = Qevp / (2 * np.pi * u_wind * sigma_y * sigma_z)
    term2 = np.exp(-y**2 / (2 * sigma_y**2))
    term3 = np.exp(-((H_E - z)**2) / (2 * sigma_z**2))
    term4 = np.exp(-((H_E + z)**2) / (2 * sigma_z**2))
    C = term1 * term2 * (term3 + term4)
    return C, sigma_y, sigma_z


# -----------------------------
# Tkinter GUI
# -----------------------------
def calculate_concentration():
    try:
        Qevp = float(entry_Qevp.get())
        u_wind = float(entry_u.get())
        H_E = float(entry_H.get())
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        stability_class = combo_class.get().upper()

        C, sigma_y, sigma_z = gaussian_plume(Qevp, u_wind, H_E, x, y, z, stability_class)

        # 결과 테이블 초기화
        for row in tree.get_children():
            tree.delete(row)

        # 결과 추가
        tree.insert("", "end", values=(
            f"{x:.1f} m",
            f"{sigma_y:.2f}",
            f"{sigma_y:.2f}",  # σx = σy 가정
            f"{sigma_z:.2f}",
            f"{C:.6e}"
        ))

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")


# -----------------------------
# Window layout
# -----------------------------
root = tk.Tk()
root.title("Gaussian Plume Model Calculator")
root.geometry("680x440")
root.resizable(False, False)

frame = ttk.Frame(root, padding=15)
frame.pack(fill="both", expand=True)

# Input labels and entries (t 제거)
labels = ["M (kg)", "u (m/s)", "H (m)", "x (m)", "y (m)", "z (m)", "Stability (A–F)"]
entries = {}

for i, text in enumerate(labels[:-1]):
    ttk.Label(frame, text=text).grid(row=i, column=0, sticky="w", pady=3)
    e = ttk.Entry(frame)
    e.grid(row=i, column=1, pady=3)
    entries[text] = e

# Stability class dropdown
ttk.Label(frame, text=labels[-1]).grid(row=6, column=0, sticky="w", pady=3)
combo_class = ttk.Combobox(frame, values=["A", "B", "C", "D", "E", "F"], width=5)
combo_class.grid(row=6, column=1)
combo_class.current(0)

# Assign entries
entry_Qevp = entries["M (kg)"]
entry_u = entries["u (m/s)"]
entry_H = entries["H (m)"]
entry_x = entries["x (m)"]
entry_y = entries["y (m)"]
entry_z = entries["z (m)"]

# Default values
entry_Qevp.insert(0, "1000")
entry_u.insert(0, "1")
entry_H.insert(0, "0")
entry_x.insert(0, "10")
entry_y.insert(0, "0")
entry_z.insert(0, "0")

# Calculate button
ttk.Button(frame, text="계산하기", command=calculate_concentration).grid(row=7, column=0, columnspan=2, pady=10)

# Result table (Treeview)
columns = ("x", "σx", "σy", "σz", "C")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=3)
for col, w in zip(columns, [80, 80, 80, 80, 180]):
    tree.heading(col, text=col)
    tree.column(col, width=w, anchor="center")
tree.grid(row=8, column=0, columnspan=2, pady=10)

root.mainloop()
