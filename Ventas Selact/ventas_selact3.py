import os
import locale
import openpyxl
import base64
from PyQt5.QtCore import QDate
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import matplotlib.pyplot as plt
import io
from email import encoders
from email.mime.base import MIMEBase
from base64 import b64encode
from PyQt5.QtWidgets import QApplication, QMessageBox

# Configurar la localización para el formato de moneda
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Obtener la ruta completa del archivo Excel
archivo_excel = os.path.join(os.path.dirname(__file__), 'Pruebas.xlsx')
hoja_excel = 'Hoja2'

# Configuración del servidor SMTP de Gmail
correo_emisor = 'jperez@selactcorp.com'
contraseña_emisor = 'qsmikukzanvbchro'

# Leer el archivo Excel
workbook = openpyxl.load_workbook(archivo_excel, data_only=True)
sheet = workbook[hoja_excel]

# Iniciar la aplicación de PyQt
app = QApplication([])

fecha = QDate.currentDate()
fecha_formato = fecha.toString("MMMM yyyy")  # Formato mes y año

# Obtener los datos para el total general
nombre_total_general = sheet['A28'].value
monto_total_general = sheet['C28'].value

# Recorrer las filas del archivo Excel
vendedores = []
montos = []

try:
    for fila in sheet.iter_rows(min_row=3, max_row=27, min_col=1, max_col=4, values_only=True):
        nombre_empleado = str(fila[0]).lower().title()
        monto_mensual = fila[2] if fila[2] is not None else 0
        
        
        palabras = nombre_empleado.split()

        # Obtener las iniciales de cada palabra
        iniciales = [palabra[0] for palabra in palabras]

        # Unir las iniciales en un solo string
        iniciales_str = ''.join(iniciales)
        
        

        vendedores.append(iniciales_str)
        montos.append(monto_mensual)

        # Verificar si se han recopilado 5 vendedores, luego generar el gráfico y reiniciar las listas
        if len(vendedores) == 5:
            # Crear gráfico de barras
            plt.bar(vendedores, montos, color='blue')
            plt.xlabel('Vendedores')
            plt.ylabel('Monto Mensual')
            plt.title(f'Reporte Mensual - {fecha_formato}')

            # Agregar etiquetas sobre cada barra
            for i, valor in enumerate(montos):
                plt.text(i, valor, f'${"{:,.2f}".format(valor)}', ha='center', va='bottom')

            # Guardar la imagen en un archivo
            imagen_path = f'grafico_{nombre_total_general}.png'
            plt.savefig(imagen_path)
            plt.close()

            # Restablecer las listas para el próximo conjunto de vendedores
            vendedores = []
            montos = []

            # Configuración del mensaje de correo con el enlace a la imagen
            asunto = f'Reporte Mensual - {fecha_formato}'
            cuerpo_mensaje = f'Hola {nombre_total_general},\n\nAdjunto el reporte mensual de los vendedores.\n\n'

            mensaje = MIMEMultipart()
            mensaje['From'] = f'Notificación de venta <{correo_emisor}>'
            mensaje['To'] = f'{nombre_total_general} <{sheet["D3"].value}>'
            mensaje['Subject'] = asunto

            # Adjuntar texto al cuerpo del correo
            mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

            # Adjuntar imagen al cuerpo del correo
            with open(imagen_path, 'rb') as archivo_imagen:
                imagen_adjunta = MIMEImage(archivo_imagen.read())
                imagen_adjunta.add_header('Content-Disposition', 'attachment', filename=os.path.basename(imagen_path))
                mensaje.attach(imagen_adjunta)

            # Establecer la conexión con el servidor SMTP de Gmail y enviar el correo
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(correo_emisor, contraseña_emisor)
                server.sendmail(correo_emisor, mensaje['To'], mensaje.as_string())

            QMessageBox.information(None, 'Correo Enviado', 'El correo se envió correctamente.')

except Exception as e:
    QMessageBox.critical(None, 'Error al enviar correo', f'Se produjo un error al enviar el correo: {str(e)}')

# Cerrar el archivo Excel
workbook.close()

# Salir de la aplicación de PyQt
app.exec_()
