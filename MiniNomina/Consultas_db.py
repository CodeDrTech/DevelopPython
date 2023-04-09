from PyQt5.QtWidgets import QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
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
        
        
def mostrar_datos_de_faltantes():
    # Conectar a la base de datos
    conn = conectar_db()

    # Ejecutar la consulta SELECT
    query = QSqlQuery()
    query.prepare("SELECT * FROM faltantes")
    if not query.exec():
        print("Error al ejecutar la consulta:", query.lastError().text())
        return

    # Crear un modelo de tabla para los resultados de la consulta
    model = QSqlTableModel()
    model.setQuery(query)

    # Crear una vista de tabla para mostrar los resultados de la consulta
    view = QTableView()
    view.setModel(model)
    view.show()

    # Cerrar la conexión a la base de datos
    conn.close()