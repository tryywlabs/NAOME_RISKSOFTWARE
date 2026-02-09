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
from tkinter import ttk, messagebox

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



def create_consequence_analysis_ui(root):
    """Create the consequence analysis UI in the provided root window."""
    frame = ttk.Frame(root, padding=10)
    frame.pack(fill="both", expand=True)

    header = ttk.Frame(frame)
    header.pack(fill="x")

    ttk.Label(header, text="Consequence Analysis", font=("Helvetica", 12, "bold")).pack(side="left")

    summary_label = ttk.Label(frame, text="Inputs: not loaded", anchor="w")
    summary_label.pack(fill="x", pady=(6, 8))

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

    def load_params_summary():
        if get_params is None:
            summary_label.config(text="Inputs: consequence input state unavailable")
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

    load_params_summary()

    return frame
