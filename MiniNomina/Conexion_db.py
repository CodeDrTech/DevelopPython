import sqlite3
from PyQt5.QtSql import QSqlQuery, QSqlDatabase

def conectar_db():
    conn = sqlite3.connect('C:\\Users\\Jose\\Documents\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db')
    return conn


    # Establecer la conexión a la base de datos
def conectar_db_db():
    db = QSqlDatabase.addDatabase('QSQLITE')
    db.setDatabaseName('MiniNomina.db')
    
    # Comprobar si la base de datos se ha abierto correctamente
    if not db.open():
        print('Error al abrir la base de datos')
        return None
        
    return db