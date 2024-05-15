# import tkinter as tk

# class MainApp:
#     def __init__(self, root):
#         self.root = root
#         self.root.title("Ventana Secundaria")
        
#         # Etiqueta de texto
#         self.label = tk.Label(root, text="Introduce algo:")
#         self.label.pack()
        
#         # Entrada de texto
#         self.entry_var = tk.StringVar()  # Variable para almacenar el texto ingresado
#         self.entry = tk.Entry(root, textvariable=self.entry_var)
#         self.entry.pack()
    
#     def cerrar_ventana(self):
#         self.root.withdraw()  # Oculta la ventana en lugar de destruirla

# class App:
#     def __init__(self):
#         self.root = tk.Tk()
#         self.root.title("Ventana Principal")
#         self.button = tk.Button(self.root, text="Abrir ventana secundaria", command=self.abrir_ventana)
#         self.button.pack()
#         self.saved_text = ""  # Variable para almacenar el texto ingresado
        
#     def abrir_ventana(self):
#         self.root.withdraw()  # Oculta la ventana principal
#         self.lda = tk.Toplevel()  # Crea una ventana secundaria
#         self.lda.title("Ventana Secundaria")
#         self.ventana_secundaria = MainApp(self.lda)
#         # Restaurar el texto guardado cuando se abre la ventana secundaria
#         self.ventana_secundaria.entry_var.set(self.saved_text)
#         self.lda.protocol("WM_DELETE_WINDOW", self.on_root_lda_close)
    
#     def on_root_lda_close(self):
#         if self.ventana_secundaria:  # Verifica si la ventana secundaria todavía existe
#             # Guardar el texto ingresado antes de cerrar la ventana
#             self.saved_text = self.ventana_secundaria.entry_var.get()
#             self.ventana_secundaria.cerrar_ventana()  # Oculta la ventana secundaria sin destruirla
#             self.root.deiconify()  # Muestra nuevamente la ventana principal

# if __name__ == "__main__":
#     app = App()
#     app.root.mainloop()
import numpy as np

# Definir media y desviación estándar
media = 10
desviacion_estandar = 2

# Generar datos que sigan una distribución normal
datos_normal = np.random.normal(loc=media, scale=desviacion_estandar, size=1000)

# Imprimir los primeros 10 datos
print(datos_normal[:10])