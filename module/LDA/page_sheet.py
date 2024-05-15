import tkinter as tk
from tksheet import Sheet
from tkinter import ttk, messagebox
import re
import json

from module.LDA.statics.method import fit_distribution, best_distribution
from module.LDA.utils.config import load_configuration

# from statics.method import calcular, fit_distribution
# from utils.config import load_configuration


class SheetPage(tk.Frame):
    def __init__(self, parent, **kwargs):
        super().__init__(parent, **kwargs)

        # self.current_font_size_index = 3
        # self.font_sizes = [("Times new roman", 8, "normal"), ("Times new roman", 10, "normal"), ("Times new roman", 12, "normal"), ("Times new roman", 14, "normal"),
        #                    ("Times new roman", 16, "normal"), ("Times new roman", 18, "normal")]

        self.sheet = Sheet(self, align="center", height=750, width=765,
                           total_rows=100, total_columns=2, empty_horizontal=0, empty_vertical=0, font=("Arial", 16, "normal"), header_font=("Arial", 16, "bold"), index_font=("Arial", 12, "normal"))
        self.sheet.enable_bindings(
            ("single_select", "drag_select", "edit_bindings", "column_width_resize", "right_click_popup_menu", "rc_insert_row"))
        self.sheet.grid(row=1, column=0, columnspan=2, sticky="nsew")
        self.config(background="#FFF")
        # self.sheet.popup_menu_add_command(
        #     "Change Font Size Up", self.increase_font_size)
        # self.sheet.popup_menu_add_command(
        #     "Change Font Size Dowm", self.decrease_font_size)
        self.sheet.font(newfont=("Times new roman", 16,
                        "normal"), reset_row_positions=True)

        # self.increase_font_size()
        self.data = []
        self.data_sorted = []
        self.is_validate = True

        self.config = load_configuration()  # Cargar configuración al iniciar
        self.unit = ''
        self.apply_configuration()

        self.previous_cell = None
        # Enlace de evento para validar después de cambiar la celda
        self.sheet.bind("<<SheetSelect>>", self.validation)

        # self.button_add_row = tk.Button(
        #     self, text="Añadir fila", command=self.add_row)
        # self.button_add_row.grid(row=0, column=0, pady=5)

        # self.button_delete_row = tk.Button(
        #     self, text="Eliminar fila", command=self.delete_row)
        # self.button_delete_row.grid(row=0, column=1, pady=5)

        self.sheet.popup_menu_add_command(
            label="Sort by ttf", func=self.sort_by_ttf)
        self.sheet.popup_menu_add_command(
            label='Add row', func=self.add_row)
        self.sheet.popup_menu_add_command(
            label='Delete row', func=self.delete_row)

    def validation(self, event):
        selected_cells = self.sheet.get_selected_cells()
        if selected_cells:
            actual_cell = selected_cells.pop()

            if (actual_cell != self.previous_cell):
                # Verificar la celda previamente seleccionada
                if self.previous_cell is not None:
                    previous_cell_data = self.sheet.get_cell_data(
                        self.previous_cell[0], self.previous_cell[1])
                    if previous_cell_data != "":
                        if self.previous_cell[1] == 0:
                            data_regex = r'^\d+(\.\d+)?$'
                            if not re.match(data_regex, previous_cell_data):
                                messagebox.showerror(
                                    "Error", "Formato inválido. Debe ser un número decimal con punto (.).\n\nVuelva a ingresar el dato en el formato adecuado")
                                self.sheet.set_cell_data(
                                    self.previous_cell[0], self.previous_cell[1], "")

                        else:
                            data_regex = r'^[a-zA-Z\s]+$'
                            if not re.match(data_regex, previous_cell_data):
                                messagebox.showerror(
                                    "Error", "Formato inválido. Solo se permiten cadenas de texto.")
                                self.sheet.set_cell_data(
                                    self.previous_cell[0], self.previous_cell[1], "")

            self.previous_cell = actual_cell

    # def increase_font_size(self):
    #     # Aumentar el tamaño de fuente
    #     if self.current_font_size_index < len(self.font_sizes) - 1:
    #         self.current_font_size_index += 1
    #         new_font = self.font_sizes[self.current_font_size_index]
    #         self.sheet.font(newfont=new_font, reset_row_positions=True)
    #         self.sheet.header_font(newfont=new_font)
    #         self.sheet.redraw()

    # def decrease_font_size(self):
    #     # Disminuir el tamaño de fuente
    #     if self.current_font_size_index > 0:
    #         self.current_font_size_index -= 1
    #         new_font = self.font_sizes[self.current_font_size_index]
    #         self.sheet.font(newfont=new_font, reset_row_positions=True)
    #         self.sheet.header_font(newfont=new_font)
    #         self.sheet.redraw()

    def delete_row(self):
        selected_row = self.sheet.get_selected_cells()
        actual_cell = selected_row.pop()
        if selected_row is not None:
            self.sheet.delete_rows(actual_cell[0], actual_cell[0] + 1)

    def add_row(self):
        self.sheet.insert_row(1)

    def update_column_title(self, units: str):
        self.column_title = f"Tiempos hasta fallar TTF ({units.lower()})"
        header_list = [self.column_title, 'Identidad']
        self.sheet.headers(header_list)
        self.sheet.column_width(column=0, width=350)
        self.sheet.column_width(column=1, width=350)

    def apply_configuration(self):
        self.unit = self.config.get("units", "CICLOS")
        self.update_column_title(self.unit)

    def sort_by_ttf(self):
        data = self.sheet.get_sheet_data()
        data_to_sort = []
        for data_line in data:
            if data_line[0] != '':
                data_to_sort.append(data_line)
        self.data_sorted = sorted(data_to_sort, key=lambda x: float(x[0]))

        self.sheet.set_sheet_data(
            self.data_sorted, reset_col_positions=False, reset_row_positions=False)

    def compute_best_distribution(self):
        self.sort_by_ttf()
        self.validate_data()
        if (self.is_validate):
            data = []
            for data_line in self.data_sorted:
                data.append(float(data_line[0]))
            best_dist, best_params = best_distribution(data)
        return best_dist, best_params

    def validate_data(self):
        data = self.sheet.get_sheet_data()
        self.is_validate = True

        data_added = []
        for data_line in data:
            if data_line[0] != '':
                data_added.append(float(data_line[0]))

        try:
            if (len(data_added) < 3):
                self.is_validate = False
                messagebox.showerror(
                    "Error", "Deben ingresarse al menos 3 datos")

            first_element = data_added[0]
            if (data_added.count(first_element) == len(data_added)):
                self.is_validate = False
                messagebox.showerror("Error", "No repita unicamente un dato")
        except Exception:
            print("No valido")
