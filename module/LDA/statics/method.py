import numpy as np
from scipy import stats
import sympy
from scipy.optimize import fsolve

# Genera datos de ejemplo

# Función para ajustar distribuciones y comparar
def fit_distribution(data):
    # Lista de distribuciones para probar
    distributions = [
        stats.lognorm, stats.expon, stats.weibull_min, stats.norm
    ]
    
    # Ajusta cada distribución a los datos y calcula el AIC
    results = []
    for dist in distributions:
        params = dist.fit(data)
        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]
        pdf = dist.cdf(data, loc=loc, scale=scale, *arg)
        sse = np.sum(np.power(data - pdf, 2.0))
        results.append((dist.name, params, sse))
    
    # Encuentra la distribución con el menor error (SSE)
    best_dist, best_params, best_sse = min(results, key=lambda x: x[2])
    return best_dist, best_params


def binomial(y):
    # Definir la variable simbólica 'x'
    x = sympy.Symbol('x')
    # Asignar el valor 0.5 a la variable 'q'
    q = 0.5

    # Inicializar una lista vacía llamada 'r'
    r = []

    for k in range(1, y + 1):
        # Iterar sobre los valores de k desde 1 hasta y+1
        summation = sympy.simplify(sum([sympy.binomial(y, i) * x ** i * (1 - x) ** (y - i) for i in range(k, y + 1)])) - q
        # Calcular la suma de los términos binomiales, simplificar la expresión y restar 'q' en un solo paso
        # Resolver la ecuación 'summation = 0' para 'x' utilizando fsolve
        # Definir la función que queremos resolver numéricamente
        def equation(x_val):
            return sympy.lambdify(x, summation)(x_val)
        # Resolver la ecuación numéricamente
        p = fsolve(equation, 0.01)
        # Obtener las partes reales que están entre 0 y 1
        p1 = [elemento for elemento in p if 0 < elemento < 1]
        if p1:
            r.append(p1[0])
            # Agregar el primer elemento de 'p1' a la lista 'r'
        else:
            print("No valid solution found.")
    return r


import numpy as np
from scipy.stats import expon, lognorm, weibull_min, norm
import matplotlib.pyplot as plt

# Funciones de distribución acumulativa (CDF) linealizadas

def exp_cdf(data, params):
    return expon.cdf(data, loc=params[0], scale=params[1])

def lognorm_cdf(data, params):
    return lognorm.cdf(data, params[0], loc=params[1], scale=params[2])

def weibull_cdf(data, params):
    return weibull_min.cdf(data, params[0], loc=params[1], scale=params[2])

def norm_cdf(data, params):
    return norm.cdf(data, loc=params[0], scale=params[1])

def best_distribution(data):
    # Función para calcular el estadístico de Kolmogorov-Smirnov
    def kolmogorov_smirnov_statistic(data, cdf, params):
        sorted_data = np.sort(data)
        n = len(sorted_data)
        empirical_cdf = np.arange(1, n + 1) / n
        theoretical_cdf = cdf(sorted_data, params)
        return np.max(np.abs(empirical_cdf - theoretical_cdf))

    # Ajuste de las distribuciones a los datos
    params_exp = expon.fit(data)
    params_lognorm = lognorm.fit(data)
    params_weibull = weibull_min.fit(data)
    params_norm = norm.fit(data)

    # Calcular el estadístico de Kolmogorov-Smirnov para cada distribución
    D_exp = kolmogorov_smirnov_statistic(data, exp_cdf, params_exp)
    D_lognorm = kolmogorov_smirnov_statistic(data, lognorm_cdf, params_lognorm)
    D_weibull = kolmogorov_smirnov_statistic(data, weibull_cdf, params_weibull)
    D_norm = kolmogorov_smirnov_statistic(data, norm_cdf, params_norm)

    # Determinar la distribución con el menor estadístico
    min_D = min(D_exp, D_lognorm, D_weibull, D_norm)
    if min_D == D_exp:
        return "Exponential", params_exp
    elif min_D == D_lognorm:
        return "Lognormal", params_lognorm
    elif min_D == D_weibull:
        return "Weibull", params_weibull
    else:
        return "Normal", params_norm

# # Generar una muestra de datos de ejemplo
# sample_data = np.array([750, 1456, 2104.5, 2847.3, 3786.456, 4578, 5461.45, 6145.23, 6896.551724, 7130.124777, 7299.270073, 7352.941176, 7581.501137, 7692.307692, 7812.5, 8061.915511, 8695.652174, 9523.809524, 12500, 20000, 20798.66889, 21276.59574, 21739.13043, 22222.22222, 29411.76471, 31466.33103, 33003.30033, 33333.33333, 33692.72237, 35663.33809, 35714.28571])

# # Determinar la mejor distribución y sus parámetros
# best_dist, best_params = best_distribution(sample_data)
# print("Best Distribution:", best_dist)
# print("Parameters:", best_params)

# # Función para graficar la CDF empírica y teórica
# def plot_cdf(data, cdf, params, label):
#     sorted_data = np.sort(data)
#     empirical_cdf = np.arange(1, len(sorted_data) + 1) / len(sorted_data)
#     theoretical_cdf = cdf(sorted_data, params)
#     plt.scatter(sorted_data, empirical_cdf, label='Empirical CDF')
#     plt.plot(sorted_data, theoretical_cdf, label=label)
#     plt.xlabel('Data')
#     plt.ylabel('Cumulative Probability')
#     plt.title('Empirical vs. Theoretical CDF')
#     plt.legend()
#     plt.show()

# # Graficar la CDF empírica y teórica para la mejor distribución
# print("Best Distribution:")
# if best_dist == "Exponential":
#     plot_cdf(sample_data, exp_cdf, best_params, 'Exponential CDF')
# elif best_dist == "Lognormal":
#     plot_cdf(sample_data, lognorm_cdf, best_params, 'Lognormal CDF')
# else:
#     plot_cdf(sample_data, weibull_cdf, best_params, 'Weibull CDF')

# import tkinter as tk
# from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
# import matplotlib.pyplot as plt
# import numpy as np

# def mostrar_ecuacion():
#     # Configurar la ventana de Tkinter
#     root = tk.Tk()
#     root.title("Ecuación")
    
#     # Crear un contenedor para el gráfico
#     frame = tk.Frame(root)
#     frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
#     # Crear la figura de matplotlib
#     fig, ax = plt.subplots()
#     ax.axis('off')  # No mostrar ejes
#     ax.text(0.5, 0.5, r'$\int_{a}^{b} f(x)\,dx$', fontsize=24, ha='center')
    
#     # Agregar la figura a la interfaz de Tkinter
#     canvas = FigureCanvasTkAgg(fig, master=frame)
#     canvas.draw()
#     canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)
    
#     # Botón para cerrar la ventana
#     button = tk.Button(root, text="Cerrar", command=root.destroy)
#     button.pack(side=tk.BOTTOM)
    
#     # Iniciar el bucle de la interfaz de Tkinter
#     root.mainloop()

# # Llamar a la función para mostrar la ecuación
# mostrar_ecuacion()


