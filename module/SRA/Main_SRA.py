import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, Image, Paragraph
import os

class main_SRA:
    def __init__(self):
        # Leer el archivo Excel
        file_path = "module/SRA/Resultado.xlsx"
        df = pd.read_excel(file_path, sheet_name='DataFrame')

        # Crear el PDF
        pdf_filename = "module/SRA/output.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Estilos de texto
        styles = getSampleStyleSheet()
        title_style = styles["Title"]
        body_style = styles["Normal"]

        # Agregar título al documento
        title_text = "<b>Informe de Resultados</b>"
        title = Paragraph(title_text, title_style)
        # Convertir el DataFrame a una lista de listas para la tabla
        data = [df.columns.tolist()] + df.values.tolist()

        # Agregar un párrafo de texto
        result_text = "Resultados obtenido de ejecutar el modulo RBD, donde se obtiene la fiabilidad y disponibilidad de los equipos"
        result_table= Paragraph(result_text, body_style)
        
        # Estilo de la tabla
        style = TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0,0), (-1,0), 12),
                            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                            ('GRID', (0,0), (-1,-1), 1, colors.black)])
        
        # Crear la tabla con estilo
        table = Table(data)
        table.setStyle(style)

        # Cargar imagen de logo
        imagen_logo = 'module/SRA/assets/cotecmar.png'
        logo_cotecmar = Image(imagen_logo, width=50, height=50)

        # Cargar imagen 2
        img_path2 = 'module/SRA/assets/utb_logo.png'
        logo_utb = Image(img_path2, width=100, height=50)

        # Organizar las imágenes en una tabla
        images_table = Table([[logo_cotecmar, logo_utb]])

        # Alinear las imágenes al centro
        images_table.setStyle(TableStyle([('ALIGN', (0, 0), (-1, -1), 'CENTER')]))
        
        # Agregar un párrafo de texto
        result_graph_text = "Gráfica de fiabilidad del sistema analizado en el modulo RBD"
        result_graph= Paragraph(result_graph_text, body_style)
        # Cargar imagen de datos
        img_path = 'module/SRA/temp_plot.png'
        img = Image(img_path, width=300, height=200)

        # Construir el PDF
        elements = [images_table,Spacer(1, 20), title, Spacer(1, 20), result_table, Spacer(1,20),table, Spacer(1, 20),result_graph,Spacer(1,20), img]

        # Añadir elementos al documento
        doc.build(elements)

        print("¡Los datos y la imagen han sido exportados correctamente a PDF!")

        # Abre automáticamente el PDF generado
        os.system("start " + pdf_filename)

