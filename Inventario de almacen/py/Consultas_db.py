from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Conexion_db import conectar_db
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox
import datetime




def insertar_nuevo_producto(codigo, categoria, nombre, medida):
    
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO Productos (Codigo, Categoria, Nombre, Medida) VALUES (?, ?, ?, ?)", (codigo, categoria, nombre, medida))
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


def insertar_salidas(fecha, cliente, codigo, categoria, producto, comentario, cantidad):
    # Conectar a la base de datos
    conn = conectar_db()

    try:
        # Verificar si el producto existe en la tabla Stock
        cursor = conn.execute("SELECT Disponible FROM Stock WHERE Codigo = ?", (codigo,))
        existing_stock = cursor.fetchone()

        if existing_stock:
            # Verificar si hay suficiente cantidad disponible
            if existing_stock[0] >= cantidad:
                # Actualizar la cantidad disponible en Stock
                nueva_cantidad = existing_stock[0] - cantidad
                conn.execute("UPDATE Stock SET Disponible = ? WHERE Codigo = ?", (nueva_cantidad, codigo))
            else:
                raise Exception("No hay suficiente cantidad disponible")
        else:
            raise Exception("Producto no encontrado en Almacen")
        
        # Insertar en la tabla Salidas (N_doc es autoincrementable)
        conn.execute("INSERT INTO Salidas (Fecha, Cliente, Codigo, Categoria, Producto, Comentario, Cantidad) VALUES (?, ?, ?, ?, ?, ?, ?)", (fecha, cliente, codigo, categoria, producto, comentario, cantidad))
        
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

