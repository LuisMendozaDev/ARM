import tkinter as tk
# import utils.util_window as util_window
from PIL import ImageDraw
import utils.util_window as util_window
from tkinter import ttk

class RootView(tk.Toplevel):
    def __init__(self, parent):
        tk.Toplevel.__init__(self, parent)
        self.title("Navegación entre Vistas")
        util_window.center_window(self,1200,900)
        self.configure(bg="#001449")

        # Crear una barra de menú
        
        menubar = tk.Menu(self)
        self.config(menu=menubar)

        # Crear un menú "Archivo" con una opción "Salir"
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Salir", command=self.quit)

        # Crear un menú "Ayuda" con una opción "Acerca de"
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.mostrar_acerca_de)

        # self.notebook = ttk.Notebook(self)
        # self.notebook.pack(pady=10, padx=10)
        # # Crear pestaña 1
        # tab1 = tk.Frame(self.notebook)
        # self.notebook.add(tab1, text="Pestaña 1")

        # # Agregar widgets a la pestaña 1
        # label1 = tk.Label(tab1, text="Hola desde la pestaña 1")
        # label1.pack(pady=10)
        # button1 = tk.Button(tab1, text="Botón 1")
        # button1.pack(pady=10)

        # # Crear pestaña 2
        # tab2 = tk.Frame(self.notebook)
        # self.notebook.add(tab2, text="Pestaña 2")

        # # Agregar widgets a la pestaña 2
        # label2 = tk.Label(tab2, text="Hola desde la pestaña 2")
        # label2.pack(pady=10)
        # button2 = tk.Button(tab2, text="Botón 2")
        # button2.pack(pady=10)

        # # Configurar el evento de selección de pestaña
        # self.notebook.bind("<<NotebookTabChanged>>", self.on_tab_selected)

    def mostrar_acerca_de(self):
        # Función que se llama al hacer clic en "Acerca de" en el menú de Ayuda
        tk.messagebox.showinfo("Acerca de", "Tu mensaje de información aquí.")

    def on_tab_selected(self,event):
        current_tab = self.notebook.index(self.notebook.select())
        print("Pestaña seleccionada:", current_tab)
