from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Conexion_db import conectar_db
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMessageBox


#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Finciones para obtener y generar el codigo de los articulos de manera automatica 
def obtener_codigo_articulo(tabla):
    conn = conectar_db()
    cursor = conn.execute(f"SELECT MAX(Codigo) FROM {tabla}")
    ultimo_codigo = cursor.fetchone()[0]
    conn.close()
    return ultimo_codigo

def generar_nuevo_codigo_articulo(prefijo, ultimo_codigo):
    if ultimo_codigo is None:
        nuevo_codigo = 0
    else:
        nuevo_codigo = int(ultimo_codigo.replace(prefijo, '')) + 1

    nuevo_codigo_formateado = f"{prefijo}{str(nuevo_codigo).zfill(5)}"
    return nuevo_codigo_formateado
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Funciones genericas para mostrar los codigos siguientes al momento de registrar en la base de dato 
def obtener_ultimo_codigo(tabla, codigo):
    conn = conectar_db()
    cursor = conn.execute(f"SELECT MAX({codigo}) FROM {tabla}")
    ultimo_codigo = cursor.fetchone()[0]
    conn.close()
    return ultimo_codigo

def generar_nuevo_codigo(ultimo_codigo):
    if ultimo_codigo is None:
        nuevo_codigo = 1
    else:
        nuevo_codigo = int(ultimo_codigo) + 1

    nuevo_codigo_formateado = str(nuevo_codigo)
    return nuevo_codigo_formateado

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Funcion generica para insertar datos en la base en alguno de los formularios 
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
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------     
# Funciones para intercambiar datos de los formularios a la base de datos
def insertar_nueva_presentacion(nombre, descripcion):
    insertar_dato_generico('presentacion', ['nombre', 'descripcion'], [nombre, descripcion])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
def insertar_nuevo_empleados(nombre, apellidos, sexo, fechanac, numdocumento, direccion, telefono, email, acceso, usuario, password):
    insertar_dato_generico('empleado', ['nombre', 'apellidos', 'sexo', 'fecha_nac', 'num_documento', 'direccion', 'telefono', 'email', 'acceso', 'usuario', 'password'], [nombre, apellidos, sexo , fechanac, numdocumento, direccion, telefono, email, acceso, usuario, password])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
def insertar_nueva_categoria(nombre, descripcion):
    insertar_dato_generico('categoria', ['nombre', 'descripcion'], [nombre, descripcion])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------      
def insertar_nuevo_proveedor(razon_soc, sector_com, tipo_doc, numdocumento, direccion, telefono, email, url):
    insertar_dato_generico('proveedor', ['razon_social', 'sector_comercial', 'tipo_documento', 'num_documento', 'direccion', 'telefono', 'email', 'url'], [razon_soc, sector_com, tipo_doc, numdocumento, direccion, telefono, email, url])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
def insertar_nuevo_cliente(nombre, apellidos, sexo, fechanac, tipo_doc, numdocumento, direccion, telefono, email):
    insertar_dato_generico('cliente', ['nombre', 'apellidos', 'sexo', 'fecha_nacimiento', 'tipo_documento', 'num_documento', 'direccion', 'telefono', 'email'], [nombre, apellidos, sexo, fechanac, tipo_doc, numdocumento, direccion, telefono, email])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

def insertar_datos_sesion(idempleado, nombre, apellidos, usuario, rol, fecha):
    insertar_dato_generico('sesiones', ['idempleado', 'nombre', 'apellidos', 'usuario', 'rol', 'fecha'], [idempleado, nombre, apellidos, usuario, rol, fecha])



#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
def insertar_nuevo_articulo(codigoventa, nombre, descripcion, imagen, categoria, presentacion):
    try:
        # Obtener los IDs de Categoria y presentacion a partir de los nombres
        id_categoria = obtener_id_categoria_por_nombre(categoria)
        id_presentacion = obtener_id_presentacion_por_nombre(presentacion)

        # Verificar si se encontraron los IDs de Categoria y presentacion
        if id_categoria is not None and id_presentacion is not None:
            # Llamar a la función genérica para insertar el artículo en la base de datos
            insertar_dato_generico('articulo', ['codigo', 'nombre', 'descripcion', 'imagen', 'idcategoria', 'idpresentacion'], [codigoventa, nombre, descripcion, imagen, id_categoria, id_presentacion])
        else:
            # Manejar el caso en el que no se encontraron los IDs mostrando un mensaje de error
            mensaje_error = QMessageBox()
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.setWindowTitle("Error")
            mensaje_error.setText("No se encontraron los IDs de Categoria y/o presentacion.")
            mensaje_error.exec_()
    except Exception as e:
        # Manejar otros errores, mostrar un mensaje de error o realizar otra acción necesaria
        mensaje_error = QMessageBox()
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al insertar artículo: {str(e)}")
        mensaje_error.exec_()

# Función para obtener el ID de Categoria a partir del nombre
def obtener_id_categoria_por_nombre(nombre_categoria):
    conn = conectar_db()
    cursor = conn.execute("SELECT idcategoria FROM Categoria WHERE nombre = ?", (nombre_categoria,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

# Función para obtener el ID de presentacion a partir del nombre
def obtener_id_presentacion_por_nombre(nombre_presentacion):
    conn = conectar_db()
    cursor = conn.execute("SELECT idpresentacion FROM presentacion WHERE nombre = ?", (nombre_presentacion,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
def insertar_nuevo_ingreso(idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado):
    insertar_dato_generico('ingreso', ['idempleado', 'idproveedor', 'fecha', 'tipo_comprobante', 'num_comprobante', 'itbis', 'estado'], [idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado])
    

def insertar_nuevo_detalle_ingreso(idingreso, idarticulo, precio_compra, precio_venta, cantidad, fecha_produccion, fecha_vencimiento):
    conn = conectar_db()

    try:
        cursor = conn.execute("SELECT stock FROM detalle_ingreso WHERE idarticulo = ?", (idarticulo,))
        existing_stock = cursor.fetchone()

        if existing_stock:
            # Si el producto existe en Stock, actualizamos la cantidad disponible
            nueva_cantidad = existing_stock[0] + cantidad
            
            
            insertar_dato_generico('detalle_ingreso', ['idingreso', 'idarticulo', 'precio_compra', 'precio_venta', 'cantidad', 'stock','fecha_produccion', 'fecha_vencimiento'], [idingreso, idarticulo, precio_compra, precio_venta, cantidad, nueva_cantidad, fecha_produccion, fecha_vencimiento])

        else:
            # Si el producto no existe en Stock, lo agregamos con la cantidad proporcionada
            insertar_dato_generico('detalle_ingreso', ['idingreso', 'idarticulo', 'precio_compra', 'precio_venta', 'cantidad', 'stock','fecha_produccion', 'fecha_vencimiento'], [idingreso, idarticulo, precio_compra, precio_venta, cantidad, cantidad, fecha_produccion, fecha_vencimiento])
    
    except Exception as e:
        # Mensaje de error
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al insertar nuevo detalle de ingreso para idarticulo {idarticulo}: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec_()
    finally:
        conn.close()    




















    
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


