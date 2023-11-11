import os
import locale
import openpyxl
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

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

# Recorrer las filas del archivo Excel
for fila in sheet.iter_rows(min_row=2, values_only=True):  # Empezamos desde la segunda fila asumiendo que la primera fila contiene encabezados
    nombre_empleado = str(fila[0]).lower().title()

    # Tratar de convertir el valor de fila[1] a un número flotante
    if isinstance(fila[1], (int, float)):
        monto_venta = float(fila[1])
    elif isinstance(fila[1], str):
        try:
            monto_venta = float(fila[1].replace(',', ''))
        except ValueError as e:
            print(f"Error: No se puede convertir '{fila[1]}' a un número flotante. Detalles: {e}")
            continue
    else:
        print(f"Error: Tipo de dato no admitido en la columna de montos.")
        continue

    # Formatear el monto de venta como una cadena con formato de moneda
    monto_venta_str = locale.currency(monto_venta, grouping=True)



    correo_destinatario = fila[2]

    # Configuración del mensaje de correo
    asunto = 'Información de venta'
    cuerpo_mensaje = f'Hola {nombre_empleado},\n\nTu venta del día es de ${monto_venta}.\n\n¡Gracias!'
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

print('Correos enviados exitosamente.')

# Cerrar el archivo Excel
workbook.close()
