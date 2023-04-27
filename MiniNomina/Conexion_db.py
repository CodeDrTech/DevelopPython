import sqlite3
from PyQt5.QtSql import QSqlDatabase
from PyQt5.QtWidgets import QMessageBox

def ruta_database():
    Ruta = 'C:\\Users\\Jose\\Documents\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db'
    Ruta2 = 'C:\\Users\\acer\\OneDrive\\Documentos\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db'
    return Ruta2

def conectar_db():
    conn = sqlite3.connect(ruta_database())
    return conn


db = QSqlDatabase.addDatabase("QSQLITE")
db.setDatabaseName(ruta_database())

