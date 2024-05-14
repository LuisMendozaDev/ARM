import pandas as pd
import matplotlib.pyplot as plt
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle
from reportlab.platypus import Image
import os

class main_SRA:
    def __init__(self):
        # Leer el archivo Excel
        file_path = "module/SRA/Resultado.xlsx"
        df = pd.read_excel(file_path, sheet_name='DataFrame')

        # Crear el PDF
        pdf_filename = "module/SRA/output.pdf"
        doc = SimpleDocTemplate(pdf_filename, pagesize=letter)

        # Convertir el DataFrame a una lista de listas para la tabla
        data = [df.columns.tolist()] + df.values.tolist()

        # Crear la tabla
        table = Table(data)

        # Estilo de la tabla
        style = TableStyle([('BACKGROUND', (0,0), (-1,0), colors.grey),
                            ('TEXTCOLOR', (0,0), (-1,0), colors.whitesmoke),
                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                            ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                            ('BOTTOMPADDING', (0,0), (-1,0), 12),
                            ('BACKGROUND', (0,1), (-1,-1), colors.beige),
                            ('GRID', (0,0), (-1,-1), 1, colors.black)])
        table.setStyle(style)
        
        imagen_logo = 'module/SRA/assets/cotecmar.png'
        logo=Image(imagen_logo, width=168, height=168)
        
        # Poner imagen en el PDF
        img_path = 'module/SRA/temp_plot.png'
        img = Image(img_path, width=300, height=200)  # Ajusta el ancho y alto según tu necesidad

        # Construir el PDF
        elements = [logo, table, img]

        # Añadir elementos al documento
        doc.build(elements)

        print("¡Los datos y la imagen han sido exportados correctamente a PDF!")
        
        os.system("start " + pdf_filename)