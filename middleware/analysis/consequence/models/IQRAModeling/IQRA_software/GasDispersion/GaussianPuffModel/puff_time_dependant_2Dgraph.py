import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

# -----------------------------
# Pasquill–Gifford 계수
# -----------------------------
PG_params = {
    'A': {'a_xy': 0.18, 'b_xy': 0.92, 'a_z': 0.60, 'b_z': 0.75},
    'B': {'a_xy': 0.14, 'b_xy': 0.92, 'a_z': 0.53, 'b_z': 0.73},
    'C': {'a_xy': 0.10, 'b_xy': 0.92, 'a_z': 0.34, 'b_z': 0.71},
    'D': {'a_xy': 0.06, 'b_xy': 0.92, 'a_z': 0.15, 'b_z': 0.70},
    'E': {'a_xy': 0.04, 'b_xy': 0.92, 'a_z': 0.10, 'b_z': 0.65},
    'F': {'a_xy': 0.02, 'b_xy': 0.89, 'a_z': 0.05, 'b_z': 0.61},
}

# -----------------------------
# σx, σy, σz 계산
# -----------------------------
def sigma_x(u, t, params): 
    return params['a_xy'] * (u * t)**params['b_xy']

def sigma_y(u, t, params): 
    return params['a_xy'] * (u * t)**params['b_xy']

def sigma_z(u, t, params): 
    return params['a_z'] * (u * t)**params['b_z']

# -----------------------------
# Puff 농도 계산
# -----------------------------
def puff_concentration(M, u, H, stability, x, y, z, t):
    if t <= 0:
        return 0.0, 0.0, 0.0, 0.0
    params = PG_params[stability]
    sig_x = sigma_x(u, t, params)
    sig_y = sigma_y(u, t, params)
    sig_z = sigma_z(u, t, params)
    term_exp = np.exp(-((x - u*t)**2)/(2*sig_x**2) - (y**2)/(2*sig_y**2))
    term_z = np.exp(-(z - H)**2/(2*sig_z**2)) + np.exp(-(z + H)**2/(2*sig_z**2))
    C = (M / ((2*np.pi)**1.5 * sig_x * sig_y * sig_z)) * term_exp * term_z
    return C, sig_x, sig_y, sig_z

# -----------------------------
# 계산 및 표 출력
# -----------------------------
def calculate_concentration():
    try:
        M = float(entry_M.get())
        H = float(entry_H.get())
        u = float(entry_u.get())
        t = float(entry_t.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        stability = combo_stab.get().strip().upper()

        if stability not in PG_params:
            messagebox.showerror("Error", "Stability must be one of A–F")
            return

        x_values_str = entry_x.get().split(',')
        x_values = [float(x.strip()) for x in x_values_str if x.strip()]

        for row in tree.get_children():
            tree.delete(row)

        for x in x_values:
            C, sig_x, sig_y, sig_z = puff_concentration(M, u, H, stability, x, y, z, t)
            tree.insert("", "end", values=(f"{x:.1f}", f"{sig_x:.2f}", f"{sig_y:.2f}", f"{sig_z:.2f}", f"{C:.6e}"))

        draw_contour(M, H, u, stability, t)

    except ValueError:
        messagebox.showerror("Invalid Input", "모든 값을 숫자로 입력하세요!")

# -----------------------------
# x-z 평면 컨투어 그리기
# -----------------------------
def draw_contour(M, H, u, stability, t):
    fig, ax = plt.subplots(figsize=(8, 5))
    x = np.linspace(0, 500, 200)
    z = np.linspace(0, 100, 200)
    X, Z = np.meshgrid(x, z)
    Y = np.zeros_like(X)

    C = np.zeros_like(X)
    for i in range(X.shape[0]):
        for j in range(X.shape[1]):
            c_val, *_ = puff_concentration(M, u, H, stability, X[i, j], Y[i, j], Z[i, j], t)
            C[i, j] = c_val

    contour = ax.contourf(X, Z, C, levels=np.linspace(0, 1.0, 40), cmap='plasma')
    c1 = ax.contour(X, Z, C, levels=[1.0], colors='black', linewidths=2)
    ax.clabel(c1, fmt={1.0: "C=1"}, inline=True, fontsize=10, colors='black')

    ax.set_title(f"Gaussian Plume Contour (C ≤ 1.0 kg/m³)\\nStability Class {stability}", fontsize=12)
    ax.set_xlabel("Downwind Distance x (m)")
    ax.set_ylabel("Height z (m)")

    cbar = fig.colorbar(contour, ax=ax)
    cbar.set_label("Concentration (kg/m³)")

    win = tk.Toplevel(root)
    win.title("x-z Concentration Contour")
    canvas = FigureCanvasTkAgg(fig, master=win)
    canvas.draw()
    canvas.get_tk_widget().pack()

# -----------------------------
# Tkinter GUI 구성
# -----------------------------
root = tk.Tk()
root.title("Gaussian Puff Model (단위: kg/m³)")

frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(fill="x")

tk.Label(frame_input, text="M (kg):").grid(row=0, column=0, sticky="e")
entry_M = tk.Entry(frame_input, width=10)
entry_M.grid(row=0, column=1)

tk.Label(frame_input, text="H (m):").grid(row=0, column=2, sticky="e")
entry_H = tk.Entry(frame_input, width=10)
entry_H.grid(row=0, column=3)

tk.Label(frame_input, text="u (m/s):").grid(row=1, column=0, sticky="e")
entry_u = tk.Entry(frame_input, width=10)
entry_u.grid(row=1, column=1)

tk.Label(frame_input, text="t (s):").grid(row=1, column=2, sticky="e")
entry_t = tk.Entry(frame_input, width=10)
entry_t.grid(row=1, column=3)

tk.Label(frame_input, text="x (m, 쉼표로):").grid(row=2, column=0, sticky="e")
entry_x = tk.Entry(frame_input, width=25)
entry_x.grid(row=2, column=1, columnspan=3, sticky="w")

tk.Label(frame_input, text="y (m):").grid(row=3, column=0, sticky="e")
entry_y = tk.Entry(frame_input, width=10)
entry_y.grid(row=3, column=1)

tk.Label(frame_input, text="z (m):").grid(row=3, column=2, sticky="e")
entry_z = tk.Entry(frame_input, width=10)
entry_z.grid(row=3, column=3)

tk.Label(frame_input, text="Stability (A–F):").grid(row=4, column=0, sticky="e")
combo_stab = ttk.Combobox(frame_input, values=list(PG_params.keys()), width=5)
combo_stab.grid(row=4, column=1)
combo_stab.set("D")

btn_calc = tk.Button(root, text="계산 및 컨투어", command=calculate_concentration,
                     bg="#2E8B57", fg="white", padx=10, pady=5)
btn_calc.pack(pady=10)

frame_table = tk.Frame(root, padx=10, pady=10)
frame_table.pack()

columns = ("x (m)", "σx", "σy", "σz", "C (kg/m³)")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=8)
for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=120)
tree.pack()

root.mainloop()
