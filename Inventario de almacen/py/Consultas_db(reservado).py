from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Conexion_db import conectar_db
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox




def obtener_ultimo_codigo():
    conn = conectar_db()
    cursor = conn.execute("SELECT MAX(Codigo) FROM Productos")
    ultimo_codigo = cursor.fetchone()[0]
    conn.close()
    return ultimo_codigo
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def generar_nuevo_codigo(ultimo_codigo):
    if ultimo_codigo is None:
        nuevo_codigo = 0
    else:
        nuevo_codigo = int(ultimo_codigo.replace('PROD', '')) + 1

    nuevo_codigo_formateado = f"PROD{str(nuevo_codigo).zfill(5)}"
    return nuevo_codigo_formateado
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def insertar_nuevo_producto(categoria, nombre, medida):
    
    # Obtener el último código de producto
    ultimo_codigo = obtener_ultimo_codigo()

    # Generar el nuevo código
    nuevo_codigo = generar_nuevo_codigo(ultimo_codigo)

    # Conectar a la base de datos
    conn = conectar_db()

    # Realizar la inserción en la base de datos
    conn.execute("INSERT INTO Productos (Codigo, Categoria, Nombre, Medida) VALUES (?, ?, ?, ?)", (nuevo_codigo, categoria, nombre, medida))
    conn.commit()

    # Cerrar la conexión
    conn.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
def insertar_nuevo_cliente(codigo, nombre):
        
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO Clientes (Codigo, Nombre) VALUES (?, ?)", (codigo, nombre))
        conn.commit()

        # Cerrar la conexión
        conn.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
def insertar_nuevo_proveedor(codigo, nombre):
        
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO Proveedores (Codigo, Nombre) VALUES (?, ?)", (codigo, nombre))
        conn.commit()

        # Cerrar la conexión
        conn.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
def insertar_compras(fecha, proveedor, codigo, categoria, producto, und, comentario, cantidad):
    # Conectar a la base de datos
    conn = conectar_db()

    try:
        # Verificar si el producto ya existe en la tabla Stock
        cursor = conn.execute("SELECT Disponible FROM Stock WHERE Codigo = ?", (codigo,))
        existing_stock = cursor.fetchone()

        if existing_stock:
            # Si el producto existe en Stock, actualizamos la cantidad disponible
            nueva_cantidad = existing_stock[0] + cantidad
            conn.execute("UPDATE Stock SET Disponible = ? WHERE Codigo = ?", (nueva_cantidad, codigo))
        else:
            # Si el producto no existe en Stock, lo agregamos
            conn.execute("INSERT INTO Stock (Codigo, Producto, Disponible) VALUES (?, ?, ?)", (codigo, producto, cantidad))
        
        # Insertar en la tabla Compras
        conn.execute("INSERT INTO Compras (Fecha, Proveedor, Codigo, Categoria, Producto, Und, Comentario, Cantidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (fecha, proveedor, codigo, categoria, producto, und, comentario, cantidad))
        
        # Confirmar los cambios en la base de datos
        conn.commit()
        
    except Exception as e:
        error_message = "Error: " + str(e)
        # Mostrar mensaje de error utilizando QMessageBox
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(error_message)
        msg_box.exec_()
        # Revertir cambios en caso de error
        conn.rollback()
        
    finally:
        # Cerrar la conexión
        conn.close()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 


def insertar_detalle_salida(fecha, cliente, comentario):
    conn = conectar_db()

    try:
        cursor = conn.cursor()
        cursor.execute("INSERT INTO DetalleSalidas (Fecha, Cliente, Comentario) VALUES (?, ?, ?)", (fecha, cliente, comentario))
        conn.commit()
        detalle_salida_id = cursor.lastrowid

        return detalle_salida_id

    except Exception as e:
        # Manejar errores aquí y mostrar un mensaje de error
        error_message = "Error al insertar producto en salida: " + str(e)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(error_message)
        msg_box.exec_()

    finally:
        conn.close()

def insertar_producto_en_salida(id_salida, codigo, categoria, producto_nombre, cantidad):
    conn = conectar_db()

    try:
        # Verificar la cantidad disponible en Stock antes de la inserción
        cursor = conn.execute("SELECT Disponible FROM Stock WHERE Codigo = ?", (codigo,))
        disponible = cursor.fetchone()

        if disponible is not None and cantidad <= disponible[0]:
            # Si la cantidad vendida es menor o igual a la cantidad disponible
            # Insertar un producto en la tabla Salidas
            conn.execute("INSERT INTO Salidas (ID_Salida, Codigo, Categoria, Producto, CantidadTotal) VALUES (?, ?, ?, ?, ?)", (id_salida, codigo, categoria, producto_nombre, cantidad))
            
            # Actualizar la tabla Stock restando la cantidad vendida
            conn.execute("UPDATE Stock SET Disponible = Disponible - ? WHERE Codigo = ?", (cantidad, codigo))

            conn.commit()
        else:
            # Mostrar un mensaje de error si la cantidad vendida supera la cantidad disponible
            error_message = "La cantidad supera la disponible en Stock."
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Critical)
            msg_box.setWindowTitle("Error")
            msg_box.setText(error_message)
            msg_box.exec_()

    except Exception as e:
        # Manejar otros errores aquí y mostrar un mensaje de error
        error_message = "Error al insertar producto en salida: " + str(e)
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Critical)
        msg_box.setWindowTitle("Error")
        msg_box.setText(error_message)
        msg_box.exec_()

    finally:
        conn.close()


