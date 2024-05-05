import tkinter as tk
from tkinter import ttk, messagebox
from tksheet import Sheet


from module.LDA.page_sheet import SheetPage

class ContextualFrame(tk.Frame):
    def __init__(self, parent, sheet: SheetPage, **kwargs):
        super().__init__(parent, **kwargs)
        self.config(background="#FFF", width=300, height=300)

        self.sheet = sheet
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

        calculate_btn = ttk.Button(
            buttons_frame, text="cl", command=self.get_distribution, width=5)
        calculate_btn.pack()

        invisible_frame = tk.Frame(buttons_frame, width=50,height=800, bg="#FFF")
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

        # analysis_settings_frame = tk.Frame(
        #     comments_frame, width=250, height=100, bg="#F0F0F0", highlightbackground="#CECDCD", highlightthickness=2)
        # analysis_settings_frame.pack(anchor="center", padx=10, pady=10)

        analysis_summary_frame = tk.Frame(
            comments_frame, width=250, height=150, bg="#F0F0F0", highlightbackground="#CECDCD", highlightthickness=2)
        analysis_summary_frame.pack(anchor="center", padx=10, pady=10)

        self.parameters = Sheet(analysis_summary_frame, align="center", height=180, width=250,
                           total_rows=6, total_columns=2, empty_horizontal=0, empty_vertical=0, font=("Arial", 10, "normal"), header_font=("Arial", 10, "bold"), index_font=("Arial", 10, "normal"))
        self.parameters.enable_bindings(
            ("single_select", "drag_select", "edit_bindings", "column_width_resize", "right_click_popup_menu", "rc_insert_row"))
        self.parameters.row_index(redraw=False)
        self.parameters.grid(row=1, column=0, columnspan=1, sticky="nsew")


    def get_distribution(self): 
        self.best_dist = self.sheet.compute_best_distribution()
        messagebox.showinfo("Mejor distibución obtenida",
                            f"La distribución que mejor se ajusta a los datos ingresados es: {self.best_dist}")
        self.combobox_distribution.set(self.best_dist)
