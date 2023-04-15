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
        
    # Crear un modelo de tabla SQL
    model = QSqlTableModel()
    model.setTable("faltantes")
    # Establecer el filtro por nombre
    #model.setFilter("")
    
    # Establecer el orden por nombre en orden ascendente
    model.setSort(0, Qt.DescendingOrder) # type: ignore    

    model.select()
    
    
    
    # Aqui empieza el codigo nuevo-----------------------------------
    # Agregar una nueva fila al final de la tabla
    suma_faltante = model.rowCount()
    model.insertRow(suma_faltante)

    # Calcular la suma de la columna
    query = QSqlQuery()
    query.exec_("SELECT SUM(FALTANTE - ABONO) FROM faltantes")
    if query.next():
        total = query.value(0)
    else:
        total = 0

    # Establecer la suma en la celda correspondiente de la nueva fila
    model.setData(model.index(suma_faltante, 4), total)
    # Aqui termina--------------------------------------------------------
    
    
    
    # Establecer el modelo en la tabla
    tbtabla.setModel(model)

    # Ajustar el tamaño de las columnas para que se ajusten al contenido
    tbtabla.resizeColumnsToContents()
    
    
    # Conectar la señal QCloseEvent de la ventana al método de eliminación de la fila de la suma
    tbtabla.window().closeEvent = lambda event: eliminar_fila_de_suma_faltante(model, suma_faltante, event)

def eliminar_fila_de_suma_faltante(model, suma_faltante, event):
    # Eliminar la fila de la suma
    model.removeRow(suma_faltante)
    # Continuar con el evento de cierre de la ventana
    event.accept()
                   
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
# Función que muestra los datos de los empleados en QTableView del FrmDatos    
def mostrar_datos_de_empleados(tbtabla):
        
    # Crear un modelo de tabla SQL
    model = QSqlTableModel()
    model.setTable("empleados")
    model.select()
    
    # Establecer el modelo en la tabla
    tbtabla.setModel(model)

    # Ajustar el tamaño de las columnas para que se ajusten al contenido
    tbtabla.resizeColumnsToContents()
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
#def select_total(tbtabla):
    
    # Conectar a la base de datos
    #conn = conectar_db()

    # Realizar la inserción en la base de datos
    #cursor = conn.execute("SELECT * FROM faltantes")
    #rows = cursor.fetchall()
    
    # Crear un modelo de tabla y agregar los datos
    #model = QStandardItemModel(len(rows), len(rows[0]))
    #for i, row in enumerate(rows):
        #for j, col in enumerate(row):
            #item = QStandardItem(str(col))
            #model.setItem(i, j, item)

    # Cerrar la conexión
    #conn.close()
    # Asignar el modelo a tu QTableView
    #tbtabla.setModel(model)
    #tbtabla.resizeColumnsToContents()
    #tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)