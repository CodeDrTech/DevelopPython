import sqlite3
from PyQt5.QtSql import QSqlQuery, QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QTableView

#def conectar_db():
    #conn = sqlite3.connect('C:\\Users\\Jose\\Documents\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db')
    #return conn


def conectar_db():
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName('C:\\Users\\Jose\\Documents\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db')
    if not db.open():
        print("No se pudo conectar a la base de datos")
        return None
    return db
