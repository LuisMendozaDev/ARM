import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from math import exp
import numpy as np
import json

from module.LDA.page_sheet import SheetPage
from module.LDA.utils.config import load_configuration


class GraphPage(tk.Frame):
    def __init__(self, parent, sheet: SheetPage, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_graph_index = 0
        self.graphs = []

        self.sheet_page = sheet

        self.sheet_data = self.sheet_page.data_sorted

        # Creamos las figuras de Matplotlib y las añadimos a la lista

        self.config = load_configuration()

        self.graphs.append(self.logaritmica())
        self.graphs.append(self.failure_time())

        # Creamos el lienzo para mostrar la figura en tkinter
        self.canvas = FigureCanvasTkAgg(
            self.graphs[self.current_graph_index], master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew")

        # Botones para navegar entre las gráficas
        prev_button = tk.Button(self, text="Anterior",
                                command=self.show_previous_graph)
        prev_button.grid(row=1, column=0, sticky="ew")
        next_button = tk.Button(self, text="Siguiente",
                                command=self.show_next_graph)
        next_button.grid(row=1, column=1, sticky="ew")

        # Configuración de pesos de las filas y columnas
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

    def show_previous_graph(self):
        self.current_graph_index -= 1
        if self.current_graph_index < 0:
            self.current_graph_index = len(self.graphs) - 1
        self.canvas.get_tk_widget().grid_forget()
        self.canvas = FigureCanvasTkAgg(
            self.graphs[self.current_graph_index], master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew")
        print(self.sheet_data)

    def show_next_graph(self):
        self.current_graph_index += 1
        if self.current_graph_index >= len(self.graphs):
            self.current_graph_index = 0
        self.canvas.get_tk_widget().grid_forget()
        self.canvas = FigureCanvasTkAgg(
            self.graphs[self.current_graph_index], master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew")

    def logaritmica(self):
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)
        x = np.linspace(0.01, 1, 5)
        y = np.array([0.12,0.37,0.5,0.63,0.88])
        ax.plot(x, y)
        ax.set_xscale('log')  # Escala logarítmica en el eje x
        ax.set_ylim(0, 1)  # Limitamos el rango de y
        # Activa la cuadrícula en ambas escalas
        ax.grid(True, which='both')
        return fig

    def failure_time(self):
        unit = self.apply_configuration()
        fig = Figure(figsize=(5, 4), dpi=100)
        ax = fig.add_subplot(111)

        # Datos de las barras y sus posiciones en el eje y
        y = [1,2,3,4]  # Por ejemplo, diez barras
        x = [100,200,300,400]  # Ancho aleatorio para cada barra

        # Creamos el gráfico de barras horizontal con una altura de 0.5
        ax.barh(y, x, height=0.02)
        ax.set_xlabel(f'{unit}')  # Etiqueta del eje x
        ax.set_xlim(0.01, 500)
        ax.grid(True, axis='x')
        ax.set_title('F/S Timeline')  # Título del gráfico

        return fig
    
    def apply_configuration(self):
        units = self.config.get("units", "CICLOS")
        return units