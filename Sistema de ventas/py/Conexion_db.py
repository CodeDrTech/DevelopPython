import mysql.connector
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QMessageBox


# Función para leer la cadena de conexión de un archivo de configuración
def read_database_config():
    import json
    config_path = "Sistema de ventas/txt/connection_string.txt"
    
    with open(config_path, "r") as file:
        config = json.load(file)
    
    return config


# Función para conectar a la base de datos MySQL
def connect_to_db():
    config = read_database_config()
    
    try:
        conn = mysql.connector.connect(**config)
        return conn
    except Exception as e:
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setText(f"An error occurred: {str(e)}")
        message.exec_()
        return None
