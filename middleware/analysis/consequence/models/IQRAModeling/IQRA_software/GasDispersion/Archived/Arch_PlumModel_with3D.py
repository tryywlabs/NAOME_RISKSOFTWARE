import tkinter as tk
from tkinter import ttk
import math
import matplotlib.pyplot as plt
import numpy as np

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

def calculate_concentration(Q, u, x, y, z, H, stability):
    sigma_y = calculate_sigma_y(x, stability)
    sigma_z = calculate_sigma_z(x, stability)

    term_y = math.exp(-(y ** 2) / (2 * sigma_y ** 2))
    term_z1 = math.exp(-((H - z) ** 2) / (2 * sigma_z ** 2))
    term_z2 = math.exp(-((H + z) ** 2) / (2 * sigma_z ** 2))
    C = (Q / (2 * math.pi * u * sigma_y * sigma_z)) * term_y * (term_z1 + term_z2)
    return C

def display_3d_graph():
    try:
        # Retrieve inputs
        Q = float(entry_Q.get())  # Keep Q in kg/s
        u = float(entry_u.get())
        H = float(entry_H.get())
        stability = combo_stability.get()

        # Generate meshgrid
        x = np.linspace(1, 1000, 50)
        y = np.linspace(-200, 200, 50)
        z = np.linspace(0, 200, 50)
        X, Y, Z = np.meshgrid(x, y, z)

        # Calculate concentrations
        C = np.vectorize(lambda x, y, z: calculate_concentration(Q, u, x, y, z, H, stability))
        concentration = C(X, Y, Z)

        # Normalize concentration for transparency
        normalized_concentration = concentration / np.max(concentration)
        alpha_values = np.clip(normalized_concentration, 0.1, 1.0)

        # Plot 3D graph
        fig = plt.figure()
        ax = fig.add_subplot(111, projection='3d')
        img = ax.scatter(X, Y, Z, c=concentration, cmap='viridis', alpha=alpha_values.flatten())
        fig.colorbar(img, ax=ax, label='Concentration (kg/m^3)')

        ax.set_xlabel('x Distance (m)')
        ax.set_ylabel('y Distance (m)')
        ax.set_zlabel('z Height (m)')
        ax.set_title('Gas Concentration 3D Graph with Transparency')

        plt.show()
    except ValueError:
        label_result.config(text="올바른 숫자를 입력하세요.")

def display_2d_graph():
    try:
        # Retrieve inputs
        Q = float(entry_Q.get())  # Keep Q in kg/s
        u = float(entry_u.get())
        y = 0  # Assume y = 0 for 2D graph
        H = float(entry_H.get())
        stability = combo_stability.get()

        # Generate x and z ranges
        x = np.linspace(1, 1000, 100)
        z = np.linspace(0, 200, 100)
        X, Z = np.meshgrid(x, z)

        # Calculate concentrations
        C = np.vectorize(lambda x, z: calculate_concentration(Q, u, x, y, z, H, stability))
        concentration = C(X, Z)

        # Plot 2D graph
        plt.figure()
        plt.contourf(X, Z, concentration, levels=50, cmap='viridis')
        plt.colorbar(label='Concentration (kg/m^3)')
        plt.xlabel('x Distance (m)')
        plt.ylabel('z Height (m)')
        plt.title('Gas Concentration 2D Graph (x-z plane)')
        plt.show()
    except ValueError:
        label_result.config(text="올바른 숫자를 입력하세요.")

def calculate_concentration_button():
    try:
        # Retrieve inputs
        Q = float(entry_Q.get())  # Keep Q in kg/s
        u = float(entry_u.get())
        x = float(entry_x.get())
        y = float(entry_y.get())
        z = float(entry_z.get())
        H = float(entry_H.get())
        stability = combo_stability.get()

        # Calculate concentration
        C = calculate_concentration(Q, u, x, y, z, H, stability)
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

# Buttons
btn_calculate = ttk.Button(root, text="농도 계산", command=calculate_concentration_button)
btn_calculate.grid(row=7, column=0, columnspan=2)

btn_3d_graph = ttk.Button(root, text="3D 그래프 표시", command=display_3d_graph)
btn_3d_graph.grid(row=8, column=0, columnspan=2)

btn_2d_graph = ttk.Button(root, text="2D 그래프 표시", command=display_2d_graph)
btn_2d_graph.grid(row=9, column=0, columnspan=2)

# Result Label
label_result = ttk.Label(root, text="")
label_result.grid(row=10, column=0, columnspan=2)

# Run the GUI
root.mainloop()
