from PIL import Image
import pytesseract
import openpyxl

# Configuración de pytesseract para la ruta del ejecutable de Tesseract OCR
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files (x86)\Tesseract-OCR\tesseract.exe'

# Ruta de la imagen
imagen_ruta = 'C:/Users/acer/OneDrive/Documentos/GitHub/DevelopPython/Bono/WhatsApp Image 2023-11-29 at 07.09.56.jpeg'

# Leer texto de la imagen con pytesseract
texto_extraido = pytesseract.image_to_string(Image.open(imagen_ruta))

# Procesar el texto extraído (esto dependerá de cómo esté estructurado tu texto)
lineas = texto_extraido.split('\n')
datos = []

for linea in lineas:
    # Aquí deberías implementar la lógica para extraer y organizar tus datos
    # Por ejemplo, podrías dividir la línea en campos usando algún delimitador

    # Ejemplo: Supongamos que los campos están separados por comas
    campos = linea.split(',')
    datos.append(campos)

# Crear un archivo Excel y escribir los datos
libro_excel = openpyxl.Workbook()
hoja_excel = libro_excel.active

for fila in datos:
    hoja_excel.append(fila)

# Guardar el archivo Excel
libro_excel.save('datos_extraidos.xlsx')
