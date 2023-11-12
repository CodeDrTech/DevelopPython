import os
import locale
import openpyxl
import base64
from PyQt5.QtCore import QDate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
from email.mime.base import MIMEBase
from email import encoders
import matplotlib.pyplot as plt
import io
from base64 import b64encode
from PyQt5.QtWidgets import QApplication, QMessageBox

# Configurar la localización para el formato de moneda
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Obtener la ruta completa del archivo Excel
archivo_excel = os.path.join(os.path.dirname(__file__), 'ventas.xlsx')
hoja_excel = 'Hoja1'

# Configuración del servidor SMTP de Gmail
correo_emisor = 'jperez@selactcorp.com'
contraseña_emisor = 'qsmikukzanvbchro'

# Leer el archivo Excel
workbook = openpyxl.load_workbook(archivo_excel)
sheet = workbook[hoja_excel]

# Iniciar la aplicación de PyQt
app = QApplication([])

fecha = QDate.currentDate()
fecha_formato = fecha.toString("dd-MMMM-yyyy")

# Recorrer las filas del archivo Excel
for fila in sheet.iter_rows(min_row=2, max_row=2, min_col=1, max_col=4, values_only=True):
    nombre_empleado = str(fila[0]).lower().title()
    monto_venta = fila[1]
    meta_venta = fila[2]
    correo_destinatario = f'{nombre_empleado} <{fila[3]}>'

    try:
        # Crear gráfico de barras
        categorias = ['Venta', 'Meta']
        valores = [monto_venta, meta_venta]

        plt.bar(categorias, valores, color=['blue', 'green'])
        plt.xlabel('Categoría')
        plt.ylabel('Monto')
        plt.title(f'Ventas de {nombre_empleado} hoy {fecha_formato}')

        # Agregar etiquetas sobre cada barra
        for i, valor in enumerate(valores):
            plt.text(i, valor, f'${"{:,.2f}".format(valor)}', ha='center', va='bottom')

        # Guardar la imagen en un archivo
        imagen_path = 'grafico_barras.png'
        plt.savefig(imagen_path)
        plt.close()

        # Configuración del mensaje de correo con el enlace a la imagen
        asunto = 'Información reporte de venta'
        cuerpo_mensaje = f'Hola {nombre_empleado},\n\nTu venta del día fue de ${"{:,.2f}".format(monto_venta)}\n\nTu meta diaria de ${"{:,.2f}".format(meta_venta)}\n\nAlcanzaste el {"{:,.2f}".format(monto_venta / meta_venta * 100)}% de tu meta.\n\nConsulta el gráfico de barras de tu rendimiento ajunta.'''

        mensaje = MIMEMultipart()
        mensaje['From'] = f'Notificacion <{correo_emisor}>'
        mensaje['To'] = correo_destinatario
        mensaje['Subject'] = asunto

        # Adjuntar texto al cuerpo del correo
        mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

        # Adjuntar imagen al cuerpo del correo
        with open(imagen_path, 'rb') as archivo_imagen:
            imagen_adjunta = MIMEBase('application', 'octet-stream')
            imagen_adjunta.set_payload(archivo_imagen.read())
            encoders.encode_base64(imagen_adjunta)
            imagen_adjunta.add_header('Content-Disposition', 'attachment', filename=os.path.basename(imagen_path))
            imagen_adjunta.add_header('Content-ID', '<grafico_barras>')
            mensaje.attach(imagen_adjunta)

        
        

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
