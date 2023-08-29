from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Conexion_db import conectar_db
from PyQt5.QtCore import Qt




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