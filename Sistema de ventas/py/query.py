import pyodbc

# Configura la conexión a la base de datos
server = 'tu_servidor_sql'
database = 'tu_base_de_datos'
username = 'tu_usuario'
password = 'tu_contraseña'

# Realiza la conexión a la base de datos
conn = pyodbc.connect(f'DRIVER={{SQL Server}};SERVER={server};DATABASE={database};UID={username};PWD={password}')

# Crea un cursor para ejecutar consultas SQL
cursor = conn.cursor()

try:
    # Obtiene el último número de serie de ventas si existe
    cursor.execute('SELECT MAX(CAST(RIGHT(serie, LEN(serie) - 4) AS INT)) FROM venta')
    last_serie_number = cursor.fetchone()[0]

    # Establece el próximo número de serie
    if last_serie_number is not None:
        next_serie_number = last_serie_number + 1
    else:
        next_serie_number = 1

    nueva_serie = f'VENT{next_serie_number:05}'

    # Supongamos que ya tienes una cotización con un ID específico
    id_cotizacion = 1

    # Obtiene los detalles de la cotización
    cursor.execute(f'SELECT * FROM detalle_cotizacion WHERE idcotizacion = {id_cotizacion}')
    detalles_cotizacion = cursor.fetchall()

    # Inserta una nueva venta con el tipo_comprobante y serie actualizados
    cursor.execute(f'INSERT INTO venta (idcliente, idempleado, fecha, tipo_comprobante, serie, itbis) '
                   f'SELECT idcliente, idempleado, fecha, "FACTURA", "{nueva_serie}", itbis '
                   f'FROM cotizacion WHERE idcotizacion = {id_cotizacion}')
    conn.commit()

    # Obtiene el ID de la venta recién insertada
    cursor.execute('SELECT SCOPE_IDENTITY()')
    id_venta = cursor.fetchone()[0]

    # Inserta los detalles de la venta
    for detalle in detalles_cotizacion:
        cursor.execute(f'INSERT INTO detalle_venta (idventa, idarticulo, cantidad, precio_venta, descuento) '
                       f'VALUES ({id_venta}, {detalle.idarticulo}, {detalle.cantidad}, {detalle.precio_venta}, {detalle.descuento})')
    conn.commit()

    print(f'Cotización con ID {id_cotizacion} ha sido convertida en venta con ID {id_venta}')
    print(f'Serie de venta: {nueva_serie}')

except Exception as e:
    print(f'Ocurrió un error: {e}')

finally:
    # Cierra el cursor y la conexión a la base de datos
    cursor.close()
    conn.close()
