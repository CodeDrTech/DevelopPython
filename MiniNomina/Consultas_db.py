from PyQt5.QtWidgets import QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from Conexion_db import conectar_db



def insertar_nuevo_empleados(Nombre, Num_banca, Salario):
    
    # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO empleados (nombre, num_banca, salario) VALUES (?, ?, ?)", (Nombre, Num_banca, Salario))
        conn.commit()

        # Cerrar la conexión
        conn.close()