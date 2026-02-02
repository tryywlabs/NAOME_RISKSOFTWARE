import tkinter as tk
from tkinter import ttk, messagebox
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.widgets import Slider
from mpl_toolkits.mplot3d import Axes3D  # noqa: F401

# -----------------------------
# Gaussian plume model functions
# -----------------------------
def sigma_yz(x, stability_class):
    if stability_class == 'A':
        sigma_y = 0.22 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.20 * x
    elif stability_class == 'B':
        sigma_y = 0.16 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.12 * x
    elif stability_class == 'C':
        sigma_y = 0.11 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.08 * x * (1 + 0.0002 * x) ** -0.5
    elif stability_class == 'D':
        sigma_y = 0.08 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.06 * x * (1 + 0.0015 * x) ** -0.5
    elif stability_class == 'E':
        sigma_y = 0.06 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.03 * x * (1 + 0.0003 * x) ** -1
    elif stability_class == 'F':
        sigma_y = 0.04 * x * (1 + 0.0001 * x) ** -0.5
        sigma_z = 0.016 * x * (1 + 0.0003 * x) ** -1
    else:
        raise ValueError("Invalid stability class")
    return sigma_y, sigma_z


def gaussian_plume(Qevp, u_wind, H_E, x, y, z, stability_class):
    if x <= 0 or u_wind <= 0:
        return 0.0
    sigma_y, sigma_z = sigma_yz(x, stability_class)
    term1 = Qevp / (2 * np.pi * u_wind * sigma_y * sigma_z)
    term2 = np.exp(-y**2 / (2 * sigma_y**2))
    term3 = np.exp(-((H_E - z)**2) / (2 * sigma_z**2))
    term4 = np.exp(-((H_E + z)**2) / (2 * sigma_z**2))
    C = term1 * term2 * (term3 + term4)
    return C


# -----------------------------
# Contour Plot Function
# -----------------------------
def plot_contour(Qevp, u_wind, H_E, stability_class, x_min, x_max, z_min, z_max, C_limit):
    x = np.linspace(x_min, x_max, 200)
    z = np.linspace(z_min, z_max, 150)
    X, Z = np.meshgrid(x, z)
    C = np.zeros_like(X)

    for i in range(len(x)):
        for j in range(len(z)):
            C[j, i] = gaussian_plume(Qevp, u_wind, H_E, x[i], 0, z[j], stability_class)

    # 클리핑 (C_limit 이하만 시각화)
    C_clipped = np.clip(C, 0, C_limit)
    levels = np.linspace(0, C_limit, 21)

    plt.figure(figsize=(8, 5))
    contour = plt.contourf(X, Z, C_clipped, levels=levels, cmap="plasma", extend="both")

    # 사용자 입력 경계선 표시
    line = plt.contour(X, Z, C, levels=[C_limit], colors="black", linewidths=1.5)
    plt.clabel(line, fmt=f"C={C_limit:g}", inline=True, fontsize=9)

    cbar = plt.colorbar(contour)
    cbar.set_label("Concentration (kg/m³)")
    plt.title(f"Gaussian Plume Contour (C ≤ {C_limit} kg/m³)\nStability Class {stability_class}")
    plt.xlabel("Downwind Distance x (m)")
    plt.ylabel("Height z (m)")
    plt.tight_layout()
    plt.show()


def plot_plume_3d(
    Qevp,
    u_wind,
    H_E,
    stability_class,
    x_min,
    x_max,
    y_max,
    z_min,
    z_max,
    C_limit,
):
    x = np.linspace(x_min, x_max, 70)
    y = np.linspace(-y_max, y_max, 70)
    z = np.linspace(z_min, z_max, 40)
    X, Y, Z = np.meshgrid(x, y, z, indexing="ij")
    C = np.zeros_like(X)

    for i, x_val in enumerate(x):
        for j, y_val in enumerate(y):
            for k, z_val in enumerate(z):
                C[i, j, k] = gaussian_plume(Qevp, u_wind, H_E, x_val, y_val, z_val, stability_class)

    positive = C[C > 0]
    if positive.size == 0:
        return

    vmax = float(positive.max())
    cutoff = vmax * 1e-3
    x_profile = C.max(axis=(1, 2))
    keep = x_profile >= cutoff
    if keep.any():
        last_idx = int(np.where(keep)[0][-1])
        x = x[: last_idx + 1]
        X = X[: last_idx + 1, :, :]
        Y = Y[: last_idx + 1, :, :]
        Z = Z[: last_idx + 1, :, :]
        C = C[: last_idx + 1, :, :]

    threshold = min(C_limit, np.percentile(positive, 90))
    fig = plt.figure(figsize=(8.5, 6))
    ax = fig.add_subplot(111, projection="3d")
    cmap = plt.get_cmap("plasma")
    positive = C[C > 0]
    vmax = float(positive.max())
    vmin = max(vmax * 1e-4, 1e-12)
    norm = colors.LogNorm(vmin=vmin, vmax=vmax)

    def _edges(values):
        step = np.diff(values).mean() if values.size > 1 else 1.0
        edges = np.concatenate(
            ([values[0] - step / 2.0], (values[:-1] + values[1:]) / 2.0, [values[-1] + step / 2.0])
        )
        if values[0] == 0.0:
            edges[0] = 0.0
        return edges

    mask = C >= threshold
    if not mask.any():
        return

    clipped = np.clip(C, norm.vmin, norm.vmax)
    norm_vals = norm(clipped.ravel()).reshape(C.shape)
    facecolors = cmap(norm_vals)
    facecolors[..., -1] = np.where(mask, 0.45 + 0.4 * norm_vals, 0.0)

    x_edges = _edges(x)
    y_edges = _edges(y)
    z_edges = _edges(z)
    x_e, y_e, z_e = np.meshgrid(x_edges, y_edges, z_edges, indexing="ij")

    voxel_artist = {"collection": None}

    def _render(max_x):
        max_idx = int(np.searchsorted(x, max_x, side="right") - 1)
        max_idx = max(0, min(max_idx, x.size - 1))
        x_e_slice = x_e[: max_idx + 2, :, :]
        y_e_slice = y_e[: max_idx + 2, :, :]
        z_e_slice = z_e[: max_idx + 2, :, :]
        mask_slice = mask[: max_idx + 1, :, :]
        face_slice = facecolors[: max_idx + 1, :, :, :]

        if voxel_artist["collection"] is not None:
            for coll in voxel_artist["collection"].values():
                coll.remove()

        voxel_artist["collection"] = ax.voxels(
            x_e_slice,
            y_e_slice,
            z_e_slice,
            mask_slice,
            facecolors=face_slice,
            edgecolor=None,
        )

    _render(x_max)

    mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap)
    mappable.set_array([])
    fig.colorbar(mappable, ax=ax, shrink=0.65, pad=0.08, label="Concentration (kg/m3)")
    ax.set_title("Gaussian Plume 3D Dispersion")
    ax.set_xlabel("X (wind direction)")
    ax.set_ylabel("Y (crosswind)")
    ax.set_zlabel("Z (height)")
    ax.set_xlim(x_min, x_max)
    ax.set_ylim(-y_max, y_max)
    ax.set_zlim(z_min, z_max)
    ax.set_box_aspect((x_max - x_min, 2 * y_max, z_max - z_min))
    ax.plot([x_min, x_max], [0, 0], [0, 0], color="black", linewidth=1.2)
    ax.plot([0, 0], [-y_max, y_max], [0, 0], color="black", linewidth=1.2)
    ax.plot([0, 0], [0, 0], [z_min, z_max], color="black", linewidth=1.2)
    ax.view_init(elev=18, azim=-60)
    if x_max > x_min:
        fig.subplots_adjust(bottom=0.18)
        slider_ax = fig.add_axes([0.18, 0.06, 0.62, 0.03])
        x_slider = Slider(
            slider_ax,
            "Max X",
            x_min,
            x_max,
            valinit=x_max,
        )

        def _update_x(val):
            new_max = float(val)
            _render(new_max)
            ax.set_xlim(x_min, new_max)
            fig.canvas.draw_idle()

        x_slider.on_changed(_update_x)

    if not (x_max > x_min):
        plt.tight_layout()
    plt.show()


# -----------------------------
# Tkinter GUI
# -----------------------------
def calculate_and_plot():
    try:
        Qevp = float(entry_Qevp.get())
        u_wind = float(entry_u.get())
        H_E = float(entry_H.get())
        stability_class = combo_class.get().upper()

        x_min = max(0.0, float(entry_xmin.get()))
        x_max = float(entry_xmax.get())
        z_min = max(0.0, float(entry_zmin.get()))
        z_max = float(entry_zmax.get())
        C_limit = float(entry_C_limit.get())

        y_max = max(10.0, x_max / 4.0)

        # 1️⃣ 그래프 표시
        plot_plume_3d(Qevp, u_wind, H_E, stability_class, x_min, x_max, y_max, z_min, z_max, C_limit)

        # 2️⃣ 중심선(y=0, z=H_E) 농도 테이블 업데이트
        update_table(Qevp, u_wind, H_E, stability_class, x_min, x_max)

    except Exception as e:
        messagebox.showerror("Error", f"Invalid input: {e}")


def update_table(Qevp, u_wind, H_E, stability_class, x_min, x_max):
    # 테이블 초기화
    for i in tree.get_children():
        tree.delete(i)

    # 일정 간격으로 x 좌표 선택 (예: 0, 50, 100, …)
    xs = np.arange(x_min, x_max + 1, (x_max - x_min) / 10)
    for x in xs:
        if x <= 0:
            continue
        C_val = gaussian_plume(Qevp, u_wind, H_E, x, 0, H_E, stability_class)
        tree.insert("", "end", values=(f"{x:.1f}", f"{C_val:.3e}"))


def launch_gui():
    root = tk.Tk()
    root.title("Gaussian Plume 2D Contour (with Concentration Table)")
    root.geometry("500x600")
    root.resizable(False, False)

    frame = ttk.Frame(root, padding=15)
    frame.pack(fill="both", expand=True)

    # 입력 영역
    ttk.Label(frame, text="Qevp (kg/s)").grid(row=0, column=0, sticky="w", pady=3)
    entry_Qevp = ttk.Entry(frame)
    entry_Qevp.grid(row=0, column=1)
    entry_Qevp.insert(0, "1")

    ttk.Label(frame, text="u (m/s)").grid(row=1, column=0, sticky="w", pady=3)
    entry_u = ttk.Entry(frame)
    entry_u.grid(row=1, column=1)
    entry_u.insert(0, "3")

    ttk.Label(frame, text="H (m)").grid(row=2, column=0, sticky="w", pady=3)
    entry_H = ttk.Entry(frame)
    entry_H.grid(row=2, column=1)
    entry_H.insert(0, "20")

    ttk.Label(frame, text="Stability (A–F)").grid(row=3, column=0, sticky="w", pady=3)
    combo_class = ttk.Combobox(frame, values=["A", "B", "C", "D", "E", "F"], width=5)
    combo_class.grid(row=3, column=1)
    combo_class.current(3)

    # 범위 입력
    ttk.Label(frame, text="x range (m)").grid(row=4, column=0, sticky="w", pady=3)
    entry_xmin = ttk.Entry(frame, width=8)
    entry_xmin.grid(row=4, column=1, sticky="w")
    entry_xmin.insert(0, "0")
    entry_xmax = ttk.Entry(frame, width=8)
    entry_xmax.grid(row=4, column=1, sticky="e")
    entry_xmax.insert(0, "500")

    ttk.Label(frame, text="z range (m)").grid(row=5, column=0, sticky="w", pady=3)
    entry_zmin = ttk.Entry(frame, width=8)
    entry_zmin.grid(row=5, column=1, sticky="w")
    entry_zmin.insert(0, "0")
    entry_zmax = ttk.Entry(frame, width=8)
    entry_zmax.grid(row=5, column=1, sticky="e")
    entry_zmax.insert(0, "100")

    # 농도 경계값
    ttk.Label(frame, text="C-limit (kg/m³)").grid(row=6, column=0, sticky="w", pady=3)
    entry_C_limit = ttk.Entry(frame)
    entry_C_limit.grid(row=6, column=1)
    entry_C_limit.insert(0, "1.0")

    # Expose widgets for callbacks
    globals().update(
        {
            "entry_Qevp": entry_Qevp,
            "entry_u": entry_u,
            "entry_H": entry_H,
            "combo_class": combo_class,
            "entry_xmin": entry_xmin,
            "entry_xmax": entry_xmax,
            "entry_zmin": entry_zmin,
            "entry_zmax": entry_zmax,
            "entry_C_limit": entry_C_limit,
        }
    )

    ttk.Button(frame, text="2D 컨투어 + 테이블 보기", command=calculate_and_plot).grid(
        row=7, column=0, columnspan=2, pady=10
    )

    # -----------------------------
    # 결과 테이블
    # -----------------------------
    ttk.Label(frame, text="Centerline Concentration (y=0, z=H)").grid(
        row=8, column=0, columnspan=2, pady=(10, 2)
    )
    tree = ttk.Treeview(frame, columns=("x", "C"), show="headings", height=8)
    tree.heading("x", text="x (m)")
    tree.heading("C", text="C (kg/m³)")
    tree.column("x", width=100, anchor="center")
    tree.column("C", width=140, anchor="center")
    tree.grid(row=9, column=0, columnspan=2, pady=5)

    globals()["tree"] = tree

    root.mainloop()


if __name__ == "__main__":
    launch_gui()
