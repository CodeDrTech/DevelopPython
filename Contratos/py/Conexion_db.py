from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from PyQt5.QtWidgets import QMessageBox
import os

def get_connection_string():
    try:
        # Obtener la ruta al archivo de conexión
        connection_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'txt', 'connection_string.txt')
        
        # Leer la cadena de conexión del archivo
        with open(connection_file, 'r') as file:
            connection_string = file.read().strip()
            return connection_string
    except Exception as e:
        print(f"Error leyendo el archivo de conexión: {str(e)}")
        return None

def connect_to_db():
    try:
        # Remover conexión existente si existe
        if 'qt_sql_default_connection' in QSqlDatabase.connectionNames():
            QSqlDatabase.removeDatabase('qt_sql_default_connection')
        
        # Obtener la cadena de conexión
        connection_string = get_connection_string()
        if not connection_string:
            print("No se pudo obtener la cadena de conexión")
            return None
        
        # Crear una nueva conexión
        db = QSqlDatabase.addDatabase('QODBC')
        db.setDatabaseName(connection_string)
        
        # Intentar abrir la conexión
        if not db.open():
            print(f"Error al conectar a la base de datos: {db.lastError().text()}")
            return None
            
        print("Conexión exitosa a SQL Server")
        return db
        
    except Exception as e:
        print(f"Error en la conexión: {str(e)}")
        return None

def close_db(db):
    if db:
        try:
            db.close()
            print("Conexión cerrada exitosamente")
        except Exception as e:
            print(f"Error al cerrar la conexión: {str(e)}")