from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors

# Datos de la factura (puedes obtenerlos de tu base de datos SQL)
cliente = "Cliente Ejemplo"
direccion = "123 Calle Principal"
fecha = "2023-11-02"
productos = [("Producto 1", 2, 10.00, 20.00),
             ("Producto 2", 1, 15.00, 15.00),
             ("Producto 3", 3, 5.00, 15.00)]

# Crear un documento PDF
doc = SimpleDocTemplate("Sistema de ventas/pdf/factura.pdf", pagesize=letter)

# Contenido de la factura
content = []

# Estilo para los párrafos
styles = getSampleStyleSheet()
style = styles["Normal"]

# Agregar encabezado
content.append(Paragraph("Factura", style))
content.append(Paragraph(f"Cliente: {cliente}", style))
content.append(Paragraph(f"Dirección: {direccion}", style))
content.append(Paragraph(f"Fecha: {fecha}", style))
content.append(Paragraph("", style))

# Crear una tabla para los productos
data = [["Descripción", "Cantidad", "Precio Unitario", "Total"]]
for producto in productos:
    data.append(producto)

table = Table(data)
table.setStyle(TableStyle([('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                           ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                           ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                           ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                           ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                           ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                           ('GRID', (0, 0), (-1, -1), 1, colors.black)]))

content.append(table)

# Generar el documento PDF
doc.build(content)
