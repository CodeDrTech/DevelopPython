import pandas as pd
import webbrowser as web
import pyautogui as pg
import time
import openpyxl
import os

# Obtener la ruta completa del archivo Excel
archivo_excel = os.path.join(os.path.dirname(__file__), 'ventas2.xlsx')
hoja_excel = 'Hoja1'

# Leer el archivo Excel
workbook = openpyxl.load_workbook(archivo_excel)
sheet = workbook[hoja_excel]

for fila in sheet.iter_rows(min_row=2, max_row=2, min_col=1, max_col=4, values_only=True):
    nombre = str(fila[0]).lower().title()
    venta = str(fila[1])
    meta = str(fila[2])
    celular = fila[3]
    

    # Crear mensaje personalizado
    mensaje = "Hola, " + nombre + "! Tu venta del día fue de " + venta + "Tu meta diaria es de " + meta + " con nosotros 🙌"

    # Abrir una nueva pestaña para entrar a WhatsApp Web usando Chrome
    chrome_path = 'C:/Program Files/Google/Chrome/Application/chrome.exe %s'
    web.get(chrome_path).open(f"https://web.whatsapp.com/send?phone={celular}&text={mensaje}")

    time.sleep(8)           # Esperar 8 segundos a que cargue
    pg.click(1230, 964)      # Hacer clic en la caja de texto
    time.sleep(2)           # Esperar 2 segundos 
    pg.press('enter')       # Enviar mensaje 
    time.sleep(3)           # Esperar 3 segundos a que se envíe el mensaje
    pg.hotkey('ctrl', 'w')  # Cerrar la pestaña
    time.sleep(2)
