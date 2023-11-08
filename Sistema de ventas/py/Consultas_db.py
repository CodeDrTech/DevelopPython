from Conexion_db import connect_to_db
from PyQt5.QtWidgets import QMessageBox
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Recibe el nombre de la tabla como parametro para buscar el ultimo codigo de articulo generado.
def obtener_codigo_articulo(tabla):
    conn = connect_to_db()
    cursor = conn.execute(f"SELECT MAX(Codigo) FROM {tabla}")
    ultimo_codigo = cursor.fetchone()[0]
    conn.close()
    return ultimo_codigo
# Recibe como parametro el ultimo codigo de articulo de la funcion obtener_codigo_articulo y el 
# prefijo que va antes de los numero para generar el proximo codigo a usar. 
def generar_nuevo_codigo_articulo(prefijo, ultimo_codigo):
    if ultimo_codigo is None:
        nuevo_codigo = 0
    else:
        nuevo_codigo = int(ultimo_codigo.replace(prefijo, '')) + 1

    nuevo_codigo_formateado = f"{prefijo}{str(nuevo_codigo).zfill(5)}"
    return nuevo_codigo_formateado
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Recibe la tabla como parametro para buscar el ultimo codigo de cotizacion, Ejem. (COT00000)
def obtener_codigo_cotizacion(tabla):
    conn = connect_to_db()
    cursor = conn.execute(f"SELECT MAX(serie) FROM {tabla}")
    ultimo_codigo = cursor.fetchone()[0]
    conn.close()
    return ultimo_codigo
# Recibe el prefijo y ultimo codigo de la funcion obtener_codigo_cotizacion para generar el proximo
# codigo en secuencia de 1 en 1 Ejem. (COT00001) donde COT es el prefijo y 00001 la secuencia
def generar_nuevo_codigo_cotizacion(prefijo, ultimo_codigo):
    if ultimo_codigo is None:
        nuevo_codigo = 0
    else:
        nuevo_codigo = int(ultimo_codigo.replace(prefijo, '')) + 1

    nuevo_codigo_formateado = f"{prefijo}{str(nuevo_codigo).zfill(5)}"
    return nuevo_codigo_formateado
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
### Estos datos seran usados para ser insertados en la bd a la hora de insertar un nuevo articulo ###
# Obtiene el id de la categoria mediante el nombre pasado como parametro ejemp. (HM (Herramientas manuales) = id 1)
def obtener_id_categoria_por_nombre(nombre_categoria):
    conn = connect_to_db()
    cursor = conn.execute("SELECT idcategoria FROM Categoria WHERE nombre = ?", (nombre_categoria,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None

# Obtiene el id de la presentacion mediante el nombre de pasado como parametro ejemp. (UDN (unidad) = id 1)
def obtener_id_presentacion_por_nombre(nombre_presentacion):
    conn = connect_to_db()
    cursor = conn.execute("SELECT idpresentacion FROM presentacion WHERE nombre = ?", (nombre_presentacion,))
    resultado = cursor.fetchone()
    conn.close()
    return resultado[0] if resultado else None
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

# Recibe la tabla como parametro para buscar el ultimo codigo de la factura, Ejem. (FACT00000)
def obtener_codigo_venta(tabla):
    conn = connect_to_db()
    cursor = conn.execute(f"SELECT MAX(serie) FROM {tabla}")
    ultimo_codigo = cursor.fetchone()[0]
    conn.close()
    return ultimo_codigo

# Recibe el prefijo y ultimo codigo de la funcion obtener_codigo_venta para generar el proximo
# codigo en secuencia de 1 en 1 Ejem. (FACT00001) donde FACT es el prefijo y 00001 la secuencia
def generar_nuevo_codigo_venta(prefijo, ultimo_codigo):
    if ultimo_codigo is None:
        nuevo_codigo = 0
    else:
        nuevo_codigo = int(ultimo_codigo.replace(prefijo, '')) + 1

    nuevo_codigo_formateado = f"{prefijo}{str(nuevo_codigo).zfill(5)}"
    return nuevo_codigo_formateado
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Obtiene la tabla y el codigo para generar un codigo nuevo, se usa para los id principales.
# basado en el u;ti id principal anterior
def obtener_ultimo_codigo(tabla, codigo):
    conn = connect_to_db()
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
# Recibe como parametro tabla, columnas y valores para hacer insert a la base de datos
# por agunas de las funciones de tipo INSERT INTO (TABLA).
def insertar_dato_generico(tabla, columnas, valores):
    # Conectar a la base de datos
    conn = connect_to_db()

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
# Obtienen los parametro de los formularios para ahcer los INSERT INTO  a la base de datos 
# utilizando la funcion de insertar generica.
def insertar_nueva_presentacion(nombre, descripcion):
    insertar_dato_generico('presentacion', ['nombre', 'descripcion'], [nombre, descripcion])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
def insertar_nuevo_empleados(nombre, apellidos, sexo, fechanac, numdocumento, direccion, telefono, email, acceso, usuario, password):
    insertar_dato_generico('empleado', ['nombre', 'apellidos', 'sexo', 'fecha_nac', 'num_documento', 'direccion', 'telefono', 'email',
        'acceso', 'usuario', 'password'], [nombre, apellidos, sexo , fechanac, numdocumento, direccion, telefono, email, acceso, usuario, password])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
def insertar_nueva_categoria(nombre, descripcion):
    insertar_dato_generico('categoria', ['nombre', 'descripcion'], [nombre, descripcion])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------      
def insertar_nuevo_proveedor(razon_soc, sector_com, tipo_doc, numdocumento, direccion, telefono, email, url):
    insertar_dato_generico('proveedor', ['razon_social', 'sector_comercial', 'tipo_documento', 'num_documento',
        'direccion', 'telefono', 'email', 'url'], [razon_soc, sector_com, tipo_doc, numdocumento, direccion, telefono, email, url])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
def insertar_nuevo_cliente(nombre, apellidos, sexo, fechanac, tipo_doc, numdocumento, direccion, telefono, email):
    insertar_dato_generico('cliente', ['nombre', 'apellidos', 'sexo', 'fecha_nacimiento', 'tipo_documento', 'num_documento',
        'direccion', 'telefono', 'email'], [nombre, apellidos, sexo, fechanac, tipo_doc, numdocumento, direccion, telefono, email])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def insertar_datos_sesion(idempleado, nombre, apellidos, usuario, rol, fechaHora):
    insertar_dato_generico('sesiones', ['idempleado', 'nombre', 'apellidos', 'usuario', 'rol', 'fecha'],
                                                [idempleado, nombre, apellidos, usuario, rol, fechaHora])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
def insertar_nuevo_articulo(codigoventa, nombre, descripcion, imagen, categoria, presentacion):
    try:
        # Obtener los IDs primarios de Categoria y presentacion a partir de los nombres
        id_categoria = obtener_id_categoria_por_nombre(categoria)
        id_presentacion = obtener_id_presentacion_por_nombre(presentacion)

        # Verificar si se encontraron los IDs de Categoria y presentacion
        if id_categoria is not None and id_presentacion is not None:
            # Llamar a la función genérica para insertar el artículo en la base de datos
            insertar_dato_generico('articulo', ['codigo', 'nombre', 'descripcion', 'imagen',
                'idcategoria', 'idpresentacion'], [codigoventa, nombre, descripcion, imagen,
                                                            id_categoria, id_presentacion])
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

# insertar un nuevo ingreso (compra) a la base de datos, este no lleva ningun proceso complejo
# ya que solo se inserta antes que los detalles de ingreso.
def insertar_nuevo_ingreso(idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado):
    insertar_dato_generico('ingreso', ['idempleado', 'idproveedor', 'fecha', 'tipo_comprobante', 'num_comprobante', 'itbis', 'estado'],
                                                    [idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado])
    
# Luego de insertar el idingrso y demas datos se procede a insertar los detalles, cmo lo son los articulos
# que conlleva dicho ingreso.
def insertar_nuevo_detalle_ingreso(idingreso, idarticulo, precio_compra, precio_venta, cantidad,
                                fecha_produccion, fecha_vencimiento, precio_venta1, precio_venta2):
    conn = connect_to_db()

    try:
        insertar_dato_generico('detalle_ingreso', ['idingreso', 'idarticulo', 'precio_compra', 'precio_venta', 'cantidad', 'fecha_produccion', 'fecha_vencimiento', 'precio_venta1', 'precio_venta2'],
                                [idingreso, idarticulo, precio_compra, precio_venta, cantidad, fecha_produccion, fecha_vencimiento, precio_venta1, precio_venta2])
        cursor = conn.execute("SELECT disponible FROM stock WHERE idarticulo = ?", (idarticulo,))
        existing_stock = cursor.fetchone()

        if existing_stock:
            # Si el producto existe en Stock, actualizamos la cantidad disponible con la nueva.
            nueva_cantidad = existing_stock[0] + cantidad
            conn.execute("UPDATE stock SET disponible = ? WHERE idarticulo = ?", (nueva_cantidad, idarticulo))
        else:
            # Si el producto no existe en la tabla stock, lo agregamos como nuevo con la cantidad proporcionada.
            insertar_dato_generico('stock', ['idarticulo', 'disponible'], [idarticulo, cantidad])
    
        conn.commit()  # Confirmar los cambios en la base de datos
    except Exception as e:
        # Mensaje de error en caso que surja uno.
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al insertar nuevo detalle de ingreso {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
    finally:
        conn.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Creacion de cotizaciones, estos no llevan casos complejo ya que no afectan stock de articulo. 
def insertar_nueva_cotizacion(idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis, comentario):
    insertar_dato_generico('cotizacion', ['idcliente', 'idempleado', 'fecha', 'tipo_comprobante', 'serie', 'itbis', 'comentario'], 
                                                    [idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis, comentario])
    

def insertar_nuevo_detalle_cotizacion(idoctizacion, idarticulo, catidad, precio_venta, descuento):
    insertar_dato_generico('detalle_cotizacion', ['idcotizacion', 'idarticulo', 'cantidad', 'precio_venta', 'descuento'], 
                                                    [idoctizacion, idarticulo, catidad, precio_venta, descuento])
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# insertar un nueva venta (factura) a la base de datos, este no lleva ningun proceso complejo
# ya que solo se inserta antes que los detalles de venta.  
def insertar_nueva_venta(idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis, comentario):
    insertar_dato_generico('venta', ['idcliente', 'idempleado', 'fecha', 'tipo_comprobante', 'serie', 'itbis', 'comentario'], 
                                                    [idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis, comentario])
# Luego de insertar el idventa y demas datos se procede a insertar los detalles, como lo son los articulos
# que conlleva dicha venta.
def insertar_nuevo_detalle_venta(idoctizacion, idarticulo, cantidad, precio_venta, descuento):
    conn = connect_to_db()

    try:
        # Verificar la cantidad disponible en la tabla stock
        cursor = conn.execute("SELECT disponible FROM stock WHERE idarticulo = ?", (idarticulo,))
        existing_stock = cursor.fetchone()

        if existing_stock and existing_stock[0] >= cantidad:
            # Si hay suficiente stock, insertar el nuevo detalle de venta
            insertar_dato_generico('detalle_venta', ['idventa', 'idarticulo', 'cantidad', 'precio_venta', 'descuento'], 
                                                    [idoctizacion, idarticulo, cantidad, precio_venta, descuento])
            # Actualizar la cantidad disponible en la tabla stock
            nueva_cantidad = existing_stock[0] - cantidad
            conn.execute("UPDATE stock SET disponible = ? WHERE idarticulo = ?", (nueva_cantidad, idarticulo))
            conn.commit()
        else:
            # Si no hay suficiente stock, mostrar un mensaje de error
            mensaje_error = QMessageBox()
            mensaje_error.setWindowTitle("Error")
            mensaje_error.setText("No hay suficiente stock para realizar la venta.")
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.exec()
    except Exception as e:
        # Mensaje de error en caso que surja.
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al insertar nuevo detalle de venta: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
    finally:
        conn.close()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def anular_ingreso(id_ingreso):
    try:
        # Obtener la cantidad ingresada para el ingreso específico
        conn = connect_to_db()
        cursor = conn.cursor()
        cursor.execute("SELECT idarticulo, SUM(cantidad) FROM detalle_ingreso WHERE idingreso = ? GROUP BY idarticulo", (id_ingreso,))
        rows = cursor.fetchall()
        
        # itera en los articulo buscando la cantidad disponible para cada uno
        for row in rows:
            idarticulo, cantidad_ingresada = row
            cursor.execute("SELECT disponible FROM stock WHERE idarticulo = ?", (idarticulo,))
            existing_stock = cursor.fetchone()
            
            # al encontrar stock disponible actualiza la cantidad antes ingresada restandola.
            if existing_stock:
                nueva_cantidad = existing_stock[0] - cantidad_ingresada
                cursor.execute("UPDATE stock SET disponible = ? WHERE idarticulo = ?", (nueva_cantidad, idarticulo))
        
        # Cambiar el estado del ingreso a "Inactivo"
        cursor.execute("UPDATE ingreso SET estado = ? WHERE idingreso = ?", ("Inactivo", id_ingreso))
        
        conn.commit()
        conn.close()
    except Exception as e:
        # Mensaje de eeror en caso que surja alguno
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al anular el ingreso: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def quitar_detalle_ingreso(id_detalle_ingreso):
    try:
        conn = connect_to_db()  # Utiliza tu función de conexión a la base de datos
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

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def convertir_cot_a_factura(id_cotizacion):
    conn = connect_to_db()
    
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
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def quitar_detalle_cotizacion(id_detalle_cotizacion):
    conn = connect_to_db()
    
    try:
        # Crea un cursor para ejecutar el procedimiento almacenado
        cursor = conn.cursor()

        # Ejecuta el procedimiento almacenado
        cursor.execute("EXEC AnularDetalleCotizacion @iddetalle_cotizacion=?", id_detalle_cotizacion)
        conn.commit()

        # Cierra el cursor
        cursor.close()
    except Exception as e:
        # Mensaje de error
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Fallo en la eliminacion de los detalles {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
    finally:
        # Cierra la conexión a la base de datos
        conn.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
def revertir_detalle_venta(iddetalle_venta):
    conn = connect_to_db()

    try:
        cursor = conn.cursor()
        cursor.execute("EXEC RevertirDetalleVenta @iddetalle_venta=?", iddetalle_venta)
        conn.commit()
    except Exception as e:
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al revertir detalle de venta: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
    finally:
        conn.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
def backup_database():
    conn = connect_to_db()
    conn.autocommit = True  # Deshabilita el modo de transacción automática

    try:
        cursor = conn.cursor()
        cursor.execute("EXEC dbo.BackupDatabaseDefaultPath")
    except Exception as e:
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al realizar el respaldo de la base de datos: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec()
    finally:
        conn.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------   
# Revertir, primero verifica si la venta ya ha sido revertira 
def revertir_venta(idventa):
    conn = connect_to_db()
    revertido_exitos = False  # Variable indicadora para saber si se ejecuto el sp RevertirVenta

    try:
        cursor = conn.cursor()

        # Obtener el comentario de la venta
        cursor.execute("SELECT comentario FROM venta WHERE idventa = ?", (idventa,))
        comentario = cursor.fetchone()[0]

        # Verificar si el comentario es "DEVOLUCION DE VENTA"
        if comentario == "DEVOLUCION DE VENTA":
            mensaje_error = QMessageBox()
            mensaje_error.setWindowTitle("Error")
            mensaje_error.setText("No se puede revertir una venta que ya ha sido devuelta.")
            mensaje_error.setIcon(QMessageBox.Critical)
            mensaje_error.exec_()
            
        else:
            cursor.execute("EXEC RevertirVenta @idventa=?", idventa)
            conn.commit()
            revertido_exitos = True  # Marcar como exitoso

    except Exception as e:
        mensaje_error = QMessageBox()
        mensaje_error.setWindowTitle("Error")
        mensaje_error.setText(f"Error al revertir venta: {str(e)}")
        mensaje_error.setIcon(QMessageBox.Critical)
        mensaje_error.exec_()
    finally:
        conn.close()
    return revertido_exitos  # Retorna True si la reversión fue exitosa