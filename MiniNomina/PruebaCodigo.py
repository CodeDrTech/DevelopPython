from PyQt5.QtWidgets import QTableView
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from Conexion_db import conectar_db, conectar_db_db

def mostrar_datos_de_faltantes():
    # Conectar a la base de datos
    conn = conectar_db()

    # Verificar que la conexión se ha establecido correctamente
    if not conn:
        print("Error al conectar a la base de datos.")
        return

    # Ejecutar la consulta SELECT
    query = QSqlQuery()
    if not query.prepare("SELECT * FROM faltantes"):
        print("Error al preparar la consulta:", query.lastError().text())
        return
    if not query.exec():
        print("Error al ejecutar la consulta:", query.lastError().text())
        return

    # Verificar que la consulta ha devuelto resultados
    if not query.first():
        print("La consulta no ha devuelto resultados.")
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

