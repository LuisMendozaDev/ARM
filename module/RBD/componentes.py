
class Componentes:
    #Lista donde se guardaran los objetos componente
    lista_Componentes = []

    def __init__(self, nombre, mttr=0, mtbf=0, tiempo_de_uso=0, disponibilidad=0, mantenibilidad=0,descripcion="", reparable=False):
        self.nombre = nombre
        self.disponibilidad = disponibilidad
        self.mttr = mttr  # mean time to repair
        self.mtbf = mtbf  # mean time to fail
        self.tiempo_de_uso = tiempo_de_uso
        self.reliability = 1
        self.descripcion=descripcion
        self.reparable=reparable
        Componentes.lista_Componentes.append(self)  
        
    # Función para obtener la instancia de nodo por nombre
    @staticmethod
    def obtener_componente_por_nombre(nombre_buscado):
        for n in Componentes.lista_Componentes:
            if str(n.get_nombre()) == str(nombre_buscado):
                return n
        return None  # Retorna None si no se encuentra el nodo con el nombre dado
    
    #imprimir todos los objetos y sus atributos 
    @staticmethod
    def imprimir_atributos():
        for n in Componentes.lista_Componentes:
            print(f"Nombre: {n.get_nombre()}, MTTR: {n.get_mttr()}, MTBF: {n.get_mtbf()}, Tiempo de Uso: {n.get_tiempo_de_uso()}")
    
    #Imprimir la informacion importante para los resultados
    @staticmethod
    def imprimir_atributos_resultado():
        datos_componentes = []
        for componente in Componentes.lista_Componentes:
            datos = {
                'Componente': componente.get_nombre(),
                'MTBF': componente.get_mtbf(),
                'MTTR': componente.get_mttr(),
                #'Tiempo de Uso': componente.get_tiempo_de_uso(),
                'Confiabilidad': round(componente.get_reliability(), 5),
                'Disponibilidad': componente.get_disponibilidad()
            }
            datos_componentes.append(datos)
        return datos_componentes
    
    #Imprimir atributos de un componente en especifico ingresando su nombre
    @staticmethod
    def diccionario_atributos(nombre_buscado):
        for n in Componentes.lista_Componentes:
            if str(n.get_nombre()) == str(nombre_buscado):
                return {"nombre":n.get_nombre(), "mttr":n.get_mttr(), "mtbf":n.get_mtbf(), "tiempo_de_uso":n.get_tiempo_de_uso(), "reparable": n.get_reparable()}
        return None
    
    #Eliminar componente
    def eliminar_componente(self, nodo):
        nodo_eliminar=Componentes.obtener_componente_por_nombre(nombre_buscado=self.tk_app_instance.mpl_canvas.grafo.plot_instance.node_label_artists[nodo].get_text())
        if(nodo_eliminar!=None):
            Componentes.lista_Componentes.remove(nodo_eliminar)
    
    @staticmethod
    def vaciar_lista_componentes():
        Componentes.lista_Componentes.clear()
    
    #Guardar el objeto tk_app del main para poder acceder a el
    def guardarAPP(self, tk_app_instance):
        self.tk_app_instance = tk_app_instance
            
    #setters y getters
    def set_nombre(self, nombre):
        self.nombre = nombre
    def get_nombre(self):
        return self.nombre
    
    def set_disponibilidad(self, disponibilidad):
        self.disponibilidad=disponibilidad
    def get_disponibilidad(self):
        return self.disponibilidad
   
    def set_mttr(self, mttr):
        self.mttr=mttr
    def get_mttr(self):
        return self.mttr 
    
    def set_mtbf(self, mtbf):
        self.mtbf=mtbf
    def get_mtbf(self):
        return self.mtbf
    
    def set_tiempo_de_uso(self, tiempo_de_uso):
        self.tiempo_de_uso = tiempo_de_uso
    def get_tiempo_de_uso(self):
        return self.tiempo_de_uso
    
    def set_reliability(self, reliability):
        self.reliability=reliability
    def get_reliability(self):
        return self.reliability
    
    def set_descripcion(self, descripcion):
        self.descripcion=descripcion
    def get_descripcion(self):
        return self.descripcion
    
    def set_reparable(self, reparable):
        self.reparable=reparable
    def get_reparable(self):
        return(self.reparable)

if __name__ == "__main__":
    print("Ejecuta main")