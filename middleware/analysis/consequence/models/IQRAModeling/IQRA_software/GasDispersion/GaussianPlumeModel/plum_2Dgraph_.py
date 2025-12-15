import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# Gaussian plume model functions
# -----------------------------
def sigma_yz(x, stability_class):
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
    sigma_y, sigma_z = sigma_yz(x, stability_class)
    term1 = Qevp / (2 * np.pi * u_wind * sigma_y * sigma_z)
    term2 = np.exp(-y**2 / (2 * sigma_y**2))
    term3 = np.exp(-((H_E - z)**2) / (2 * sigma_z**2))
    term4 = np.exp(-((H_E + z)**2) / (2 * sigma_z**2))
    C = term1 * term2 * (term3 + term4)
    return C


# -----------------------------
# Contour Plot Function
# -----------------------------
def plot_contour(Qevp, u_wind, H_E, stability_class, x_min, x_max, z_min, z_max, C_limit):
    x = np.linspace(x_min, x_max, 200)
    z = np.linspace(z_min, z_max, 150)
    X, Z = np.meshgrid(x, z)
    C = np.zeros_like(X)

    for i in range(len(x)):
        for j in range(len(z)):
            C[j, i] = gaussian_plume(Qevp, u_wind, H_E, x[i], 0, z[j], stability_class)

    # 클리핑 (C_limit 이하만 시각화)
    C_clipped = np.clip(C, 0, C_limit)
    levels = np.linspace(0, C_limit, 21)

    plt.figure(figsize=(8, 5))
    contour = plt.contourf(X, Z, C_clipped, levels=levels, cmap="plasma", extend="both")

    # 사용자 입력 경계선 표시
    line = plt.contour(X, Z, C, levels=[C_limit], colors="black", linewidths=1.5)
    plt.clabel(line, fmt=f"C={C_limit:g}", inline=True, fontsize=9)

    cbar = plt.colorbar(contour)
    cbar.set_label("Concentration (kg/m³)")
    plt.title(f"Gaussian Plume Contour (C ≤ {C_limit} kg/m³)\nStability Class {stability_class}")
    plt.xlabel("Downwind Distance x (m)")
    plt.ylabel("Height z (m)")
    plt.tight_layout()
    plt.show()


# -----------------------------
# Tkinter GUI
# -----------------------------
def calculate_and_plot():
    try:
        Qevp = float(entry_Qevp.get())
        u_wind = float(entry_u.get())
        H_E = float(entry_H.get())
        stability_class = combo_class.get().upper()

        x_min = float(entry_xmin.get())
        x_max = float(entry_xmax.get())
        z_min = float(entry_zmin.get())
        z_max = float(entry_zmax.get())
        C_limit = float(entry_C_limit.get())

        # 1️⃣ 그래프 표시
        plot_contour(Qevp, u_wind, H_E, stability_class, x_min, x_max, z_min, z_max, C_limit)

        # 2️⃣ 중심선(y=0, z=H_E) 농도 테이블 업데이트
        update_table(Qevp, u_wind, H_E, stability_class, x_min, x_max)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")


def update_table(Qevp, u_wind, H_E, stability_class, x_min, x_max):
    # 테이블 초기화
    for i in tree.get_children():
        tree.delete(i)

    # 일정 간격으로 x 좌표 선택 (예: 0, 50, 100, …)
    xs = np.arange(x_min, x_max + 1, (x_max - x_min) / 10)
    for x in xs:
        if x <= 0:
            continue
        C_val = gaussian_plume(Qevp, u_wind, H_E, x, 0, H_E, stability_class)
        tree.insert("", "end", values=(f"{x:.1f}", f"{C_val:.3e}"))


# -----------------------------
# GUI Layout
# -----------------------------
root = tk.Tk()
root.title("Gaussian Plume 2D Contour (with Concentration Table)")
root.geometry("500x600")
root.resizable(False, False)

frame = ttk.Frame(root, padding=15)
frame.pack(fill="both", expand=True)

# 입력 영역
ttk.Label(frame, text="Qevp (kg/s)").grid(row=0, column=0, sticky="w", pady=3)
entry_Qevp = ttk.Entry(frame); entry_Qevp.grid(row=0, column=1); entry_Qevp.insert(0, "1")

ttk.Label(frame, text="u (m/s)").grid(row=1, column=0, sticky="w", pady=3)
entry_u = ttk.Entry(frame); entry_u.grid(row=1, column=1); entry_u.insert(0, "3")

ttk.Label(frame, text="H (m)").grid(row=2, column=0, sticky="w", pady=3)
entry_H = ttk.Entry(frame); entry_H.grid(row=2, column=1); entry_H.insert(0, "20")

ttk.Label(frame, text="Stability (A–F)").grid(row=3, column=0, sticky="w", pady=3)
combo_class = ttk.Combobox(frame, values=["A", "B", "C", "D", "E", "F"], width=5)
combo_class.grid(row=3, column=1); combo_class.current(3)

# 범위 입력
ttk.Label(frame, text="x range (m)").grid(row=4, column=0, sticky="w", pady=3)
entry_xmin = ttk.Entry(frame, width=8); entry_xmin.grid(row=4, column=1, sticky="w"); entry_xmin.insert(0, "0")
entry_xmax = ttk.Entry(frame, width=8); entry_xmax.grid(row=4, column=1, sticky="e"); entry_xmax.insert(0, "500")

ttk.Label(frame, text="z range (m)").grid(row=5, column=0, sticky="w", pady=3)
entry_zmin = ttk.Entry(frame, width=8); entry_zmin.grid(row=5, column=1, sticky="w"); entry_zmin.insert(0, "0")
entry_zmax = ttk.Entry(frame, width=8); entry_zmax.grid(row=5, column=1, sticky="e"); entry_zmax.insert(0, "100")

# 농도 경계값
ttk.Label(frame, text="C-limit (kg/m³)").grid(row=6, column=0, sticky="w", pady=3)
entry_C_limit = ttk.Entry(frame); entry_C_limit.grid(row=6, column=1); entry_C_limit.insert(0, "1.0")

# 실행 버튼
ttk.Button(frame, text="2D 컨투어 + 테이블 보기", command=calculate_and_plot).grid(row=7, column=0, columnspan=2, pady=10)

# -----------------------------
# 결과 테이블
# -----------------------------
ttk.Label(frame, text="Centerline Concentration (y=0, z=H)").grid(row=8, column=0, columnspan=2, pady=(10, 2))
tree = ttk.Treeview(frame, columns=("x", "C"), show="headings", height=8)
tree.heading("x", text="x (m)")
tree.heading("C", text="C (kg/m³)")
tree.column("x", width=100, anchor="center")
tree.column("C", width=140, anchor="center")
tree.grid(row=9, column=0, columnspan=2, pady=5)

root.mainloop()
