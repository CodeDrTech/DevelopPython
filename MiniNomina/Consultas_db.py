from PyQt5.QtWidgets import QTableView, QTabWidget,QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5 import QtWidgets
from Conexion_db import conectar_db, db
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel

    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
def insertar_nuevo_empleados(Nombre, Num_banca, Salario):
    
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO empleados (nombre, banca, salario) VALUES (?, ?, ?)", (Nombre, Num_banca, Salario))
        conn.commit()

        # Cerrar la conexión
        conn.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
def insertar_nuevo_faltante(Fecha, Nombre, Num_banca, Abono, Faltante):
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO faltantes (fecha ,nombre, banca, abono, faltante) VALUES (?, ?, ?, ?, ?)", (Fecha, Nombre, Num_banca, Abono, Faltante))
        conn.commit()

        # Cerrar la conexión
        conn.close()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
# Función que muestra los datos de los faltantes en QTableView del FrmDatos        
def mostrar_datos_de_faltantes(tbtabla):
    query = QSqlQuery()
    query.exec_("SELECT e.NOMBRE, 
       COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS TOTAL_FALTANTES,
       COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS TOTAL_ABONOS,
       e.SALARIO - COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) + COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS SALARIO_NETO FROM empleados e;")

   
    # Crear un modelo de tabla SQL
    model = QSqlTableModel()
    #model.setTable("faltantes")#
    
    model.setQuery(query)
    
    # Establecer el orden en orden ascendente
    #model.setSort(0, Qt.DescendingOrder) # type: ignore    
    #model.select()   
    
    # Establecer el modelo en la tabla
    tbtabla.setModel(model)

    # Ajustar el tamaño de las columnas para que se ajusten al contenido
    tbtabla.resizeColumnsToContents()
                   
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
# Función que muestra los datos de los empleados en QTableView del FrmDatos    
def mostrar_datos_de_empleados(tbtabla):
        
    # Crear un modelo de tabla SQL
    model = QSqlTableModel()
    model.setTable("empleados")
    
    # Establecer el orden en orden ascendente
    model.setSort(0, Qt.AscendingOrder) # type: ignore
    model.select()
    
    # Establecer el modelo en la tabla
    tbtabla.setModel(model)

    # Ajustar el tamaño de las columnas para que se ajusten al contenido
    tbtabla.resizeColumnsToContents()
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------