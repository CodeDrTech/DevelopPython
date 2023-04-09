import sqlite3
from PyQt5.QtSql import QSqlQuery, QSqlDatabase, QSqlTableModel
from PyQt5.QtWidgets import QTableView

def conectar_db():
    conn = sqlite3.connect('C:\\Users\\Jose\\Documents\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db')
    return conn