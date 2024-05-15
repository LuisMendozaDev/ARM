from pathlib import Path

from tkinter import Image, Tk, Canvas, Entry, Text, Button, PhotoImage, Toplevel, font, Label
import tkinter
from PIL import Image, ImageTk
import customtkinter
# from functions.util_window
import utils.util_window as util_window
from module.RBD.main import TkApp
from module.LDA import main

from tkinter import filedialog
import PyPDF2
import os

def relative_to_assets(path: str) -> Path:
    script_path = Path(__file__).resolve().parent
    # Asumiendo que la carpeta 'assets' está en el mismo nivel que el script
    assets_path = script_path / "views" / "assets" / "frame0"
    return assets_path / Path(path)


class mainWindow:
    def __init__(self, root: Tk):
        self.root = root
        # self.root.geometry("1440x1000")
        self.root.configure(bg="#FFFFFF")
        self.root.title("TritonOps")
        self.images = []
        self.root_view = None

        self.root.bind("<Configure>", self.on_window_resize)

        # Dimensiones originales de la ventana
        width = 1200
        height = 900
        util_window.center_window(self.root, 1200, 900)
        self.root.minsize(1200, 900)

        logo_image = PhotoImage(file=relative_to_assets("icon.png"))  # Cambia "ruta/al/logo.png" por la ubicación de tu imagen de logo

        # Establecer la imagen del logo como icono de la ventana
        self.root.iconphoto(True, logo_image)
        self.canvas = Canvas(
            root,
            bg="#FFFFFF",
            height=height,
            width=width,
            bd=0,
            highlightthickness=0,
            relief="ridge"
        )
        self.canvas.place(x=0, y=0)

        self.title = self.create_image("title.png", 476, 476)

        self.title_image = Label(self.root, image=self.title, bg="white")

        self.button_1 = customtkinter.CTkButton(
            master=self.root, text="LDA", font=('Britannic Bold', 30), command=lambda:  self.lda_window())
        self.button_1.configure(width=100, height=100)

        self.button_2 = customtkinter.CTkButton(
            master=self.root, text="RBD", font=('Britannic Bold', 30), command=lambda: self.rbd_window())
        self.button_2.configure(width=100, height=100)

        self.button_3 = customtkinter.CTkButton(
            master=self.root, text="SRA", font=('Britannic Bold', 30), command=lambda: self.play_SRA())
        self.button_3.configure(width=100, height=100)

        self.image_1 = self.create_image("decorator_1.png", 495, 420)
        self.image_2 = self.create_image("decorator_2.png", 420, 495)
        self.image_3 = self.create_image("cotecmar.png", 100, 100)

        self.label_imagen = Label(self.root, image=self.image_1, bg="white")
        self.label_imagen.place(relx=0.06, rely=0.1, anchor="center")

        self.label_imagen = Label(self.root, image=self.image_2, bg="white")
        self.label_imagen.place(relx=0.95, rely=0.9, anchor="center")

        self.label_imagen = Label(self.root, image=self.image_3, bg="white")
        self.label_imagen.place(relx=0.58, rely=0.9, anchor="center")

        self.create_button("intructions.png", lambda: self.abrir_pdf(), 0.38, 0.9, 156.0, 32.0)

        self.place_buttons()
    
    def play_SRA(self):
        main_SRA()
    
    def lda_window(self):
        self.root.withdraw()
        self.lda = MainApp()

        self.lda.protocol("WM_DELETE_WINDOW", self.on_root_lda_close)

        self.lda.run()
    
    def on_root_lda_close(self):
        # Este método se llama cuando la nueva ventana (RootView) se cierra
        # Muestra nuevamente la ventana principal
        self.root.deiconify()

        # Destruye la segunda ventana (RootView)
        if hasattr(self, 'lda'):
            self.lda.cerrar_ventana()
            self.lda = None  # Resetea la referencia a la ventana RootView
    def rbd_window(self):
        # Oculta la ventana principal
        self.root.withdraw()
        self.app = TkApp()

        # Configura el evento de cierre
        self.app.root.protocol("WM_DELETE_WINDOW", self.on_root_view_close)
        self.app.run()

    def on_root_view_close(self):
        # Este método se llama cuando la nueva ventana (RootView) se cierra
        # Muestra nuevamente la ventana principal
        self.root.deiconify()
        # Destruye la segunda ventana (RootView)
        if self.app:
            self.app.cerrar_ventana()
            self.app = None  # Resetea la referencia a la ventana RootView

    def abrir_pdf(self):
        # Ruta del archivo PDF
        ruta_pdf = "instructions.pdf"
        
        # Verificar si el archivo existe
        if os.path.exists(ruta_pdf):
            # Abrir el archivo PDF
            os.startfile(ruta_pdf)
        else:
            print("El archivo PDF no se encontró en la ruta especificada.")

    def place_buttons(self):
        self.title_image.place(relx=0.48, rely=0.35, anchor="center")
        self.button_1.place(relx=0.33, rely=0.65)
        self.button_2.place(relx=0.45, rely=0.65)
        self.button_3.place(relx=0.57, rely=0.65)

    def on_window_resize(self, event):
        # Esta función se llama cuando cambia el tamaño de la ventana
        self.place_buttons()

    def create_button(self, image_path, command, x, y, width, height):
        button_image = PhotoImage(file=relative_to_assets(image_path))
        self.images.append(button_image)
        button = Button(
            self.root,
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat",
            activebackground="#eFFFFF",  # Establece el color de fondo al hacer clic
            highlightbackground="#FF0000"  # Establece el color de fondo del resaltado del borde
        )
        button.place(relx=x, rely=y, width=width, height=height)
        button.configure(bg="#FFFFFF")

    def create_image(self, image_path, width=0, height=0):
        imagen = Image.open(relative_to_assets(image_path))
        if width != 0 and height != 0:
            imagen = imagen.resize((width, height))
        imagen_tk = ImageTk.PhotoImage(imagen)
        return imagen_tk

    def button_clicked(self, button_number):
        print(f"button_{button_number} clicked")

    def lda_window(self):
        self.root.withdraw()
        self.lda = main.MainApp()

        self.lda.protocol("WM_DELETE_WINDOW", self.on_root_lda_close)

        self.lda.run()

    def ir_a_pantalla_2(self):
        # Oculta la ventana principal
        self.root.withdraw()
        # Crea la nueva ventana después de cerrar la ventana principal
        # self.root_view = RootView(self.root)
        # app = Controlador(self.root_view)
        self.app = TkApp()

        # Configura el evento de cierre
        self.app.root.protocol("WM_DELETE_WINDOW", self.on_root_view_close)
        self.app.run()

    def on_root_view_close(self):
        # Este método se llama cuando la nueva ventana (RootView) se cierra
        # Muestra nuevamente la ventana principal
        self.root.deiconify()

        # Destruye la segunda ventana (RootView)
        if self.app:
            self.app.cerrar_ventana()
            self.app = None  # Resetea la referencia a la ventana RootView

    def on_root_lda_close(self):
        # Este método se llama cuando la nueva ventana (RootView) se cierra
        # Muestra nuevamente la ventana principal
        self.root.deiconify()

        # Destruye la segunda ventana (RootView)
        if self.lda:
            self.lda.cerrar_ventana()
            self.lda = None  # Resetea la referencia a la ventana RootView


if __name__ == "__main__":
    root = Tk()
    app = mainWindow(root)
    root.mainloop()
