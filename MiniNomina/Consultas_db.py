from PyQt5.QtWidgets import QTableView, QTabWidget,QTableWidget, QTableWidgetItem, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5 import QtWidgets
from Conexion_db import conectar_db




def insertar_nuevo_empleados(Nombre, Num_banca, Salario):
    
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO empleados (nombre, num_banca, salario) VALUES (?, ?, ?)", (Nombre, Num_banca, Salario))
        conn.commit()

        # Cerrar la conexión
        conn.close()
        
        
def insertar_nuevo_faltante(Fecha, Nombre, Num_banca, Abono, Faltante):
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO faltantes (fecha ,nombre, banca, abono, faltante) VALUES (?, ?, ?, ?, ?)", (Fecha, Nombre, Num_banca, Abono, Faltante))
        conn.commit()

        # Cerrar la conexión
        conn.close()
        
        
def mostrar_datos_de_faltantes(tbtabla):
    # Conectar a la base de datos    
    db = QSqlDatabase.addDatabase("QSQLITE")
    db.setDatabaseName("C:\\Users\\acer\\OneDrive\\Documentos\\GitHub\\DevelopPython\\Base de datos\\MiniNomina.db")
    if not db.open():
        QMessageBox.critical(None, "Error", "No se pudo abrir la base de datos")
        return

        
    
    # Crear un modelo de tabla SQL
    model = QSqlTableModel()
    model.setTable("faltantes")
    model.select()

    # Establecer el modelo en la tabla
    tbtabla.setModel(model)

    # Ajustar el tamaño de las columnas para que se ajusten al contenido
    tbtabla.resizeColumnsToContents()

    # Cerrar la conexión
    #db.close() 