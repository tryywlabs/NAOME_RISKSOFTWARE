import tkinter as tk
from tkinter import messagebox
import matplotlib.pyplot as plt
import numpy as np

# Global variable to store TNT equivalent mass (W)
tnt_mass_global = None

def calculate_tnt_equivalency():
    global tnt_mass_global
    try:
        # Get user input values for TNT equivalency
        eta = float(eta_entry.get())
        mass = float(mass_entry.get())
        heat_combustion = float(heat_combustion_entry.get())
        tnt_heat_combustion = float(tnt_heat_combustion_entry.get())

        # Calculate W using the formula
        tnt_mass_global = (eta * mass * heat_combustion) / tnt_heat_combustion

        # Display the TNT equivalent mass result
        tnt_result_label.config(text=f"TNT Equivalent Mass (W): {tnt_mass_global:.2f} kg")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numerical values.")

def update_overpressure(*args):
    global tnt_mass_global
    try:
        # Ensure TNT mass is calculated first
        if tnt_mass_global is None:
            overpressure_label.config(text="Please calculate TNT equivalent mass first.")
            return

        # Get the slider value for distance
        distance = distance_slider.get()

        # Calculate Z_e and P_s
        Z_e = distance / (tnt_mass_global ** (1/3))
        P_s = (573 * Z_e ** -1.685) / 100

        # Update the overpressure results
        ze_result_label.config(text=f"Scaled Distance (Z_e): {Z_e:.2f}")
        ps_result_label.config(text=f"Overpressure (P_s): {P_s:.2f} bar")
    except ValueError:
        overpressure_label.config(text="Error in calculation. Please check inputs.")

def plot_overpressure_graph():
    global tnt_mass_global
    try:
        # Ensure TNT mass is calculated first
        if tnt_mass_global is None:
            messagebox.showerror("Calculation Error", "Please calculate TNT equivalent mass first.")
            return

        # Generate data points
        distances = np.linspace(1, 500, 100)  # Distance range from 1m to 500m
        Z_e_values = distances / (tnt_mass_global ** (1/3))
        P_s_values = (573 * Z_e_values ** -1.685) / 100

        # Plot the graph
        plt.figure(figsize=(8, 5))
        plt.plot(distances, P_s_values, label="Overpressure (P_s)", color="blue")
        plt.title("Overpressure vs Distance")
        plt.xlabel("Distance from Explosion (R_d) [m]")
        plt.ylabel("Overpressure (P_s) [bar]")
        plt.grid(True)
        plt.legend()
        plt.show()
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while plotting: {str(e)}")

# Create the Tkinter window
root = tk.Tk()
root.title("Explosion Impact Calculator")

# TNT Equivalency Inputs
tk.Label(root, text="TNT Equivalency Calculation", font=("Arial", 14)).pack(pady=10)
tk.Label(root, text="Empirical Explosion Efficiency (η):").pack(pady=5)
eta_entry = tk.Entry(root)
eta_entry.pack(pady=5)

tk.Label(root, text="Mass of Hydrocarbon (M) [kg]:").pack(pady=5)
mass_entry = tk.Entry(root)
mass_entry.pack(pady=5)

tk.Label(root, text="Heat of Combustion of Flammable Gas (E_c) [kJ/kg]:").pack(pady=5)
heat_combustion_entry = tk.Entry(root)
heat_combustion_entry.pack(pady=5)

tk.Label(root, text="Heat of Combustion of TNT (E_TNT) [kJ/kg]:").pack(pady=5)
tnt_heat_combustion_entry = tk.Entry(root)
tnt_heat_combustion_entry.pack(pady=5)

# TNT Equivalency Calculate Button
calculate_button = tk.Button(root, text="Calculate TNT Equivalency", command=calculate_tnt_equivalency)
calculate_button.pack(pady=10)

# TNT Equivalency Result
tnt_result_label = tk.Label(root, text="TNT Equivalent Mass (W): ", fg="blue")
tnt_result_label.pack(pady=10)

# Overpressure Inputs with Slider
tk.Label(root, text="Overpressure Calculation", font=("Arial", 14)).pack(pady=10)
tk.Label(root, text="Distance from Explosion (R_d) [m]:").pack(pady=5)

# Slider for distance
distance_slider = tk.Scale(root, from_=1, to=500, orient="horizontal", length=300, label="Select Distance (m)")
distance_slider.pack(pady=5)

# Bind slider to update_overpressure function
distance_slider.config(command=update_overpressure)

# Overpressure Results
ze_result_label = tk.Label(root, text="Scaled Distance (Z_e): ", fg="blue")
ze_result_label.pack(pady=5)
ps_result_label = tk.Label(root, text="Overpressure (P_s): ", fg="blue")
ps_result_label.pack(pady=5)

# Plot Graph Button
plot_graph_button = tk.Button(root, text="Plot Overpressure Graph", command=plot_overpressure_graph)
plot_graph_button.pack(pady=10)

# Run the application
root.mainloop()
