import sqlite3
from PyQt5.QtSql import QSqlQuery, QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QTableView

def ruta_database():
    Ruta = 'C:\\Users\\Jose\\Documents\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db'
    Ruta2 = 'C:\\Users\\acer\\OneDrive\\Documentos\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db'
    return Ruta2
def conectar_db():
    conn = sqlite3.connect(ruta_database())#'C:\\Users\\acer\\OneDrive\\Documentos\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db')
    return conn


