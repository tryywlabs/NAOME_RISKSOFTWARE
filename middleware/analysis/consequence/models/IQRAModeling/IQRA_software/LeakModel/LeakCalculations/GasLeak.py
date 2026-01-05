import math

class gasLeakCalculator:

    def __init__(self):
        pass

    def calculate_Qg(self, entry_d, entry_rho_g, entry_P_g):
        d = float(entry_d.get())  # 구멍 직경 (mm)
        rho_g = float(entry_rho_g.get())  # 초기 가스 밀도 (kg/m^3)
        P_g_Pa = float(entry_P_g.get())  # 초기 가스 압력 (bar gauge)

        # 수식 적용: Qg = 1.4 * 10^-4 * d^2 * sqrt(rho_g * P_g)
        Q_g = 1.4 * 10**-4 * d**2 * math.sqrt(rho_g * P_g_Pa)
        return Q_g



'''
Unnecessary code, separate UI component not needed
TODO (15/12/25): Delete when UI has been integrated in the main app
'''

# # Tkinter UI 설정
# root = tk.Tk()
# root.title("Gas Flow Rate Calculator")

# # 입력 레이블 및 입력 필드
# tk.Label(root, text="d (구멍 직경, mm):").grid(row=0, column=0, padx=5, pady=5)
# entry_d = tk.Entry(root)
# entry_d.grid(row=0, column=1, padx=10, pady=5)

# tk.Label(root, text="ρg (가스 밀도, kg/m³):").grid(row=1, column=0, padx=5, pady=5)
# entry_rho_g = tk.Entry(root)
# entry_rho_g.grid(row=1, column=1, padx=10, pady=5)

# tk.Label(root, text="Pg (가스 압력, bar):").grid(row=2, column=0, padx=5, pady=5)
# entry_P_g = tk.Entry(root)
# entry_P_g.grid(row=2, column=1, padx=10, pady=5)

# # 결과 표시 라벨
# result_label = tk.Label(root, text="Qg = ? kg/s", font=("Arial", 12, "bold"))
# result_label.grid(row=4, column=0, columnspan=2, pady=10)

# # 계산 버튼
# calculate_button = tk.Button(root, text="Calculate", command=calculate_Qg)
# calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

# # 메인 루프 실행
# root.mainloop()
