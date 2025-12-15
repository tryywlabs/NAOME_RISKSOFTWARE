import tkinter as tk
from tkinter import ttk
import math

def calculate_sigma(stability_class, x):
    # Define coefficients for each stability class
    coefficients = {
        "A": {"sigma_xy": (0.18, 0.92), "sigma_z": (0.60, 0.75)},
        "B": {"sigma_xy": (0.14, 0.92), "sigma_z": (0.53, 0.73)},
        "C": {"sigma_xy": (0.10, 0.92), "sigma_z": (0.34, 0.71)},
        "D": {"sigma_xy": (0.06, 0.92), "sigma_z": (0.15, 0.70)},
        "E": {"sigma_xy": (0.04, 0.92), "sigma_z": (0.10, 0.65)},
        "F": {"sigma_xy": (0.02, 0.89), "sigma_z": (0.05, 0.61)}
    }

    if stability_class not in coefficients:
        raise ValueError("Invalid stability class")

    a_xy, b_xy = coefficients[stability_class]["sigma_xy"]
    a_z, b_z = coefficients[stability_class]["sigma_z"]

    sigma_xy = a_xy * (x ** b_xy)
    sigma_z = a_z * (x ** b_z)

    return sigma_xy, sigma_z

def calculate_gaussian_puff():
    try:
        G_star = float(g_star_entry.get())
        x = float(x_entry.get())
        y = float(y_entry.get())
        z = float(z_entry.get())
        H = float(h_entry.get())
        stability_class = stability_class_var.get()

        # Calculate sigma_x, sigma_y, and sigma_z
        sigma_x, sigma_z = calculate_sigma(stability_class, x)
        sigma_y = sigma_x  # Assume sigma_x = sigma_y as per the table

        term1 = (G_star / ((2 * math.pi) ** (3/2) * sigma_x * sigma_y * sigma_z))
        exp_y = math.exp(-0.5 * (y / sigma_y) ** 2)
        exp_z1 = math.exp(-0.5 * ((z - H) / sigma_z) ** 2)
        exp_z2 = math.exp(-0.5 * ((z + H) / sigma_z) ** 2)

        concentration = term1 * exp_y * (exp_z1 + exp_z2)

        result_label.config(text=f"Concentration (C): {concentration:.6f}")
    except ValueError:
        result_label.config(text="Invalid input. Please enter numerical values.")

# Create the Tkinter window
root = tk.Tk()
root.title("Gaussian Puff Model Calculator")

# Input labels and entries
ttk.Label(root, text="Total mass released (G*):").grid(row=0, column=0, padx=10, pady=5)
g_star_entry = ttk.Entry(root)
g_star_entry.grid(row=0, column=1, padx=10, pady=5)

ttk.Label(root, text="Distance downwind (x):").grid(row=1, column=0, padx=10, pady=5)
x_entry = ttk.Entry(root)
x_entry.grid(row=1, column=1, padx=10, pady=5)

ttk.Label(root, text="Cross-wind direction (y):").grid(row=2, column=0, padx=10, pady=5)
y_entry = ttk.Entry(root)
y_entry.grid(row=2, column=1, padx=10, pady=5)

ttk.Label(root, text="Distance above the ground (z):").grid(row=3, column=0, padx=10, pady=5)
z_entry = ttk.Entry(root)
z_entry.grid(row=3, column=1, padx=10, pady=5)

ttk.Label(root, text="Release height above ground (H):").grid(row=4, column=0, padx=10, pady=5)
h_entry = ttk.Entry(root)
h_entry.grid(row=4, column=1, padx=10, pady=5)

ttk.Label(root, text="Stability class (A-F):").grid(row=5, column=0, padx=10, pady=5)
stability_class_var = tk.StringVar()
stability_class_menu = ttk.Combobox(root, textvariable=stability_class_var)
stability_class_menu['values'] = ("A", "B", "C", "D", "E", "F")
stability_class_menu.grid(row=5, column=1, padx=10, pady=5)
stability_class_menu.current(0)

# Calculate button
calculate_button = ttk.Button(root, text="Calculate", command=calculate_gaussian_puff)
calculate_button.grid(row=6, column=0, columnspan=2, pady=10)

# Result label
result_label = ttk.Label(root, text="", foreground="blue")
result_label.grid(row=7, column=0, columnspan=2, pady=10)

# Run the Tkinter event loop
root.mainloop()
