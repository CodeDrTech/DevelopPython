import pyodbc
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QMessageBox



# Funcion que lee la ruta a la base de datos establecida en el archivo configuracion.txt
def ruta_database():
    ruta_configuracion = "Sistema de ventas/txt/configuracion.txt"
    
    with open(ruta_configuracion, "r") as f:
         cadena_conexion = f.read().strip()
    
    return cadena_conexion
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Funcion usada para insertar datos a la base de datos.
def conectar_db():
    cadena_conexion = ruta_database()
    
    try:
        
        conn = pyodbc.connect(cadena_conexion)        
        return conn
    except Exception as e:
        mensaje = QMessageBox()
        mensaje.setIcon(QMessageBox.Critical)
        mensaje.setWindowTitle("Error")
        mensaje.setText(f"Se produjo un error: {str(e)}")
        mensaje.exec_()
        return None
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

        
# Conexion a la base de datos mediante driver usado por PYQT para QODBC.
cadena_conexion = ruta_database()
db = QSqlDatabase.addDatabase("QODBC")
db.setDatabaseName(cadena_conexion)#"DRIVER={SQL Server Native Client 11.0};SERVER=LAPTOPTECNOLOGI;DATABASE=Ventas;UID=sa;PWD=Ye.891916;")
