import os
import locale
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import QMessageBox
#--------------------------------------------------------- Envio de reportes sin meta diaria.
# Configurar la localización para el formato de moneda
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Obtener la ruta completa del archivo Excel
archivo_excel = os.path.join(os.path.dirname(__file__), 'ventas.xlsx')
hoja_excel = 'Envios'

# Configuración del servidor SMTP de Gmail
correo_emisor = 'jperez@selactcorp.com'
contraseña_emisor = 'qsmikukzanvbchro' # del otro correo jgtlqydfeuosgzma.


# Leer el archivo Excel
workbook = openpyxl.load_workbook(archivo_excel, data_only=True)
sheet = workbook[hoja_excel]

# Recorrer las filas del archivo Excel
for fila in sheet.iter_rows(min_row=3, max_row=30, min_col=1, max_col=9, values_only=True):
    nombre_empleado = str(fila[0]).lower().title()
    monto_venta = fila[1] if fila[1] is not None else 0
    
    
    
    # Manejar casos especiales en correo_destinatario
    correo_destinatario = f'{nombre_empleado} <{str(fila[8]) if fila[8] is not None and fila[8] != "#N/D" else "jperez@selactcorp.com"}>'

    
    # Verificar si el correo_destinatario es válido antes de intentar enviar el correo
    if "@" in correo_destinatario:
        try:
            # Configuración del mensaje de correo
            asunto = 'Información sobre los pedidos'

            cuerpo_mensaje = f'Buenos dias {nombre_empleado}.\n\nEl día de hoy los pedidos estan bajos, necesitamos de tu colaboracion para que estos aumenten para el final del día, gracias.\n\nMensaje de Jose Alfredo Tejeda.'

            mensaje = MIMEMultipart()
            mensaje['From'] = f'Pedidos de ventas <{correo_emisor}>'
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
            # Mostrar un mensaje de error en la consola
            print(f"Error al enviar el correo: {str(e)}")

print("Correos enviado exitosamente.")

# Cerrar el archivo Excel
workbook.close()
