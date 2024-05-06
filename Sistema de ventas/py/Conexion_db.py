import mysql.connector
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QMessageBox

# Configuración de la base de datos directamente en el archivo
DATABASE_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Jose.Luis.8715',
    'database': 'ventas'
}

# Función para conectar a la base de datos MySQL
def connect_to_db():
    try:
        conn = mysql.connector.connect(**DATABASE_CONFIG)
        return conn
    except Exception as e:
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setText(f"An error occurred: {str(e)}")
        message.exec_()
        return None
