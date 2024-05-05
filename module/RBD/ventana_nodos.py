import tkinter as tk
from tkinter import scrolledtext
from module.RBD.nodos import nodos


class Vista_general(tk.Frame):
    def __init__(self, master, controller, tk_app_instance, nodo, nodo_encontrado):
        # Cambia color_principal al color que desees
        tk.Frame.__init__(self, master)
        self.controller = controller
        
        # Crear widgets
        self.basic_info_frame=tk.LabelFrame(self, text="Informacion Basica")
        self.basic_info_frame.grid(row= 0, column=0, padx=20, pady=10)
        
        self.label_nombre = tk.Label( self.basic_info_frame, text="Nombre:")
        self.label_nombre.grid(row=0, column=0 , sticky=tk.W)
        
        self.entry_nombre = tk.Entry( self.basic_info_frame)
        self.entry_nombre.grid(row=0, column=1, ipadx=20, sticky=tk.W)
        
        #Obtener el nombre que le asigno el usuario
        self.entry_nombre.insert(0, tk_app_instance.mpl_canvas.grafo.plot_instance.node_label_artists[nodo].get_text())
        
        # Crear widgets
        self.paths_info_frame=tk.LabelFrame(self, text="Paths")
        self.paths_info_frame.grid(row= 1, column=0, padx=20, pady=10)
        
        self.label_paths = tk.Label(self.paths_info_frame, text="Number of paths required [k-out-of-n):")
        self.label_paths.grid(row=0, column=0 , pady=20, sticky=tk.W)
        
        self.entry_paths = tk.Entry(self.paths_info_frame)
        self.entry_paths.grid(row=0, column=1, ipadx=1 , pady=20, sticky=tk.W)
        
        self.entry_paths.insert(0, nodo_encontrado.get_paths_required())
        
        n= tk_app_instance.mpl_canvas.grafo.plot_instance.precursores_de_nodo(nodo)
        
        self.label_paths = tk.Label(self.paths_info_frame, text=f"Out of {n}")
        self.label_paths.grid(row=0, column=2, padx=0 , pady=20, sticky=tk.W)
        
        self.texto_scroll = scrolledtext.ScrolledText(self.basic_info_frame, wrap=tk.WORD, width=20, height=5)
        self.texto_scroll.grid(row=0, column=2, padx=(80, 20), pady=(10,20))


class Vista_standby(tk.Frame):
    def __init__(self, master,nodo_encontrado, controller):
        # Cambia color_principal al color que desees
        tk.Frame.__init__(self, master)
        self.controller = controller

        # Contenido de la segunda vista
        label = tk.Label(self, text="Standby", font=(
            "Helvetica", 16, "bold"))
        label.pack(pady=10)

        # Cuadro para el Entry
        # Cambia color_principal al color que desees
        entry_frame = tk.Frame(self)
        entry_frame.pack(pady=10)

        #Checkbox si es reparable
        self.standby = tk.IntVar()
        self.check_standby = tk.Checkbutton(entry_frame, text="Standby", variable=self.standby)
        self.check_standby.pack(side=tk.LEFT)
        
        if(nodo_encontrado.get_stanby_bool()):
            self.standby.set(1)
        else:
            self.standby.set(0)



class ventana_nodos:
    def __init__(self,tk_app_instance, root):
        self.root = root
        self.tk_app_instance = tk_app_instance
        # Crear un nuevo Frame en la raíz para los botones y las vistas
        self.vista_general=Vista_general
        self.vista_standby=Vista_standby
        
        
    def show_nodo_window(self, node_in_menu):
        
        #Nodo donde se desplego el menu
        self.node_in_menu=node_in_menu
        self.boton_actual = None  # Almacena el botón de la vista actual
        self.nodo_encontrado=nodos.obtener_nodo_por_nombre(nombre_buscado=self.tk_app_instance.mpl_canvas.grafo.plot_instance.node_label_artists[self.node_in_menu].get_text())
        
        
        #Crear ventana
        self.ventana = tk.Toplevel(self.root)
        self.ventana.attributes('-toolwindow', True)
        self.ventana.attributes('-topmost', True)
        self.ventana.focus_force()
        self.ventana.grab_set()
        self.ventana.title("Ingreso de datos para nodo")
        
        self.frame_contenedor = tk.Frame(self.ventana)
        self.frame_contenedor.pack(pady=10, padx=10)

         # Crear un nuevo Frame para los botones
        self.frame_botones = tk.Frame(self.frame_contenedor)
        self.frame_botones.pack(side=tk.TOP, anchor=tk.NW)
        
        self.button_Vista_general = tk.Button(self.frame_botones, text="General", command=lambda: self.mostrar_vista(self.vista_general), bd=3, relief="raised")
        self.button_Vista_general.pack(side=tk.LEFT, padx=0)
        
        self.button_Vista_standby = tk.Button(self.frame_botones, text="Standby", command=lambda: self.mostrar_vista(self.vista_standby), bd=3, relief="raised")
        self.button_Vista_standby.pack(side=tk.LEFT, padx=0)

        # Para agregar otro botones es simplemente crear la instanica y añadirlos al self.frame_botones

        # Frame que contiene las vistas
        self.cuadro_vistas = tk.Frame(
            self.frame_contenedor, width=560, height=400, bd=3, relief="raised")

        self.cuadro_vistas.pack_propagate(False)
        self.cuadro_vistas.pack()
        
        self.vistas = {}
        self.vistas[self.vista_general] = self.vista_general(self.cuadro_vistas, self, self.tk_app_instance, self.node_in_menu,  self.nodo_encontrado)
        self.vistas[self.vista_standby] = self.vista_standby(self.cuadro_vistas,self.nodo_encontrado, self)
        
        self.boton_editar_nodo = tk.Button(self.ventana, text="Editar nodo", command=self.editar_nodo, bd=4, relief="raised")
        self.boton_editar_nodo.pack(side=tk.BOTTOM, pady=20)

        self.mostrar_vista(self.vista_general)

    def mostrar_vista(self, vista):
        # Ocultar vistas anteriores
        for vista_actual in self.vistas.values():
            vista_actual.pack_forget()

        # Mostrar la nueva vista en el cuadro
        self.vistas[vista].pack()

        # Resaltar el botón de la vista actual
        if self.boton_actual:
            self.boton_actual.config(relief=tk.SUNKEN)

        for boton, vista_clase in zip([self.button_Vista_general, self.button_Vista_standby], [self.vista_general, self.vista_standby]):
            if vista_clase == vista:
                boton.config(relief=tk.SUNKEN)
                self.boton_actual = boton
            else:
                boton.config(relief=tk.RAISED)
                
    def cerrar_ventana_nodos(self):
        self.ventana.destroy()
        #Actualizar grafo por si hubo algun cambio
        self.tk_app_instance.mpl_canvas.grafo.plot_instance.fig.canvas.draw_idle()
        
    def editar_nodo(self):
        # Obtener los datos de los widgets
        self.nombre = self.vistas[self.vista_general].entry_nombre.get()
        self.entry_paths= self.vistas[self.vista_general].entry_paths.get()
        self.standby=self.vistas[self.vista_standby].standby.get()
        self.tk_app_instance.mpl_canvas.grafo.plot_instance.node_label_artists[self.node_in_menu].set_text(self.nombre)
        # editar Componente
        
        
        
        self.nodo_encontrado.set_nombre(self.nombre)
        self.nodo_encontrado.set_stanby_bool(self.standby)
        
        
        #cerrar ventana
        
        self.nodo_encontrado.set_paths_required(self.entry_paths)
        
        
        
        
        
        
        self.cerrar_ventana_nodos()
    
