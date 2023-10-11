import pyodbc  # Asumiendo que estás utilizando pyodbc para SQL Server
from PyQt5.QtWidgets import QMessageBox

# Esta función debería manejar la conexión a tu base de datos SQL Server
def conectar_db():
    conn = pyodbc.connect("Driver={SQL Server};Server=tu_servidor;Database=Ventas;Trusted_Connection=yes;")
    return conn

def insertar_dato_generico(tabla, columnas, valores):
    conn = conectar_db()

    try:
        cursor = conn.cursor()
        columnas_str = ', '.join(columnas)
        valores_str = ', '.join(['?'] * len(columnas))
        query = f"INSERT INTO {tabla} ({columnas_str}) VALUES ({valores_str})"
        cursor.execute(query, valores)
        conn.commit()
    except Exception as e:
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al insertar datos en la tabla {tabla}: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec_()
    finally:
        conn.close()

def insertar_nuevo_ingreso(idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado):
    conn = conectar_db()

    try:
        cursor = conn.cursor()

        # Paso 1: Insertar un registro en la tabla 'ingreso'
        cursor.execute("INSERT INTO ingreso (idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado) VALUES (?, ?, ?, ?, ?, ?, ?)",
                       (idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado))
        conn.commit()

        # Paso 2: Obtener el ID del ingreso recién insertado
        cursor.execute("SELECT SCOPE_IDENTITY()")
        lastIngresoID = cursor.fetchone()[0]

        # Paso 3: Insertar un registro en la tabla 'detalle_ingreso' haciendo referencia al mismo ID de 'ingreso'
        columnas = ['idingreso', 'idarticulo', 'precio_compra', 'precio_venta', 'cantidad', 'stock', 'fecha_produccion', 'fecha_vencimiento', 'precio_venta1', 'precio_venta2']
        valores = [lastIngresoID, 1, 10.0, 15.0, 100, 100, '2023-10-10', '2024-10-10', 20.0, 25.0]
        insertar_dato_generico('detalle_ingreso', columnas, valores)

    except Exception as e:
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al insertar nuevo ingreso: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
    finally:
        conn.close()
