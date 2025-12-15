import tkinter as tk
from tkinter import messagebox

# 함수: Q_o 계산
def calculate_Qo():
    try:
        GOR = float(entry_GOR.get())  # 가스 오일 비율
        Q_g = float(entry_Qg.get())   # 기체 방출률 (kg/s)
        Q_L = float(entry_QL.get())   # 액체 방출률 (kg/s)
        
        # 수식 적용: Qo = (GOR / (GOR + 1)) * Qg + (1 / (GOR + 1)) * QL
        Qo = (GOR / (GOR + 1)) * Q_g + (1 / (GOR + 1)) * Q_L

        # 결과 표시
        result_label.config(text=f"Q_o = {Qo:.4f} kg/s")
    except ValueError:
        messagebox.showerror("Invalid input", "숫자를 정확하게 입력하세요!")

# Tkinter UI 설정
root = tk.Tk()
root.title("Initial Release Rate Calculator")

# 입력 레이블 및 입력 필드
tk.Label(root, text="GOR (가스 오일 비율):").grid(row=0, column=0, padx=10, pady=5)
entry_GOR = tk.Entry(root)
entry_GOR.grid(row=0, column=1, padx=10, pady=5)

tk.Label(root, text="Q_g (기체 방출률, kg/s):").grid(row=1, column=0, padx=10, pady=5)
entry_Qg = tk.Entry(root)
entry_Qg.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Q_L (액체 방출률, kg/s):").grid(row=2, column=0, padx=10, pady=5)
entry_QL = tk.Entry(root)
entry_QL.grid(row=2, column=1, padx=10, pady=5)

# 결과 표시 라벨
result_label = tk.Label(root, text="Q_o = ? kg/s", font=("Arial", 12, "bold"))
result_label.grid(row=4, column=0, columnspan=2, pady=10)

# 계산 버튼
calculate_button = tk.Button(root, text="Calculate", command=calculate_Qo)
calculate_button.grid(row=3, column=0, columnspan=2, pady=10)

# 메인 루프 실행
root.mainloop()
