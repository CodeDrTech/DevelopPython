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
# Generar el codigo de las cotizaciones de manera automatica 
def obtener_codigo_cotizacion(tabla):
    conn = conectar_db()
    cursor = conn.execute(f"SELECT MAX(serie) FROM {tabla}")
    ultimo_codigo = cursor.fetchone()[0]
    conn.close()
    return ultimo_codigo

def generar_nuevo_codigo_cotizacion(prefijo, ultimo_codigo):
    if ultimo_codigo is None:
        nuevo_codigo = 0
    else:
        nuevo_codigo = int(ultimo_codigo.replace(prefijo, '')) + 1

    nuevo_codigo_formateado = f"{prefijo}{str(nuevo_codigo).zfill(5)}"
    return nuevo_codigo_formateado
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Generar el codigo de las ventas de manera automatica 
def obtener_codigo_venta(tabla):
    conn = conectar_db()
    cursor = conn.execute(f"SELECT MAX(serie) FROM {tabla}")
    ultimo_codigo = cursor.fetchone()[0]
    conn.close()
    return ultimo_codigo

def generar_nuevo_codigo_venta(prefijo, ultimo_codigo):
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

def insertar_datos_sesion(idempleado, nombre, apellidos, usuario, rol, fechaHora):
    insertar_dato_generico('sesiones', ['idempleado', 'nombre', 'apellidos', 'usuario', 'rol', 'fecha'], [idempleado, nombre, apellidos, usuario, rol, fechaHora])



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
    insertar_dato_generico('ingreso', ['idempleado', 'idproveedor', 'fecha', 'tipo_comprobante', 'num_comprobante', 'itbis', 'estado'],
                                                     [idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado])
    

def insertar_nuevo_detalle_ingreso(idingreso, idarticulo, precio_compra, precio_venta, cantidad, fecha_produccion, fecha_vencimiento, precio_venta1, precio_venta2):
    conn = conectar_db()

    try:
        insertar_dato_generico('detalle_ingreso', ['idingreso', 'idarticulo', 'precio_compra', 'precio_venta', 'cantidad', 'fecha_produccion', 'fecha_vencimiento', 'precio_venta1', 'precio_venta2'],
                                [idingreso, idarticulo, precio_compra, precio_venta, cantidad, fecha_produccion, fecha_vencimiento, precio_venta1, precio_venta2])
        cursor = conn.execute("SELECT disponible FROM stock WHERE idarticulo = ?", (idarticulo,))
        existing_stock = cursor.fetchone()

        if existing_stock:
            # Si el producto existe en Stock, actualizamos la cantidad disponible
            nueva_cantidad = existing_stock[0] + cantidad
            conn.execute("UPDATE stock SET disponible = ? WHERE idarticulo = ?", (nueva_cantidad, idarticulo))
        else:
            # Si el producto no existe en Stock, lo agregamos con la cantidad proporcionada
            insertar_dato_generico('stock', ['idarticulo', 'disponible'], [idarticulo, cantidad])
    
        conn.commit()  # Confirmar los cambios en la base de datos
    except Exception as e:
        # Mensaje de error
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al insertar nuevo detalle de ingreso {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
    finally:
        conn.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
def insertar_nueva_cotizacion(idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis, comentario):
    insertar_dato_generico('cotizacion', ['idcliente', 'idempleado', 'fecha', 'tipo_comprobante', 'serie', 'itbis', 'comentario'], 
                                                    [idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis, comentario])
    

def insertar_nuevo_detalle_cotizacion(idoctizacion, idarticulo, catidad, precio_venta, descuento):
    insertar_dato_generico('detalle_cotizacion', ['idcotizacion', 'idarticulo', 'cantidad', 'precio_venta', 'descuento'], 
                                                    [idoctizacion, idarticulo, catidad, precio_venta, descuento])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def anular_ingreso(id_ingreso):
    try:
        # Obtener la cantidad ingresada para el ingreso específico
        conn = conectar_db()
        cursor = conn.cursor()
        cursor.execute("SELECT idarticulo, SUM(cantidad) FROM detalle_ingreso WHERE idingreso = ? GROUP BY idarticulo", (id_ingreso,))
        rows = cursor.fetchall()
        
        for row in rows:
            idarticulo, cantidad_ingresada = row
            cursor.execute("SELECT disponible FROM stock WHERE idarticulo = ?", (idarticulo,))
            existing_stock = cursor.fetchone()
            
            if existing_stock:
                nueva_cantidad = existing_stock[0] - cantidad_ingresada
                cursor.execute("UPDATE stock SET disponible = ? WHERE idarticulo = ?", (nueva_cantidad, idarticulo))
        
        # Cambiar el estado del ingreso a "Inactivo"
        cursor.execute("UPDATE ingreso SET estado = ? WHERE idingreso = ?", ("Inactivo", id_ingreso))
        
        conn.commit()
        conn.close()
    except Exception as e:
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al anular el ingreso: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def quitar_detalle_ingreso(id_detalle_ingreso):
    try:
        conn = conectar_db()  # Utiliza tu función de conexión a la base de datos
        cursor = conn.cursor()

        # Obtener el idarticulo y la cantidad ingresada
        cursor.execute("SELECT idarticulo, cantidad, idingreso FROM detalle_ingreso WHERE iddetalle_ingreso = ?", (id_detalle_ingreso,))
        detalle = cursor.fetchone()

        if detalle:
            idarticulo, cantidad_ingresada, idingreso = detalle

            # Actualizar la cantidad disponible en la tabla stock
            cursor.execute("UPDATE stock SET disponible = disponible - ? WHERE idarticulo = ?", (cantidad_ingresada, idarticulo))

            # Eliminar el detalle de ingreso
            cursor.execute("DELETE FROM detalle_ingreso WHERE iddetalle_ingreso = ?", (id_detalle_ingreso,))

            # Comprobar si el ingreso ya no tiene más detalles
            cursor.execute("SELECT COUNT(*) FROM detalle_ingreso WHERE idingreso = ?", (idingreso,))
            num_detalles = cursor.fetchone()[0]

            if num_detalles == 0:
                # Cambiar el estado del ingreso a "Inactivo" si no hay más detalles
                cursor.execute("UPDATE ingreso SET estado = 'Inactivo' WHERE idingreso = ?", (idingreso,))

            conn.commit()
        else:
            mensaje_error = QMessageBox()
            mensaje_error.setWindowTitle("Error")
            mensaje_error.setText("Detalle de ingreso no encontrado.")
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.exec()

        conn.close()
    except Exception as e:
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al anular el ingreso: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def quitar_detalle_cotizacion(id_detalle_cotizacion):
    try:
        conn = conectar_db()  # Utiliza tu función de conexión a la base de datos
        cursor = conn.cursor()

        # Obtener el idcotizacion desde el detalle
        cursor.execute("SELECT iddetalle_cotizacion, idcotizacion FROM detalle_cotizacion WHERE iddetalle_cotizacion = ?", (id_detalle_cotizacion,))
        detalle = cursor.fetchone()

        if detalle:
            iddetalle_cotizacion, idcotizacion = detalle

            # Eliminar el detalle de cotizacion
            cursor.execute("DELETE FROM detalle_cotizacion WHERE iddetalle_cotizacion = ?", (iddetalle_cotizacion,))

            # Comprobar si la cotizacion ya no tiene más detalles
            cursor.execute("SELECT COUNT(*) FROM detalle_cotizacion WHERE idcotizacion = ?", (idcotizacion,))
            num_detalles = cursor.fetchone()[0]

            if num_detalles == 0:
                # Agregar un detalle de cotización genérico
                cursor.execute("INSERT INTO detalle_cotizacion (idcotizacion, idarticulo, cantidad, precio_venta, descuento) VALUES (?, 1, 0, 0, 0)", (idcotizacion,))

                # Actualizar el comentario en la cotización
                cursor.execute("UPDATE cotizacion SET comentario = 'COTIZACION ANULADA' WHERE idcotizacion = ?", (idcotizacion,))

            conn.commit()
        else:
            mensaje_error = QMessageBox()
            mensaje_error.setWindowTitle("Error")
            mensaje_error.setText("Detalle de cotizacion no encontrado.")
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.exec()

        conn.close()
    except Exception as e:
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al anular el ingreso: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def convertir_cot_a_factura(id_cotizacion):
    conn = conectar_db()
    
    try:
        # Crea un cursor para ejecutar el procedimiento almacenado
        cursor = conn.cursor()

        # Ejecuta el procedimiento almacenado
        cursor.execute("EXEC ConvertirCotizacionAFactura @idcotizacion=?", id_cotizacion)
        conn.commit()

        # Cierra el cursor
        cursor.close()
    except Exception as e:
        # Mensaje de error
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Fallo la convercion a factura {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
    finally:
        # Cierra la conexión a la base de datos
        conn.close()
        
        
# def convertir_cot_a_factura(id_cotizacion):
#     conn = conectar_db()
#     cursor = conn.cursor()
#     try:
#         # Obtiene el último número de serie de ventas si existe
#         cursor.execute('SELECT MAX(CAST(RIGHT(serie, LEN(serie) - 4) AS INT)) FROM venta')
#         last_serie_number = cursor.fetchone()[0]
# 
#         # Establece el próximo número de serie
#         if last_serie_number is not None:
#             next_serie_number = last_serie_number + 1
#         else:
#             next_serie_number = 1
# 
#         nueva_serie = f'VENT{next_serie_number:05}'
# 
#         # Obtiene los detalles de la cotización
#         cursor.execute(f'SELECT * FROM detalle_cotizacion WHERE idcotizacion = {id_cotizacion}')
#         detalles_cotizacion = cursor.fetchall()
# 
#         # Inserta una nueva venta con el tipo_comprobante y serie actualizados
#         cursor.execute(f'INSERT INTO venta (idcliente, idempleado, fecha, tipo_comprobante, serie, itbis) '
#                f'SELECT idcliente, idempleado, fecha, ?, ?, itbis '  # Utiliza ? como marcador de posición
#                f'FROM cotizacion WHERE idcotizacion = {id_cotizacion}', 'FACTURA', nueva_serie)
#         conn.commit()
# 
#         # Obtiene el ID de la venta recién insertada
#         cursor.execute('SELECT SCOPE_IDENTITY()')
#         id_venta = cursor.fetchone()[0]
# 
#         
#         # Inserta los detalles de la venta
#         for detalle in detalles_cotizacion:
#             cursor.execute(f'INSERT INTO detalle_venta (idventa, idarticulo, cantidad, precio_venta, descuento) '
#                    f'VALUES (?, ?, ?, ?, ?)', (id_venta, detalle.idarticulo, detalle.cantidad, detalle.precio_venta, detalle.descuento))
#             conn.commit()
#         
#     except Exception as e:
#         # Mensaje de error
#         mensaje_error = QMessageBox()
#         mensaje_error.setWindowTitle("Error")
#         mensaje_error.setText(f"Fallo la convercion a factura {str(e)}")
#         mensaje_error.setIcon(QMessageBox.Critical)
#         mensaje_error.exec()
#     finally:
#         # Cierra el cursor y la conexión a la base de datos
#         cursor.close()
#         conn.close()