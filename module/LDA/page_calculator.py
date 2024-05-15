import tkinter as tk
from tkinter import ttk, messagebox

import customtkinter as ctk


from module.LDA.statics.method import exp_cdf, lognorm_cdf, weibull_cdf
from module.LDA.utils.config import load_configuration


class CalculatorPage(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)
        self.parent = parent

        self.best_dist = ""
        self.best_params = []
        self.mode = True
        self.is_valid = False
        self.unit = ''

        pantalla = tk.Frame(self, width=1, height=200, bg="#FFF",
                            highlightbackground="#CECDCD", highlightthickness=2)
        pantalla.pack(fill="both", expand=True)

        self.calc = tk.Text(pantalla, height=1, width=5,
                            bg="#fbeed3", state="disabled", font=("Arial", 100))
        self.calc.pack(side=tk.LEFT, padx=20, pady=30,
                       fill="both", expand=True)

        teclado = tk.Frame(self, width=1, height=400, bg="#FFF",
                           highlightbackground="#CECDCD", highlightthickness=2)
        teclado.pack(fill="both", expand=True)

        calculate_frame = tk.Frame(teclado, width=280, height=350,
                                   bg="#FFF", highlightbackground="#CECDCD", highlightthickness=2)
        calculate_frame.pack(side=tk.LEFT, fill="both",
                             expand=True, padx=10, pady=20)

        commands = [
            self.command_1,
            self.command_2,
        ]

        button_name = [
            "Reliability",
            "Failure Rate"
        ]

        self.button_reliability = tk.Button(
            calculate_frame, width=35, text=button_name[0], command=commands[0], bg="#149F01" if self.mode else "white")
        self.button_reliability.pack(pady=5, padx=10)
        self.button_failure_rate = tk.Button(
            calculate_frame, width=35, text=button_name[1], command=commands[1], bg="white" if self.mode else "#149F01")
        self.button_failure_rate.pack(pady=5, padx=10)

        self.on_color_change()

        input_frame = tk.Frame(teclado, width=220, height=350, bg="#FFF",
                               highlightbackground="#CECDCD", highlightthickness=2)
        input_frame.pack(side=tk.LEFT, fill="both",
                         expand=True, padx=10, pady=20)

        inputs = tk.Frame(input_frame, width=100, height=50, bg="#FFF",
                          highlightbackground="#CECDCD", highlightthickness=2)
        inputs.pack(fill="both", expand=False, padx=10, pady=10)

        # Etiqueta
        label_text = tk.Label(inputs, text="Ingrese el tiempo operativo:")
        label_text.pack()

        # Entrada de texto
        self.input = tk.Entry(inputs, width=30)
        self.input.pack()

        invicible_frame = tk.Frame(inputs, width=100, height=40, bg="#FFF")
        invicible_frame.pack()

        calculate_btn = ctk.CTkButton(master=input_frame,
                                      width=100,
                                      height=60,
                                      border_width=0,
                                      corner_radius=8,
                                      text="CALCULATE", command=self.calculate)

        calculate_btn.pack(pady=10)

        self.units = {
            "CICLOS": "CICLOS",
            "SEGUNDOS": "SEG",
            "MINUTOS": "MIN",
            "HORAS": "HR",
            "DÍAS": "DÍAS",
            "SEMANAS": "SEM",
            "SEMANAS LABORALES": "SEM LAB",
            "MESES": "MES",
            "AÑOS": "AÑO",
            "MILLAS": "MI",
            "KILÓMETROS": "KM"
        }

    def on_color_change(self):
        text_color = "white" if self.button_reliability.cget(
            "bg") == "#149F01" else "black"
        self.button_reliability.configure(fg=text_color)

        text_color = "white" if self.button_failure_rate.cget(
            "bg") == "#149F01" else "black"
        self.button_failure_rate.configure(fg=text_color)

    def command_1(self):
        self.mode = True
        self.button_reliability.config(bg="#149F01" if self.mode else "white")
        self.button_failure_rate.config(bg="white" if self.mode else "#149F01")
        self.on_color_change()

    def command_2(self):
        self.mode = False
        self.button_failure_rate.config(
            bg="#149F01" if not self.mode else "white")
        self.button_reliability.config(
            bg="white" if not self.mode else "#149F01")
        self.on_color_change()

    def mostrar_resultado(self):
        ab_unit = self.units.get(self.unit.upper(), "Unidad no encontrada")
        if self.best_dist == "Exponential":
            dist = exp_cdf(float(self.input.get()), self.best_params)
        elif self.best_dist == "Lognormal":
            dist = lognorm_cdf(float(self.input.get()), self.best_params)
        else:
            dist = weibull_cdf(float(self.input.get()), self.best_params)

        if (self.mode):
            # reliability
            result = 1-dist
        else:
            # failure_rate
            result = dist

        # Configuración de fuente para el texto completo
        self.calc.configure(font=("Arial", 75))

        # Insertar el nuevo texto
        self.calc.configure(state="normal")  # Habilita la edición
        self.calc.delete("1.0", "end")  # Borra todo el contenido actual

        # Insertar el texto con diferentes tamaños de fuente
        self.calc.insert("end", "Q(")
        # Tamaño de fuente normal para el valor ingresado
        self.calc.insert("end", self.input.get(), "normal")
        # Tamaño de fuente más pequeño para ab_unit
        self.calc.insert("end", ab_unit, "small")
        self.calc.insert("end", f") = \n{round(result, 5)}")

        # Definir el estilo de fuente para ab_unit
        self.calc.tag_configure("small", font=("Arial", 30))

        # Deshabilita la edición nuevamente
        self.calc.configure(state="disabled")
    
    def calculate(self):
        try:
            if(self.is_valid):
                self.mostrar_resultado()
            else:
                messagebox.showerror("Error", "Debe hacer el calculo de la mejor distribución")
        except ValueError:
            messagebox.showerror("Error", "El valor ingresado no es un número válido.")
