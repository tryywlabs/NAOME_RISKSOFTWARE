import tkinter as tk

def create_ui(calculate_QL_callback, parent):
    # 입력 레이블 및 입력 필드
    tk.Label(parent, text="d (구멍 직경, mm):").grid(row=0, column=0, padx=10, pady=5)
    entry_d = tk.Entry(parent)
    entry_d.grid(row=0, column=1, padx=10, pady=5)

    tk.Label(parent, text="ρ_L (액체 밀도, kg/m³):").grid(row=1, column=0, padx=10, pady=5)
    entry_rho_L = tk.Entry(parent)
    entry_rho_L.grid(row=1, column=1, padx=10, pady=5)

    tk.Label(parent, text="P_L (압력, bar):").grid(row=2, column=0, padx=10, pady=5)
    entry_P_L = tk.Entry(parent)
    entry_P_L.grid(row=2, column=1, padx=10, pady=5)

    # 결과 표시 라벨
    result_label = tk.Label(parent, text="Q_L = ? kg/s", font=("Arial", 12, "bold"))
    result_label.grid(row=4, column=0, columnspan=2, pady=10)

    # 계산 버튼
    calculate_button = tk.Button(
        parent,
        text="Calculate",
        command=lambda: calculate_QL_callback(entry_d.get(), entry_rho_L.get(), entry_P_L.get(), result_label)
    )
    calculate_button.grid(row=3, column=0, columnspan=2, pady=10)