from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox
import os

def get_connection_string():
    try:
        # Obtener la ruta al archivo de conexión
        connection_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'txt', 'connection_string2.txt')
        
        # Leer la cadena de conexión del archivo
        with open(connection_file, 'r') as file:
            connection_string = file.read().strip()
            return connection_string
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error leyendo el archivo de conexión: {str(e)}")
        return None

def connect_to_db():
    try:
        if 'qt_sql_default_connection' in QSqlDatabase.connectionNames():
            QSqlDatabase.removeDatabase('qt_sql_default_connection')
        
        connection_string = get_connection_string()
        if not connection_string:
            QMessageBox.critical(None, "Error", "No se pudo obtener la cadena de conexión")
            return None
        
        db = QSqlDatabase.addDatabase('QODBC')
        db.setDatabaseName(connection_string)
        
        if not db.open():
            QMessageBox.critical(None, "Error", f"Error al conectar a la base de datos: {db.lastError().text()}")
            return None
            
        # Quitar el mensaje de conexión exitosa
        return db
        
    except Exception as e:
        QMessageBox.critical(None, "Error", f"Error en la conexión: {str(e)}")
        return None

def close_db(db):
    if db:
        try:
            db.close()
            # Quitar el mensaje de cierre exitoso
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al cerrar la conexión: {str(e)}")

def close_db(db):
    if db:
        try:
            db.close()
            #QMessageBox.information(None, "Éxito", "Conexión cerrada exitosamente")
        except Exception as e:
            QMessageBox.critical(None, "Error", f"Error al cerrar la conexión: {str(e)}")