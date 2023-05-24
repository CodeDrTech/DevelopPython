from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os


# Busca la ruta de la base de datos segun elija el usuario y la escribe en el archivo configuracion.txt
def funcion_de_conexion():
    ruta_configuracion = "MiniNomina/txt/configuracion.txt"

    # Crear archivo de configuración si no existe
    if not os.path.exists(ruta_configuracion):
        with open(ruta_configuracion, "w") as f:
            f.write("")  # Escribir un archivo vacío
    # Abre y lee al archivo configuracion.txt
    with open(ruta_configuracion, "r") as f:
        ruta_guardada = f.read().strip()

    # Si le archivo esta vacío o con informacion se le pide al usuario seleccionar una ruta de base de datos.
    if ruta_guardada or not ruta_guardada:
        # Mensaje que pide al usuario seleccionar la ruta a la base de datos.
        ruta_seleccionada, _ = QFileDialog.getOpenFileName(None, "Seleccionar base de datos", "", "Archivos de base de datos (*.db)")
        
        
        # Se guarda la ruta seleccionada en el archivo de configuración
        with open(ruta_configuracion, "w") as f:
            f.write(ruta_seleccionada)
        
        # Mensajes enviados al usuario partiendo de la decision que tomó.    
        if not ruta_seleccionada:    
            QMessageBox.information(None, "Cancelado", "No seleccionaste la base de datos, la aplicacion se va a cerrar.") # type: ignore
        else:
            QMessageBox.information(None, "Base de datos configurada", "Se reiniciara la aplicaion para terminar la configuracion.") # type: ignore
                