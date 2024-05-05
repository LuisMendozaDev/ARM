import matplotlib.pyplot as plt
import networkx as nx
import netgraph
import netgraph._artists 
import netgraph._utils
import tkinter as tk
import keyboard
from module.RBD.componentes import Componentes
import pandas as pd
from tkinter import filedialog
from module.RBD.nodos import nodos




#CLASE PADRE DEL GRAFO    
class EditableGraph(netgraph.EditableGraph):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        
    #TODO Arreglar la grilla
    # def _draw_grid(self):
    #         eps = 1e-13
            
    #         num_lines_x=50
    #         num_lines_y=50
            
    #         self.grid_dx = self.scale[0] / (num_lines_x - 1)
    #         self.grid_dy = self.scale[1] / (num_lines_y - 1)
            
    #         for x in np.arange(self.origin[0], self.origin[0] + self.scale[0] + eps, self.grid_dx):
    #             line = self.ax.axvline(x, color='k', alpha=0.1, linestyle='--')
    #             self._grid_lines.append(line)

    #         for y in np.arange(self.origin[1], self.origin[1] + self.scale[1] + eps, self.grid_dy):
    #             line = self.ax.axhline(y, color='k', alpha=0.1, linestyle='--')
    #             self._grid_lines.append(line)
    
    # def _get_nearest_grid_coordinate(self, x, y):
    #     x = np.round((x - self.origin[0]) / self.grid_dx) * self.grid_dx + self.origin[0]
    #     y = np.round((y - self.origin[1]) / self.grid_dy) * self.grid_dy + self.origin[1]
    #     return x, y
    
        
            
    #Añadir nodo
    def _add_node(self, event):
        #Importar barra de herramientas 
        from barradeherramientas import barradeherramientas
        
        #Comprobar que este dentro de la grafica
        if event.inaxes != self.ax:
            print('Position outside of axis limits! Cannot create node.')
            return
        
        #Comprobar que el nodo no se ponga encima de otro
        if event.xdata is not None and event.ydata is not None:
                    for node, (x, y) in self.node_positions.items():
                        if abs(event.xdata - x) < 8/100 and abs(event.ydata - y) < 8/100:
                            print("No puedes poner un nodo encima de otro")
                            return

        # create node ID; use smallest unused int
        node = 0
        #print("position",self.node_positions.keys())
        
        while (node in self.node_positions.keys()):
            #print(node)
            node += 1
        nombre_node=(node)
        
        # get position of cursor place node at cursor position
        pos = self._set_position_of_newly_created_node(event.xdata, event.ydata)

        # copy attributes of last selected artist;
        # if none is selected, use boton seleccionado en barra de herraientas
        if self._selected_artists:
            node_properties = self._extract_node_properties(self._selected_artists[-1])
            
        else:
            node_properties = self._last_selected_node_properties
            if(barradeherramientas.Get_button_clicked(barradeherramientas)=='Componente'):
                node_properties['shape']='s'
                
            elif(barradeherramientas.Get_button_clicked(barradeherramientas)=='Nodo'):
                node_properties['shape']='o'
            
            elif(barradeherramientas.Get_button_clicked(barradeherramientas)=='inicio'):
                node_properties['shape']='>'
                
            elif(barradeherramientas.Get_button_clicked(barradeherramientas)=='fin'):
                node_properties['shape']='<'
        
        #Si tiene forma cuadrada es componentes, añadir a componentes
        if ( node_properties['shape']=='s'):
            self.componente = Componentes(nombre_node)
            
        if ( node_properties['shape']=='o'):
            self.nodo = nodos(nombre_node)
            

        artist = netgraph._artists.NodeArtist(xy = pos, **node_properties)
        self._reverse_node_artists[artist]= nombre_node
        self._draggable_artist_to_node[artist] = nombre_node
        self.artist_to_key[artist] = nombre_node
        self._clickable_artists.append(artist)
        self._selectable_artists.append(artist)
        self._draggable_artists.append(artist)
        self._base_linewidth[artist] = artist._lw_data
        self._base_edgecolor[artist] = artist.get_edgecolor()
        self.emphasizeable_artists.append(artist)
        self._base_alpha[artist] = artist.get_alpha()
        
        #Importante
        self.nodes.append(nombre_node)
        self.node_positions[nombre_node] = pos
        
        #importante
        self.node_artists[nombre_node] = artist
        self.ax.add_patch(artist)
        self.node_label_offset[nombre_node] = (0.0, 0.1)
    
        #self._update_node_label_offsets() 
        self.draw_node_labels({nombre_node : nombre_node}, self.node_label_fontdict)
        
        #Informacion relevante para desarrollo
        #print(self.node_label_artists[nombre_node].get_text())    
        # print("self.node_label_fontdict", self.node_label_fontdict)
        #self.node_label_artists[nombre_node].set_text('Sacala')
        # print(self.node_label_offset)
        # print(self.node_label_artists)
        # print("Arist_to_key",self.artist_to_key.values())
        # print(self.node_label_artists.keys())
        # print(plot_instance.node_artists.keys())
    
    #Eliminar nodo
    def _delete_node(self, node):
        #heredar funciones de clase padre
        if(str(self.node_artists[node].shape)=='s'):
            #Si el nodo es un componente eliminarlo de la lista
            Componentes.eliminar_componente(Componentes, node)
            
        if(str(self.node_artists[node].shape)=='o'):
            #Si el nodo es un componente eliminarlo de la lista
            nodos.eliminar_nodo(nodos, node)
            
        super()._delete_node(node)
    
    #Agregar aristas
    def _add_or_remove_nascent_edge(self, event):
        for node, artist in self.node_artists.items():
            if artist.contains(event)[0]:
                if self._nascent_edge:
                    target_edge = (self._nascent_edge.source, node)
                    reversed_edge = (node, self._nascent_edge.source)
                    same_edge = self._nascent_edge.source == node

                    if target_edge not in self.edges and reversed_edge not in self.edges and not same_edge:
                        self._add_edge(target_edge)
                        self._update_edges([target_edge])
                    else:
                        print("Edge already exists!")
                    
                    self._remove_nascent_edge()
                else:
                    self._nascent_edge = self._add_nascent_edge(node)
                break
        else:
            if self._nascent_edge:
                self._remove_nascent_edge()
                
        self.mouseover_highlight_mapping = self._get_default_mouseover_highlight_mapping()
    
               
    #Funcion para encontrar las conexiones entre los componentes
    def encontrar_caminos(self):
        #Hacer una lista de todos los nodos y sus shapes
        lista_nodos = self.nodes.copy()
        #Nodos cambiados es una lista que guarda el nombre de los nodos que ingresa el usuario
        #Porque para el grafo no tienen ese nombre
        lista_nodos_cambiados=[]
        #Shape es la forma del nodos
        lista_shapes = []
         
        #Cambiar los nombres de los nodos por los que ingreso el usuario
        for nodo in lista_nodos:
            lista_shapes.append(str(self.node_artists[nodo].shape))
            indice=lista_nodos.index(nodo)
            if(lista_nodos[indice]!=self.node_label_artists[nodo].get_text()):
                lista_nodos_cambiados.append((lista_nodos[indice], self.node_label_artists[nodo].get_text()))
                lista_nodos[indice]=self.node_label_artists[nodo].get_text()
                
        
        #print(lista_nodos_cambiados)
        
            
        #lista de nodos y sus shapes
        lista_nodos_shapes = list(zip(lista_nodos, lista_shapes))
        
        #los nodos que tengan un shape 'o' son nodos para el usuario
        nodos=[]
        for nodo, shape in lista_nodos_shapes:
            if shape == 'o':
                nodos.append(nodo)
                
        #print(lista_shapes)
        #print("nodos: ",nodos)
        #print("componentes",componentes)
        
        #Cambiar los nombres de los nodos conectados por aristas en las aristas
        lista_edges = self.edges.copy()                
        if lista_nodos_cambiados:
            for cambio in lista_nodos_cambiados:
                for i, tupla in enumerate(lista_edges):
                    if cambio[0] in tupla:
                        lista_edges[i] = (cambio[1] if tupla[0] == cambio[0] else tupla[0], cambio[1] if tupla[1] == cambio[0] else tupla[1])
        #print(lista_edges)
        
        
        #print("edges",edges)
        # Crear un grafo dirigido
        Analisis = nx.DiGraph()
        # Agregar nodos
        Analisis.add_nodes_from(nodos)
        # Agregar aristas
        Analisis.add_edges_from(lista_edges)
        
        # Determinar si hay un ciclo en Analisis
        ciclos = list(nx.simple_cycles(Analisis))
        if ciclos:
            print("El grafo contiene ciclos:", ciclos)
        else:
            print("El grafo no contiene ciclos")
            # Encontrar el orden topológico
            orden_topologico = list(nx.topological_sort(Analisis))
            
            #print(orden_topologico[1])
            #print(orden_topologico[-2])
            
            # Filtrar caminos que contienen algún nodo presente en la lista nodos
            caminos_totales = list(nx.all_simple_paths(Analisis, source=orden_topologico[1], target=orden_topologico[-2]))

            # Lista de nodos a eliminar
            nodos_a_eliminar = set(nodos)  # Convertir a un conjunto para una búsqueda más eficiente
            # Eliminar los nodos de cada camino
            caminos_actualizados = [[nodo for nodo in camino if nodo not in nodos_a_eliminar] for camino in caminos_totales]
            #print(caminos_actualizados)
            
            nodos_ordenados=[[nodo for nodo in camino if nodo in nodos] for camino in caminos_totales]
        
            #nodos_ordenados = [nodo for nodo in orden_topologico if nodo in nodos]
                
            return(Analisis, nodos_ordenados, nodos)
        
    def precursores_de_nodo(self, nodo_buscado):
        lista_nodos = self.nodes.copy()
        lista_edges=self.edges.copy()
        
        G = nx.DiGraph()
        G.add_nodes_from(lista_nodos)
        G.add_edges_from(lista_edges)
        predecessors=len(list(G.predecessors(nodo_buscado)))
        #print(predecessors)
        return(predecessors)
        
        
    def organizar(self):
        lista_nodos=self.nodes.copy()
        lista_edges=self.edges.copy()    
        
        GA = nx.DiGraph()
        # Agregar nodos
        GA.add_nodes_from(lista_nodos)
        # Agregar aristas
        GA.add_edges_from(lista_edges)
        
        #print(list(nx.topological_generations(GA)))
       
        for layer, nodes in enumerate(nx.topological_generations(GA)):
            # `multipartite_layout` expects the layer as a node attribute, so add the
            # numeric layer value as a node attribute
            for node in nodes:
                GA.nodes[node]["layer"] = layer
            
        # Compute the multipartite_layout using the "layer" node attribute
        pos = nx.multipartite_layout(GA, subset_key="layer", scale=2, center=[0,0])
       
        self.node_layout=pos
        
        for node in lista_nodos:
            self.node_positions[node] = pos[node]
        
        self._update_node_artists(lista_nodos)
        if hasattr(self, 'node_label_artists'):
            self._update_node_label_positions()

        edges = self._get_stale_edges(lista_nodos)
        # In the interest of speed, we only compute the straight edge paths here.
        # We will re-compute other edge layouts only on mouse button release,
        # i.e. when the dragging motion has stopped.
        edge_paths = dict()
        edge_paths.update(self._update_straight_edge_paths([(source, target) for (source, target) in edges if source != target]))
        edge_paths.update(self._update_selfloop_paths([(source, target) for (source, target) in edges if source == target]))
        self.edge_paths.update(edge_paths)
        self._update_edge_artists(edge_paths)

        if hasattr(self, 'edge_label_artists'):
            self._update_edge_label_positions(lista_edges)
        self.fig.canvas.draw_idle()
    
    def eliminar_todos_los_nodos(self):
        nodes = [self._reverse_node_artists[artist] for artist in  self._clickable_artists if isinstance(artist, netgraph._artists.NodeArtist)]
        # delete edges to and from selected nodes
        edges = [(source, target) for (source, target) in self.edges if ((source in nodes) or (target in nodes))]
        for edge in edges:
            self._delete_edge(edge)
        # delete nodes
        for node in nodes:
            self._delete_node(node)
        self.fig.canvas.draw_idle()
        
    def guardar_en_archivo(self):
        #Hacer una lista de todos los nodos y sus shapes
        lista_nodos = self.nodes.copy()
        #Nodos cambiados es una lista que guarda el nombre de los nodos que ingresa el usuario
        #Porque para el grafo no tienen ese nombre
        lista_nodos_cambiados=[]
        #Shape es la forma del nodos
        
        diccionario_nodos_guardar={}
         
        #Cambiar los nombres de los nodos por los que ingreso el usuario
        for nodo in lista_nodos:
            shape=(str(self.node_artists[nodo].shape))
            
            if shape == 'o':
                tipo = 'nodo'   
            elif shape == 's':
                tipo = 'componente'
            elif shape == '<':
                tipo = 'fin'
            elif shape == '>':
               tipo = 'inicio'
            
            indice=lista_nodos.index(nodo)
            if(lista_nodos[indice]!=self.node_label_artists[nodo].get_text()):
                lista_nodos_cambiados.append((lista_nodos[indice], self.node_label_artists[nodo].get_text()))
                lista_nodos[indice]=self.node_label_artists[nodo].get_text()
                
            if tipo=='componente':
                atributos = Componentes.diccionario_atributos(str(self.node_label_artists[nodo].get_text()))
                mtbf=float(atributos['mtbf'])
                mttr=float(atributos['mttr'])
                tiempo_de_uso=float(atributos['tiempo_de_uso'])
                reparable=bool(atributos['reparable'])
                knout="No aplica"
            
            elif tipo=='nodo':
                atributos_nodo=nodos.diccionario_atributos(str(self.node_label_artists[nodo].get_text()))
                mtbf="No aplica"
                mttr="No aplica"
                tiempo_de_uso="No aplica"
                reparable="No aplica"
                knout=int(atributos_nodo['knout'])
            else:
                mtbf="No aplica"
                mttr="No aplica"
                tiempo_de_uso="No aplica"
                reparable="No aplica"
                knout="No aplica"
                
                
            diccionario_nodos_guardar[self.node_label_artists[nodo].get_text()]={
                'tipo': tipo,
                'mtbf': mtbf,
                'mttr': mttr,
                'tiempo_de_uso': tiempo_de_uso,
                'reparable': reparable,
                'knout':knout,
                'posicion': self.node_positions[nodo]
                
            }
    
        lista_edges = self.edges.copy()                
        if lista_nodos_cambiados:
            for cambio in lista_nodos_cambiados:
                for i, tupla in enumerate(lista_edges):
                    if cambio[0] in tupla:
                        lista_edges[i] = (cambio[1] if tupla[0] == cambio[0] else tupla[0], cambio[1] if tupla[1] == cambio[0] else tupla[1])
        #print(lista_edges)
        
        
        print(diccionario_nodos_guardar)
        
        G = nx.DiGraph()
        for node, node_data in diccionario_nodos_guardar.items():
            G.add_node(node, **node_data)
        G.add_edges_from(lista_edges)
        # Abrir el cuadro de diálogo para seleccionar la ubicación y el nombre del archivo
        nombre_archivo = filedialog.asksaveasfilename(defaultextension=".xlsx", filetypes=(("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")))

        
        if nombre_archivo:
            # Crear un DataFrame para los nodos y sus atributos
            node_data = []
            for node, attr in G.nodes(data=True):
                node_attr = {'Nodo': node}
                node_attr.update(attr)
                node_data.append(node_attr)

            node_df = pd.DataFrame(node_data)

            # Crear un DataFrame para las aristas
            edge_df = pd.DataFrame(list(G.edges()), columns=['Nodo1', 'Nodo2'])

            # Guardar los DataFrames en un archivo Excel en la ubicación elegida por el usuario
            with pd.ExcelWriter(nombre_archivo) as writer:
                node_df.to_excel(writer, sheet_name='Nodos', index=False)
                edge_df.to_excel(writer, sheet_name='Aristas', index=False)

            print(f"El grafo con atributos se ha guardado en: {nombre_archivo}")
        else:
            print("No se ha seleccionado ninguna ubicación o nombre de archivo.")
        
        
    
    
        
                
class Grafo:    
    def __init__(self,root, app, G, inicio):
        
        self.app=app
        self.root=root  
        self.G=G
        
        self.fig, self.ax = plt.subplots(figsize=(5, 5))
        # Deshabilitar atajos de teclado predeterminados
        for key in ('keymap.fullscreen', 'keymap.home', 'keymap.back',
                    'keymap.forward', 'keymap.pan', 'keymap.zoom', 'keymap.save',
                    'keymap.quit', 'keymap.grid', 'keymap.yscale', 'keymap.xscale'):
            plt.rcParams[key] = ''

        
        self.fig.subplots_adjust(left=0, right=1, bottom=0, top=1)
        self.ax.set_aspect('auto', adjustable='datalim', anchor='C')
        
        self.create_context_menu()
        self.create_context_menu2()
        
        # Dibujar el grafo
        node_color= 'tab:blue'
        edge_color= 'tab:gray'
        
        # Crear un diccionario y guardar el nombre del nodo y su forma
        self.nodes_shapes = {}
        for node, shape in self.G.nodes(data='tipo'):
            if shape == 'nodo':
                knout_value=G.nodes[node].get('knout')
                self.nodes_shapes[node] = 'o'
                self.nodos=nodos(node, paths_required=knout_value if knout_value is not None else 1)
                  
            elif shape == 'componente':
                self.nodes_shapes[node] = 's'
                if(inicio):
                    self.componentes = Componentes(node)
                else:
                    # Obtener los valores del diccionario
                    mtbf_value = G.nodes[node].get('mtbf')
                    tiempo_de_uso_value = G.nodes[node].get('tiempo_de_uso')
                    mttr_value = G.nodes[node].get('mttr')
                    reparable= bool(G.nodes[node].get('reparable'))
                    self.componentes = Componentes(node,
                                mtbf=mtbf_value if mtbf_value is not None else 0,
                                tiempo_de_uso=tiempo_de_uso_value if tiempo_de_uso_value is not None else 0,
                                mttr=mttr_value if mttr_value is not None else 0,
                                reparable= reparable if reparable is not None else False
                            )
                            
            elif shape == 'fin':
                self.nodes_shapes[node] = '<'
            elif shape == 'inicio':
                self.nodes_shapes[node] = '>'
                
        if (inicio):
            # Definir posiciones
            for layer, nodes in enumerate(nx.topological_generations(self.G)):
                # `multipartite_layout` expects the layer as a node attribute, so add the
                # numeric layer value as a node attribute
                for node in nodes:
                    self.G.nodes[node]["layer"] = layer

            # Compute the multipartite_layout using the "layer" node attribute
            self.pos = nx.multipartite_layout(self.G, subset_key="layer")
            #print(self.pos)
        else:
            self.pos={}
            for node, position in G.nodes(data='posicion'):
               # Eliminar los corchetes del string
               # Elimina los corchetes exteriores y divide los elementos por espacios
                numeros = position.strip('[]').split(', ')

                # Elimina los paréntesis de los elementos que son tuplas y divide los elementos por espacios
                numeros = [elemento.strip('()').split() if '(' or ')' in elemento else elemento for elemento in numeros]

                # Divide los elementos por espacios si hay alguno dentro de una tupla
                numeros = [subelemento.split() if isinstance(subelemento, str) and ' ' in subelemento else subelemento for subelemento in numeros]

                # Aplanar la lista si hay listas anidadas
                numeros = [item for sublist in numeros for item in (sublist if isinstance(sublist, list) else [sublist])]

                # Convertir los números de string a punto flotante
                num1 = float(numeros[0])
                num2 = float(numeros[1])
                self.pos[node] = [num1, num2]
            #print(self.pos)
        
        
        self.node_size=7
        self.plot_instance = EditableGraph(
            self.G, node_size=self.node_size, node_color=node_color, node_shape=self.nodes_shapes,
            node_labels=True, node_label_fontdict=dict(size=5),
            edge_color=edge_color, edge_width=1, arrows=True, ax=self.ax,  node_label_offset=(0.0, 0.12), node_layout=self.pos
        )
        #node_layout=self.node_positions
        
    # Obtener las coordenadas del evento
    def on_scroll(self, event):
        # Verificar si el evento fue un gesto de scroll en el trackpad
        if event.button == 'up':
            factor = 1.1  # Factor de aumento para hacer zoom
        elif event.button == 'down':
            factor = 0.9  # Factor de reducción para hacer zoom
        else:
            return

        # Obtener las coordenadas del evento
        x = event.xdata
        y = event.ydata
        
        if x is None or y is None:
            return

        # Calcular los nuevos límites de los ejes
        new_xlim = [x - (x - plt.xlim()[0]) / factor, x + (plt.xlim()[1] - x) / factor]
        new_ylim = [y - (y - plt.ylim()[0]) / factor, y + (plt.ylim()[1] - y) / factor]
        
        self.fig.gca().set_xlim(new_xlim)
        self.fig.gca().set_ylim(new_ylim)
        self.fig.canvas.draw_idle()
        
    def _delete_node_safe(self):
        #eliminar nodo con boton
       keyboard.press_and_release('delete')
        
    def create_context_menu(self):
        #Menu cuando se hace click en un componente
        self.context_menu = tk.Menu(self.root, tearoff=0)  
        self.context_menu.add_command(label="Eliminar", command=self._delete_node_safe)
        #self.context_menu.add_command()    
            
    def show_context_menu(self, node, shape):
        x_root = self.root.winfo_pointerx()
        y_root = self.root.winfo_pointery()
        self.node_in_menu = node
       
        if shape == 's':
                # Insertar el comando "Editar componente" solo si la forma no es 'o'
                editar_componente_exist=False
                for i in range(0,3):
                    if self.context_menu.entryconfigure(i)['label'].__contains__('Editar Nodo') and self.context_menu.entryconfigure(i)['label']!=None:
                        self.context_menu.delete(i)
                        
                    if self.context_menu.entryconfigure(i)['label'].__contains__('Editar componente') and self.context_menu.entryconfigure(i)['label']!=None:
                        editar_componente_exist=True
                        
                if not editar_componente_exist:
                    editar_comando = lambda: self.app.ventana_registro_instance.show_componente_window(self.node_in_menu)
                    self.context_menu.add_command(label="Editar componente", command=editar_comando)
                    
                
        elif (shape=='o'):
                editar_nodo_exist=False
                for i in range(0,3):
                    if self.context_menu.entryconfigure(i)['label'].__contains__('Editar componente') and self.context_menu.entryconfigure(i)['label']!=None:
                        self.context_menu.delete(i)
                        
                    elif self.context_menu.entryconfigure(i)['label'].__contains__('Editar Nodo') and self.context_menu.entryconfigure(i)['label']!=None:
                        editar_nodo_exist=True
        
                if not editar_nodo_exist:
                    editar_comando = lambda: self.app.ventana_nodos_instance.show_nodo_window(self.node_in_menu)
                    self.context_menu.add_command(label="Editar Nodo", command=editar_comando)
            
        else:
        # Eliminar el comando "Editar componente" si la forma es 'o'
            for i in range(0,3):
                    if self.context_menu.entryconfigure(i)['label'].__contains__('Editar componente') and self.context_menu.entryconfigure(i)['label']!=None:
                        self.context_menu.delete(i)
                        
                    elif self.context_menu.entryconfigure(i)['label'].__contains__('Editar Nodo') and self.context_menu.entryconfigure(i)['label']!=None:
                        self.context_menu.delete(i)
            # for item in self.context_menu.winfo_children():
            #     print(item['label'])
            #     if item['label'] == "Editar componente":
            #         self.context_menu.deletecommand("Editar componente")
            #         break
                    
                    
            
            
        self.context_menu.post(x_root, y_root)   
            
    def create_context_menu2(self):
        self.context_menu2 = tk.Menu(self.root, tearoff=0)  
        self.context_menu2.add_command(label="Agregar Componente", command=lambda: self.plot_instance._add_node(self.evento_grafico))
        
        #self.context_menu2.add_command(label="Agregar Evento", command=lambda: self.elegir_opcion("Agregar Evento")) 
        #self.context_menu2.add_command(label="Simular", command=lambda: self.elegir_opcion("Simular")) 
        
        
    def show_context_menu2(self,event):
        #Mostrar menu           
        x_root = self.root.winfo_pointerx()
        y_root = self.root.winfo_pointery()
        self.context_menu2.post(x_root, y_root)
        self.evento_grafico=event 
    
    def onclick(self, event):
    # print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
    #       ('double' if event.dblclick else 'single', event.button,
    #        event.x, event.y, event.xdata, event.ydata))
    
        if event.xdata is not None and event.ydata is not None:
            for node, (x, y) in self.plot_instance.node_positions.items():
                if abs(event.xdata - x) < self.node_size/100 and abs(event.ydata - y) < self.node_size/100:
                    if event.button == 1:  # Clic izquierdo
                        #print(f'Nodo clickeado con botón izquierdo: {node}')
                        break
                    elif event.button == 3:  # Clic derecho
                        #print(f'Nodo clickeado con botón derecho: {node}')
                        #print(self.plot_instance._extract_artist_properties(self.plot_instance._reverse_node_artists[node]))
                        shape=(self.plot_instance._extract_node_properties(self.plot_instance.node_artists[node])['shape'])
                        self.show_context_menu(node, shape)
                        self.fig.canvas.draw_idle()
                        break 
                             
            else:
                if event.button == 1:
                    #añadir nodo
                    
                    pass
                    
                    
                elif event.button == 3:
                    # coordenadas del evento
                    # print("Coordenadas del evento", event.xdata, event.ydata)
                    # self.plot_instance._add_node(event)
                    # self.main_app.show_context_menu2()
                    self.show_context_menu2(event)
                    self.fig.canvas.draw_idle()
                         
    def mostrar_grafo(self):
         # Conectar los eventos
        self.cid_scroll = self.fig.canvas.mpl_connect('scroll_event', self.on_scroll)
        self.cid_click = self.fig.canvas.mpl_connect('button_press_event', self.onclick)
        self.cid_key = self.fig.canvas.mpl_connect('key_press_event', self.plot_instance._on_key_toggle)
        self.ax.set_xlim(-1, 1)
        self.ax.set_ylim(-1, 1)
        return(self.fig)
        #plt.show()    
   

    def __del__(self):
        #Eliminar figura
        plt.close(self.fig)



if __name__ == "__main__":
    print("Ejecuta main")
