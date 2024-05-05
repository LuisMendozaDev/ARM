import tkinter as tk
from tkinter import ttk

import customtkinter as ctk


class CalculatorPage(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        pantalla = tk.Frame(self, width=1, height=200, bg="#FFF", highlightbackground="#CECDCD", highlightthickness=2)
        pantalla.pack(fill="both", expand=True)

        self.calc = tk.Text(pantalla, height=16, width=80, bg="#fbeed3", state="disabled")
        self.calc.pack(side=tk.LEFT, padx=20, pady=30, fill="both", expand=True)

        teclado = tk.Frame(self, width=1, height=400, bg="#FFF", highlightbackground="#CECDCD", highlightthickness=2)
        teclado.pack(fill="both", expand=True)

        calculate_frame = tk.Frame(teclado, width=280, height=350, bg="#FFF",highlightbackground="#CECDCD", highlightthickness=2)
        calculate_frame.pack(side=tk.LEFT, fill="both",
                             expand=True, padx=10, pady=20)

        commands = [
            self.command_1,
            self.command_2,
            self.command_3,
            self.command_4,
            self.command_5,
            self.command_6,
            self.command_7,
            self.command_8,
            self.command_9
        ]

        button_name = [
            "Reliability",
            "Pro. of Failure",
            "Con. Realiability",
            "Cond. Prob. of Failure",
            "Reliable Life",
            "BX Life",
            "Mean Life",
            "Mean Remaining Life",
            "Failure Rate"
        ]

        # Creamos los botones
        for i in range(0, 9):
            button_text = button_name[i]
            button = tk.Button(calculate_frame, width=35,
                               text=button_text, command=commands[i-1])
            button.pack(pady=5, padx=10)

        input_frame = tk.Frame(teclado, width=220, height=350, bg="#FFF", highlightbackground="#CECDCD", highlightthickness=2)
        input_frame.pack(side=tk.LEFT, fill="both",
                         expand=True, padx=10, pady=20)

        inputs = tk.Frame(input_frame, width=100, height=50, bg="#FFF", highlightbackground="#CECDCD", highlightthickness=2)
        inputs.pack(fill="both", expand=True, padx=10, pady=10)

        # Etiqueta
        label_text = tk.Label(inputs, text="Ingrese un número:")
        label_text.pack()

        # Entrada de texto
        self.input_text = tk.Entry(inputs, width=30)
        self.input_text.pack()

        invicible_frame = tk.Frame(inputs, width=100, height=40, bg="#FFF")
        invicible_frame.pack()

        calculate_btn = ctk.CTkButton(master=input_frame,
                                      width=100,
                                      height=60,
                                      border_width=0,
                                      corner_radius=8,
                                      text="CALCULATE")

        calculate_btn.pack(pady=10)

    def command_1(self):
        print("Se hizo clic en el botón 1")

    def command_2(self):
        print("Se hizo clic en el botón 2")

    def command_3(self):
        print("Se hizo clic en el botón 3")

    def command_4(self):
        print("Se hizo clic en el botón 4")

    def command_5(self):
        print("Se hizo clic en el botón 5")

    def command_6(self):
        print("Se hizo clic en el botón 6")

    def command_7(self):
        print("Se hizo clic en el botón 7")

    def command_8(self):
        print("Se hizo clic en el botón 8")

    def command_9(self):
        print("Se hizo clic en el botón 9")
