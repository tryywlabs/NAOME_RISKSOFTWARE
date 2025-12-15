import tkinter as tk
from tkinter import ttk, messagebox
import math

# --------------------------
# Briggs (1973) σy, σz 계수
# --------------------------
coeffs_briggs = {
    "A": (0.18, 0.92, 0.60, 0.75),
    "B": (0.14, 0.92, 0.53, 0.73),
    "C": (0.10, 0.92, 0.34, 0.71),
    "D": (0.06, 0.92, 0.15, 0.70),
    "E": (0.04, 0.92, 0.10, 0.65),
    "F": (0.02, 0.89, 0.05, 0.61),
}


# --------------------------
# Gaussian Puff 농도 계산 함수
# --------------------------
def calculate_concentration():
    try:
        Q = float(entry_Q.get())     # total released mass (kg)
        H = float(entry_H.get())     # effective height (m)
        y = float(entry_y.get())     # crosswind distance (m)
        z = float(entry_z.get())     # vertical position (m)
        stability = combo_stability.get().strip()
        x_values = entry_x.get().split(",")  # 여러 x 값 가능 (쉼표로 구분)

        if stability not in coeffs_briggs:
            messagebox.showerror("Error", "Please select a valid stability class (A–F).")
            return

        # 표 초기화
        for row in tree.get_children():
            tree.delete(row)

        a, b, c, d = coeffs_briggs[stability]

        for x_str in x_values:
            try:
                x = float(x_str.strip())
            except ValueError:
                continue

            sigma_y = a * (x ** b)
            sigma_z = c * (x ** d)

            # Gaussian Puff 농도 계산식
            C = (Q / ((2 * math.pi) ** 1.5 * sigma_y * sigma_y * sigma_z)) * \
                math.exp(-0.5 * (y / sigma_y) ** 2) * \
                (math.exp(-0.5 * ((z - H) / sigma_z) ** 2) + math.exp(-0.5 * ((z + H) / sigma_z) ** 2))

            tree.insert("", "end", values=(f"{x:.1f}", f"{sigma_y:.3f}", f"{sigma_z:.3f}", f"{C:.6e}"))

    except ValueError:
        messagebox.showerror("Error", "Please enter valid numeric input values.")


# --------------------------
# Tkinter GUI 설정
# --------------------------
root = tk.Tk()
root.title("Gaussian Puff Model Concentration Calculator")
root.geometry("600x550")
root.resizable(False, False)

frame = ttk.Frame(root, padding=15)
frame.pack(fill="both", expand=True)

# 제목
ttk.Label(frame, text="Gaussian Puff Model Concentration Calculator", font=("Arial", 11, "bold")).pack(pady=8)

# 입력창 생성 함수
def add_input(label):
    frm = ttk.Frame(frame)
    frm.pack(pady=4)
    ttk.Label(frm, text=f"{label}: ", width=18).pack(side="left")
    ent = ttk.Entry(frm, width=25)
    ent.pack(side="left")
    return ent

# 입력 필드
entry_Q = add_input("G (kg)")
entry_H = add_input("H (m)")
entry_x = add_input("X (m, comma-separated)")
entry_y = add_input("Y (m)")
entry_z = add_input("Z (m)")

# 안정도 등급 선택
frm_stab = ttk.Frame(frame)
frm_stab.pack(pady=5)
ttk.Label(frm_stab, text="Stability class (A–F): ", width=22).pack(side="left")
combo_stability = ttk.Combobox(frm_stab, values=["A", "B", "C", "D", "E", "F"], width=5)
combo_stability.pack(side="left")

# 계산 버튼
ttk.Button(frame, text="Calculate Concentration", command=calculate_concentration).pack(pady=10)

# 결과 테이블 (Treeview)
columns = ("x", "sigma_y", "sigma_z", "concentration")
tree = ttk.Treeview(frame, columns=columns, show="headings", height=10)
tree.heading("x", text="x (m)")
tree.heading("sigma_y", text="σy (m)")
tree.heading("sigma_z", text="σz (m)")
tree.heading("concentration", text="C (kg/m³)")

for col in columns:
    tree.column(col, width=120, anchor="center")

tree.pack(pady=15)

# 실행
root.mainloop()
