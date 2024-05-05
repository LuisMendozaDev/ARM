import tkinter as tk
from tkinter import ttk

class MiApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Ejemplo de Notebook en Tkinter")

        self.notebook = ttk.Notebook(self)

        self.crear_pestana("Pestaña 1", "Contenido de la Pestaña 1")
        self.crear_pestana("Pestaña 2", "Contenido de la Pestaña 2")
        self.crear_pestana("Pestaña 3", "Contenido de la Pestaña 3")
        self.crear_pestana("Pestaña 4", "Contenido de la Pestaña 4")

        self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

        self.notebook.pack(expand=True, fill=tk.BOTH, padx=10, pady=10)

    def crear_pestana(self, nombre, contenido):
        pestana = ttk.Frame(self.notebook)
        self.notebook.add(pestana, text=nombre)

        label = tk.Label(pestana, text=contenido)
        label.pack(padx=10, pady=10)

    def on_tab_selected(self, event):
        selected_tab = self.notebook.index(self.notebook.select())
        print(f"Se seleccionó la pestaña {selected_tab}")

if __name__ == "__main__":
    app = MiApp()
    app.mainloop()
