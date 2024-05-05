import tkinter as tk

class Vista2(tk.Frame):
    def __init__(self, master, controller):
        tk.Frame.__init__(self, master, bg=controller.color_principal)
        self.controller = controller

        # Contenido de la segunda vista
        label = tk.Label(self, text="Tabla con resultados", font=(
            "Helvetica", 16, "bold"), bg=controller.color_principal)
        label.pack(pady=10)

    def get_info(self):
        return self.entry_text.get()
