import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

from module.LDA.page_sheet import SheetPage
from module.LDA.page_graph import GraphPage
from module.LDA.page_calculator import CalculatorPage
from module.LDA.contextual_frame import ContextualFrame

from module.LDA.utils.config import load_configuration

CONFIG_FILE = "config.json"


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
    def __init__(self, parent, sheet_page: SheetPage):
        super().__init__(parent)
        self.title("Configuración")

        self.sheet_page = sheet_page

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

        label_decimal_format = tk.Label(self, text="Formato decimal:")
        label_decimal_format.grid(row=1, column=0, padx=10, pady=5)
        self.entry_decimal_format = tk.Entry(
            self, textvariable=self.decimal_format)
        self.entry_decimal_format.grid(row=1, column=1, padx=10, pady=5)

        button_save = tk.Button(self, text="Guardar",
                                command=self.save_configuration)
        button_save.grid(row=2, column=0, columnspan=2, padx=10, pady=5)

    def save_configuration(self):
        # Guardar la configuración en el archivo JSON
        self.config_data["units"] = self.units.get()
        self.config_data["decimal_format"] = self.decimal_format.get()
        with open(CONFIG_FILE, "w") as f:
            json.dump(self.config_data, f)

        messagebox.showinfo("Guardar Configuración",
                            "Configuración guardada exitosamente.")
        self.sheet_page.update_column_title(str(self.units.get()))
        self.destroy()


class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Ejemplo de TkSheet")
        center_window(self, 1100, 800)

        menubar = tk.Menu(self)
        self.config_menu = tk.Menu(menubar, tearoff=0)
        self.config_menu.add_command(
            label="Configurar", command=self.open_config_dialog)
        menubar.add_cascade(label="Configuración", menu=self.config_menu)
        self.config(menu=menubar)

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

        # Frame al lado del notebook
        side_frame = ContextualFrame(main_frame, self.sheet_page)
        side_frame.pack(side="left")

        # Evento para imprimir el cambio de pestaña
        self.notebook.bind("<<NotebookTabChanged>>", self.print_current_tab)

    def open_config_dialog(self):
        dialog = ConfigDialog(self, self.sheet_page)

    # def apply_configuration(self):
    #     units = self.config.get("units", "CICLOS")
    #     self.sheet_update_column_title(units)

    def print_current_tab(self, event):
        current_tab_index = self.notebook.index("current")
        if current_tab_index == 1:
            self.sheet_page.validate_data()
            if not self.sheet_page.is_validate:
                self.notebook.select(self.last_tab_index)
        else:
            self.last_tab_index = current_tab_index

    def run(self):
        # Iniciar ventana
        self.mainloop()
    
    def cerrar_ventana(self):
        self.destroy()

# if __name__ == "__main__":
#     app = MainApp()
#     app.mainloop()
