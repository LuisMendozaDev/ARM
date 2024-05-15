import tkinter as tk
from tkinter import PhotoImage, ttk, messagebox, Button
from tksheet import Sheet
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure



from module.LDA.page_sheet import SheetPage
from module.LDA.page_graph import GraphPage
from module.LDA.page_calculator import CalculatorPage

from module.LDA.utils.config import CreateToolTip
# from page_sheet import SheetPage


class ContextualFrame(tk.Frame):
    def __init__(self, parent, sheet_page: SheetPage, graph_page: GraphPage, calculator_page: CalculatorPage, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(background="#FFF", width=300, height=300)

        self.sheet_page = sheet_page
        self.graph_page = graph_page
        self.calculator_page = calculator_page
        self.best_dist = "Exponencial"

        Frame = tk.Frame(self, width=300, height=800, bg="#FFF")
        Frame.pack(fill="both", expand=True)

        title_frame = tk.Frame(Frame, bg="#0000FF")
        title_frame.pack(fill="both", expand=True)

        label = tk.Label(title_frame, text="Life Data Analysis",
                         bg="#0000FF", fg="#FFF", font=("Verdana", 20, "bold"))
        label.pack()

        buttons_frame = tk.Frame(Frame, width=50, height=800, bg="#FFF")
        buttons_frame.pack(side=tk.LEFT)

        # Crear el botón con la imagen
        calculate_btn = Button(
            buttons_frame, text="CAL", command=self.get_distribution)
        calculate_btn.pack()

        calculate_tooltip = CreateToolTip(calculate_btn,"calcular distribucion "
                                          "a partir de los datos")
        invisible_frame = tk.Frame(
            buttons_frame, width=50, height=800, bg="#FFF")
        invisible_frame.pack(expand=True)

        comments_frame = tk.Frame(Frame, width=300, height=800, bg="#FFF",
                                  highlightbackground="#CECDCD", highlightthickness=2)
        comments_frame.pack(side=tk.LEFT, fill="both")

        distribution_frame = tk.Frame(comments_frame, width=250, height=60,
                                      bg="#F0F0F0", highlightbackground="#CECDCD", highlightthickness=2)
        distribution_frame.pack(anchor="center", padx=10, pady=10)

        distribution_label = tk.Label(
            distribution_frame, text="Distributions", bg="#F0F0F0", font=("Verdana", 12, "bold"))
        distribution_label.pack(expand=False)

        self.combobox_distribution = ttk.Combobox(distribution_frame, state="readonly", width=35, values=[
                                                  "Exponencial", "Lognormal", "Normal", "Weibull", "Logaritmica"])
        self.combobox_distribution.set("Exponencial")
        self.combobox_distribution.pack(padx=5, pady=5)

        analysis_summary_frame = tk.Frame(
            comments_frame, width=250, height=150, bg="#F0F0F0", highlightbackground="#CECDCD", highlightthickness=2)
        analysis_summary_frame.pack(anchor="center", padx=10, pady=10)

        self.parameters = Sheet(analysis_summary_frame, align="center", height=180, width=250,
                                total_rows=6, total_columns=2, empty_horizontal=0, empty_vertical=0, font=("Arial", 10, "normal"), header_font=("Arial", 10, "bold"), index_font=("Arial", 10, "normal"))
        self.parameters.enable_bindings(
            ("single_select", "drag_select", "edit_bindings", "column_width_resize", "right_click_popup_menu", "rc_insert_row"))
        self.parameters.row_index(redraw=False)
        self.parameters.grid(row=1, column=0, columnspan=1, sticky="nsew")

        self.equation_frame = tk.Frame(comments_frame, width=250, height=60,
                                       bg="#F0F0F0", highlightbackground="#CECDCD", highlightthickness=2)
        self.equation_frame.pack(anchor="center", padx=10, pady=10)
        equiation_label = tk.Label(
            self.equation_frame, text="Cumulative Distribution Function", bg="#F0F0F0", font=("Verdana", 12, "bold"))
        equiation_label.pack(expand=False)

        self.equation = Figure(figsize=(4, 2), dpi=100)
        self.ax = self.equation.add_subplot(111)
        self.ax.axis('off')

        self.canvas = FigureCanvasTkAgg(
            self.equation, master=self.equation_frame)
        self.canvas.get_tk_widget().pack(anchor="center", padx=10, pady=10)
        # Crear la figura de matplotlib
        self.dibujar_funcion(r'$R(t) =$')

    def get_distribution(self):
        best_dist, best_parametros = self.sheet_page.compute_best_distribution()
        sheet_data = [float(fila[0])
                      for fila in self.sheet_page.sheet.get_sheet_data()]
        self.graph_page.failure_time(data=sheet_data)
        self.graph_page.logaritmica(
            data=sheet_data, best_dist=best_dist, best_params=best_parametros)
        messagebox.showinfo("Mejor distibución obtenida",
                            f"La distribución que mejor se ajusta a los datos ingresados es: {best_dist}")
        self.combobox_distribution.set(best_dist)

        data = [["Distribución", best_dist], ["Parametros", ""]]
        self.calculator_page.best_dist = best_dist
        self.calculator_page.best_params = best_parametros
        self.calculator_page.is_valid = True
        self.calculator_page.unit = self.sheet_page.unit
        if best_dist == "Exponential":
            data.extend([["γ (loc)", round(best_parametros[0], 5)], [
                        "λ (scale)", round(best_parametros[1], 5)]])
            self.dibujar_funcion(r'$R(t) = e^{-\lambda(t-\gamma)} $')
        elif best_dist == "Lognormal":
            data.extend([["s", round(best_parametros[0], 5)], ["loc", round(best_parametros[1], 5)], [
                        "scale", round(best_parametros[2], 5)]])
            self.dibujar_funcion(r'$R(t) =e^{x}  +2$')
        elif best_dist == "Weibull":
            data.extend([["c", round(best_parametros[0], 5)], ["loc", round(best_parametros[1], 5)], [
                        "scale", round(best_parametros[2], 5)]])
            self.dibujar_funcion(
                r'$R(t) = e^{-\left(\frac{t-\gamma}{\eta}\right)^{\beta}}$')

        # Mostrar los datos en la hoja de cálculo
        self.parameters.set_sheet_data(data)

    def dibujar_funcion(self, funcion_latex):
        # Dibujar la función LaTeX en el canvas
        self.ax.clear()
        self.ax.axis('off')  # No mostrar ejes
        self.ax.text(0.5, 0.5, funcion_latex, fontsize=24, ha='center')

        self.equation.canvas.draw()

    def apply_configuration(self):
        units = self.config.get("units", "CICLOS")
        return units
