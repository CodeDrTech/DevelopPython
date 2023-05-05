import sqlite3
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QMessageBox, QFileDialog
import os
import sys
from PyQt5.QtWidgets import QApplication


# def ruta_database():
#     Ruta = 'C:\\Users\\Jose\\Documents\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db'
#     Ruta2 = 'C:\\Users\\acer\\OneDrive\\Documentos\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db'
#     return Ruta2

# def conectar_db():
#     conn = sqlite3.connect(funcion_de_conexion())
#     return conn


# db = QSqlDatabase.addDatabase("QSQLITE")
# db.setDatabaseName(funcion_de_conexion())


def funcion_de_conexion():
    ruta_db = "ruta/a/la/base/de/datos.db"
    ruta_configuracion = "MiniNomina/configuracion.txt"
    
    # Crear archivo de configuración si no existe
    if not os.path.exists(ruta_configuracion):
        with open(ruta_configuracion, "w") as f:
            f.write("")  # Escribir un archivo vacío
    
    with open(ruta_configuracion, "r") as f:
        ruta_guardada = f.read().strip()
    
    if not ruta_guardada:
        # La configuración no tiene una ruta de base de datos
        # Se debe pedirle al usuario que seleccione la ruta
        ruta_seleccionada, _ = QFileDialog.getOpenFileName(None, "Seleccionar base de datos", "", "Archivos de base de datos (*.db)")
        
        # Se guarda la ruta seleccionada en el archivo de configuración
        with open(ruta_configuracion, "w") as f:
            f.write(ruta_seleccionada)
        
        # Código para crear la base de datos
        
    elif ruta_guardada != ruta_db:
        # La ruta de la base de datos ha cambiado
        # Se debe mostrar un mensaje de error o hacer algo al respecto
        
        # Se pide al usuario que seleccione la nueva ruta de la base de datos
        ruta_seleccionada, _ = QFileDialog.getOpenFileName(None, "Seleccionar base de datos", "", "Archivos de base de datos (*.db)")
        
        # Se guarda la nueva ruta en el archivo de configuración
        with open(ruta_configuracion, "w") as f:
            f.write(ruta_seleccionada)
        
        # Código para actualizar la base de datos
        
    else:
        # La ruta de la base de datos es la misma
        # Se puede continuar con la ejecución del programa
        pass
    return ruta_db

def conectar_db():
    conn = sqlite3.connect(funcion_de_conexion())
    return conn

    #db = QSqlDatabase.addDatabase("QSQLITE")
    #db.setDatabaseName(funcion_de_conexion())
