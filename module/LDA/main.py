import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from pathlib import Path

from module.LDA.page_sheet import SheetPage
from module.LDA.page_graph import GraphPage
from module.LDA.page_calculator import CalculatorPage
from module.LDA.contextual_frame import ContextualFrame

from module.LDA.utils.config import load_configuration, relative_to_assets

# from page_sheet import SheetPage
# from page_graph import GraphPage
# from page_calculator import CalculatorPage
# from contextual_frame import ContextualFrame

# from utils.config import load_configuration, relative_to_assets


def center_window(window, width, height):
    """
    Basado en https://stackoverflow.com/a/10018670.
    """
    window.update_idletasks()
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + 2*frm_width
    titlebar_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = window.winfo_screenwidth()//2 - win_width//2
    y = window.winfo_screenheight()//2 - win_height//2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.deiconify()


class ConfigDialog(tk.Toplevel):
    def __init__(self, parent, sheet_page: SheetPage, graph_page: GraphPage, calculator_page:CalculatorPage):
        super().__init__(parent)
        self.title("Configuración")

        self.sheet_page = sheet_page
        self.graph_page = graph_page
        self.calculator_page = calculator_page

        # Cargar la configuración desde el archivo si existe
        self.config_data = load_configuration()

        # Variables para almacenar la configuración
        self.units = tk.StringVar(
            value=self.config_data.get("units", "CICLOS"))
        self.decimal_format = tk.StringVar(
            value=self.config_data.get("decimal_format", ""))
        
        # Configurar la interfaz de usuario
        label_units = tk.Label(self, text="Unidades:")
        label_units.grid(row=0, column=0, padx=10, pady=5)
        self.combobox_units = ttk.Combobox(self, state="readonly", textvariable=self.units, values=[
                                           "CICLOS", "SEGUNDOS", "MINUTOS", "HORAS", "DÍAS", "SEMANAS", "SEMANAS LABORALES", "MESES", "AÑOS", "MILLAS", "KILÓMETROS"])
        self.combobox_units.grid(row=0, column=1, padx=10, pady=5)
        
        # Enlace del evento de cambio en el Combobox con la actualización de la variable
        self.combobox_units.bind("<<ComboboxSelected>>", self.update_units)

        label_decimal_format = tk.Label(self, text="Formato decimal:")
        label_decimal_format.grid(row=1, column=0, padx=10, pady=5)
        self.entry_decimal_format = tk.Entry(
            self, textvariable=self.decimal_format)
        self.entry_decimal_format.grid(row=1, column=1, padx=10, pady=5)

        button_save = tk.Button(self, text="Guardar",
                                command=self.save_configuration)
        button_save.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def update_units(self, event):
        # Actualizar la variable 'units' al valor seleccionado en el Combobox
        self.units.set(self.combobox_units.get())

    def save_configuration(self):
        # Guardar la configuración en el archivo JSON
        self.config_data["units"] = self.units.get()
        self.config_data["decimal_format"] = self.decimal_format.get()
        CONFIG_FILE = relative_to_assets("config.json")
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config_data, f)

        self.sheet_page.update_column_title(str(self.units.get()))
        self.sheet_page.unit = str(self.units.get())
        self.graph_page.update_units(str(self.units.get()))
        self.calculator_page.unit = str(self.units.get())
        messagebox.showinfo("Guardar Configuración",
                            "Configuración guardada exitosamente.")
        self.destroy()


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("LDA")
        center_window(self, 1200, 800)

        # Frame principal para contener el notebook y el otro frame
        main_frame = ttk.Frame(self)
        main_frame.pack()

        self.notebook = ttk.Notebook(main_frame, height=800)
        self.notebook.pack(side="left")

        self.sheet_page = SheetPage(self.notebook)
        self.notebook.add(self.sheet_page, text="Datos")

        self.graph_page = GraphPage(self.notebook, self.sheet_page)
        self.notebook.add(self.graph_page, text="Gráfica")

        self.calculator_page = CalculatorPage(self.notebook)
        self.notebook.add(self.calculator_page, text="Calculadora")

        menubar = tk.Menu(self)
        self.config_menu = tk.Menu(menubar, tearoff=0)
        self.config_menu.add_command(
            label="Configurar", command=self.open_config_dialog)
        menubar.add_cascade(label="Configuración", menu=self.config_menu)
        self.config(menu=menubar)

        # Frame al lado del notebook
        side_frame = ContextualFrame(main_frame, self.sheet_page, self.graph_page, self.calculator_page)
        side_frame.pack(side="left")

        # Evento para imprimir el cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.print_current_tab)

    def open_config_dialog(self):
        dialog = ConfigDialog(self, self.sheet_page, self.graph_page, self.calculator_page)

    def print_current_tab(self, event):
        current_tab_index = self.notebook.index("current")
        if current_tab_index == 1:
            self.sheet_page.validate_data()
            if not self.sheet_page.is_validate:
                self.notebook.select(self.last_tab_index)
            else: 
                self.sheet_page.sort_by_ttf()
        else:
            self.last_tab_index = current_tab_index

    def run(self):
        # Iniciar ventana
        self.mainloop()
    
    def cerrar_ventana(self):
        self.destroy()

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
