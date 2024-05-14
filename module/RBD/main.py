from module.RBD.grafo import Grafo
import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from matplotlib.figure import Figure
from module.RBD.ventana_registro_componentes import ventana_registro_componentes
from module.RBD.componentes import Componentes
from module.RBD.ventana_calculos import vetana_calculos
from module.RBD.barradeherramientas import barradeherramientas
from module.RBD.ventana_resultados import vetana_resultados
import networkx as nx
import pandas as pd
from tkinter import filedialog
from module.RBD.ventana_nodos import ventana_nodos
from module.RBD.nodos import nodos
from module.RBD.Ventanamisiones import VentanaMisiones

# Autores:
# Angel De Jesus Tuñon Cuello
# Luis Fernando Mendoza Cardona
# Jose De Jesus Caro Urueta

# Python 3.9.13 64-bits
# Librerias utilizadas: tkinter, matplotlib, networkx, netgraph, pandas, keyboard, numpy.

# TODO: Cambiar el color de los nodos cuando la confiabilidad es baja
# TODO: Poner limites al zoom
# TODO: Arreglar Grilla
# TODO: Calculos de disponibilidad
# TODO: Calculos de mantenibilidad
# TODO: Arreglar Organizar en sistemas complejos
# TODO: Agregar objeto barra de herramientas a grafo
# TODO: Ventana nodos para los K-out, cambiar el nombre, y un comentario.

# URGENTES
# BUG


# Canvas del matplotlib que contiene al grafo
class MplCanvas(FigureCanvasTkAgg):
    def __init__(self, root, tapp, width=5, height=5):
        self.root = root
        self.width = width
        self.height = height
        self.tapp = tapp
        self.fig = Figure(figsize=(width, height))
        super().__init__(self.fig, master=self.root)

        # Crear widget que contiene al grafo
        G = nx.DiGraph()
        G.add_node('inicio', tipo='inicio')
        G.add_node('Fin', tipo='fin')
        G.add_node('Nodo1', tipo='nodo')
        G.add_node('Nodo2', tipo='nodo')
        G.add_node('R1', tipo='componente')

        G.add_edges_from([
            ('inicio', 'Nodo1'),
            ('Nodo1', 'R1'),
            ('R1', 'Nodo2'),
            ('Nodo2', 'Fin')
        ])

        self.grafo = Grafo(self.root, tapp, G, inicio=True)
        self.canvas = FigureCanvasTkAgg(
            self.grafo.mostrar_grafo(), master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side='top', expand=True, fill=tk.BOTH)

        # Agrega la barra de herramientas personalizada
        self.toolbar = CustomToolbar(self.canvas, self.root)
        self.toolbar.update()
        self.toolbar.pack(side='bottom', fill=tk.X)

    def eliminar_y_aniadir_nuevo_grafo(self, G):
        self.canvas_widget.destroy()
        self.toolbar.destroy()

        self.fig = Figure(figsize=(self.width, self.height))
        super().__init__(self.fig, master=self.root)

        # Crear widget que contiene al grafo
        self.grafo = Grafo(self.root, self.tapp, G, inicio=False)
        self.canvas = FigureCanvasTkAgg(
            self.grafo.mostrar_grafo(), master=self.root)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(side='top', expand=True, fill=tk.BOTH)

        # Agrega la barra de herramientas personalizada
        self.toolbar = CustomToolbar(self.canvas, self.root)
        self.toolbar.update()
        self.toolbar.pack(side='bottom', fill=tk.X)


class CustomToolbar(NavigationToolbar2Tk):
    # Seleccion de botones para matplotlib
    toolitems = [t for t in NavigationToolbar2Tk.toolitems if t[0]
                 in ('Home', 'Pan', 'Zoom', 'Save')]

    def home(self, *args, **kwargs):
        # Aquí puedes personalizar la acción de 'Home'
        super().home(*args, **kwargs)
        ax = self.canvas.figure.gca()
        ax.set_xlim(-1, 1)
        ax.set_ylim(-1, 1)
        self.canvas.draw_idle()

    # Eliminar las coordenadas en la pantalla
    def set_message(self, message):
        pass


class TkApp:
    def __init__(self):
        self.menu2_opcion = ""

        # iniciar ventana
        self.root = tk.Tk()
        self.root.title("TritonOps")
        self.root.state('zoomed')
        self.root.maxsize(self.root.winfo_screenwidth(),
                          self.root.winfo_screenheight())
        self.root.minsize(self.root.winfo_screenwidth(),
                          self.root.winfo_screenheight())

        # DECLARAR VARIABLE PARA MOSTRAR BARRA DE ESTADO:
        self.estado = tk.IntVar()
        self.estado.set(1)  # Mostrar Barra de Estado

        # DEFINIR BARRA DE MENÚ DE LA APLICACION:
        barramenu = tk.Menu(self.root)
        self.root['menu'] = barramenu

        # DEFINIR SUBMENÚS 'Sesiones', 'Opciones' y 'Ayuda':
        menu1 = tk.Menu(barramenu, tearoff=0)
        barramenu.add_cascade(menu=menu1, label='Archivo')
        menu1.add_command(label='Guardar', command=self.guardar)
        menu1.add_command(label='Abrir archivo', command=self.abrir_archivo)

        menu2 = tk.Menu(barramenu, tearoff=0)

        barramenu.add_cascade(menu=menu2, label='Opciones')
        # menu2.add_command(label='Encontrar caminos', command=self.encontrar_caminos)
        # menu2.add_command(label='Imprimir atributos', command=self.imprimir_atributos)
        # menu2.add_command(label='Imprimir Boton', command=self.imprimir_boton)
        menu2.add_command(label='Calcular', command=self.calcular)
        menu2.add_command(label='Simulacion misiones', command=self.simularmisiones)
        menu2.add_command(label='Organizar', command=self.organizar)
        menu2.add_command(label='Borrar todo', command=self.borrar_todo)

        menu3 = tk.Menu(barramenu, tearoff=0)
        barramenu.add_cascade(menu=menu3, label='Ayuda')

        # Conectar la ventana principal con el grafo con los otros objetos que necesiten acceder a el
        barradeherramientas.create_toolbar(barradeherramientas, self.root)
        #self.ventana_resultados = vetana_resultados(self.root, Componentes)
        
        self.mpl_canvas = MplCanvas(self.root, self)
        self.ventana_registro_instance = ventana_registro_componentes(
            self, self.root)
        self.ventana_nodos_instance = ventana_nodos(self, self.root)
        self.ventana_calculos_intance = vetana_calculos(self, self.root)
        Componentes.guardarAPP(Componentes, self)
        nodos.guardarAPP(nodos, self)

    def encontrar_caminos(self):
        # Encontrar caminos
        print(self.mpl_canvas.grafo.plot_instance.encontrar_caminos())

    def imprimir_atributos(self):
        # imprimir los atributos de todos los componentes
        # util para comprobar que se este guardando al informacion de los componentes
        Componentes.imprimir_atributos()

    def imprimir_boton(self):
        # Para saber que boton esta presionado en la barra de herramientas // (solo mientras se desarrolla la app)
        barradeherramientas.Get_button_clicked(barradeherramientas)

    def calcular(self):
        # Abrir ventana de calculos
        self.ventana_calculos_intance.show_ventana_calculos()
    
    def simularmisiones(self):
        ventana_misiones = tk.Toplevel(self.root)  # Crea una nueva ventana
        app_misiones = VentanaMisiones(ventana_misiones, self)  # Crea una instancia de VentanaMisiones dentro de la nueva ventana
        
        

    def run(self):
        # Iniciar ventana
        self.root.mainloop()

    def organizar(self):
        # Organizar el grafo
        self.mpl_canvas.grafo.plot_instance.organizar()

    def borrar_todo(self):
        self.mpl_canvas.grafo.plot_instance.eliminar_todos_los_nodos()

    def abrir_archivo(self):

        # Abrir el cuadro de diálogo para seleccionar el archivo
        archivo_excel = filedialog.askopenfilename(title="Selecciona un archivo Excel", filetypes=(
            ("Archivos de Excel", "*.xlsx"), ("Todos los archivos", "*.*")))

        if archivo_excel:
            try:
                # Code inside the try block
                nodos_df = pd.read_excel(archivo_excel, sheet_name='Nodos')
                aristas_df = pd.read_excel(archivo_excel, sheet_name='Aristas')

                # Crear un grafo vacío
                G = nx.DiGraph()

                # Agregar nodos con atributos al grafo
                for _, row in nodos_df.iterrows():
                    nodo = row['Nodo']
                    atributos = {key: row[key]
                                 for key in row.index if key != 'Nodo'}
                    G.add_node(nodo, **atributos)

                # Agregar aristas al grafo
                for _, row in aristas_df.iterrows():
                    G.add_edge(row['Nodo1'], row['Nodo2'])

                # Verificar el grafo cargado con atributos
                # print("Nodos del grafo:", G.nodes(data=False))
                # print("Aristas del grafo:", G.edges())

            except Exception as e:
                print(e)
                return
                # Handle the exception
                # Leer el archivo Excel

            Componentes.vaciar_lista_componentes()
            self.mpl_canvas.eliminar_y_aniadir_nuevo_grafo(G)

        else:
            print("No se ha seleccionado ningún archivo.")

    def guardar(self):
        self.mpl_canvas.grafo.plot_instance.guardar_en_archivo()
    
    def cerrar_ventana(self):
        self.root.destroy()


if __name__ == "__main__":
    app = TkApp()
    app.run()
