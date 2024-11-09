import pyodbc
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QMessageBox


#---------------------------------------------Este modulo esta comentado---------------------------------------------------------
# Read the configuration file connection_string.txt, which contains the database connection string.
def read_database_config():
    config_path = "Sistema de ventas/txt/connection_string.txt"
    
    with open(config_path, "r") as file:
        connection_string = file.read().strip()
    
    return connection_string
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Connect to the SQL Server.
def connect_to_db():
    connection_string = read_database_config()
    
    try:
        conn = pyodbc.connect(connection_string)        
        return conn
    except Exception as e:
        message = QMessageBox()
        message.setIcon(QMessageBox.Critical)
        message.setWindowTitle("Error")
        message.setText(f"An error occurred: {str(e)}")
        message.exec_()
        return None

# --------------------------------------------------------------------------------------------
# --------------------------------------------------------------------------------------------

# Connect to the database using the driver used by PyQt for QODBC.
connection_string = read_database_config()
db = QSqlDatabase.addDatabase("QODBC")
db.setDatabaseName(connection_string)
