import tkinter as tk

def create_ui_Qo(calculate_Qo_callback, parent):
    # 입력 레이블 및 입력 필드
    tk.Label(parent, text="GOR (가스 오일 비율):").grid(row=0, column=0, padx=10, pady=5)
    entry_GOR = tk.Entry(parent)
    entry_GOR.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(parent, text="Q_g (기체 방출률, kg/s):").grid(row=1, column=0, padx=10, pady=5)
    entry_Qg = tk.Entry(parent)  # 변수 이름 일치
    entry_Qg.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(parent, text="Q_L (액체 방출률, kg/s):").grid(row=2, column=0, padx=10, pady=5)
    entry_QL = tk.Entry(parent)
    entry_QL.grid(row=2, column=1, padx=10, pady=5)

    # 결과 표시 라벨
    result_label = tk.Label(parent, text="Q_o = ? kg/s", font=("Arial", 12, "bold"))
    result_label.grid(row=4, column=0, columnspan=2, pady=10)

    # 계산 버튼
    calculate_button = tk.Button(
        parent,
        text="Calculate",
        command=lambda: calculate_Qo_callback(entry_GOR.get(), entry_Qg.get(), entry_QL.get(), result_label)
    )
    calculate_button.grid(row=3, column=0, columnspan=2, pady=10)
