import numpy as np
import matplotlib.pyplot as plt

# 신뢰도 데이터 (t vs R(t))
t_values = np.array([i for i in range(21)])
R_values = np.array([1.0000, 0.9985, 0.9943, 0.9876, 0.9785,
                     0.9674, 0.9544, 0.9396, 0.9234, 0.9059,
                     0.8872, 0.8675, 0.8470, 0.8258, 0.8041,
                     0.7819, 0.7594, 0.7368, 0.7140, 0.6912,
                     0.6685])

# 누적 고장 확률 F(t) = 1 - R(t)
F_values = 1 - R_values

# 시뮬레이션 횟수
n_simulations = 10000

# 고장 발생 시간 저장
failure_times = []

# 몬테 칼로 시뮬레이션
for _ in range(n_simulations):
    u = np.random.rand()  # [0, 1) 균등분포 난수
    # 누적 분포 함수에 따라 고장 시간 결정
    for t, F in zip(t_values, F_values):
        if u < F:
            failure_times.append(t)
            break
    else:
        failure_times.append(t_values[-1])  # 고장 안났다면 마지막 시간으로 설정

# 결과 시각화
plt.hist(failure_times, bins=range(0, 22), edgecolor='black', alpha=0.7)
plt.title("Failure Time Distribution (Monte Carlo Simulation)")
plt.xlabel("Failure Time (t)")
plt.ylabel("Frequency")
plt.grid(True)
plt.show()