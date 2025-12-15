import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from Tab1_Liquid import create_ui
from Tab2_Gas import create_ui_Qg
from Tab3_Twophase import create_ui_Qo
from Tab4_ESD import create_ui_RE
import math

# 계산 함수 정의
def calculate_QL(d, rho_L, P_L, result_label):
    try:
        d = float(d)
        rho_L = float(rho_L)
        P_L = float(P_L)

        # 단위 변환: 압력을 Pa로
        P_L_Pa = P_L * 1e5
        Q_L = 2.1 * 10**-4 * (d**2) * math.sqrt(rho_L * P_L_Pa)

        result_label.config(text=f"Q_L = {Q_L:.4f} kg/s")
    except ValueError:
        result_label.config(text="올바른 숫자를 입력하세요.")

def calculate_Qg(d, rho_g, P_g, result_label):
    try:
        d = float(d)
        rho_g = float(rho_g)
        P_g_Pa = float(P_g) * 1e5

        Q_g = 1.4 * 10**-4 * d**2 * math.sqrt(rho_g * P_g_Pa)
        result_label.config(text=f"Q_g = {Q_g:.4f} m³/s")
    except ValueError:
        result_label.config(text="올바른 숫자를 입력하세요.")

def calculate_Qo(GOR, Q_g, Q_L, result_label):  # result_label 추가
    try:
        GOR = float(GOR)  # 가스 오일 비율
        Q_g = float(Q_g)  # 기체 방출률 (kg/s)
        Q_L = float(Q_L)  # 액체 방출률 (kg/s)

        # 수식 적용: Qo = (GOR / (GOR + 1)) * Qg + (1 / (GOR + 1)) * QL
        Qo = (GOR / (GOR + 1)) * Q_g + (1 / (GOR + 1)) * Q_L

        # 결과 표시
        result_label.config(text=f"Q_o = {Qo:.4f} kg/s")
    except ValueError:
        messagebox.showerror("Invalid input", "숫자를 정확하게 입력하세요!")

def calculate_RE(Qo, I, t_l, t_B, d, b, rho_g, rho_l, result_label):
    try:
        # 입력값 가져오기
        Qo = float(Qo)
        I = float(I)
        t_l = float(t_l)
        t_B = float(t_B)
        d = float(d)
        b = float(b)
        rho_g = float(rho_g)
        rho_l = float(rho_l)

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
    except ValueError:
        messagebox.showerror("Invalid Input", "숫자를 정확하게 입력하세요!")


def main():

# 메인 프로그램 실행
    root = tk.Tk()
    root.title("4 Tabs Example")
    root.geometry("500x400")

    # Notebook 위젯 생성
    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill="both")

    # Tab 1: Liquid Leak
    frame1 = ttk.Frame(notebook)
    notebook.add(frame1, text="Liquid Leak")
    create_ui(calculate_QL, frame1)

    # Tab 2: Gas Leak
    frame2 = ttk.Frame(notebook)
    notebook.add(frame2, text="Gas Leak")
    create_ui_Qg(calculate_Qg, frame2)

    # Tab 3: Two-phase Leak
    frame3 = ttk.Frame(notebook)
    notebook.add(frame3, text="Two Phase Leak")
    create_ui_Qo(calculate_Qo, frame3)

    # Tab 4: Two-phase Leak
    frame4 = ttk.Frame(notebook)
    notebook.add(frame4, text="ESD Breakdown")
    create_ui_RE(calculate_RE, frame4)

    root.mainloop()


if __name__ == "__main__":

    main()