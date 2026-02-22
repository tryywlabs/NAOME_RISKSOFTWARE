"""
FILE: consequence_input.py
DESCRIPTION:
    DATA INPUT -> Consequence Data
    Collects shared inputs for consequence calculations.
FUNCTIONS:
    create_consequence_input_ui(root): Render the consequence input UI.
"""
import ttkbootstrap as tb
from ttkbootstrap.constants import *
from tkinter import ttk, StringVar, messagebox
import sys
import os

# Add middleware path for consequence state
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../..'))
cons_state_path = os.path.join(project_root, 'middleware/data-input/consequence')
if cons_state_path not in sys.path:
    sys.path.insert(0, cons_state_path)

try:
    from consequence_state import get_params, update_params
except Exception:
    get_params = None
    update_params = None


def create_consequence_input_ui(root):
    """Create the consequence input UI in the provided root window."""
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    title = ttk.Label(frame, text="Consequence Inputs", font=("Helvetica", 12, "bold"))
    title.grid(row=0, column=0, columnspan=4, sticky="w", pady=(0, 10))

    defaults = get_params() if get_params else None

    gas_density_var = StringVar(value=str(getattr(defaults, 'gas_density_kg_m3', 1.2)))
    liquid_density_var = StringVar(value=str(getattr(defaults, 'liquid_density_kg_m3', 800.0)))
    gor_var = StringVar(value=str(getattr(defaults, 'gor', 5.0)))
    wind_speed_var = StringVar(value=str(getattr(defaults, 'wind_speed_m_s', 3.0)))
    height_var = StringVar(value=str(getattr(defaults, 'release_height_m', 10.0)))
    stability_var = StringVar(value=str(getattr(defaults, 'stability_class', 'D')))
    model_var = StringVar(value=str(getattr(defaults, 'model', 'plume')))
    x_var = StringVar(value=str(getattr(defaults, 'x_m', 50.0)))
    y_var = StringVar(value=str(getattr(defaults, 'y_m', 0.0)))
    z_var = StringVar(value=str(getattr(defaults, 'z_m', 0.0)))
    puff_time_var = StringVar(value=str(getattr(defaults, 'puff_time_s', 30.0)))
    duration_var = StringVar(value=str(getattr(defaults, 'release_duration_s', 60.0)))
    critical_conc_var = StringVar(value=str(getattr(defaults, 'critical_concentration_kg_m3', 0.0)))
    explosion_eta_var = StringVar(value=str(getattr(defaults, 'explosion_eta', 0.01)))
    explosion_mass_var = StringVar(value=str(getattr(defaults, 'explosion_mass_kg', 1.0)))
    explosion_heat_combustion_var = StringVar(
        value=str(getattr(defaults, 'explosion_heat_combustion_kj_kg', 0.0))
    )
    explosion_tnt_heat_var = StringVar(
        value=str(getattr(defaults, 'explosion_tnt_heat_combustion_kj_kg', 4680.0))
    )
    explosion_distance_var = StringVar(value=str(getattr(defaults, 'explosion_distance_m', 10.0)))
    explosion_p0_var = StringVar(value=str(getattr(defaults, 'explosion_ambient_pressure_bar', 1.013)))
    pool_fire_q_var = StringVar(value=str(getattr(defaults, 'pool_fire_heat_release_rate_kw', 1000.0)))
    pool_fire_diameter_var = StringVar(value=str(getattr(defaults, 'pool_fire_diameter_m', 5.0)))
    pool_fire_distance_var = StringVar(value=str(getattr(defaults, 'pool_fire_distance_m', 20.0)))
    pool_fire_fraction_var = StringVar(value=str(getattr(defaults, 'pool_fire_radiative_fraction', 0.35)))
    pool_fire_tau_var = StringVar(value=str(getattr(defaults, 'pool_fire_atmospheric_transmissivity', 1.0)))

    def add_label_entry(row, col, text, var, parent=frame):
        ttk.Label(parent, text=text).grid(row=row, column=col, sticky="w", padx=5, pady=4)
        entry = ttk.Entry(parent, textvariable=var, width=14)
        entry.grid(row=row + 1, column=col, sticky="w", padx=5, pady=(0, 6))
        return entry

    add_label_entry(1, 0, "Gas density (kg/m3)", gas_density_var)
    add_label_entry(1, 1, "Liquid density (kg/m3)", liquid_density_var)
    add_label_entry(1, 2, "GOR (-)", gor_var)

    add_label_entry(3, 0, "Wind speed (m/s)", wind_speed_var)
    add_label_entry(3, 1, "Release height (m)", height_var)

    ttk.Label(frame, text="Stability class (A-F)").grid(row=3, column=2, sticky="w", padx=5, pady=4)
    stability_combo = ttk.Combobox(frame, textvariable=stability_var, values=["A", "B", "C", "D", "E", "F"], width=10)
    stability_combo.grid(row=4, column=2, sticky="w", padx=5, pady=(0, 6))

    ttk.Label(frame, text="Dispersion model").grid(row=5, column=0, sticky="w", padx=5, pady=4)
    model_combo = ttk.Combobox(frame, textvariable=model_var, values=["plume", "puff"], width=10)
    model_combo.grid(row=6, column=0, sticky="w", padx=5, pady=(0, 6))

    add_label_entry(5, 1, "Max x (m)", x_var)
    add_label_entry(5, 2, "y (m)", y_var)
    add_label_entry(5, 3, "z (m)", z_var)

    add_label_entry(7, 0, "Puff time (s)", puff_time_var)
    add_label_entry(7, 1, "Release duration (s)", duration_var)
    add_label_entry(7, 2, "Critical conc. (kg/m3)", critical_conc_var)

    explosion_frame = ttk.LabelFrame(frame, text="Explosion Model Inputs (TNT / TNO / BST)", padding=8)
    explosion_frame.grid(row=9, column=0, columnspan=4, sticky="ew", padx=5, pady=(10, 0))

    add_label_entry(0, 0, "Eta (0.005 - 0.2)", explosion_eta_var, parent=explosion_frame)
    add_label_entry(0, 1, "Mass (kg)", explosion_mass_var, parent=explosion_frame)
    add_label_entry(0, 2, "Heat combustion (kJ/kg)", explosion_heat_combustion_var, parent=explosion_frame)
    add_label_entry(0, 3, "TNT heat (kJ/kg)", explosion_tnt_heat_var, parent=explosion_frame)
    add_label_entry(2, 0, "Distance (m)", explosion_distance_var, parent=explosion_frame)
    add_label_entry(2, 1, "Ambient pressure p0 (bar)", explosion_p0_var, parent=explosion_frame)

    pool_fire_frame = ttk.LabelFrame(frame, text="Pool Fire Model Inputs", padding=8)
    pool_fire_frame.grid(row=10, column=0, columnspan=4, sticky="ew", padx=5, pady=(10, 0))
    add_label_entry(0, 0, "Heat release rate Q (kW)", pool_fire_q_var, parent=pool_fire_frame)
    add_label_entry(0, 1, "Pool diameter D (m)", pool_fire_diameter_var, parent=pool_fire_frame)
    add_label_entry(0, 2, "Distance x (m)", pool_fire_distance_var, parent=pool_fire_frame)
    add_label_entry(2, 0, "Radiative fraction f (0-1)", pool_fire_fraction_var, parent=pool_fire_frame)
    add_label_entry(2, 1, "Transmissivity tau (0-1)", pool_fire_tau_var, parent=pool_fire_frame)

    def save_params():
        if update_params is None:
            messagebox.showerror("Error", "Consequence input state is unavailable.")
            return
        try:
            eta_val = float(explosion_eta_var.get())
            if not 0.005 <= eta_val <= 0.2:
                raise ValueError("Eta must be between 0.005 and 0.2.")
            update_params(
                gas_density_kg_m3=float(gas_density_var.get()),
                liquid_density_kg_m3=float(liquid_density_var.get()),
                gor=float(gor_var.get()),
                wind_speed_m_s=float(wind_speed_var.get()),
                release_height_m=float(height_var.get()),
                stability_class=stability_var.get().strip().upper(),
                model=model_var.get().strip().lower(),
                x_m=float(x_var.get()),
                y_m=float(y_var.get()),
                z_m=float(z_var.get()),
                puff_time_s=float(puff_time_var.get()),
                release_duration_s=float(duration_var.get()),
                critical_concentration_kg_m3=float(critical_conc_var.get()),
                explosion_eta=eta_val,
                explosion_mass_kg=float(explosion_mass_var.get()),
                explosion_heat_combustion_kj_kg=float(explosion_heat_combustion_var.get()),
                explosion_tnt_heat_combustion_kj_kg=float(explosion_tnt_heat_var.get()),
                explosion_distance_m=float(explosion_distance_var.get()),
                explosion_ambient_pressure_bar=float(explosion_p0_var.get()),
                pool_fire_heat_release_rate_kw=float(pool_fire_q_var.get()),
                pool_fire_diameter_m=float(pool_fire_diameter_var.get()),
                pool_fire_distance_m=float(pool_fire_distance_var.get()),
                pool_fire_radiative_fraction=float(pool_fire_fraction_var.get()),
                pool_fire_atmospheric_transmissivity=float(pool_fire_tau_var.get()),
            )
            messagebox.showinfo("Saved", "Consequence inputs saved.")
        except ValueError as exc:
            messagebox.showerror("Error", str(exc) or "Please enter valid numeric values.")

    save_button = tb.Button(frame, text="Save Inputs", bootstyle=SUCCESS, command=save_params)
    save_button.grid(row=11, column=0, sticky="w", padx=5, pady=10)

    return frame
