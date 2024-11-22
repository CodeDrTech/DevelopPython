import os
import openpyxl
from PyQt5.QtCore import QDate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
import io
from PyQt5.QtWidgets import QApplication, QMessageBox
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph


# Obtener la ruta completa del archivo Excel
archivo_excel = os.path.join(os.path.dirname(__file__), 'Pruebas.xlsx')
hoja_excel = 'Hoja2'

# Leer el archivo Excel
workbook = openpyxl.load_workbook(archivo_excel, data_only=True)
sheet = workbook[hoja_excel]

# Obtener la fecha actual en formato "MMMM yyyy"
fecha = QDate.currentDate()
fecha_formato = fecha.toString("MMMM yyyy")

# Obtener los datos para el total general
nombre_total_general = sheet['A28'].value
monto_total_general = sheet['C28'].value

# Crear lista de datos para la tabla en el PDF
datos_tabla = [['Vendedor', 'Monto Mensual']]

# Recorrer las filas del archivo Excel y agregar datos a la lista
for fila in sheet.iter_rows(min_row=3, max_row=27, min_col=1, max_col=4, values_only=True):
    nombre_empleado = str(fila[0]).title()
    monto_mensual = fila[2] if fila[2] is not None else 0
    datos_tabla.append([nombre_empleado, monto_mensual])

# Configurar estilos para el PDF
estilos = getSampleStyleSheet()

# Configurar la ubicación del archivo PDF
pdf_path = os.path.join(os.path.dirname(__file__), f'reporte_mensual_{nombre_total_general}.pdf')

# Crear el documento PDF
pdf = SimpleDocTemplate(pdf_path, pagesize=letter)
contenido = []

# Crear la tabla con los datos
tabla = Table(datos_tabla)
tabla.setStyle(TableStyle([
    ('BACKGROUND', (0, 0), (-1, 0), estilos['Heading1'].backColor),
    ('TEXTCOLOR', (0, 0), (-1, 0), estilos['Heading1'].textColor),
    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
    ('FONTNAME', (0, 0), (-1, 0), estilos['Heading1'].fontName),
    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
    ('BACKGROUND', (0, 1), (-1, -1), estilos['BodyText'].backColor),
]))

# Agregar la tabla al contenido del PDF
contenido.append(Paragraph(f'Reporte Mensual - {fecha_formato}', estilos['Heading1']))
contenido.append(tabla)

# Generar el PDF
pdf.build(contenido)

# Cerrar el archivo Excel
workbook.close()

# Configuración del servidor SMTP de Gmail
correo_emisor = 'jperez@selactcorp.com'
contraseña_emisor = 'qsmikukzanvbchro'
correo_destinatario = 'destinatario@example.com'  # Cambiar al destinatario deseado

# Configurar el mensaje de correo
asunto = f'Reporte Mensual - {fecha_formato}'
cuerpo_mensaje = f'Buenas tardes {nombre_total_general},\n\nAdjunto el reporte mensual de los vendedores.\n\n'

mensaje = MIMEMultipart()
mensaje['From'] = f'Notificación de venta <{correo_emisor}>'
mensaje['To'] = correo_destinatario
mensaje['Subject'] = asunto

# Adjuntar texto al cuerpo del correo
mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

# Adjuntar archivo PDF al cuerpo del correo
with open(pdf_path, 'rb') as archivo_pdf:
    pdf_adjunto = MIMEApplication(archivo_pdf.read(), _subtype="pdf")
    pdf_adjunto.add_header('Content-Disposition', f'attachment; filename={os.path.basename(pdf_path)}')
    mensaje.attach(pdf_adjunto)

# Establecer la conexión con el servidor SMTP de Gmail y enviar el correo
with smtplib.SMTP('smtp.gmail.com', 587) as server:
    server.starttls()
    server.login(correo_emisor, contraseña_emisor)
    server.sendmail(correo_emisor, correo_destinatario, mensaje.as_string())

# Mostrar mensaje informativo
print("Correos enviado exitosamente.")

# Eliminar el archivo PDF después de enviar el correo (opcional)
os.remove(pdf_path)

