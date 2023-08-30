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
        
        
def insertar_nuevo_cliente(codigo, nombre):
        
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO Clientes (Codigo, Nombre) VALUES (?, ?)", (codigo, nombre))
        conn.commit()

        # Cerrar la conexión
        conn.close()
        
def insertar_nuevo_proveedor(codigo, nombre):
        
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO Proveedores (Codigo, Nombre) VALUES (?, ?)", (codigo, nombre))
        conn.commit()

        # Cerrar la conexión
        conn.close()
        
def insertar_compras(fecha, proveedor, codigo, categoria, producto, und, comentario, cantidad):
        
        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO Compras (Fecha, Proveedor, Codigo, Categoria, Producto, Und, Comentario, Cantidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (fecha, proveedor, codigo, categoria, producto, und, comentario, cantidad))
        conn.commit()

        # Cerrar la conexión
        conn.close()
        


        

def registrar_salida(id_prod, cantidad_rebajada, cliente, comentario_salida):
    # Conectar a la base de datos
    conn = conectar_db()

    # Obtener información de la compra original
    cursor = conn.execute("SELECT * FROM Compras WHERE Codigo=?", (id_prod,))
    compra = cursor.fetchone()
    
    if compra:
        cantidad_actual = compra["Cantidad"]
        
        # Verificar si hay suficientes existencias para la salida
        if cantidad_actual >= cantidad_rebajada:
            # Insertar registro de salida en la tabla de salidas
            fecha_actual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            conn.execute("INSERT INTO Salidas (Fecha, N_doc, Clientes, Codigo, Categoria, Producto, Comentario, Cantidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                         (fecha_actual, None, cliente, compra["Codigo"], compra["Categoria"], compra["Producto"], comentario_salida, cantidad_rebajada))
            
            # Calcular nueva cantidad después de la salida
            nueva_cantidad = cantidad_actual - cantidad_rebajada
            # Actualizar la cantidad en la tabla de compras
            conn.execute("UPDATE Compras SET Cantidad=? WHERE N_doc=?", (nueva_cantidad, id_prod))
            
            conn.commit()
            
            # Mostrar mensaje de éxito
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Information)
            msg_box.setWindowTitle("Éxito")
            msg_box.setText("Salida registrada con éxito.")
            msg_box.exec_()
        else:
            # Mostrar mensaje de error
            msg_box = QMessageBox()
            msg_box.setIcon(QMessageBox.Warning)
            msg_box.setWindowTitle("Error")
            msg_box.setText("No hay suficientes existencias para la salida.")
            msg_box.exec_()
    else:
        # Mostrar mensaje de error
        msg_box = QMessageBox()
        msg_box.setIcon(QMessageBox.Warning)
        msg_box.setWindowTitle("Error")
        msg_box.setText("Compra no encontrada.")
        msg_box.exec_()

    # Cerrar la conexión
    conn.close()
