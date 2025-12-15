import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np

# --------------------------------------------
# 1️⃣ Pasquill–Gifford 계수 (σx, σy, σz 모두 (u·t) 기반)
# --------------------------------------------
PG_params = {
    'A': {'a_xy': 0.18, 'b_xy': 0.92, 'a_z': 0.60, 'b_z': 0.75},
    'B': {'a_xy': 0.14, 'b_xy': 0.92, 'a_z': 0.53, 'b_z': 0.73},
    'C': {'a_xy': 0.10, 'b_xy': 0.92, 'a_z': 0.34, 'b_z': 0.71},
    'D': {'a_xy': 0.06, 'b_xy': 0.92, 'a_z': 0.15, 'b_z': 0.70},
    'E': {'a_xy': 0.04, 'b_xy': 0.92, 'a_z': 0.10, 'b_z': 0.65},
    'F': {'a_xy': 0.02, 'b_xy': 0.89, 'a_z': 0.05, 'b_z': 0.61},
}

# --------------------------------------------
# 2️⃣ σx, σy, σz 계산
# --------------------------------------------
def sigma_x(u, t, params):
    return params['a_xy'] * (u * t)**params['b_xy']

def sigma_y(u, t, params):
    return params['a_xy'] * (u * t)**params['b_xy']

def sigma_z(u, t, params):
    return params['a_z'] * (u * t)**params['b_z']

# --------------------------------------------
# 3️⃣ Puff 농도 계산 (공식 반영)
# --------------------------------------------
def puff_concentration(M, u, H, stability, x, y, z, t):
    if t <= 0:
        return 0.0, 0.0, 0.0, 0.0

    params = PG_params[stability]
    sig_x = sigma_x(u, t, params)
    sig_y = sigma_y(u, t, params)
    sig_z = sigma_z(u, t, params)

    # Gaussian Puff 공식
    term_exp = np.exp(-((x - u*t)**2) / (2 * sig_x**2) - (y**2) / (2 * sig_y**2))
    term_z = np.exp(-(z - H)**2 / (2 * sig_z**2)) + np.exp(-(z + H)**2 / (2 * sig_z**2))
    C = (M / ((2 * np.pi)**1.5 * sig_x * sig_y * sig_z)) * term_exp * term_z  # kg/m³

    return C, sig_x, sig_y, sig_z

# --------------------------------------------
# 4️⃣ Tkinter 계산 함수
# --------------------------------------------
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

        # 쉼표로 구분된 x 값들 입력 → 리스트로 변환
        x_values_str = entry_x.get().split(',')
        x_values = []
        for x_str in x_values_str:
            try:
                x_values.append(float(x_str.strip()))
            except ValueError:
                continue  # 숫자가 아닌 값은 무시

        if not x_values:
            messagebox.showerror("Invalid Input", "x 값을 쉼표로 구분하여 입력하세요 (예: 10, 20, 50)")
            return

        # 결과 테이블 초기화
        for row in tree.get_children():
            tree.delete(row)

        # 각 x 값에 대해 계산
        for x in x_values:
            C, sig_x, sig_y, sig_z = puff_concentration(M, u, H, stability, x, y, z, t)
            tree.insert("", "end", values=(f"{x:.1f} m", f"{sig_x:.2f}", f"{sig_y:.2f}", f"{sig_z:.2f}", f"{C:.6e}"))

    except ValueError:
        messagebox.showerror("Invalid Input", "모든 값을 숫자로 입력하세요!")

# --------------------------------------------
# 5️⃣ Tkinter GUI 구성
# --------------------------------------------
root = tk.Tk()
root.title("Gaussian Puff Model (단위: kg/m³)")

frame_input = tk.Frame(root, padx=10, pady=10)
frame_input.pack(fill="x")

# 첫 번째 줄
tk.Label(frame_input, text="M (kg):").grid(row=0, column=0, sticky="e")
entry_M = tk.Entry(frame_input, width=10)
entry_M.grid(row=0, column=1, padx=5)

tk.Label(frame_input, text="H (m):").grid(row=0, column=2, sticky="e")
entry_H = tk.Entry(frame_input, width=10)
entry_H.grid(row=0, column=3, padx=5)

# 두 번째 줄
tk.Label(frame_input, text="u (m/s):").grid(row=1, column=0, sticky="e")
entry_u = tk.Entry(frame_input, width=10)
entry_u.grid(row=1, column=1, padx=5)

tk.Label(frame_input, text="t (s):").grid(row=1, column=2, sticky="e")
entry_t = tk.Entry(frame_input, width=10)
entry_t.grid(row=1, column=3, padx=5)

# 세 번째 줄
tk.Label(frame_input, text="x (m, 쉼표로 구분):").grid(row=2, column=0, sticky="e")
entry_x = tk.Entry(frame_input, width=25)
entry_x.grid(row=2, column=1, columnspan=3, padx=5, sticky="w")

# 네 번째 줄
tk.Label(frame_input, text="y (m):").grid(row=3, column=0, sticky="e")
entry_y = tk.Entry(frame_input, width=10)
entry_y.grid(row=3, column=1, padx=5)

tk.Label(frame_input, text="z (m):").grid(row=3, column=2, sticky="e")
entry_z = tk.Entry(frame_input, width=10)
entry_z.grid(row=3, column=3, padx=5)

# 다섯 번째 줄
tk.Label(frame_input, text="Stability (A–F):").grid(row=4, column=0, sticky="e")
combo_stab = ttk.Combobox(frame_input, values=list(PG_params.keys()), width=8)
combo_stab.grid(row=4, column=1, padx=5)
combo_stab.set("D")

# 버튼
btn_calc = tk.Button(root, text="계산하기", command=calculate_concentration,
                     bg="#2E8B57", fg="white", padx=10, pady=5)
btn_calc.pack(pady=10)

# 결과 테이블
frame_table = tk.Frame(root, padx=10, pady=10)
frame_table.pack()

columns = ("X (m)", "σx (m)", "σy (m)", "σz (m)", "Concentration (kg/m³)")
tree = ttk.Treeview(frame_table, columns=columns, show="headings", height=8)

for col in columns:
    tree.heading(col, text=col)
    tree.column(col, anchor="center", width=130)

tree.pack()

root.mainloop()
