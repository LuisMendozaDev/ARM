import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from math import exp
import numpy as np
import json

from module.LDA.page_sheet import SheetPage
from module.LDA.statics.method import binomial, best_distribution, exp_cdf, lognorm_cdf, weibull_cdf, fit_distribution
from module.LDA.utils.config import load_configuration

# from page_sheet import SheetPage
# from utils.config import load_configuration


class GraphPage(tk.Frame):
    def __init__(self, parent, sheet: SheetPage, **kwargs):
        super().__init__(parent, **kwargs)
        self.current_graph_index = 0
        self.graphs = []
        # Creamos las figuras de Matplotlib y las añadimos a la lista

        self.config = load_configuration()
        self.unit = self.apply_configuration()
        self.logaritmica_graph = Figure(figsize=(5, 4), dpi=100)
        self.ax_log = self.logaritmica_graph.add_subplot(111)
        self.failure_time_graph = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.failure_time_graph.add_subplot(111)

        self.graphs.append(self.failure_time_graph)
        self.graphs.append(self.logaritmica_graph)

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

    def show_next_graph(self):
        self.current_graph_index += 1
        if self.current_graph_index >= len(self.graphs):
            self.current_graph_index = 0
        self.canvas.get_tk_widget().grid_forget()
        self.canvas = FigureCanvasTkAgg(
            self.graphs[self.current_graph_index], master=self)
        self.canvas.get_tk_widget().grid(row=0, column=0, columnspan=2, sticky="nsew")

    def logaritmica(self, data, best_dist, best_params):
        # Limpiamos el eje x e y
        self.ax_log.clear()

        x = data
        y = binomial(len(data))

        # Activa la cuadrícula en ambas escalas
        # best_dist_j, best_params_j = fit_distribution(x)
        # distribution_names = {
        #     "expon": "Exponential",
        #     "lognorm": "Lognormal",
        #     "gamma": "Gamma",
        #     "weibull_min": "Weibull min",
        #     "weibull_max": "Weibull max"
        # }
        # best_dist_j = distribution_names.get(best_dist_j, best_dist_j)
        self.ax_log.grid(True, which='both')

        # if best_dist_j == "Exponential":
        #     plot_cdf_j = exp_cdf(x, best_params_j)
        # elif best_dist_j == "Lognormal":
        #     plot_cdf_j = lognorm_cdf(x, best_params_j)
        # else:
        #     plot_cdf_j = weibull_cdf(x, best_params_j)

        if best_dist == "Exponential":
            plot_cdf = exp_cdf(x, best_params)
        elif best_dist == "Lognormal":
            plot_cdf = lognorm_cdf(x, best_params)
        else:
            plot_cdf = weibull_cdf(x, best_params)

        self.ax_log.set_title(f'Probability Reliability') 

        self.ax_log.scatter(x, y)
        self.ax_log.plot(x, plot_cdf)
        # self.ax_log.plot(x,plot_cdf_j, label=f'{best_dist_j} jose')
        # self.ax_log.legend()
        self.ax_log.set_ylabel('Reliabilty') 
        self.ax_log.set_xlabel(f'{self.unit}')  # Etiqueta del eje x
        self.ax_log.set_xscale('log')  # Escala logarítmica en el eje x
        self.ax_log.set_ylim(0, 1)  # Limitamos el rango de y
        # Actualizamos el gráfico
        self.logaritmica_graph.canvas.draw()

    def failure_time(self, data):
        # Limpiamos el eje x e y
        self.ax.clear()

        # Datos de las barras y sus posiciones en el eje y
        y = [i for i in range(1, len(data)+1)]  # Por ejemplo, diez barras
        x = data  # Ancho aleatorio para cada barra

        # Creamos el gráfico de barras horizontal con una altura de 0.5
        self.ax.barh(y, x, height=len(data)*0.01)
        self.ax.set_xlabel(f'{self.unit}')  # Etiqueta del eje x
        self.ax.set_xlim(1, data[-1]*1.1)
        self.ax.grid(True, axis='x')
        self.ax.set_title('F/S Timeline')  # Título del gráfico

        # Actualizamos el gráfico
        self.failure_time_graph.canvas.draw()
    
    def update_units(self, unit):
        self.unit = unit # Etiqueta del eje x con las nuevas unidades
        self.failure_time_graph.canvas.draw() # Etiqueta del eje x con las nuevas unidades
        self.logaritmica_graph.canvas.draw()

    def apply_configuration(self):
        units = self.config.get("units", "CICLOS")
        return units
