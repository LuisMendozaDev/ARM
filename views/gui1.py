import tkinter as tk
from tkinter import Label
from module.RBD.main import *


class Vista1(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg=controller.color_principal)
        self.controller = controller

        # Contenido de la primera vista
        label = tk.Label(self, text="Modulo RBD", font=("Helvetica", 16, "bold"), bg=controller.color_principal)
        label.pack(pady=10)

    def get_info(self):
        pass
