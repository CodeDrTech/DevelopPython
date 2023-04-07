import sqlite3

def conectar_db():
    conn = sqlite3.connect('C:\\Users\\Jose\\Documents\\Base de datos\\MiniNomina.db')
    return conn
