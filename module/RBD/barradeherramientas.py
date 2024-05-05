import tkinter as tk

class barradeherramientas:
    def create_toolbar(self, root):
        toolbar = tk.Frame(root)
        self.buttons = []
        

        # Crear botones de la barra de herramientas
        componente_button = tk.Button(toolbar, text="Componente", compound=tk.LEFT)
        componente_button.config(command=lambda: self.button_clicked(self,componente_button))
        componente_button.pack(side=tk.LEFT, padx=1, pady=0, ipady=4)
        self.buttons.append(componente_button)

        nodo_button = tk.Button(toolbar, text="Nodo")
        nodo_button.config(command=lambda: self.button_clicked(self,nodo_button))
        nodo_button.pack(side=tk.LEFT, padx=1, pady=0, ipady=4)
        self.buttons.append(nodo_button)
        
        inicio_button = tk.Button(toolbar, text="inicio")
        inicio_button.config(command=lambda: self.button_clicked(self,inicio_button))
        inicio_button.pack(side=tk.LEFT, padx=1, pady=0, ipady=4)
        self.buttons.append(inicio_button)
        
        fin_button = tk.Button(toolbar, text="fin")
        fin_button.config(command=lambda: self.button_clicked(self,fin_button))
        fin_button.pack(side=tk.LEFT, padx=1, pady=0, ipady=4)
        self.buttons.append(fin_button)

        # cut_button = tk.Button(toolbar, text="Cut")
        # cut_button.config(command=lambda: self.button_clicked(self,cut_button))
        # cut_button.pack(side=tk.LEFT, padx=1, pady=0, ipady=4)
        # self.buttons.append(cut_button)

        # copy_button = tk.Button(toolbar, text="Copy")
        # copy_button.config(command=lambda: self.button_clicked(self,copy_button))
        # copy_button.pack(side=tk.LEFT, padx=1, pady=0, ipady=4)
        # self.buttons.append(copy_button)

        # paste_button = tk.Button(toolbar, text="Paste", command=paste_text)
        # paste_button.config(command=lambda: self.button_clicked(self, paste_button))
        # paste_button.pack(side=tk.LEFT, padx=1, pady=0, ipady=4)
        # self.buttons.append(paste_button)

        # Add the toolbar to the root window
        toolbar.pack(side=tk.TOP, fill=tk.X, pady=5)
    
    #Funcion que me permite dejar precionado el boton de la barra de herramientas pero si presiono otro se libera
    def button_clicked(self, button):
        # Función para cambiar el estado visual del botón al hacer clic
        button_relief = button.cget('relief')
        #print(button_relief)
        if button_relief == 'raised':
            button.config(relief=tk.SUNKEN)
            # Cambiar el estado de todos los botones en la lista self.buttons a SUNKEN excepto el button
            for btn in self.buttons:
                if btn != button:
                    btn.config(relief=tk.RAISED)
        if button_relief == 'sunken':
            button.config(relief=tk.RAISED)
    
    #Retorna el boton presionado
    def Get_button_clicked(self):
        for button in self.buttons:
            if button.cget('relief') == 'sunken':
                print(button.cget('text'))
                return button.cget('text')
        return None
    
#Funciones no implementadas
def open_file():
    print("Opening file...")

def save_file():
    print("Saving file...")

def cut_text():
    print("Cutting text...")

def copy_text():
    print("Copying text...")

def paste_text():
    print("Pasting text...") 