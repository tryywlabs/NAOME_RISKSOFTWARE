"""
FILE: consequence_analysis.py
DESCRIPTION:
    ANALYSIS & RESULT -> Consequence Analysis
    Computes leak rates and gas dispersion per group.
FUNCTIONS:
    create_consequence_analysis_ui(root)
"""
import os
import sys
from tkinter import ttk, messagebox, StringVar
import matplotlib.pyplot as plt

# Add middleware paths
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.abspath(os.path.join(current_dir, '../../../..'))

freq_input_path = os.path.join(project_root, 'middleware/data-input/frequency')
if freq_input_path not in sys.path:
    sys.path.insert(0, freq_input_path)

cons_state_path = os.path.join(project_root, 'middleware/data-input/consequence')
if cons_state_path not in sys.path:
    sys.path.insert(0, cons_state_path)

cons_calc_path = os.path.join(project_root, 'middleware/analysis/consequence')
if cons_calc_path not in sys.path:
    sys.path.insert(0, cons_calc_path)

plume_plot_path = os.path.join(
    project_root,
    'middleware/analysis/consequence/models/IQRAModeling/IQRA_software/GasDispersion/GaussianPlumeModel',
)
if plume_plot_path not in sys.path:
    sys.path.insert(0, plume_plot_path)

explosion_model_path = os.path.join(
    project_root,
    'middleware/analysis/consequence/models/IQRAModeling/IQRA_software/ExplosionModel',
)
if explosion_model_path not in sys.path:
    sys.path.insert(0, explosion_model_path)

fire_model_path = os.path.join(
    project_root,
    'middleware/analysis/consequence/models/IQRAModeling/IQRA_software/FireModel',
)
if fire_model_path not in sys.path:
    sys.path.insert(0, fire_model_path)


try:
    from frequency_group import FrequencyGroupManager
except Exception:
    FrequencyGroupManager = None

try:
    from consequence_state import get_params
except Exception:
    get_params = None

try:
    from calculate_consequence import calculate_group_consequence
except Exception:
    calculate_group_consequence = None

try:
    from plum_2Dgraph_ import plot_plume_3d, plot_plume_2d_profile
except Exception:
    plot_plume_3d = None
    plot_plume_2d_profile = None

_tnt_import_error = None
try:
    from TNTEqModel import per_distance_pressure
except Exception as exc:
    per_distance_pressure = None
    _tnt_import_error = exc

_tno_import_error = None
try:
    from TNOModel import energy_context_calc as tno_energy_context_calc
    from TNOModel import scenario_calc as tno_scenario_calc
except Exception as exc:
    tno_energy_context_calc = None
    tno_scenario_calc = None
    _tno_import_error = exc

_bst_import_error = None
try:
    from BSTModel import scenario_calc as bst_scenario_calc
except Exception as exc:
    bst_scenario_calc = None
    _bst_import_error = exc

_pool_fire_import_error = None
try:
    from PoolFire import calculate_radiant_heat_flux
except Exception as exc:
    calculate_radiant_heat_flux = None
    _pool_fire_import_error = exc



def create_consequence_analysis_ui(root):
    """Create the consequence analysis UI in the provided root window."""
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    header = ttk.Frame(frame)
    header.pack(fill="x")

    ttk.Label(header, text="Consequence Analysis", font=("Helvetica", 12, "bold")).pack(side="left")

    summary_label = ttk.Label(frame, text="Inputs: not loaded", anchor="w")
    summary_label.pack(fill="x", pady=(6, 8))

    explosion_frame = ttk.LabelFrame(frame, text="Explosion / Pool Fire Outputs", padding=8)
    explosion_frame.pack(fill="x", pady=(0, 8))

    explosion_w_var = StringVar(value="-")
    explosion_ze_var = StringVar(value="-")
    explosion_ps_var = StringVar(value="-")
    tno_ps_var = StringVar(value="-")
    bst_ps_var = StringVar(value="-")
    pool_fire_q_var = StringVar(value="-")

    def add_explosion_row(row, label, var):
        ttk.Label(explosion_frame, text=label).grid(row=row, column=0, sticky="w", padx=5, pady=2)
        ttk.Label(explosion_frame, textvariable=var).grid(row=row, column=1, sticky="w", padx=5, pady=2)

    add_explosion_row(0, "TNT equivalent mass W (kg)", explosion_w_var)
    add_explosion_row(1, "Scaled distance Z_e (-)", explosion_ze_var)
    add_explosion_row(2, "Overpressure P_s (bar)", explosion_ps_var)
    add_explosion_row(3, "TNO overpressure P_s (bar)", tno_ps_var)
    add_explosion_row(4, "BST overpressure P_s (bar)", bst_ps_var)
    add_explosion_row(5, "Pool fire radiant flux q'' (kW/m2)", pool_fire_q_var)

    columns = (
        "group",
        "phase",
        "pressure",
        "temperature",
        "category",
        "leak_rate",
        "model",
        "concentration",
    )
    tree = ttk.Treeview(frame, columns=columns, show="headings", height=12)
    tree.heading("group", text="Group")
    tree.heading("phase", text="Phase")
    tree.heading("pressure", text="Pressure (bar)")
    tree.heading("temperature", text="Temp")
    tree.heading("category", text="Leak Cat")
    tree.heading("leak_rate", text="Leak Rate (kg/s)")
    tree.heading("model", text="Dispersion")
    tree.heading("concentration", text="C (kg/m3)")

    tree.column("group", width=60, anchor="center")
    tree.column("phase", width=80, anchor="center")
    tree.column("pressure", width=100, anchor="center")
    tree.column("temperature", width=80, anchor="center")
    tree.column("category", width=80, anchor="center")
    tree.column("leak_rate", width=120, anchor="center")
    tree.column("model", width=90, anchor="center")
    tree.column("concentration", width=120, anchor="center")

    tree.pack(fill="both", expand=True)

    def _try_float(value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return None

    def update_explosion_outputs(params):
        if params is None:
            explosion_w_var.set("-")
            explosion_ze_var.set("-")
            explosion_ps_var.set("-")
            tno_ps_var.set("-")
            bst_ps_var.set("-")
            pool_fire_q_var.set("-")
            return

        eta = _try_float(getattr(params, "explosion_eta", None))
        mass = _try_float(getattr(params, "explosion_mass_kg", None))
        heat_combustion = _try_float(getattr(params, "explosion_heat_combustion_kj_kg", None))
        tnt_heat = _try_float(getattr(params, "explosion_tnt_heat_combustion_kj_kg", None))
        distance = _try_float(getattr(params, "explosion_distance_m", None))
        ambient_pressure = _try_float(getattr(params, "explosion_ambient_pressure_bar", None))

        if (
            eta is None
            or mass is None
            or heat_combustion is None
            or tnt_heat is None
            or mass <= 0
            or tnt_heat <= 0
            or distance is None
            or distance <= 0
        ):
            explosion_w_var.set("-")
            explosion_ze_var.set("-")
            explosion_ps_var.set("-")
            tno_ps_var.set("-")
            bst_ps_var.set("-")
            pool_fire_q_var.set("-")
            return

        w_mass = (eta * mass * heat_combustion) / tnt_heat
        if w_mass <= 0:
            explosion_w_var.set("-")
            explosion_ze_var.set("-")
            explosion_ps_var.set("-")
            tno_ps_var.set("-")
            bst_ps_var.set("-")
            pool_fire_q_var.set("-")
            return

        explosion_w_var.set(f"{w_mass:.3f}")
        ze = distance / (w_mass ** (1 / 3))
        ps = (573 * ze ** -1.685) / 100 if ze > 0 else None

        explosion_ze_var.set(f"{ze:.3f}" if ze is not None else "-")
        explosion_ps_var.set(f"{ps:.3f}" if ps is not None else "-")

        tno_ps = None
        bst_ps = None
        if ambient_pressure is not None and ambient_pressure > 0 and heat_combustion > 0 and distance > 0:
            try:
                if tno_energy_context_calc is not None:
                    energy_kj = tno_energy_context_calc(mass, heat_combustion)
                    tno_points = tno_scenario_calc(energy_kj, ambient_pressure) if tno_scenario_calc else []
                    if 1 <= int(distance) <= len(tno_points):
                        tno_ps = tno_points[int(distance) - 1][2]
                if bst_scenario_calc is not None:
                    bst_points = bst_scenario_calc(energy_kj, ambient_pressure)
                    if 1 <= int(distance) <= len(bst_points):
                        bst_ps = bst_points[int(distance) - 1][2]
            except Exception:
                tno_ps = None
                bst_ps = None

        tno_ps_var.set(f"{tno_ps:.3f}" if tno_ps is not None else "-")
        bst_ps_var.set(f"{bst_ps:.3f}" if bst_ps is not None else "-")

        pool_flux = None
        try:
            if calculate_radiant_heat_flux is not None:
                pool_flux = calculate_radiant_heat_flux(
                    float(getattr(params, "pool_fire_heat_release_rate_kw", 0.0)),
                    float(getattr(params, "pool_fire_diameter_m", 0.0)),
                    float(getattr(params, "pool_fire_distance_m", 0.0)),
                    float(getattr(params, "pool_fire_radiative_fraction", 0.0)),
                    float(getattr(params, "pool_fire_atmospheric_transmissivity", 0.0)),
                )
        except Exception:
            pool_flux = None
        pool_fire_q_var.set(f"{pool_flux:.3f}" if pool_flux is not None else "-")

    def load_params_summary():
        if get_params is None:
            summary_label.config(text="Inputs: consequence input state unavailable")
            update_explosion_outputs(None)
            return None
        params = get_params()
        summary_label.config(
            text=(
                "Inputs: gas rho={:.2f} kg/m3, liq rho={:.1f} kg/m3, GOR={:.2f}, "
                "u={:.1f} m/s, H={:.1f} m, stability={}, model={}, x_max/y/z=({:.1f},{:.1f},{:.1f})"
            ).format(
                params.gas_density_kg_m3,
                params.liquid_density_kg_m3,
                params.gor,
                params.wind_speed_m_s,
                params.release_height_m,
                params.stability_class,
                params.model,
                params.x_m,
                params.y_m,
                params.z_m,
            )
        )
        update_explosion_outputs(params)
        return params

    def run_consequence():
        if calculate_group_consequence is None:
            messagebox.showerror("Error", "Consequence calculation module not available.")
            return
        if FrequencyGroupManager is None:
            messagebox.showerror("Error", "Frequency group manager not available.")
            return
        params = load_params_summary()
        if params is None:
            messagebox.showerror("Error", "Consequence inputs are not available.")
            return

        group_manager = FrequencyGroupManager()
        group_ids = [group.group_number for group in group_manager.get_all_groups()]
        density_overrides = {
            group_id: {
                "gas_density": params.gas_density_kg_m3,
                "liquid_density": params.liquid_density_kg_m3,
                "gor": params.gor,
            }
            for group_id in group_ids
        }

        dispersion_params = {
            "model": params.model,
            "wind_speed_m_s": params.wind_speed_m_s,
            "release_height_m": params.release_height_m,
            "stability_class": params.stability_class,
            "x_m": params.x_m,
            "y_m": params.y_m,
            "z_m": params.z_m,
            "puff_time_s": params.puff_time_s,
            "release_duration_s": params.release_duration_s,
        }

        try:
            results = calculate_group_consequence(
                group_manager=group_manager,
                density_overrides=density_overrides,
                dispersion_params=dispersion_params,
            )
        except Exception as exc:
            messagebox.showerror("Error", f"Consequence calculation failed: {exc}")
            return

        for item in tree.get_children():
            tree.delete(item)

        if not results:
            return

        for group_num, data in sorted(results.items()):
            ops = data.get("operational_conditions", {})
            phase = data.get("phase", "")
            pressure = ops.get("pressure", "")
            temperature = ops.get("temperature", "")

            categories = data.get("categories", {})
            for category, cat_data in categories.items():
                leak_rate = cat_data.get("leak_rate_kg_s", 0.0)
                dispersion = cat_data.get("dispersion") or {}
                model = dispersion.get("model", "-")
                concentration = dispersion.get("concentration_kg_m3")
                if concentration is None:
                    concentration_display = "-"
                else:
                    concentration_display = f"{concentration:.3e}"

                tree.insert(
                    "",
                    "end",
                    values=(
                        group_num,
                        phase,
                        f"{pressure}",
                        f"{temperature}",
                        category,
                        f"{leak_rate:.3e}",
                        model,
                        concentration_display,
                    ),
                )

    def _parse_float(value, fallback=0.0):
        try:
            return float(value)
        except (TypeError, ValueError):
            return fallback

    def _plot_overpressure_curve(distances, pressures, title, color):
        fig, ax = plt.subplots(figsize=(10, 5.5))
        ax.plot(distances, pressures, label="Overpressure (P_s)", color=color, linewidth=2.5)
        ax.set_title(title)
        ax.set_xlabel("Distance from Explosion [m]")
        ax.set_ylabel("Overpressure (P_s) [bar]")
        ax.set_yscale("log")
        ax.set_xlim(min(distances), max(distances))

        span = max(distances) - min(distances)
        tick_step = max(1, int(span / 40))
        xticks = list(range(int(min(distances)), int(max(distances)) + 1, tick_step))
        ax.set_xticks(xticks)
        ax.tick_params(axis="x", rotation=90)

        ax.grid(True, which="major", linestyle="-", alpha=0.35)
        ax.grid(True, which="minor", linestyle="-", alpha=0.15)
        ax.legend()
        fig.tight_layout()
        plt.show()

    def open_plume_plot():
        if plot_plume_3d is None:
            messagebox.showerror("Error", "Plume plotting module not available.")
            return
        selection = tree.selection()
        if not selection:
            messagebox.showerror("Selection Required", "Select a row to plot dispersion.")
            return
        params = load_params_summary()
        if params is None:
            messagebox.showerror("Error", "Consequence inputs are not available.")
            return

        row = tree.item(selection[0], "values")
        leak_rate = _parse_float(row[5], 0.0)
        model_type = str(row[6] or params.model).lower()
        if model_type != "plume":
            messagebox.showerror("Unsupported Model", "Only plume plots are supported right now.")
            return

        x_max = float(params.x_m)
        if x_max <= 0:
            x_max = 50.0
        z_max = max(50.0, float(params.release_height_m) * 2.0)
        c_limit = _parse_float(getattr(params, "critical_concentration_kg_m3", 0.0), 0.0)
        if c_limit <= 0:
            c_limit = _parse_float(row[7], 1.0)
            if c_limit <= 0:
                c_limit = 1.0

        y_max = max(20.0, x_max / 4.0)
        plot_plume_3d(
            leak_rate,
            float(params.wind_speed_m_s),
            float(params.release_height_m),
            str(params.stability_class).upper(),
            0.0,
            x_max,
            y_max,
            0.0,
            z_max,
            c_limit,
        )

    def open_plume_profile():
        if plot_plume_2d_profile is None:
            messagebox.showerror("Error", "Plume plotting module not available.")
            return
        selection = tree.selection()
        if not selection:
            messagebox.showerror("Selection Required", "Select a row to plot dispersion.")
            return
        params = load_params_summary()
        if params is None:
            messagebox.showerror("Error", "Consequence inputs are not available.")
            return

        row = tree.item(selection[0], "values")
        leak_rate = _parse_float(row[5], 0.0)
        model_type = str(row[6] or params.model).lower()
        if model_type != "plume":
            messagebox.showerror("Unsupported Model", "Only plume plots are supported right now.")
            return

        x_max = float(params.x_m)
        if x_max <= 0:
            x_max = 50.0
        c_limit = _parse_float(getattr(params, "critical_concentration_kg_m3", 0.0), 0.0)

        plot_plume_2d_profile(
            leak_rate,
            float(params.wind_speed_m_s),
            float(params.release_height_m),
            str(params.stability_class).upper(),
            0.0,
            x_max,
            c_limit,
        )

    def open_explosion_plot():
        if per_distance_pressure is None:
            if _tnt_import_error:
                messagebox.showerror(
                    "Error",
                    f"Explosion plotting module not available: {_tnt_import_error}",
                )
            else:
                messagebox.showerror("Error", "Explosion plotting module not available.")
            return
        params = load_params_summary()
        if params is None:
            messagebox.showerror("Error", "Consequence inputs are not available.")
            return

        eta = _try_float(getattr(params, "explosion_eta", None))
        mass = _try_float(getattr(params, "explosion_mass_kg", None))
        heat_combustion = _try_float(getattr(params, "explosion_heat_combustion_kj_kg", None))
        tnt_heat = _try_float(getattr(params, "explosion_tnt_heat_combustion_kj_kg", None))

        if (
            eta is None
            or mass is None
            or heat_combustion is None
            or tnt_heat is None
            or mass <= 0
            or tnt_heat <= 0
        ):
            messagebox.showerror("Error", "Explosion inputs must be valid positive numbers.")
            return
        w_mass = (eta * mass * heat_combustion) / tnt_heat
        if w_mass <= 0:
            messagebox.showerror("Error", "Computed TNT equivalent mass is invalid.")
            return

        try:
            if per_distance_pressure is None:
                if _tnt_import_error:
                    messagebox.showerror(
                        "Error",
                        f"TNT equivalency plotting module not available: {_tnt_import_error}",
                    )
                else:
                    messagebox.showerror("Error", "TNT equivalency plotting module not available.")
                return
            points = per_distance_pressure(tnt_mass=w_mass, start=1, end=200)
        except Exception as exc:
            messagebox.showerror("Error", f"Explosion plotting failed: {exc}")
            return

        if not points:
            messagebox.showerror("Error", "Explosion plotting returned no data.")
            return

        distances = [d for d, _ in points]
        pressures = [p for _, p in points]

        _plot_overpressure_curve(
            distances,
            pressures,
            "Explosion Overpressure vs Distance (TNTEq)",
            "tab:blue",
        )

    def open_tno_plot():
        if tno_energy_context_calc is None or tno_scenario_calc is None:
            messagebox.showerror("Error", f"TNO module not available: {_tno_import_error}")
            return
        params = load_params_summary()
        if params is None:
            messagebox.showerror("Error", "Consequence inputs are not available.")
            return
        mass = _try_float(getattr(params, "explosion_mass_kg", None))
        heat_combustion = _try_float(getattr(params, "explosion_heat_combustion_kj_kg", None))
        ambient_pressure = _try_float(getattr(params, "explosion_ambient_pressure_bar", None))
        if mass is None or heat_combustion is None or ambient_pressure is None or mass <= 0 or heat_combustion <= 0 or ambient_pressure <= 0:
            messagebox.showerror("Error", "TNO inputs must be valid positive numbers.")
            return
        try:
            energy_kj = tno_energy_context_calc(mass, heat_combustion)
            points = tno_scenario_calc(energy_kj, ambient_pressure)
        except Exception as exc:
            messagebox.showerror("Error", f"TNO plotting failed: {exc}")
            return
        if not points:
            messagebox.showerror("Error", "TNO plotting returned no data.")
            return
        distances = [d for d, _, _ in points]
        pressures = [p for _, _, p in points]
        _plot_overpressure_curve(
            distances,
            pressures,
            "Explosion Overpressure vs Distance (TNO)",
            "darkgreen",
        )

    def open_bst_plot():
        if bst_scenario_calc is None:
            messagebox.showerror("Error", f"BST module not available: {_bst_import_error}")
            return
        params = load_params_summary()
        if params is None:
            messagebox.showerror("Error", "Consequence inputs are not available.")
            return
        mass = _try_float(getattr(params, "explosion_mass_kg", None))
        heat_combustion = _try_float(getattr(params, "explosion_heat_combustion_kj_kg", None))
        ambient_pressure = _try_float(getattr(params, "explosion_ambient_pressure_bar", None))
        if mass is None or heat_combustion is None or ambient_pressure is None or mass <= 0 or heat_combustion <= 0 or ambient_pressure <= 0:
            messagebox.showerror("Error", "BST inputs must be valid positive numbers.")
            return
        try:
            energy_kj = mass * heat_combustion
            points = bst_scenario_calc(energy_kj, ambient_pressure)
        except Exception as exc:
            messagebox.showerror("Error", f"BST plotting failed: {exc}")
            return
        if not points:
            messagebox.showerror("Error", "BST plotting returned no data.")
            return
        distances = [d for d, _, _ in points]
        pressures = [p for _, _, p in points]
        _plot_overpressure_curve(
            distances,
            pressures,
            "Explosion Overpressure vs Distance (BST)",
            "purple",
        )

    def open_pool_fire_plot():
        if calculate_radiant_heat_flux is None:
            messagebox.showerror("Error", f"Pool fire module not available: {_pool_fire_import_error}")
            return
        params = load_params_summary()
        if params is None:
            messagebox.showerror("Error", "Consequence inputs are not available.")
            return
        q_kw = _try_float(getattr(params, "pool_fire_heat_release_rate_kw", None))
        d_m = _try_float(getattr(params, "pool_fire_diameter_m", None))
        f = _try_float(getattr(params, "pool_fire_radiative_fraction", None))
        tau = _try_float(getattr(params, "pool_fire_atmospheric_transmissivity", None))
        if q_kw is None or d_m is None or f is None or tau is None or q_kw <= 0 or d_m <= 0:
            messagebox.showerror("Error", "Pool fire inputs are invalid.")
            return

        distances = list(range(1, 201))
        try:
            fluxes = [
                calculate_radiant_heat_flux(q_kw, d_m, float(distance), f, tau)
                for distance in distances
            ]
        except Exception as exc:
            messagebox.showerror("Error", f"Pool fire plotting failed: {exc}")
            return

        plt.figure(figsize=(8, 5))
        plt.plot(distances, fluxes, label="Radiant heat flux q''", color="orangered")
        plt.title("Pool Fire Radiant Flux vs Distance")
        plt.xlabel("Distance from Pool Center [m]")
        plt.ylabel("Radiant Heat Flux [kW/m2]")
        plt.grid(True)
        plt.legend()
        plt.show()

    button_row = ttk.Frame(frame)
    button_row.pack(fill="x", pady=(8, 0))

    ttk.Button(button_row, text="Run Consequence Analysis", command=run_consequence).pack(
        side="left", padx=5
    )
    ttk.Button(button_row, text="Reload Inputs", command=load_params_summary).pack(
        side="left", padx=5
    )
    ttk.Button(button_row, text="Plot Dispersion (3D)", command=open_plume_plot).pack(
        side="left", padx=5
    )
    ttk.Button(button_row, text="Plot Dispersion (2D)", command=open_plume_profile).pack(
        side="left", padx=5
    )
    ttk.Button(button_row, text="Plot Explosion (TNT)", command=open_explosion_plot).pack(
        side="left", padx=5
    )
    ttk.Button(button_row, text="Plot Explosion (TNO)", command=open_tno_plot).pack(
        side="left", padx=5
    )
    ttk.Button(button_row, text="Plot Explosion (BST)", command=open_bst_plot).pack(
        side="left", padx=5
    )
    ttk.Button(button_row, text="Plot Pool Fire", command=open_pool_fire_plot).pack(
        side="left", padx=5
    )

    load_params_summary()

    return frame
