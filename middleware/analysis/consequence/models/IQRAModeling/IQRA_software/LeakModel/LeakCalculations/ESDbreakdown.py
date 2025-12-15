import tkinter as tk
from tkinter import messagebox
import math

'''
FUNCTION: calculate_RE():
DESCRIPTION: Calculate the release rate (R_E) and expected outflow (Q_B) based on user inputs.
'''
def calculate_RE():
    try:
        # 입력값 가져오기
        Qo = float(entry_Qo.get())        # 초기 방출률 (kg/s)
        I = float(entry_I.get())          # 고립된 구역의 재고량 (kg)
        t_l = float(entry_tl.get())       # 격리까지의 시간 (s)
        t_B = float(entry_tB.get())       # 누출 후 블로우다운까지의 시간 (s)      
        d = float(entry_d.get())          # 밸브 직경 (mm)
        b = float(entry_b.get())          # 블로우다운 밸브 직경 (mm)
        rho_g = float(entry_rho_g.get())  # 가스 밀도 (kg/m³)
        rho_l = float(entry_rho_l.get())  # 액체 밀도 (kg/m³)

        # 밀도 비율
        f = 0.5
        rho_d = f * (rho_g / rho_l)  # 밀도 인자
        
        # Eqn 13: QB = Qo * exp(-Qo * (tB - tl) / I)
        QB_calculated = Qo * math.exp(-Qo * (t_B - t_l) / I)
        
        # Eqn 15: QB/Qt = d^2 / (d^2 + rho_d * b^2)
        QB_over_Qt = d**2 / (d**2 + rho_d * b**2)
        
        # Eqn 14: MB = 1 * (QB / Qo)
        MB = I * (QB_calculated / Qo)
        
        # Eqn 12: RE = tl * Qo + I * (1 - (QB / Qo)) + MB * (QB / Qt)
        RE = t_l * Qo + I * (1 - (QB_calculated / Qo)) + MB * QB_over_Qt

        # 결과 표시
        result_label.config(text=f"R_E = {RE:.4f} kg")
        QB_label.config(text=f"Calculated Q_B = {QB_calculated:.4f} kg/s")
    except ValueError:
        messagebox.showerror("Invalid Input", "숫자를 정확하게 입력하세요!")

# Tkinter UI 설정
root = tk.Tk()
root.title("Release Rate and Expected Outflow Calculator")

# 입력 레이블 및 입력 필드
tk.Label(root, text="Q₀ (초기 방출률, kg/s):").grid(row=0, column=0, padx=10, pady=5)
entry_Qo = tk.Entry(root)
entry_Qo.grid(row=0, column=1, padx=10, pady=5)


tk.Label(root, text="I (격리 구역 재고량, kg):").grid(row=3, column=0, padx=10, pady=5)
entry_I = tk.Entry(root)
entry_I.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="tₗ (격리 시간, s):").grid(row=4, column=0, padx=10, pady=5)
entry_tl = tk.Entry(root)
entry_tl.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="t_B (블로우다운 시간, s):").grid(row=5, column=0, padx=10, pady=5)
entry_tB = tk.Entry(root)
entry_tB.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="d (밸브 직경, mm):").grid(row=7, column=0, padx=10, pady=5)
entry_d = tk.Entry(root)
entry_d.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="b (블로우다운 직경, mm):").grid(row=8, column=0, padx=10, pady=5)
entry_b = tk.Entry(root)
entry_b.grid(row=8, column=1, padx=10, pady=5)

tk.Label(root, text="ρg (가스 밀도, kg/m³):").grid(row=9, column=0, padx=10, pady=5)
entry_rho_g = tk.Entry(root)
entry_rho_g.grid(row=9, column=1, padx=10, pady=5)

tk.Label(root, text="ρl (액체 밀도, kg/m³):").grid(row=10, column=0, padx=10, pady=5)
entry_rho_l = tk.Entry(root)
entry_rho_l.grid(row=10, column=1, padx=10, pady=5)

# 결과 표시 라벨
result_label = tk.Label(root, text="R_E = ? kg", font=("Arial", 12, "bold"))
result_label.grid(row=12, column=0, columnspan=2, pady=10)

QB_label = tk.Label(root, text="Calculated Q_B = ? kg/s", font=("Arial", 10))
QB_label.grid(row=13, column=0, columnspan=2, pady=5)

# 계산 버튼
calculate_button = tk.Button(root, text="Calculate", command=calculate_RE)
calculate_button.grid(row=11, column=0, columnspan=2, pady=10)

# 메인 루프 실행
root.mainloop()
