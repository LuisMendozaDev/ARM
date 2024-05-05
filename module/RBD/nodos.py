
class nodos:
    #Lista donde se guardaran los objetos componente
    lista_nodos = []

    def __init__(self, nombre, paths_required=1, stanby_bool=False):
        self.nombre = nombre
        self.paths_required=paths_required
        self.stanby_bool=stanby_bool 
        nodos.lista_nodos.append(self) 
        
    
    # Función para obtener la instancia de nodo por nombre
    @staticmethod
    def obtener_nodo_por_nombre(nombre_buscado):
        for n in nodos.lista_nodos:
            if str(n.get_nombre()) == str(nombre_buscado):
                return n
        return None  # Retorna None si no se encuentra el nodo con el nombre dado
    
    @staticmethod
    def diccionario_atributos(nombre_buscado):
        for n in nodos.lista_nodos:
            if str(n.get_nombre()) == str(nombre_buscado):
                return {"nombre":n.get_nombre(), "knout":n.get_paths_required()}
        return None
    
    def eliminar_nodo(self, nodo):
        nodo_eliminar=nodos.obtener_nodo_por_nombre(nombre_buscado=self.tk_app_instance.mpl_canvas.grafo.plot_instance.node_label_artists[nodo].get_text())
        if(nodo_eliminar!=None):
            nodos.lista_nodos.remove(nodo_eliminar)
            
    #Guardar el objeto tk_app del main para poder acceder a el
    def guardarAPP(self, tk_app_instance):
        self.tk_app_instance = tk_app_instance
    
    #setters y getters
    def get_nombre(self):
        return self.nombre
    def set_nombre(self, nombre):
        self.nombre = nombre
        
    def get_paths_required(self):
        return self.paths_required
    def set_paths_required(self, paths_required):
        self.paths_required = paths_required
        
    def set_stanby_bool(self, stanby_bool):
        self.stanby_bool=stanby_bool
    def get_stanby_bool(self):
        return self.stanby_bool
    