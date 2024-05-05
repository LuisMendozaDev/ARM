from tkinter.tix import IMAGETEXT


def center_window(window, width, height):
    """
    Basado en https://stackoverflow.com/a/10018670.
    """
    window.update_idletasks()
    frm_width = window.winfo_rootx() - window.winfo_x()
    win_width = width + 2*frm_width
    titlebar_height = window.winfo_rooty() - window.winfo_y()
    win_height = height + titlebar_height + frm_width
    x = window.winfo_screenwidth()//2 - win_width//2
    y = window.winfo_screenheight()//2 - win_height//2
    window.geometry('{}x{}+{}+{}'.format(width, height, x, y))
    window.deiconify()


def calcular_tamano_fuente(self, proporcion):
    # Calcula el tamaño de la fuente en función del tamaño de la ventana
    return int(proporcion * self.winfo_width())

