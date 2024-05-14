import tkinter as tk
from module.RBD.componentes import Componentes
from module.RBD.ventana_resultados import vetana_resultados 
from math import exp
from itertools import product
from module.RBD.nodos import nodos
import networkx as nx
import numpy as np
import time

class vetana_calculos():
    
    def __init__(self, tk_app_instance, root):
        self.tk_app_instance = tk_app_instance
        self.root=root
    
    def show_ventana_calculos(self):
        #Crear ventana
        self.ventana = tk.Toplevel(self.root)
        self.ventana.grab_set()
        self.ventana.title("Ingreso de Datos para Calculo")
        
        # label y entrada para el tiempo de estudio
        self.label_tiempo = tk.Label(self.ventana, text="Tiempo (horas):")
        self.entry_tiempo = tk.Entry(self.ventana)
        
        #poner 0 en el entry
        self.entry_tiempo.insert(0, 0)

        #Crear boton calcular
        self.boton_calcular = tk.Button(self.ventana, text="Calcular", command=self.calcular)

        # Posicionar widgets en la ventana
        self.label_tiempo.grid(row=0, column=0)
        self.entry_tiempo.grid(row=0, column=1)
        self.boton_calcular.grid(row=5, column=0, columnspan=2)
        

    def calcular(self):
        inicio_tiempo = time.time()
        
        #obtener tiempo de estudio
        self.tiempo_estudio = float(self.entry_tiempo.get())
        #obtener lista caminos del grafo
        Analisis, nodos_ordenados, lista_nodos=self.tk_app_instance.mpl_canvas.grafo.plot_instance.encontrar_caminos()
        
        
        #print("Tiempo", self.tiempo_estudio)
       
        #print("Todos",lista_todos_caminos)
        #Relacionar el primero de Resultados y los true false, con eso hacer las ecuaciones, pero antes sacar eso de un diccionario que tenga los reliabilitys
        #prevalidacion k out n
        #print("Nodos ordenados", nodos_ordenados)
        
        primer_nodo = nodos_ordenados[0][0]
        ultimo_nodo = nodos_ordenados[0][-1]
        
        
        if nodos_ordenados.count(nodos_ordenados[0]) != len(nodos_ordenados):
            for sublista in nodos_ordenados:
                if len(sublista)>2:
                    sublista.pop(0)
                    sublista.pop(-1)
                    
        # Convertir listas internas a tuplas y luego a un conjunto para eliminar duplicados
        lista_sin_repetir = list(map(tuple, nodos_ordenados))
        lista_sin_repetir = list(map(list, set(lista_sin_repetir)))

        #print("eliminados: ", lista_sin_repetir)
        
        caminos_entre_nodos_totales=[]
        grupos_componentes=[]
        
        for sublista in lista_sin_repetir:
            #print("sublista: ", sublista)
            caminos_entre_nodos_totales_parciales=[]
            
            for i in range(len(sublista) - 1):
                #nodo_inicio = nodos.obtener_nodo_por_nombre(sublista[i])
                nodo_fin = nodos.obtener_nodo_por_nombre(sublista[i + 1])
                #print("Nodo inicial:", sublista[i], " kn inicial:", nodo_inicio.get_paths_required())
                #print("Nodo final:", sublista[i + 1], " kn final:", nodo_fin.get_paths_required())
                # Filtrar caminos que contienen algún nodo presente en la lista nodos
                caminos_entre_nodos = list(nx.all_simple_paths(Analisis, source=sublista[i], target=sublista[i + 1]))
                
                caminos_entre_nodos_filtrados = []
                for camino in caminos_entre_nodos:
                    nuevo_camino = [elemento for elemento in camino if elemento not in lista_nodos]
                    if len(nuevo_camino)>0:
                        caminos_entre_nodos_filtrados.append(nuevo_camino)
                            
                caminos_entre_nodos=caminos_entre_nodos_filtrados.copy()
                
                #print("caminos_entre_nodos", caminos_entre_nodos)
                for camino in caminos_entre_nodos:
                    #print("Camino: ", camino)
                    if len(caminos_entre_nodos) == 1:  # Verificar la longitud del camino actual en lugar de la lista de caminos
                        grupos_componentes.append(camino)
                    else:
                        for elemento in camino:  # Cambiar el nombre de la variable a elemento o algo apropiado
                            grupos_componentes.append([elemento])
                                
                #print("Caminos entre nodos",caminos_entre_nodos)
                caminos_entre_nodos_totales_parciales.append(int(nodo_fin.get_paths_required()))
                caminos_entre_nodos_totales_parciales.append(caminos_entre_nodos)
            
            caminos_entre_nodos_totales.append(caminos_entre_nodos_totales_parciales)
            
        #print("grupos_componentes", grupos_componentes)
        #####################################################################################
        #En caso de sistemas Mixtos
        #####################################################################################
        #print(grupos_componentes)
        def tiene_repetidos(lista_de_listas):
            elementos_vistos = set()
            for sublista in lista_de_listas:
                for elemento in sublista:
                    if elemento in elementos_vistos:
                        return True
                    elementos_vistos.add(elemento)
            return False
        
        # Verificamos si tiene elementos repetidos
        if tiene_repetidos(grupos_componentes):
            #print("Tiene elementos repetidos")
            # Crear una lista para almacenar los elementos únicos
            elementos_unicos = []
            lista_resultante=[]

            # Crear la lista resultante con elementos únicos y desagrupar elementos repetidos
            for index_org, sublist in enumerate(grupos_componentes):
                buffer=[]
                for index, item in enumerate(sublist):
                    if item not in elementos_unicos:
                        elementos_unicos.append(item)
                        if index_org==0:
                            lista_resultante.append([item])
                        else:
                            buffer.append(item)
                        
                    if index == len(sublist) - 1:
                        if buffer:
                            if len(buffer)==1:
                                lista_resultante.append([buffer[0]])
                            else:
                                lista_resultante.append(buffer)
                                
            grupos_componentes=lista_resultante
            
        #print("Grupo componentes: ", grupos_componentes)

        #print(combinaciones_estados)
        #######################################################################################################################
        #######################################################################################################################
        
        # Inicializar un diccionario vacío
        diccionario_grupos_componentes = {}
        # Iterar sobre la lista y agregar elementos al diccionario con claves dinámicas
        for i, elementos in enumerate(grupos_componentes):
            diccionario_grupos_componentes[f'Grupo {i}'] = elementos
        #print(diccionario_grupos_componentes)

        componentes = [str(n.get_nombre()) for n in Componentes.lista_Componentes]
        #print("Componentes", componentes)
        
        # Definir los estados posibles para los grupos
        estados_grupos = [0, 1]
        # Generar todas las combinaciones de estados para los grupos de componentes
        combinaciones_estados = list(product(estados_grupos, repeat=len(diccionario_grupos_componentes)))

        # Imprimir las combinaciones de estados generadas
        resultados = []
        for combinacion in combinaciones_estados:
            resultado={}
            for idx, (grupo, componentes_grupo) in enumerate(diccionario_grupos_componentes.items()):
                estado_grupo = combinacion[idx]
                for componente in componentes_grupo:
                    resultado[componente] = estado_grupo
            resultados.append(resultado)
            
            
        #print("Resultados ",resultados)
            
        #print("caminos totalessss: ", caminos_entre_nodos_totales)
                
        #Optimización con NumPy
        booleanos2 = np.empty((len(resultados), len(caminos_entre_nodos_totales)), dtype=object)
        for i, dicc in enumerate(resultados):
            for j, claves in enumerate(caminos_entre_nodos_totales):
                temp_result = [
                    np.array([[dicc[clave] for clave in subclave] for subclave in elemento])
                    if isinstance(elemento, list)
                    else elemento
                    for elemento in claves
                ]
                booleanos2[i, j] = temp_result
        #print("bool2:", booleanos2)
        
        comprobacion = []  # Lista donde se guardarán los resultados de las comprobaciones
        nodo_final = nodos.obtener_nodo_por_nombre(ultimo_nodo)
        knout_total=int(nodo_final.get_paths_required())
        #print("knout ",knout_total)
        
        for sublista_externa in booleanos2:
            subcomprobaciones = []
            for elementos in sublista_externa:
                subsubcomprobaciones=[]
                for index in range(0, len(elementos), 2):
                    subsubsubcomprobaciones = []
                    elemento = elementos[index]
                    elemento2 = elementos[index+1]
                    #print(elemento, elemento2)
                    
                    for listas in elemento2:
                        #print(listas)
                        todos_uno = all(num == 1 for num in listas)
                        subsubsubcomprobaciones.append(todos_uno)
                        
                    if(subsubsubcomprobaciones):
                        #print("subsubsub", subsubsubcomprobaciones)
                        numeros_caminos_kout = subsubsubcomprobaciones.count(True)
                        if numeros_caminos_kout >= elemento:
                            subsubcomprobaciones.append(True)
                        else:
                            subsubcomprobaciones.append(False)
                        
                subcomprobaciones.append(all(subsubcomprobaciones))
    
            #print("sub", subcomprobaciones)
            if len(lista_sin_repetir)>1:
                if subcomprobaciones.count(True)>=knout_total:
                    comprobacion.append(True)
                else:
                    comprobacion.append(False)
            else:
                comprobacion.append(all(subcomprobaciones))
            
        #print("Comprobacion",comprobacion)
        
        
        
        diccionario_reliabilitys={}
        disponibilidad_del_sistema=1
        
        # Crear una nueva lista de diccionarios sin los elementos correspondientes a False
        nueva_lista_diccionarios = [d for d, b in zip(resultados, comprobacion) if b]
        #print(nueva_lista_diccionarios)
        casos = len(nueva_lista_diccionarios)
            
        for elemento in componentes:
            atributos = Componentes.diccionario_atributos(str(elemento))
            if not atributos:
                continue
        
            #Calcular la tasa de fallas
            rate=1/float(atributos['mtbf'])
            #obtener el tiempo de uso del componente
            tiempo_uso=float(atributos['tiempo_de_uso'])
            
            #Casos donde funciona el sistema
            contador = sum(1 for d in nueva_lista_diccionarios if d.get(str(elemento)) == 1)
            
            #print(casos,contador)
            
            Componentes.obtener_componente_por_nombre(atributos['nombre']).get_reliability()
            #distribucion exponencial
            unreliability= 1-exp(-(rate*(self.tiempo_estudio+tiempo_uso)))
            reliability=Componentes.obtener_componente_por_nombre(atributos['nombre']).get_reliability()-(unreliability)
            #print(reliability)
            
           
            
            if(reliability<0):
                reliability=0
            
            #Guardar su confiabilidad en su objeto componentes
            Componentes.obtener_componente_por_nombre(atributos['nombre']).set_reliability(reliability)
                                            
            #Agregar la confiabilidad a la lista
            diccionario_reliabilitys[atributos['nombre']]=reliability
            
            if(Componentes.obtener_componente_por_nombre(atributos['nombre']).get_reparable()):
                mttr=float(atributos['mttr'])
                mtbf=float(atributos['mtbf'])
                disponibilidad=round(((mtbf/(mtbf+mttr))+((mttr/(mtbf+mttr)*exp(-(((1/mtbf)+(1/mttr))*self.tiempo_estudio))))), 4)
                Componentes.obtener_componente_por_nombre(atributos['nombre']).set_disponibilidad(disponibilidad)
                disponibilidad_del_sistema*=disponibilidad
            else:
                disponibilidad=round(reliability, 4)
                Componentes.obtener_componente_por_nombre(atributos['nombre']).set_disponibilidad(disponibilidad)
                disponibilidad_del_sistema*=disponibilidad
            
            
                
        #print("Diccionario reliabilitys: ", diccionario_reliabilitys)
        
        lista_confiabilidades_parciales = []

        for diccionario, condiciones in zip(resultados, comprobacion):
            if condiciones:  # Si el valor en la segunda lista es True
                confiabilidad_parcial = 1.0  # Inicializar la confiabilidad parcial como un número decimal
                for clave, valor in diccionario.items():
                    confiabilidad_parcial *= diccionario_reliabilitys[clave] if valor == 1 else (1 - diccionario_reliabilitys[clave])
                lista_confiabilidades_parciales.append(confiabilidad_parcial)

        #print(lista_confiabilidades_parciales)

        confiabilidad_total = sum(lista_confiabilidades_parciales)
        confiabilidad_total= round(confiabilidad_total, 4)*100
    
        #Hacer los calculos
        print("Confiabilidad general del sistema: ",confiabilidad_total,"%")
        
        # Registra el tiempo de finalización
        fin_tiempo = time.time()

        # Calcula la diferencia para obtener el tiempo total de ejecución
        tiempo_total = fin_tiempo - inicio_tiempo

        #print(f"El código tomó {tiempo_total} segundos en ejecutarse.")
        
        #Cerrar ventana
        self.cerrar_ventana()
        
        disponibilidad_del_sistema = round(disponibilidad_del_sistema, 4)*100
        
        #Mostrar resultados
        #self.tk_app_instance.ventana_resultados.show_ventana_resultados(confiabilidad_total, self.tiempo_estudio, disponibilidad_del_sistema)
        vetana_resultados(self.root, confiabilidad_total, self.tiempo_estudio, disponibilidad_del_sistema)  # Crea una instancia de VentanaMisiones dentro de la nueva ventana
        
        
    def cerrar_ventana(self):
        self.ventana.destroy()
        
     