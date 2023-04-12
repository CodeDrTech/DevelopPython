from PyQt5.QtWidgets import QTableView, QTabWidget,QTableWidget, QTableWidgetItem, QMessageBox, QAbstractItemView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5 import QtWidgets
from Conexion_db import conectar_db, db
import PyQt5.QtCore
from PyQt5.QtGui import QStandardItemModel
#from FrmDatos import VentanaDatos #El error esta aqui


    
    
def insertar_nuevo_empleados(Nombre, Num_banca, Salario):
    
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO empleados (nombre, banca, salario) VALUES (?, ?, ?)", (Nombre, Num_banca, Salario))
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
        
# Función que muestra los datos de los faltantes en QTableView del FrmDatos        
def mostrar_datos_de_faltantes(tbtabla):
        
    # Crear un modelo de tabla SQL
    model = QSqlTableModel()
    model.setTable("faltantes")
    model.select()
    
    # Establecer el modelo en la tabla
    tbtabla.setModel(model)
    
    # Evita que se puedan actualizar los datos de la tabla
    #tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)

    # Ajustar el tamaño de las columnas para que se ajusten al contenido
    tbtabla.resizeColumnsToContents()
                   
    
    
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
    
    
def ver_datos_de_faltantes_por_nombres(tbtabla):
        
        #self.llamar_venana_datos = VentanaDatos()
        #self.llamar_venana_datos.show()
        #self.llamar_venana_datos.datos_en_tabla_empleados_por_nombres()
        
    llamar_a_combobox = VentanaDatos()
    llamar_a_combobox.currentText()
    
            
    # Crear un modelo de tabla SQL
    model = QSqlTableModel()
    model.setTable("faltantes")
    
    # Establecer el filtro por nombre
    model.setFilter(f"nombre = '{llamar_a_combobox}'")
    
    # Seleccionar los datos filtrados
    model.select()
    
    # Establecer el modelo en la tabla
    tbtabla.setModel(model)

    # Ajustar el tamaño de las columnas para que se ajusten al contenido
    tbtabla.resizeColumnsToContents()
