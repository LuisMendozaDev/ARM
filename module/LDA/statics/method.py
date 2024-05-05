import numpy as np
from scipy import stats
import matplotlib.pyplot as plt

# Genera datos de ejemplo
# data = [24.5,35.5,38.5,39.5,42.5,57.5,62.5]

# Función para ajustar distribuciones y comparar
def fit_distribution(data):
    # Lista de distribuciones para probar
    distributions = [
        stats.lognorm, stats.expon, stats.gamma, stats.weibull_min, stats.weibull_max
    ]
    
    # Ajusta cada distribución a los datos y calcula el AIC
    results = []
    for dist in distributions:
        params = dist.fit(data)
        arg = params[:-2]
        loc = params[-2]
        scale = params[-1]
        pdf = dist.pdf(data, loc=loc, scale=scale, *arg)
        sse = np.sum(np.power(data - pdf, 2.0))
        results.append((dist.name, params, sse))
    
    # Encuentra la distribución con el menor error (SSE)
    best_dist, best_params, best_sse = min(results, key=lambda x: x[2])
    return best_dist, best_params

# Ajusta la distribución y obtén el resultado
# best_dist, best_params = fit_distribution(data)
# print("La mejor distribución es:",best_dist)
# print("Parámetros de la distribución:", best_params)

# # Gráfica de histograma y distribución ajustada
# plt.hist(data, bins=30, density=True, alpha=0.6, color='g', label='Data')
# xmin, xmax = plt.xlim()
# x = np.linspace(xmin, xmax, 100)
# pdf = getattr(stats, best_dist).pdf(x, *best_params)
# plt.plot(x, pdf, 'k', linewidth=2, label='Best fit')
# plt.legend()
# plt.show()

def calcular():
    print("calcular")