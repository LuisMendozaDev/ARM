import tkinter as tk
from tkinter import ttk
from tkinter import simpledialog
from tkinter import messagebox
import numpy as np
import random
from module.RBD.nodos import nodos

class VentanaMisiones:
    def __init__(self, root, main):
        self.root = root
        self.main=main
        self.root.title("Gestor de Misiones")
        
        # Configurar la ventana para que no se pueda maximizar ni cambiar de tamaño
        self.root.resizable(width=False, height=False)

        # Diccionario para almacenar las misiones
        self.misiones = {}

        # Etiqueta y entrada para agregar una nueva misión
        self.label_nueva_mision = tk.Label(root, text="Nueva Misión:")
        self.label_nueva_mision.grid(row=0, column=0, padx=10, pady=20)
        self.entry_nueva_mision = tk.Entry(root)
        self.entry_nueva_mision.grid(row=0, column=1, padx=10, pady=20)
        self.btn_agregar_mision = tk.Button(root, text="Agregar Misión", command=self.agregar_mision)
        self.btn_agregar_mision.grid(row=0, column=2, padx=10, pady=20)
        
        self.btn_ejecutar = tk.Button(root, text="Ejecutar simulacion", command= self.ejecutar_simulacion)
        self.btn_ejecutar.grid(row=2, column=1, padx=10, pady=(30,30))
        
        # Crear un Notebook para manejar múltiples pestañas para cada misión
        self.notebook = ttk.Notebook(root)
        self.notebook.grid(row=1, column=0, columnspan=3, padx=10, pady=5)
        
        #informacion relevante para operaciones
        lista_nodos=self.main.mpl_canvas.grafo.plot_instance.nodes.copy()
        dict_nombre_nodos={}
         
        #Cambiar los nombres de los nodos por los que ingreso el usuario
        
        
        for nodo in lista_nodos:
            if str(self.main.mpl_canvas.grafo.plot_instance.node_artists[nodo].shape)=='o':
                nombre_nodo=self.main.mpl_canvas.grafo.plot_instance.node_label_artists[nodo].get_text()
                nodo_final = nodos.obtener_nodo_por_nombre(nombre_nodo)
                knout_total=int(nodo_final.get_paths_required())
                dict_nombre_nodos[nombre_nodo]=knout_total
                
        self.nombre_nodos=list(dict_nombre_nodos.keys())
        self.knouts=list(dict_nombre_nodos.values())
            
        
        
    def validar_numerico(self, event):
            tecla_pulsada = event.char
            if not tecla_pulsada.isdigit() and tecla_pulsada != '\b':
                return 'break'
            

    def agregar_mision(self):
        # Obtener el nombre de la nueva misión desde la entrada
        nombre_mision = self.entry_nueva_mision.get()
        

        # Verificar si el nombre de la misión está en blanco
        if not nombre_mision:
            messagebox.showwarning("Error", "Por favor, ingrese un nombre para la misión.")
            return
        
        # Verificar si el nombre de la misión ya está en uso
        if nombre_mision in self.misiones:
            messagebox.showwarning("Error", "El nombre de la misión ya está en uso. Por favor, ingrese un nombre diferente.")
            return

        # Crear una nueva pestaña para la misión
        frame_mision = ttk.Frame(self.notebook)
        
        # Crear un nuevo marco para contener la etiqueta y la entrada
        frame_duracion_mision = tk.Frame(frame_mision)
        frame_duracion_mision.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        # Etiqueta para la duración de la misión
        self.label_duracion_mision = tk.Label(frame_duracion_mision, text="Duración de la Misión (Horas):")
        self.label_duracion_mision.grid(row=0, column=0, padx=5, pady=10, sticky="w")

        # Entrada para la duración de la misión
        self.entry_duracion_mision = tk.Entry(frame_duracion_mision)
        self.entry_duracion_mision.grid(row=0, column=1, padx=5, pady=10, sticky="w")
        self.entry_duracion_mision.bind('<KeyPress>', self.validar_numerico)

        
        self.notebook.add(frame_mision, text=nombre_mision)
    
        # Crear un Treeview para la misión
        columns = ['Nodos', 'K of n out']
        tabla_mision = ttk.Treeview(frame_mision, columns=columns, show='headings')
        for col in columns:
            tabla_mision.heading(col, text=col)
        tabla_mision.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        # Permitir la edición de "K of n out" con el teclado
        tabla_mision.bind('<Double-1>', self.editar_valor_kn_out)

        # Obtener la lista de nodos
        nodos = self.nombre_nodos # Ejemplo, reemplaza con tu lista de nodos
        #nodos=self.lista_nodos
        # Agregar los nodos al Treeview
        lista_knout=self.knouts
        
        print("nodos",nodos)
        print("lista kout",lista_knout)
        
        for nodo, kout in zip(nodos, lista_knout):
            tabla_mision.insert('', 'end', values=(nodo, kout))

        # Agregar la tabla al diccionario de misiones
        self.misiones[nombre_mision] = tabla_mision

        # Limpiar la entrada de nueva misión
        self.entry_nueva_mision.delete(0, tk.END)
        
        # Crear un nuevo marco para contener 
        frame_botones = tk.Frame(frame_mision)
        frame_botones.grid(row=1, column=1, padx=5, pady=10, sticky="w")
        
        #Botón para editar el nombre de la misión
        btn_editar_nombre = tk.Button(frame_botones, text="Editar Nombre", command= self.editar_nombre_mision)
        btn_editar_nombre.grid(row=0, column=0, padx=10, pady=5)

        # Botón para eliminar la misión
        btn_eliminar_mision = tk.Button(frame_botones, text="Eliminar Misión", command=self.eliminar_mision)
        btn_eliminar_mision.grid(row=1, column=0, padx=10, pady=5)
    
        # Seleccionar la nueva pestaña
        index_nueva_pestaña = self.notebook.index("end") - 1  # Obtener el índice de la nueva pestaña
        self.notebook.select(index_nueva_pestaña)
    
    #ejecturar simulacion
    
    def ejecutar_simulacion(self):
        while True:
            numeros_intervalos = int(simpledialog.askstring("Número de Intervalos", "Por favor ingresa el número de intervalos:"))
            if numeros_intervalos is not None:
                try:
                    numeros_intervalos = int(numeros_intervalos)
                    if numeros_intervalos > 0:
                        print("El número de intervalos ingresado es:", numeros_intervalos)
                        break
                    else:
                        print("Por favor, ingresa un valor numérico positivo.")
                except ValueError:
                    print("Por favor, ingresa un valor numérico válido.")
            else:
                print("No se ingresó ningún valor.")
                break
        
        diccionario_misiones={}
        #imprimir la duracion de las misiones
        for mision in self.misiones:
            duracion = self.misiones[mision].master.winfo_children()[0].winfo_children()[1].get()
            #print(f"La duracion de la mision {mision} es de {duracion} horas")
            if not duracion.isdigit():
                messagebox.showerror("Error", "La duración de todas las misiones debe ser un valor numérico mayor a 0.")
                return
            else:
                # Continuar con el resto de tu lógica aquí
                pass
            diccionario_misiones[mision]=int(duracion)
        print(diccionario_misiones)
        
        def generar_horas_aleatorias(n, total):
            numeros=[0]
            while numeros[-1]<=0:
                numeros = []
                for i in range(n - 1):
                    numero=0
                    while numero<=0:
                        numero = round(random.uniform(1, total - sum(numeros)-(n-i)), 2)
                    numeros.append(numero)
                numeros.append(total - sum(numeros))
            return numeros

        # Número de intervalos
        def combinacion_misiones_aleatorias(num_intervalos, dic_misiones_y_duracion):
            #num_intervalos = 5
            #dic_misiones_y_duracion = {'patrulla': 20, 'combate': 2, 'viaje': 10}
            misiones=list(dic_misiones_y_duracion.keys())

            # Distribuir aleatoriamente el tiempo en los intervalos
            misiones_en_intervalos_asignados = np.random.choice(misiones, size=num_intervalos)

            # Crear un diccionario para almacenar el recuento de cada tipo de misión
            num_por_mision = {mision: 0 for mision in misiones}

            # Contar cuántas veces se asignó cada misión y actualizar el diccionario
            for mision in misiones:
                num_por_mision[mision] = np.sum(misiones_en_intervalos_asignados == mision)

            mision_y_duraciones ={mision: 0 for mision in misiones_en_intervalos_asignados}

            for mision in misiones:
                #duracion total de la mision seleccionada
                duracion = dic_misiones_y_duracion[mision]
                repeticiones=num_por_mision[mision]
                horas_por_mision = generar_horas_aleatorias(repeticiones, duracion) #lista
                mision_y_duraciones[mision] = horas_por_mision

            Lista_final_misiones=[]
            for mision in misiones_en_intervalos_asignados:
                Lista_final_misiones.append([mision,  mision_y_duraciones[mision].pop(0)])

            return(Lista_final_misiones)
        
        print(combinacion_misiones_aleatorias(numeros_intervalos ,diccionario_misiones))
        
        for mision in self.misiones:
            filas  = self.misiones[mision].get_children()
             # Iterar sobre cada fila y extraer la información
            for fila in filas:
                # Obtener los valores de la fila actual
                valores = self.misiones[mision].item(fila)['values']
                # Si hay valores en la fila
                if valores:
                    # Aquí puedes procesar los valores como desees
                    nodo = valores[0]
                    k_of_n_out = valores[1]
                    # Por ejemplo, podrías imprimir los valores
                    #print("Nodo:", nodos)
                    #print("K of n out:", k_of_n_out)
                    objeto_nodo = nodos.obtener_nodo_por_nombre(nodo)
                    objeto_nodo.set_paths_required(k_of_n_out)
                    
    def eliminar_mision(self):
        # Buscar la pestaña asociada al nombre de la misión
        nombre_mision=self.notebook.tab(self.notebook.select(), "text")
        for index in range(self.notebook.index("end")):
            tab = self.notebook.tab(index, option="text")
            if tab == nombre_mision:
                # Eliminar la pestaña y la misión del diccionario
                if nombre_mision in self.misiones:
                    self.misiones.pop(nombre_mision)
                self.notebook.forget(index)
                break

    def editar_nombre_mision(self):
    # Obtener el nuevo nombre de la misión
        nuevo_nombre = simpledialog.askstring("Editar Nombre de Misión", "Nuevo Nombre de Misión:")
        nombre_mision=self.notebook.tab(self.notebook.select(), "text")
        # Si se proporciona un nuevo nombre, actualizar el nombre de la pestaña y el diccionario de misiones
        if nuevo_nombre=="":
                messagebox.showerror("Error", "Ingrese un nombre.")
        else:
            #metodo
            if nuevo_nombre:
                if nombre_mision in self.misiones:
                    tabla_mision = self.misiones.pop(nombre_mision)
                    self.misiones[nuevo_nombre] = tabla_mision
                    self.notebook.tab(self.notebook.index(tabla_mision.master), text=nuevo_nombre)
        

    def editar_valor_kn_out(self, event):
        # Obtener el widget Treeview y la fila seleccionada
        widget = event.widget
        item_id = widget.selection()[0]
        
        #valor de la primera columna seleccionada
        nodo_seleccionado = widget.item(item_id, 'values')[0]
        numero_precursores_nodo= self.main.mpl_canvas.grafo.plot_instance.precursores_de_nodo(nodo_seleccionado)
        
        # Crear una ventana de diálogo simple para editar el valor de "K of n out"
        valor_actual = widget.item(item_id, 'values')[1]
        nuevo_valor = simpledialog.askinteger("Editar K of n out", f"Ingrese el nuevo valor para 'K of n out' para {widget.item(item_id, 'values')[0]}:", initialvalue=valor_actual)
        
        # Si se proporciona un nuevo valor, actualizar la tabla
        if nuevo_valor is not None:
            if nuevo_valor>numero_precursores_nodo:
                messagebox.showerror("Error", f"El valor de 'K of n out' no puede ser mayor a {numero_precursores_nodo}.")
            #no puede ser menor o igual a 0
            elif nuevo_valor<=0:
                messagebox.showerror("Error", f"El valor de 'K of n out' no puede ser menor o igual a 0.")
            #no puede contener letras o simbolos, solo digitos
            elif not isinstance(nuevo_valor, int):
                messagebox.showerror("Error", "El valor de 'K of n out' debe ser un número entero.")
            else:
                widget.item(item_id, values=(widget.item(item_id, 'values')[0], nuevo_valor))
        
        #si el nuevo valor es mayor a numero_precursores_nodo generar error
        
            
        
        

