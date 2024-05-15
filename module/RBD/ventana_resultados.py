import tkinter as tk
from tkinter import ttk
import pandas as pd
from module.RBD.componentes import Componentes

        
class vetana_resultados():
    def __init__(self, root, Confiabilidad_general_sistema, tiempo_estudio, disponibilidad_del_sistema):
        self.root=root
        
        # Datos en forma de diccionario
        datos = Componentes.imprimir_atributos_resultado()
        # Convertir el diccionario a un DataFrame de Pandas
        self.df = pd.DataFrame(datos)

        #iniciar ventana
        ventana = tk.Toplevel(self.root)
        ventana.grab_set()
        ventana.title("Resultados")
        
        # Título arriba de la tabla
        etiqueta_titulo = tk.Label(ventana, text="Tabla de Resultados", font=("Arial", 14))
        etiqueta_titulo.pack(pady=1)
        
        #Tiempo de estudio
        etiqueta_resultado = tk.Label(ventana, text="Tiempo de estudio: "+str(tiempo_estudio)+" horas")
        etiqueta_resultado.pack(pady=10, ipadx=5)
        
        #Resultado de la Confiabilidad General del Sistema
        etiqueta_resultado = tk.Label(ventana, text="Confiabilidad del Sistema: "+str(Confiabilidad_general_sistema)+"%")
        etiqueta_resultado.pack(pady=10, anchor='w')
        
        etiqueta_resultado = tk.Label(ventana, text="Disponibilidad del Sistema: "+str(disponibilidad_del_sistema)+"%")
        etiqueta_resultado.pack(pady=10, anchor='w')
        
        # Frame principal para organizar los elementos
        frame_principal = tk.Frame(ventana)
        frame_principal.pack(fill='both', expand=True)

        # Frame para la tabla y las barras de desplazamiento
        frame_tabla = tk.Frame(frame_principal)
        frame_tabla.pack(side='left', fill='both', expand=True)

        # Crear barras de desplazamiento
        scrollbar_y = ttk.Scrollbar(frame_tabla, orient="vertical")
        scrollbar_x = ttk.Scrollbar(frame_tabla, orient="horizontal")

        # Crear un Treeview (tabla) en el Frame para la tabla de componentes
        tabla_componentes = ttk.Treeview(frame_tabla, yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)
        scrollbar_y.config(command=tabla_componentes.yview)
        scrollbar_x.config(command=tabla_componentes.xview)
        tabla_componentes['columns'] = tuple(self.df.columns)
        tabla_componentes['show'] = 'headings'

        # Agregar encabezados a la tabla de componentes
        for columna in self.df.columns:
            tabla_componentes.heading(columna, text=columna)

        # Agregar filas y datos a la tabla de componentes
        for indice, fila in self.df.iterrows():
            tabla_componentes.insert("", "end", values=tuple(fila))

        # Mostrar la tabla de componentes y barras de desplazamiento usando grid()
        frame_tabla.rowconfigure(0, weight=1)  # Permite que la fila 0 (donde está la tabla) se expanda verticalmente
        frame_tabla.columnconfigure(0, weight=1)  # Permite que la columna 0 se expanda horizontalmente

        # Mostrar la tabla de componentes y barras de desplazamiento usando grid()
        tabla_componentes.grid(row=0, column=0, sticky='nsew')  # Colocar la tabla en la fila 0, columna 0
        scrollbar_y.grid(row=0, column=1, sticky='ns')  # Colocar scrollbar_y en la fila 0, columna 1 al lado de la tabla
        scrollbar_x.grid(row=1, column=0, sticky='ew')  # Colocar scrollbar_x debajo de la tabla (fila 1, columna 0)


        

        

