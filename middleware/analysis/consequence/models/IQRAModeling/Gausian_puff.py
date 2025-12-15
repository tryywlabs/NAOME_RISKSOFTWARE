import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------
# 1. 기본 매개변수 설정
# ------------------------------------
M = 1.0              # 방출 질량 (kg)
u = 2.0              # 평균 풍속 (m/s)
H = 10.0             # 방출 높이 (m)
Kx, Ky, Kz = 2.0, 2.0, 1.0   # 난류 확산계수 (m2/s)

# 공간 격자
x = np.linspace(0, 100, 200)
y = np.linspace(-50, 50, 200)
z = 0
X, Y = np.meshgrid(x, y)

# ------------------------------------
# 2. 퍼프 농도 계산 함수
# ------------------------------------
def puff_concentration(x, y, z, t):
    if t <= 0:
        return np.zeros_like(x)
    
    # 시간에 따른 분산 (σi(t) = sqrt(2Ki t))
    sigma_x = np.sqrt(2 * Kx * t)
    sigma_y = np.sqrt(2 * Ky * t)
    sigma_z = np.sqrt(2 * Kz * t)
    
    # 퍼프 중심 이동 (x - ut)
    x0 = u * t
    
    # 가우시안 퍼프 모델
    term1 = np.exp(-0.5 * ((x - x0) / sigma_x)**2)
    term2 = np.exp(-0.5 * (y / sigma_y)**2)
    term3 = np.exp(-0.5 * ((z - H) / sigma_z)**2) + np.exp(-0.5 * ((z + H) / sigma_z)**2)
    
    C = (M / ((2 * np.pi)**1.5 * sigma_x * sigma_y * sigma_z)) * term1 * term2 * term3
    return C

# ------------------------------------
# 3. 시간별 시뮬레이션 (1~30초)
# ------------------------------------
fig, axes = plt.subplots(5, 6, figsize=(18, 12))
axes = axes.flatten()

for i, t in enumerate(range(1, 31)):
    C = puff_concentration(X, Y, z, t)
    im = axes[i].contourf(X, Y, C, levels=40, cmap='plasma')
    axes[i].set_title(f"t = {t} s")
    axes[i].set_xticks([])
    axes[i].set_yticks([])

fig.colorbar(im, ax=axes.ravel().tolist(), label="Concentration (kg/m³)")
plt.suptitle("Gaussian Puff Dispersion (1–30 s)", fontsize=16)
plt.tight_layout()
plt.show()