import numpy as np
import matplotlib.pyplot as plt

# --------------------------------------------
# 1️⃣ 기본 설정값 (기본 물리 변수)
# --------------------------------------------
M = 1.0            # 방출 질량 (kg)
u = 3.0            # 평균 풍속 (m/s)
H = 10.0           # 방출 높이 (m)
stability = 'A'    # 대기 안정도 등급 (A~F)

# --------------------------------------------
# 2️⃣ PG 경험식 계수 (a, b 값)
# --------------------------------------------
PG_params = {
    'A': {'a_y': 0.18, 'b_y': 0.92, 'a_z': 0.60, 'b_z': 0.75},
    'B': {'a_y': 0.14, 'b_y': 0.92, 'a_z': 0.53, 'b_z': 0.73},
    'C': {'a_y': 0.10, 'b_y': 0.92, 'a_z': 0.34, 'b_z': 0.71},
    'D': {'a_y': 0.06, 'b_y': 0.92, 'a_z': 0.15, 'b_z': 0.70},
    'E': {'a_y': 0.04, 'b_y': 0.92, 'a_z': 0.10, 'b_z': 0.65},
    'F': {'a_y': 0.02, 'b_y': 0.89, 'a_z': 0.05, 'b_z': 0.61},
}

params = PG_params[stability]

# --------------------------------------------
# 3️⃣ σ(t) 함수 정의 (PG → Puff 변환)
#     x = u * t 관계를 사용
# --------------------------------------------
def sigma_y(t):
    return params['a_y'] * (u * t)**params['b_y']

def sigma_z(t):
    return params['a_z'] * (u * t)**params['b_z']

# --------------------------------------------
# 4️⃣ Puff 농도 계산 함수
# --------------------------------------------
def puff_concentration(x, y, z, t):
    if t <= 0:
        return np.zeros_like(x)

    sig_y = sigma_y(t)
    sig_z = sigma_z(t)
    x0 = u * t

    term1 = np.exp(-0.5 * ((x - x0) / sig_y)**2)
    term2 = np.exp(-0.5 * (y / sig_y)**2)
    term3 = np.exp(-0.5 * ((z - H) / sig_z)**2) + np.exp(-0.5 * ((z + H) / sig_z)**2)

    C = (M / ((2 * np.pi)**1.5 * sig_y**2 * sig_z)) * term1 * term2 * term3
    return C

# --------------------------------------------
# 5️⃣ 시뮬레이션 공간 및 시간 설정
# --------------------------------------------
x = np.linspace(0, 500, 200)
y = np.linspace(-100, 100, 200)
z = 0
X, Y = np.meshgrid(x, y)

time_steps = [10, 30, 60, 120]  # 시각 (초 단위)

# --------------------------------------------
# 6️⃣ 시각화
# --------------------------------------------
fig, axes = plt.subplots(1, len(time_steps), figsize=(18, 4))

for i, t in enumerate(time_steps):
    C = puff_concentration(X, Y, z, t)
    im = axes[i].contourf(X, Y, C, levels=50, cmap='plasma')
    axes[i].set_title(f"t = {t}s (Class {stability})")
    axes[i].set_xlabel("x (m)")
    if i == 0:
        axes[i].set_ylabel("y (m)")

fig.colorbar(im, ax=axes.ravel().tolist(), label="Concentration (kg/m³)")
plt.suptitle(f"PG-based Gaussian Puff Model (Stability Class {stability})", fontsize=14)
plt.tight_layout()
plt.show()
