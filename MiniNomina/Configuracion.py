from PyQt5.QtWidgets import QFileDialog, QMessageBox
import os

def funcion_de_conexion():
    ruta_configuracion = "MiniNomina/configuracion.txt"

    # Crear archivo de configuración si no existe
    if not os.path.exists(ruta_configuracion):
        with open(ruta_configuracion, "w") as f:
            f.write("")  # Escribir un archivo vacío

    with open(ruta_configuracion, "r") as f:
        ruta_guardada = f.read().strip()

    if ruta_guardada or not ruta_guardada:
        # La configuración no tiene una ruta de base de datos
        # Se debe pedirle al usuario que seleccione la ruta
        ruta_seleccionada, _ = QFileDialog.getOpenFileName(None, "Seleccionar base de datos", "", "Archivos de base de datos (*.db)")
        
        
        # Se guarda la ruta seleccionada en el archivo de configuración
        with open(ruta_configuracion, "w") as f:
            f.write(ruta_seleccionada)
            
        if not ruta_seleccionada:    
            QMessageBox.information(None, "Cancelado", "No seleccionaste la base de datos, la aplicacion se va a cerrar.") # type: ignore
        else:
            QMessageBox.information(None, "Base de datos configurada", "Reinicia la aplicaion para terminar la configuracion.") # type: ignore
                