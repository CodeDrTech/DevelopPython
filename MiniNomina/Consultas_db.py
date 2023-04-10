from PyQt5.QtWidgets import QTableView, QTabWidget
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from Conexion_db import conectar_db
from FrmDatos import VentanaDatos



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
        
        
def mostrar_datos_de_faltantes(tbTablas):
        # Conectar a la base de datos
        conn = conectar_db()

        # Crear el cursor y ejecutar la consulta SELECT
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM faltantes")

        # Obtener los datos y establecerlos en el QTableView
        datos = cursor.fetchall()
        tbTablas.setRowCount(len(datos))
        tbTablas.setColumnCount(len(datos[0]))
        for fila, registro in enumerate(datos):
                for columna, valor in enumerate(registro):
                        tbTablas.setItem(fila, columna, QtWidgets.QTableWidgetItem(str(valor)))

        # Cerrar la conexión
        conn.close()