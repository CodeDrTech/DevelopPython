import os
import locale
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from PyQt5.QtWidgets import QMessageBox
#--------------------------------------------------------- Envio de reportes sin meta diaria.
# Configurar la localización para el formato de moneda.
locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')

# Obtener la ruta completa del archivo Excel
archivo_excel = os.path.join(os.path.dirname(__file__), 'ventas.xlsx')
hoja_excel = 'Envios'

# Configuración del servidor SMTP de Gmail
correo_emisor = 'jperez@selactcorp.com'
contraseña_emisor = 'ggauphuvqfuzjlhm' 

# Leer el archivo Excel
workbook = openpyxl.load_workbook(archivo_excel, data_only=True)
sheet = workbook[hoja_excel]

# Recorrer las filas del archivo Excel
for fila in sheet.iter_rows(min_row=6, max_row=31, min_col=1, max_col=5, values_only=True):
    nombre_empleado = str(fila[0]).lower().title()
    monto_venta = fila[1] if fila[1] is not None else 0
    cant_pedidos = fila[2] if fila[2] is not None else 0
    
    
    
    # Manejar casos especiales en correo_destinatario
    correo_destinatario = f'{nombre_empleado} <{str(fila[3]) if fila[3] is not None and fila[3] != "#N/D" else "jperez@selactcorp.com"}>'
    correos_copia = ['dvarela@selactcorp.com', 'atejeda@selactcorp.com']  # Lista de correos a los que se enviará una copia
    
    # Convierte la lista de correos de copia en una cadena de texto
    correos_copia_str = ', '.join(correos_copia)

    
    # Verificar si el correo_destinatario es válido antes de intentar enviar el correo
    if "@" in correo_destinatario:
        try:
            # Configuración del mensaje de correo
            asunto = 'Información sobre reporte de ventas'

            cuerpo_mensaje = f'Buenas tardes {nombre_empleado}.\n\nTus ventas en el día de ayer suman un total de ${"{:,.2f}".format(monto_venta)}\n\nCantidad de pedidos {cant_pedidos}'

            mensaje = MIMEMultipart()
            mensaje['From'] = f'Notificacion de reporte <{correo_emisor}>'
            mensaje['To'] = correo_destinatario
            mensaje['CC'] = correos_copia_str
            mensaje['Subject'] = asunto
            mensaje.attach(MIMEText(cuerpo_mensaje, 'plain'))

            # Establecer la conexión con el servidor SMTP de Gmail
            with smtplib.SMTP('smtp.gmail.com', 587) as server:
                server.starttls()
                server.login(correo_emisor, contraseña_emisor)

                # Enviar el correo
                server.sendmail(correo_emisor, [correo_destinatario] + correos_copia, mensaje.as_string())

        except Exception as e:
            # Mostrar un mensaje de error en la consola
            print(f"Error al enviar el correo: {str(e)}")

print("Correos enviado exitosamente.")

# Cerrar el archivo Excel
workbook.close()
