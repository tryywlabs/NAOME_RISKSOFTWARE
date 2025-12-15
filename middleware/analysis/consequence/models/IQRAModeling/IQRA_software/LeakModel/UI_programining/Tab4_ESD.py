import tkinter as tk

def create_ui_RE(calculate_RE_callback, parent):
    # 입력 레이블 및 필드
    tk.Label(parent, text="Qo (초기 방출률, kg/s):").grid(row=0, column=0, padx=5, pady=5)
    entry_Qo = tk.Entry(parent)
    entry_Qo.grid(row=0, column=1, padx=5, pady=5)

    tk.Label(parent, text="I (재고량, kg):").grid(row=1, column=0, padx=5, pady=5)
    entry_I = tk.Entry(parent)
    entry_I.grid(row=1, column=1, padx=5, pady=5)

    tk.Label(parent, text="t_l (격리 시간, s):").grid(row=2, column=0, padx=5, pady=5)
    entry_tl = tk.Entry(parent)
    entry_tl.grid(row=2, column=1, padx=5, pady=5)

    tk.Label(parent, text="t_B (블로우다운 시간, s):").grid(row=3, column=0, padx=5, pady=5)
    entry_tB = tk.Entry(parent)
    entry_tB.grid(row=3, column=1, padx=5, pady=5)

    tk.Label(parent, text="d (밸브 직경, mm):").grid(row=4, column=0, padx=5, pady=5)
    entry_d = tk.Entry(parent)
    entry_d.grid(row=4, column=1, padx=5, pady=5)

    tk.Label(parent, text="b (블로우다운 밸브 직경, mm):").grid(row=5, column=0, padx=5, pady=5)
    entry_b = tk.Entry(parent)
    entry_b.grid(row=5, column=1, padx=5, pady=5)

    tk.Label(parent, text="ρ_g (가스 밀도, kg/m³):").grid(row=6, column=0, padx=5, pady=5)
    entry_rho_g = tk.Entry(parent)
    entry_rho_g.grid(row=6, column=1, padx=5, pady=5)

    tk.Label(parent, text="ρ_l (액체 밀도, kg/m³):").grid(row=7, column=0, padx=5, pady=5)
    entry_rho_l = tk.Entry(parent)
    entry_rho_l.grid(row=7, column=1, padx=5, pady=5)

    # 결과 라벨
    result_label = tk.Label(parent, text="R_E = ? kg", font=("Arial", 12, "bold"))
    result_label.grid(row=9, column=0, columnspan=2, pady=10)

    # 계산 버튼
    calculate_button = tk.Button(
        parent,
        text="Calculate",
        command=lambda: calculate_RE_callback(
            entry_Qo.get(), entry_I.get(), entry_tl.get(), entry_tB.get(),
            entry_d.get(), entry_b.get(), entry_rho_g.get(), entry_rho_l.get(), result_label
        )
    )
    calculate_button.grid(row=8, column=0, columnspan=2, pady=10)