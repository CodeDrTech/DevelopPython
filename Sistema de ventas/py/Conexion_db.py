import sqlite3
from PyQt5.QtSql import QSqlDatabase



# Funcion que lee la ruta a la base de datos establecida en el archivo configuracion.txt
def ruta_database():
    ruta_configuracion = "Sistema de ventas/txt/configuracion.txt"
    with open(ruta_configuracion, "r") as f:
         ruta_guardada = f.read().strip()
    
    Ruta = ruta_guardada
    return Ruta

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Funcion usada para insertar datos a la base de datos.
def conectar_db():
    conn = sqlite3.connect(ruta_database())
    return conn
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Conexion a la base de datos mediante driver usado por PYQT para QSQLITE.
db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(ruta_database())