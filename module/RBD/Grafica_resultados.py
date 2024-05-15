import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import make_interp_spline
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from scipy.interpolate import interp1d

class GraficaResultados:
    def __init__(self, master, puntos_grafica):
        self.master = master
        self.master.title("Gráfica de Resultados")
        
        self.frame = ttk.Frame(self.master)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        self.fig, self.ax = plt.subplots()
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.frame)
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.puntos = puntos_grafica  # Puedes inicializar con puntos por defecto
        
        self.graficar_curva()

    def graficar_curva(self):
        x = [p[0] for p in self.puntos]
        y = [p[1] for p in self.puntos]
        
        # Transforma los datos para ajustarse a una curva exponencial
        y_log = np.log(y)
        
        # Interpolación lineal en los datos transformados
        f = interp1d(x, y_log, kind='cubic')
        x_interp = np.linspace(min(x), max(x), 300)
        y_interp = np.exp(f(x_interp))
        
        self.ax.clear()
        self.ax.plot(x_interp, y_interp)
        # Eliminar los puntos
        self.ax.scatter([], []) 
        self.ax.set_xlabel('Tiempo (horas)')
        self.ax.set_ylabel('Fiabilidad (%)')
        self.ax.set_title('Gráfico de Fiabilidad')
        # Establecer el origen del eje y en 0
        self.ax.set_ylim(0, 1.1)
        self.ax.grid(True)
        self.canvas.draw()
        
        img_path = 'module/SRA/temp_plot.png'  # Guardar la gráfica temporalmente como imagen
        self.fig.savefig(img_path)