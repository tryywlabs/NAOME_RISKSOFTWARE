import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# -------------------------------------------------
# 1️⃣ 기본 설정
# -------------------------------------------------
M = 1.0
u = 3.0
H = 10.0
stability = 'D'

# -------------------------------------------------
# 2️⃣ Pasquill–Gifford 계수
# -------------------------------------------------
PG_params = {
    'A': {'a_y': 0.18, 'b_y': 0.92, 'a_z': 0.60, 'b_z': 0.75},
    'B': {'a_y': 0.14, 'b_y': 0.92, 'a_z': 0.53, 'b_z': 0.73},
    'C': {'a_y': 0.10, 'b_y': 0.92, 'a_z': 0.34, 'b_z': 0.71},
    'D': {'a_y': 0.06, 'b_y': 0.92, 'a_z': 0.15, 'b_z': 0.70},
    'E': {'a_y': 0.04, 'b_y': 0.92, 'a_z': 0.10, 'b_z': 0.65},
    'F': {'a_y': 0.02, 'b_y': 0.89, 'a_z': 0.05, 'b_z': 0.61},
}
params = PG_params[stability]

# -------------------------------------------------
# 3️⃣ σ(t) 함수
# -------------------------------------------------
def sigma_y(t): return params['a_y'] * (u * t)**params['b_y']
def sigma_z(t): return params['a_z'] * (u * t)**params['b_z']

# -------------------------------------------------
# 4️⃣ 퍼프 농도 계산
# -------------------------------------------------
def puff_concentration(x, y, z, t):
    if t <= 0:
        return np.zeros_like(x)
    sig_y, sig_z = sigma_y(t), sigma_z(t)
    x0 = u * t
    term1 = np.exp(-0.5 * ((x - x0) / sig_y)**2)
    term2 = np.exp(-0.5 * (y / sig_y)**2)
    term3 = np.exp(-0.5 * ((z - H) / sig_z)**2) + np.exp(-0.5 * ((z + H) / sig_z)**2)
    return (M / ((2 * np.pi)**1.5 * sig_y**2 * sig_z)) * term1 * term2 * term3

# -------------------------------------------------
# 5️⃣ 격자 설정
# -------------------------------------------------
x = np.linspace(0, 500, 200)
y = np.linspace(-100, 100, 200)
z = 0
X, Y = np.meshgrid(x, y)

# -------------------------------------------------
# 6️⃣ 초기 그래프
# -------------------------------------------------
fig, ax = plt.subplots(figsize=(8, 5))
ax.set_xlim(0, 500)
ax.set_ylim(-100, 100)
ax.set_xlabel("x (m)")
ax.set_ylabel("y (m)")
ax.set_title(f"PG-based Puff | Class {stability}")
contour = ax.contourf(X, Y, np.zeros_like(X), levels=50, cmap='plasma')
cbar = plt.colorbar(contour, ax=ax, label="Concentration (kg/m³)")

# -------------------------------------------------
# 7️⃣ 업데이트 함수
# -------------------------------------------------
def update(frame):
    ax.clear()
    t = frame
    C = puff_concentration(X, Y, z, t)
    cont = ax.contourf(X, Y, C, levels=50, cmap='plasma')
    ax.set_xlim(0, 500)
    ax.set_ylim(-100, 100)
    ax.set_xlabel("x (m)")
    ax.set_ylabel("y (m)")
    ax.set_title(f"PG-based Puff | {stability} | t = {t:>3}s")
    return []

# -------------------------------------------------
# 8️⃣ 애니메이션 생성
# -------------------------------------------------
frames = np.arange(1, 121, 2)
anim = FuncAnimation(fig, update, frames=frames, interval=200, blit=False, save_count=len(frames))

# -------------------------------------------------
# 9️⃣ 저장: MP4 → GIF fallback
# -------------------------------------------------
try:
    from matplotlib.animation import FFMpegWriter
    writer = FFMpegWriter(fps=10, bitrate=1800)
    anim.save("pg_puff.mp4", writer=writer, dpi=150)
    print("✅ Saved as MP4: pg_puff.mp4")
except Exception as e:
    print("⚠️ ffmpeg not available, saving as GIF...")
    anim.save("pg_puff.gif", writer="pillow", fps=10, dpi=120)
    print("✅ Saved as GIF: pg_puff.gif")

plt.close()
