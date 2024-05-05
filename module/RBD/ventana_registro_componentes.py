import tkinter as tk
from module.RBD.componentes import Componentes
from tkinter import scrolledtext, ttk

class frame_distribucion_exponencial(tk.Frame):
    def __init__(self, master, controller):
        # Cambia color_principal al color que desees
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        self.label_mtbf = tk.Label(self, text="MTBF: ")
        self.label_mtbf.grid(row=0, column=0, pady=10)
        
        self.entry_mtbf = tk.Entry(self)
        self.entry_mtbf.grid(row=0, column=1 , sticky=tk.W, pady=10)
        
        self.label_mttr = tk.Label(self, text="MTTR: ")
        self.label_mttr.grid(row=1, column=0, pady=10)
        
        self.entry_mttr = tk.Entry(self)
        self.entry_mttr.grid(row=1, column=1 , sticky=tk.W, pady=10)

        self.label_tiempo_de_uso = tk.Label(self, text="Tiempo de uso:")
        self.label_tiempo_de_uso.grid(row=2, column=0, pady=10)
        
        self.entry_tiempo_de_uso = tk.Entry(self)
        self.entry_tiempo_de_uso.grid(row=2, column=1 , sticky=tk.W, pady=10)
        
class Vista_general(tk.Frame):
    def __init__(self, master, controller, tk_app_instance, node_in_menu):
        # Cambia color_principal al color que desees
        tk.Frame.__init__(self, master)
        self.controller = controller
        self.tk_app_instance=tk_app_instance
        self.frame_distribucion_exponencial=frame_distribucion_exponencial
     
        self.basic_info_frame=tk.LabelFrame(self, text="Informacion basica")
        self.basic_info_frame.grid(row= 0, column=0, padx=20, pady=10)

        self.label_nombre = tk.Label(self.basic_info_frame, text="Nombre:")
        self.label_nombre.grid(row=0, column=0)

        self.entry_nombre = tk.Entry(self.basic_info_frame)
        self.entry_nombre.grid(row=0, column=1, ipadx=20)

        self.texto_scroll = scrolledtext.ScrolledText(self.basic_info_frame, wrap=tk.WORD, width=20, height=5)
        self.texto_scroll.grid(row=0, column=2, padx=(80, 20), pady=(10,20))


        self.falla_info_frame=tk.LabelFrame(self, text="Informacion de falla")
        self.falla_info_frame.grid(row=1, column=0, padx=20, pady=10, ipadx=50) 

        self.label_distribucion=tk.Label(self.falla_info_frame, text="Distribucion:")
        #self.label_distribucion.grid(row=0, column=0, pady=10, padx=0, sticky=tk.W)
        self.label_distribucion.grid(row=0, column=0, pady=10,padx=0, sticky=tk.W)


        self.distribuciones = ["Exponencial", "Weibull", "Logaritmica", "Normal"]
        self.distribucion_combobox = ttk.Combobox(self.falla_info_frame, state="readonly", values=self.distribuciones, exportselection=0)
        #self.distribucion_combobox.grid(row=0, column=1, pady=10, sticky=tk.W, padx=0)
        self.distribucion_combobox.grid(row=1, column=0, padx=10, pady=10)
        
        #Checkbox si es reparable
        self.reparable = tk.IntVar()
        self.check_reparable = tk.Checkbutton(self.falla_info_frame, text="Reparable", variable=self.reparable)
        self.check_reparable.grid(row=1, column=1, padx=0, pady=10, sticky=tk.W)
        
        
        self.distribucion_combobox.current(0)
        self.distribucion_combobox.bind("<<ComboboxSelected>>", self.mostrar_vista)

        self.cuadro_vistas = tk.Frame(self.falla_info_frame)
        self.cuadro_vistas.grid(row=2, column=0)

        self.vistas = {}
        self.vistas["Exponencial"] = frame_distribucion_exponencial(self.cuadro_vistas, self)

        self.mostrar_vista("Exponencial")
            
        #Nodo donde se desplego el menu
        self.node_in_menu=node_in_menu

        #Obtener el nombre que le asigno el usuario
        self.entry_nombre.insert(0, self.tk_app_instance.mpl_canvas.grafo.plot_instance.node_label_artists[self.node_in_menu].get_text())

        #Obtener el objeto componente
        self.Componente_encontrado = Componentes.obtener_componente_por_nombre(nombre_buscado=self.tk_app_instance.mpl_canvas.grafo.plot_instance.node_label_artists[self.node_in_menu].get_text())

        #Si encontro el objeto, llenar las casillas de ingreso de texto con su informacion
        if(self.Componente_encontrado!=None):
            self.vistas["Exponencial"].entry_mtbf.insert(0, self.Componente_encontrado.get_mtbf())
            self.vistas["Exponencial"].entry_mttr.insert(0, self.Componente_encontrado.get_mttr())
            self.vistas["Exponencial"].entry_tiempo_de_uso.insert(0,self.Componente_encontrado.get_tiempo_de_uso())
            self.texto_scroll.insert(tk.END, self.Componente_encontrado.get_descripcion())
            
            if(self.Componente_encontrado.get_reparable()):
                self.reparable.set(1)
            else:
                self.reparable.set(0)
                
               
    def mostrar_vista(self, event):
        
        seleccion = self.distribucion_combobox.get()
            
        # Ocultar vistas anteriores
        for vista_actual in self.vistas.values():
            vista_actual.pack_forget()
            
        if seleccion in self.vistas:
            vista_seleccionada = self.vistas[seleccion]
            # Mostrar el frame correspondiente
            vista_seleccionada.pack()
        else:
            # Manejo si el elemento seleccionado no está en las vistas disponibles
            print("El elemento seleccionado no tiene un frame asociado.")





class ventana_registro_componentes():
    def __init__(self, tk_app_instance, root):
        self.tk_app_instance = tk_app_instance
        self.root=root
        # Crear un nuevo Frame en la raíz para los botones y las vistas
        self.vista_general=Vista_general
        
    
    def show_componente_window(self, node_in_menu):
      
        #Nodo donde se desplego el menu
        self.node_in_menu=node_in_menu
        self.boton_actual = None  # Almacena el botón de la vista actual
        #Obtener el objeto componente
        self.Componente_encontrado = Componentes.obtener_componente_por_nombre(nombre_buscado=self.tk_app_instance.mpl_canvas.grafo.plot_instance.node_label_artists[self.node_in_menu].get_text())
        
        #Crear ventana
        self.ventana = tk.Toplevel(self.root)
        self.ventana.attributes('-toolwindow', True)
        self.ventana.attributes('-topmost', True)
        self.ventana.focus_force()
        self.ventana.grab_set()
        self.ventana.title("Ingreso de datos para componente")
        
        self.frame_contenedor = tk.Frame(self.ventana)
        self.frame_contenedor.pack(pady=10, padx=10)

         # Crear un nuevo Frame para los botones
        self.frame_botones = tk.Frame(self.frame_contenedor)
        self.frame_botones.pack(side=tk.TOP, anchor=tk.NW)
        
        self.button_Vista_general = tk.Button(self.frame_botones, text="General", command=lambda: self.mostrar_vista(self.vista_general), bd=3, relief="raised")
        self.button_Vista_general.pack(side=tk.LEFT, padx=0)
        
        #self.button_Vista_standby = tk.Button(self.frame_botones, text="Standby", command=lambda: self.mostrar_vista(self.vista_standby), bd=3, relief="raised")
        #self.button_Vista_standby.pack(side=tk.LEFT, padx=0)

        # Para agregar otro botones es simplemente crear la instanica y añadirlos al self.frame_botones

        # Frame que contiene las vistas
        self.cuadro_vistas = tk.Frame(
            self.frame_contenedor, width=560, height=400, bd=3, relief="raised")

        self.cuadro_vistas.pack_propagate(False)
        self.cuadro_vistas.pack()
        
        self.vistas = {}
        self.vistas[self.vista_general] = self.vista_general(self.cuadro_vistas, self, self.tk_app_instance, self.node_in_menu)
        
        self.boton_editar_Componente = tk.Button(self.ventana, text="Editar Componente", command=self.editar_Componente)
        self.boton_editar_Componente.pack(side=tk.BOTTOM, pady=20)

        self.mostrar_vista(self.vista_general)
        
       
    
    #Cerrar ventana
    def cerrar_ventana_Componentes(self):
        self.ventana.destroy()
        #Actualizar grafo por si hubo algun cambio
        self.tk_app_instance.mpl_canvas.grafo.plot_instance.fig.canvas.draw_idle()
        
    def mostrar_vista(self, vista):
        # Ocultar vistas anteriores
        for vista_actual in self.vistas.values():
            vista_actual.pack_forget()

        # Mostrar la nueva vista en el cuadro
        self.vistas[vista].pack()

        # Resaltar el botón de la vista actual
        if self.boton_actual:
            self.boton_actual.config(relief=tk.SUNKEN)

        for boton, vista_clase in zip([self.button_Vista_general], [self.vista_general]):
            if vista_clase == vista:
                boton.config(relief=tk.SUNKEN)
                self.boton_actual = boton
            else:
                boton.config(relief=tk.RAISED)
        
    
       
    def editar_Componente(self):
        # Obtener los datos de los widgets
        self.nombre = self.vistas[self.vista_general].entry_nombre.get()
        if(self.nombre!=self.Componente_encontrado.get_nombre()):
            self.tk_app_instance.mpl_canvas.grafo.plot_instance.node_label_artists[self.node_in_menu].set_text(self.nombre)
        
        self.descripcion= self.vistas[self.vista_general].texto_scroll.get("1.0", tk.END)
        self.mtbf = self.vistas[self.vista_general].vistas["Exponencial"].entry_mtbf.get()
        self.tiempo_de_uso = self.vistas[self.vista_general].vistas["Exponencial"].entry_tiempo_de_uso.get()
        self.mttr = self.vistas[self.vista_general].vistas["Exponencial"].entry_mttr.get()
        self.es_reparable=self.vistas[self.vista_general].reparable.get()
       
        
        # editar Componente
        self.Componente_encontrado.set_nombre(self.nombre)
        self.Componente_encontrado.set_descripcion(self.descripcion)
        self.Componente_encontrado.set_mtbf(self.mtbf)
        self.Componente_encontrado.set_mttr(self.mttr)
        self.Componente_encontrado.set_tiempo_de_uso(self.tiempo_de_uso)
        self.Componente_encontrado.set_reparable(self.es_reparable)
        
        #cerrar ventana
        self.cerrar_ventana_Componentes()


if __name__ == "__main__":
    print("Ejecuta main")
