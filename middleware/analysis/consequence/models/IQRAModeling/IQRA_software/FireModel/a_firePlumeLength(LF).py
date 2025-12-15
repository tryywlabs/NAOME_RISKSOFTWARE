import tkinter as tk
from tkinter import messagebox
import math

def calculate_plume_length():
    try:
        # Input values
        gb = float(entry_gb.get())  # Liquid mass burning flux (kg/m^2s)
        diameter = float(entry_diameter.get())  # Diameter of fire base (m)
        u_wind = float(entry_u_wind.get())  # Mean wind speed (m/s)
        rho_air = float(entry_rho_air.get())  # Air density (kg/m^3)

        # Constants
        g = 9.81  # Gravity (m/s^2)

        # Combustion Froude Number (F)
        F = gb / (rho_air * math.sqrt(g * diameter))

        # Dimensionless wind speed (U*)
        u_star = u_wind / ((gb * g * diameter / rho_air) ** (1/3))

        # Calculate Lf/D based on U*
        if u_star < 1:
            lf_d = 55 * (F ** (2/3))
        else:
            lf_d = 55 * (F ** (2/3)) * (u_star ** -0.21)

        # Calculate Lf (plume length)
        plume_length = lf_d * diameter

        # Display result
        result_label.config(text=f"Calculated Plume Length: {plume_length:.2f} m")
    except ValueError:
        messagebox.showerror("Input Error", "Please enter valid numeric values.")

# Create main window
root = tk.Tk()
root.title("Fire Plume Length Calculator")

# Input fields
frame = tk.Frame(root)
frame.pack(padx=10, pady=10)

tk.Label(frame, text="Liquid Mass Burning Flux (Gₐ in kg/m²s):").grid(row=0, column=0, sticky="e")
entry_gb = tk.Entry(frame)
entry_gb.grid(row=0, column=1, padx=5, pady=5)

tk.Label(frame, text="Fire Base Diameter (D in m):").grid(row=1, column=0, sticky="e")
entry_diameter = tk.Entry(frame)
entry_diameter.grid(row=1, column=1, padx=5, pady=5)

tk.Label(frame, text="Mean Wind Speed (Uₙₓ in m/s):").grid(row=2, column=0, sticky="e")
entry_u_wind = tk.Entry(frame)
entry_u_wind.grid(row=2, column=1, padx=5, pady=5)

tk.Label(frame, text="Air Density (ρₐₙ in kg/m³):").grid(row=3, column=0, sticky="e")
entry_rho_air = tk.Entry(frame)
entry_rho_air.grid(row=3, column=1, padx=5, pady=5)

# Calculate button
calculate_button = tk.Button(root, text="Calculate", command=calculate_plume_length)
calculate_button.pack(pady=10)

# Result label
result_label = tk.Label(root, text="", font=("Helvetica", 12))
result_label.pack(pady=10)

# Run the application
root.mainloop()
