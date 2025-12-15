import tkinter as tk
from tkinter import ttk
from math import pow, pi, exp

def calculate_radiant_heat_flux():
    try:
        # Get user inputs
        Q = float(heat_release_rate_entry.get())  # Total heat release rate (kW)
        D = float(pool_diameter_entry.get())  # Pool diameter (m)
        x = float(distance_entry.get())  # Distance from fire center to target (m)
        f = float(fraction_radiative_entry.get())  # Radiative fraction (dimensionless)
        tau = float(atmospheric_trans_entry.get())  # Atmospheric transmissivity (dimensionless)

        # Perform calculations based on the formula
        # q'' = \u03C4 \u00b7 f \u00b7 Q / (\u03C0 \u00b7 R^2)
        R = (x**2 + (D/2)**2)**0.5  # Effective distance from fire center to target
        q = (tau * f * Q) / (pi * pow(R, 2))  # Radiant heat flux (kW/m^2)

        # Display the result
        result_label.config(text=f"Radiant Heat Flux (q): {q:.2f} kW/m²")
    except ValueError:
        result_label.config(text="Invalid input. Please enter numeric values.")

# Create the main application window
root = tk.Tk()
root.title("Radiant Heat Flux Calculator")

# Input fields
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E))

# Heat release rate
ttk.Label(frame, text="Heat Release Rate (Q) [kW]:").grid(row=0, column=0, sticky=tk.W)
heat_release_rate_entry = ttk.Entry(frame, width=20)
heat_release_rate_entry.grid(row=0, column=1)

# Pool diameter
ttk.Label(frame, text="Pool Diameter (D) [m]:").grid(row=1, column=0, sticky=tk.W)
pool_diameter_entry = ttk.Entry(frame, width=20)
pool_diameter_entry.grid(row=1, column=1)

# Distance from fire center
ttk.Label(frame, text="Distance to Target (x) [m]:").grid(row=2, column=0, sticky=tk.W)
distance_entry = ttk.Entry(frame, width=20)
distance_entry.grid(row=2, column=1)

# Radiative fraction
ttk.Label(frame, text="Radiative Fraction (f):").grid(row=3, column=0, sticky=tk.W)
fraction_radiative_entry = ttk.Entry(frame, width=20)
fraction_radiative_entry.grid(row=3, column=1)

# Atmospheric transmissivity
ttk.Label(frame, text="Atmospheric Transmissivity (\u03C4):").grid(row=4, column=0, sticky=tk.W)
atmospheric_trans_entry = ttk.Entry(frame, width=20)
atmospheric_trans_entry.grid(row=4, column=1)

# Calculate button
calculate_button = ttk.Button(frame, text="Calculate", command=calculate_radiant_heat_flux)
calculate_button.grid(row=5, column=0, columnspan=2)

# Result label
result_label = ttk.Label(frame, text="", foreground="blue")
result_label.grid(row=6, column=0, columnspan=2)

# Start the Tkinter event loop
root.mainloop()
