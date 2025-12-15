import tkinter as tk
from tkinter import ttk
import math

def calculate_sigma_y(x, stability):
    """ Calculate sigma_y based on stability class and x """
    if stability == 'A':
        return 0.22 * x * (1 + 0.0001 * x) ** -0.5
    elif stability == 'B':
        return 0.16 * x * (1 + 0.0001 * x) ** -0.5
    elif stability == 'C':
        return 0.11 * x * (1 + 0.0001 * x) ** -0.5
    elif stability == 'D':
        return 0.08 * x * (1 + 0.0001 * x) ** -0.5
    elif stability == 'E':
        return 0.06 * x * (1 + 0.0001 * x) ** -0.5
    elif stability == 'F':
        return 0.04 * x * (1 + 0.0001 * x) ** -0.5

def calculate_sigma_z(x, stability):
    """ Calculate sigma_z based on stability class and x """
    if stability == 'A':
        return 0.20 * x
    elif stability == 'B':
        return 0.12 * x
    elif stability == 'C':
        return 0.08 * x * (1 + 0.0002 * x) ** -0.5
    elif stability == 'D':
        return 0.06 * x * (1 + 0.0015 * x) ** -0.5
    elif stability == 'E':
        return 0.03 * x * (1 + 0.0003 * x) ** -1
    elif stability == 'F':
        return 0.016 * x * (1 + 0.0003 * x) ** -1

def calculate_concentration():
    try:
        # Retrieve inputs
        Q = float(entry_Q.get())  # Keep Q in kg/s
        u = float(entry_u.get())
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        H = float(entry_H.get())
        stability = combo_stability.get()

        # Calculate sigma_y and sigma_z
        sigma_y = calculate_sigma_y(x, stability)
        sigma_z = calculate_sigma_z(x, stability)

        # Calculate concentration using Gaussian Plume Model
        term_y = math.exp(-(y ** 2) / (2 * sigma_y ** 2))
        term_z1 = math.exp(-((H - z) ** 2) / (2 * sigma_z ** 2))
        term_z2 = math.exp(-((H + z) ** 2) / (2 * sigma_z ** 2))
        C = (Q / (2 * math.pi * u * sigma_y * sigma_z)) * term_y * (term_z1 + term_z2)

        # Display result
        label_result.config(text=f"농도 C: {C:.6f} kg/m^3")
    except ValueError:
        label_result.config(text="올바른 숫자를 입력하세요.")

# GUI Creation
root = tk.Tk()
root.title("Gaussian Plume Model Calculator")

# Labels and Entry fields
ttk.Label(root, text="오염 물질 배출량 Q (kg/s):").grid(row=0, column=0)
entry_Q = ttk.Entry(root)
entry_Q.grid(row=0, column=1)

ttk.Label(root, text="바람 속도 u (m/s):").grid(row=1, column=0)
entry_u = ttk.Entry(root)
entry_u.grid(row=1, column=1)

ttk.Label(root, text="x 거리 (m):").grid(row=2, column=0)
entry_x = ttk.Entry(root)
entry_x.grid(row=2, column=1)

ttk.Label(root, text="y 거리 (m):").grid(row=3, column=0)
entry_y = ttk.Entry(root)
entry_y.grid(row=3, column=1)

ttk.Label(root, text="z 높이 (m):").grid(row=4, column=0)
entry_z = ttk.Entry(root)
entry_z.grid(row=4, column=1)

ttk.Label(root, text="배출 높이 H (m):").grid(row=5, column=0)
entry_H = ttk.Entry(root)
entry_H.grid(row=5, column=1)

ttk.Label(root, text="대기 안정도 (Stability Class):").grid(row=6, column=0)
combo_stability = ttk.Combobox(root, values=['A', 'B', 'C', 'D', 'E', 'F'])
combo_stability.grid(row=6, column=1)
combo_stability.set('A')

# Calculate Button
btn_calculate = ttk.Button(root, text="농도 계산", command=calculate_concentration)
btn_calculate.grid(row=7, column=0, columnspan=2)

# Result Label
label_result = ttk.Label(root, text="")
label_result.grid(row=8, column=0, columnspan=2)

# Run the GUI
root.mainloop()
