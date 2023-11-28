import os
import locale
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.image import MIMEImage
import matplotlib.pyplot as plt
from PyQt5.QtCore import QDate

# Configurar la localización para el formato de moneda
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Obtener la ruta completa del archivo Excel
archivo_excel = os.path.join(os.path.dirname(__file__), 'ventas.xlsx')
hoja_excel = 'Envios'

# Configuración del servidor SMTP de Gmail
correo_emisor = 'jperez@selactcorp.com'
contraseña_emisor = 'qsmikukzanvbchro'

# Leer el archivo Excel
workbook = openpyxl.load_workbook(archivo_excel, data_only=True)
sheet = workbook[hoja_excel]

# Obtener la fecha actual
fecha = QDate.currentDate()
fecha_formato = fecha.toString("dd-MMMM-yyyy")

# Variable para indicar si hubo algún error
error_envio = False

# Recorrer las filas del archivo Excel
for fila in sheet.iter_rows(min_row=3, max_row=30, min_col=1, max_col=9, values_only=True):
    nombre_empleado = str(fila[0]).lower().title()

    try:
        # Datos de la semana
        dias_semana = ['Lunes', 'Martes', 'Miércoles', 'Jueves', 'Viernes', 'Sábado']
        ventas_semana = [fila[6], fila[5], fila[4], fila[3], fila[2], fila[1]]
        suma_semanal = fila[7] if fila[7] is not None else 0
        # Crear gráfico de barras
        plt.bar(dias_semana, ventas_semana, color='blue')
        plt.xlabel('Días de la semana')
        plt.ylabel('Ventas diarias')
        plt.title(f'Reporte Semanal -- {nombre_empleado} -- ${"{:,.2f}".format(suma_semanal)}')

        # Agregar etiquetas sobre cada barra
        for i, valor in enumerate(ventas_semana):
            plt.text(i, valor, f'${"{:,.2f}".format(valor) if valor is not None else "N/A"}', ha='center', va='bottom')

        # Calcular la suma de las ventas de la semana
        suma_ventas = sum(venta for venta in ventas_semana if venta is not None)

        # Agregar la etiqueta con la suma en el gráfico
        #plt.text(len(dias_semana) - 0.5, max(ventas_semana), f'Suma Semanal: ${"{:,.2f}".format(suma_ventas)}', ha='right', va='bottom')

        # Guardar la imagen en un archivo
        imagen_path = f'grafico_{nombre_empleado}.png'
        plt.savefig(imagen_path)
        plt.close()

        # Configuración del mensaje de correo con el enlace a la imagen
        asunto = 'Información sobre reporte de ventas'
        cuerpo_mensaje = f'''Buenas tardes {nombre_empleado},\n\nAdjunto el reporte semanal con las ventas diarias.\n\n'''

        mensaje = MIMEMultipart()
        mensaje['From'] = f'Notificacion de reporte {correo_emisor}'
        mensaje['To'] = f'{nombre_empleado} <{str(fila[8]) if fila[8] is not None and fila[8] != "#N/D" else "jperez@selactcorp.com"}>'
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

    except Exception as e:
        # Mostrar un mensaje de error en la consola
        print(f"Error al enviar correo a {nombre_empleado}: {str(e)}")
        error_envio = True

# Mensaje de éxito o error al final
if error_envio:
    print("Error al enviar correos.")
else:
    print("Correos enviados exitosamente.")

# Cerrar el archivo Excel
workbook.close()
