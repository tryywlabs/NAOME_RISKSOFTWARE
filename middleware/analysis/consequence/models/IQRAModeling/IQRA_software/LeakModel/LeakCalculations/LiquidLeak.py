import tkinter as tk
from tkinter import messagebox
import math

# 함수: QL 계산
def calculate_QL():
    try:
        # 입력값 가져오기
        d = float(entry_d.get())  # 구멍 직경 (mm)
        rho_L = float(entry_rho_L.get())  # 액체 밀도 (kg/m³)
        P_L_Pa = float(entry_P_L.get())  # 초기 압력 (bar gauge)

        # 수식 적용: QL = 2.1 * 10^-4 * d^2 * sqrt(rho_L * P_L)
        Q_L = 2.1 * 10**-4 * d**2 * math.sqrt(rho_L * P_L_Pa)

        # 결과 표시
        result_label.config(text=f"Q_L = {Q_L:.2f} kg/s")
    except ValueError:
        messagebox.showerror("Invalid input", "숫자를 정확하게 입력하세요!")

'''
Unnecessary code, separate UI component not needed
TODO (15/12/25): Delete when UI has been integrated in the main app
'''

# Tkinter UI 설정
root = tk.Tk()
root.title("Liquid Flow Rate Calculator")

# 입력 레이블 및 입력 필드
tk.Label(root, text="d (구멍 직경, mm):").grid(row=0, column=0, padx=10, pady=5)
entry_d = tk.Entry(root)
entry_d.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="ρ_L (액체 밀도, kg/m³):").grid(row=1, column=0, padx=10, pady=5)
entry_rho_L = tk.Entry(root)
entry_rho_L.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="P_L (압력, bar):").grid(row=2, column=0, padx=10, pady=5)
entry_P_L = tk.Entry(root)
entry_P_L.grid(row=2, column=1, padx=10, pady=5)

# 결과 표시 라벨
result_label = tk.Label(root, text="Q_L = ? kg/s", font=("Arial", 12, "bold"))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# 계산 버튼
calculate_button = tk.Button(root, text="Calculate", command=calculate_QL)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

# 메인 루프 실행
root.mainloop()
