from pathlib import Path

# from tkinter import *
# Explicit imports to satisfy Flake8
from tkinter import Tk, Canvas, Entry, Text, Button, PhotoImage

def relative_to_assets(path: str) -> Path:
    script_path = Path(__file__).resolve().parent
    assets_path = script_path / "assets" / "frame0"  # Asumiendo que la carpeta 'assets' está en el mismo nivel que el script
    return assets_path / Path(path)


class AvailabilityWindow:
    def __init__(self, root:Tk):
        self.root = root
        self.root.geometry("1440x1024")
        self.root.configure(bg="#FFFFFF")
        self.images = []

        canvas = Canvas(
            root,
            bg = "#012677",
            height = 1024,
            width = 1440,
            bd = 0,
            highlightthickness = 0,
            relief = "ridge"
        )

        canvas.place(x = 0, y = 0)

        canvas.create_rectangle(
            23.0,
            100.0,
            1416.0,
            981.0,
            fill="#F8F8F8",
            outline="")
        
        canvas.create_rectangle(
            23.0,
            20.0,
            1416.0,
            80.0,
            fill="#8197C4",
            outline="")
        self.create_button("button_1.png", lambda: self.button_clicked(1), 38.0,35.0, 30.0, 30.0)
        
    def create_button(self, image_path, command, x, y, width, height):
        button_image = PhotoImage(file="assets\\frame3\\" + image_path)
        self.images.append(button_image)
        button = Button(
            self.root,
            image=button_image,
            borderwidth=0,
            highlightthickness=0,
            command=command,
            relief="flat", 
            activebackground="#eFFFFF",  # Establece el color de fondo al hacer clic
            highlightbackground = "#FF0000"  # Establece el color de fondo del resaltado del borde
        )
        button.place(x=x, y=y, width=width, height=height)
        button.configure(bg="#8197C4")
    
    def button_clicked(self, button_number):
        print(f"button_{button_number} clicked")

if __name__ == "__main__":  
    root = Tk()
    app = AvailabilityWindow(root)
    root.mainloop()