import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import poisson, gamma

# ------------------------------
# 1. Bayesian posterior parameters (from prior + observed data)
# ------------------------------
alpha_post = 11       # shape parameter α'
beta_post = 108760    # rate parameter β' (단위: hr)

# ------------------------------
# 2. Monte Carlo settings
# ------------------------------
t_year = 8760         # 시간 (1년)
N = 10000             # 시뮬레이션 반복 횟수

# ------------------------------
# 3. Monte Carlo Simulation
# ------------------------------
lambda_samples = gamma.rvs(alpha_post, scale=1/beta_post, size=N)  # λ 샘플들
mu_samples = lambda_samples * t_year                               # 연간 평균 누출횟수 μ = λt
k_samples = np.random.poisson(mu_samples)                          # 포아송 분포로 실제 누출횟수 샘플

# ------------------------------
# 4. 통계 결과 계산
# ------------------------------
p_ge1_sim = np.mean(k_samples >= 1)
mean_k_sim = np.mean(k_samples)
mean_lambda = np.mean(lambda_samples)

print("📘 베이지안-몬테카를로 시뮬레이션 결과")
print(f" - λ 평균값 (posterior mean): {mean_lambda:.8f} /hr")
print(f" - 연평균 누출 횟수 (μ 평균): {np.mean(mu_samples):.4f} 회/년")
print(f" - 1년 내 ≥1회 누출 확률     : {p_ge1_sim:.4f}")

# ------------------------------
# 5. λ (누출률) 분포 시각화
# ------------------------------
plt.figure(figsize=(9, 4))
plt.hist(lambda_samples, bins=50, color='lightgreen', edgecolor='darkgreen', alpha=0.7, density=True)
plt.axvline(np.mean(lambda_samples), color='red', linestyle='--', label=f"평균 λ = {mean_lambda:.6f}")
plt.title("Posterior Distribution of λ (Leak Rate per Hour)")
plt.xlabel("λ (1/hr)")
plt.ylabel("Density")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# ------------------------------
# 6. 연간 누출 횟수 분포 시각화
# ------------------------------
max_k = np.max(k_samples)
bins = np.arange(0, max_k + 2) - 0.5

plt.figure(figsize=(9, 5))
plt.hist(k_samples, bins=bins, density=True, alpha=0.6, color='skyblue', label='Bayesian Monte Carlo (simulated)')

# 평균 μ를 이용한 이론 포아송분포도 함께 표시
k_values = np.arange(0, max_k + 1)
plt.plot(k_values, poisson.pmf(k_values, np.mean(mu_samples)), 'ro-', label='Poisson(mean μ)')
plt.xlabel("연간 누출 횟수 (k)")
plt.ylabel("확률 P(k)")
plt.title("LNG 배관 누출 횟수 분포 (Bayesian Monte Carlo vs Poisson Theory)")
plt.legend()
plt.grid(alpha=0.3)
plt.show()

# ------------------------------
# 7. 예시: 첫 번째 시뮬레이션의 누출 시점
# ------------------------------
k_example = k_samples[0]
lambda_example = lambda_samples[0]

if k_example > 0:
    leak_times = np.sort(np.random.uniform(0, t_year, k_example))
    print(f"\n🕐 예시: 첫 번째 시뮬레이션의 λ={lambda_example:.8f}/hr, 누출 {k_example}회")
    print(" - 누출 시점 (hr):", np.round(leak_times, 1))
else:
    print(f"\n🕐 예시: 첫 번째 시뮬레이션의 λ={lambda_example:.8f}/hr, 누출 없음")
