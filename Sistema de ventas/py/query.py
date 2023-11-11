import os
import locale
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import QApplication, QMessageBox

# Configurar la localización para el formato de moneda
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Obtener la ruta completa del archivo Excel
archivo_excel = os.path.join(os.path.dirname(__file__), 'ventas.xlsx')
hoja_excel = 'Hoja1'

# Configuración del servidor SMTP de Gmail
correo_emisor = 'joseperez8715@gmail.com'
contraseña_emisor = 'jgtlqydfeuosgzma'

# Leer el archivo Excel
workbook = openpyxl.load_workbook(archivo_excel)
sheet = workbook[hoja_excel]

# Iniciar la aplicación de PyQt
app = QApplication([])

# Recorrer las filas del archivo Excel
for fila in sheet.iter_rows(min_row=2, max_row=2, min_col=1, max_col=4, values_only=True):
    nombre_empleado = str(fila[0]).lower().title()
    monto_venta = fila[1]
    meta_venta = fila[2]
    correo_destinatario = f'{nombre_empleado} <{fila[3]}>'

    try:
        # Configuración del mensaje de correo
        asunto = 'Información reporte de venta'

        cuerpo_mensaje = f'Hola {nombre_empleado},\n\nTu venta del día fue de ${"{:,.2f}".format(monto_venta)}.\n\nTu meta diaria de ${"{:,.2f}".format(meta_venta)}.\n\nAlcanzaste el {"{:,.2f}".format(monto_venta / meta_venta * 100)}% de tu meta.'

        mensaje = MIMEMultipart()
        mensaje['From'] = correo_emisor
        mensaje['To'] = correo_destinatario
        mensaje['Subject'] = asunto
        mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

        # Establecer la conexión con el servidor SMTP de Gmail
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(correo_emisor, contraseña_emisor)

            # Enviar el correo
            server.sendmail(correo_emisor, correo_destinatario, mensaje.as_string())

    except Exception as e:
        # Mostrar un mensaje de error utilizando QMessageBox
        QMessageBox.critical(None, 'Error', f'Error al enviar correo: {str(e)}')

print('Correos enviados exitosamente.')

# Cerrar el archivo Excel
workbook.close()

# Salir de la aplicación de PyQt
app.exec_()
