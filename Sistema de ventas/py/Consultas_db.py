from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Conexion_db import conectar_db
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox



def insertar_dato_generico(tabla, columnas, valores):
    

    # Conectar a la base de datos
    conn = conectar_db()

    # Construir la consulta SQL dinámica
    columnas_str = ', '.join(columnas)
    valores_str = ', '.join(['?'] * len(columnas))
    query = f"INSERT INTO {tabla} ({columnas_str}) VALUES ({valores_str})"

    # Realizar la inserción en la base de datos
    conn.execute(query, valores)
    conn.commit()

    # Cerrar la conexión
    conn.close()
def insertar_nueva_presentacion(nombre, descripcion):
    insertar_dato_generico('presentacion', ['nombre', 'descripcion'], [nombre, descripcion])






























    
# de aqui en adelante el codigo es de otro sistema    
# def obtener_ultimo_codigo(tabla):
#     conn = conectar_db()
#     cursor = conn.execute(f"SELECT MAX(Codigo) FROM {tabla}")
#     ultimo_codigo = cursor.fetchone()[0]
#     conn.close()
#     return ultimo_codigo

# def generar_nuevo_codigo(prefijo, ultimo_codigo):
#     if ultimo_codigo is None:
#         nuevo_codigo = 0
#     else:
#         nuevo_codigo = int(ultimo_codigo.replace(prefijo, '')) + 1

#     nuevo_codigo_formateado = f"{prefijo}{str(nuevo_codigo).zfill(5)}"
#     return nuevo_codigo_formateado

# def insertar_generico(tabla, columnas, valores, prefijo):
#     # Obtener el último código de la tabla
#     ultimo_codigo = obtener_ultimo_codigo(tabla)

#     # Generar el nuevo código
#     nuevo_codigo = generar_nuevo_codigo(prefijo, ultimo_codigo)

#     # Conectar a la base de datos
#     conn = conectar_db()

#     # Construir la consulta SQL dinámica
#     columnas_str = ', '.join(columnas)
#     valores_str = ', '.join(['?'] * len(columnas))
#     query = f"INSERT INTO {tabla} ({columnas_str}) VALUES ({valores_str})"

#     # Realizar la inserción en la base de datos
#     conn.execute(query, (nuevo_codigo, *valores))
#     conn.commit()

#     # Cerrar la conexión
#     conn.close()

# def insertar_nuevo_producto(categoria, nombre, medida):
#     insertar_generico('Productos', ['Codigo', 'Categoria', 'Nombre', 'Medida'], [categoria, nombre, medida], 'PROD')

# def insertar_nuevo_cliente(nombre):
#     insertar_generico('Clientes', ['Codigo', 'Nombre'], [nombre], 'CLI')

# def insertar_nuevo_proveedor(nombre):
#     insertar_generico('Proveedores', ['Codigo', 'Nombre'], [nombre], 'PROV')

        
# #------------------------------------------------------------------------------------------------------
# #------------------------------------------------------------------------------------------------------        
# def insertar_compras(fecha, proveedor, codigo, categoria, producto, und, comentario, cantidad):
#     # Conectar a la base de datos
#     conn = conectar_db()

#     try:
#         # Verificar si el producto ya existe en la tabla Stock
#         cursor = conn.execute("SELECT Disponible FROM Stock WHERE Codigo = ?", (codigo,))
#         existing_stock = cursor.fetchone()

#         if existing_stock:
#             # Si el producto existe en Stock, actualizamos la cantidad disponible
#             nueva_cantidad = existing_stock[0] + cantidad
#             conn.execute("UPDATE Stock SET Disponible = ? WHERE Codigo = ?", (nueva_cantidad, codigo))
#         else:
#             # Si el producto no existe en Stock, lo agregamos
#             conn.execute("INSERT INTO Stock (Codigo, Producto, Disponible) VALUES (?, ?, ?)", (codigo, producto, cantidad))
        
#         # Insertar en la tabla Compras
#         conn.execute("INSERT INTO Compras (Fecha, Proveedor, Codigo, Categoria, Producto, Und, Comentario, Cantidad) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", (fecha, proveedor, codigo, categoria, producto, und, comentario, cantidad))
        
#         # Confirmar los cambios en la base de datos
#         conn.commit()
        
#     except Exception as e:
#         error_message = "Error: " + str(e)
#         # Mostrar mensaje de error utilizando QMessageBox
#         msg_box = QMessageBox()
#         msg_box.setIcon(QMessageBox.Critical)
#         msg_box.setWindowTitle("Error")
#         msg_box.setText(error_message)
#         msg_box.exec_()
#         # Revertir cambios en caso de error
#         conn.rollback()
        
#     finally:
#         # Cerrar la conexión
#         conn.close()

# #------------------------------------------------------------------------------------------------------
# #------------------------------------------------------------------------------------------------------ 


# def insertar_detalle_salida(fecha, cliente, comentario):
#     conn = conectar_db()

#     try:
#         cursor = conn.cursor()
#         cursor.execute("INSERT INTO DetalleSalidas (Fecha, Cliente, Comentario) VALUES (?, ?, ?)", (fecha, cliente, comentario))
#         conn.commit()
#         detalle_salida_id = cursor.lastrowid

#         return detalle_salida_id

#     except Exception as e:
#         # Manejar errores aquí y mostrar un mensaje de error
#         error_message = "Error al insertar producto en salida: " + str(e)
#         msg_box = QMessageBox()
#         msg_box.setIcon(QMessageBox.Critical)
#         msg_box.setWindowTitle("Error")
#         msg_box.setText(error_message)
#         msg_box.exec_()

#     finally:
#         conn.close()

# def insertar_producto_en_salida(id_salida, codigo, categoria, producto_nombre, cantidad):
#     conn = conectar_db()

#     try:
#         # Verificar la cantidad disponible en Stock antes de la inserción
#         cursor = conn.execute("SELECT Disponible FROM Stock WHERE Codigo = ?", (codigo,))
#         disponible = cursor.fetchone()

#         if disponible is not None and cantidad <= disponible[0]:
#             # Si la cantidad vendida es menor o igual a la cantidad disponible
#             # Insertar un producto en la tabla Salidas
#             conn.execute("INSERT INTO Salidas (ID_Salida, Codigo, Categoria, Producto, CantidadTotal) VALUES (?, ?, ?, ?, ?)", (id_salida, codigo, categoria, producto_nombre, cantidad))
            
#             # Actualizar la tabla Stock restando la cantidad vendida
#             conn.execute("UPDATE Stock SET Disponible = Disponible - ? WHERE Codigo = ?", (cantidad, codigo))

#             conn.commit()
#         else:
#             # Mostrar un mensaje de error si la cantidad vendida supera la cantidad disponible
#             error_message = "La cantidad supera la disponible en Stock."
#             msg_box = QMessageBox()
#             msg_box.setIcon(QMessageBox.Critical)
#             msg_box.setWindowTitle("Error")
#             msg_box.setText(error_message)
#             msg_box.exec_()

#     except Exception as e:
#         # Manejar otros errores aquí y mostrar un mensaje de error
#         error_message = "Error al insertar producto en salida: " + str(e)
#         msg_box = QMessageBox()
#         msg_box.setIcon(QMessageBox.Critical)
#         msg_box.setWindowTitle("Error")
#         msg_box.setText(error_message)
#         msg_box.exec_()

#     finally:
#         conn.close()


