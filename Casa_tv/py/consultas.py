from database import connect_to_database
import sqlite3
import datetime

def get_clientes():
    """
    Obtiene todos los clientes ordenados por fecha de inicio descendente.

    Returns:
        list: Lista de tuplas con datos de clientes:
            - id_cliente (int)
            - nombre (str)
            - fecha_inicio (str)
            - whatsapp (str)
            - estado (str)
            - frecuencia_pago (int)
            - comentario (str)
        list vacía si hay error.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT 
                    id,
                    nombre,
                    inicio,
                    whatsapp,
                    estado,
                    frecuencia,
                    comentario,
                    saldo_pendiente,
                    saldo_neto
                FROM clientes 
                ORDER BY date(inicio) DESC
            ''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error consultando clientes: {e}")
            return []
        finally:
            conn.close()
    return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

def actualizar_cliente(cliente_id: int, nombre: str, whatsapp: str, fecha_inicio: str, estado: str, frecuencia: int, comentario: str) -> bool:
    """
    Actualiza los datos de un cliente en la base de datos.

    Args:
        cliente_id (int): ID del cliente a actualizar
        nombre (str): Nombre del cliente
        whatsapp (str): Número de WhatsApp
        fecha_inicio (str): Fecha de inicio en formato YYYY-MM-DD
        estado (str): Estado del cliente (Activo/Inactivo)
        frecuencia (int): Frecuencia de pago en días
        monto (float): Monto asignado al cliente
        correo (str): Correo electrónico del cliente
        comentario (str): Comentario asociado al cliente

    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario
    """
    if not all([cliente_id, nombre, whatsapp, fecha_inicio, estado, frecuencia]):
        raise ValueError("Todos los campos son requeridos")
    
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE clientes 
                SET nombre = ?, 
                    whatsapp = ?,
                    inicio = ?,
                    estado = ?,
                    frecuencia = ?,
                    comentario = ?
                WHERE id = ?
            ''', (nombre, whatsapp, fecha_inicio, estado, frecuencia, comentario, cliente_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error actualizando cliente: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

def get_estado_pagos():
    """
    Obtiene el estado de pagos de todos los clientes activos.

    Returns:
        list: Lista de tuplas con:
            - cliente_id (int)
            - nombre_cliente (str)
            - fecha_inicio (str)
            - fecha_base (str): Último pago o fecha inicio
            - proximo_pago (str)
            - frecuencia (int)
            - dias_transcurridos (int)
            - estado_pago (str): En corte/Pendiente/Cerca/Al día
            - monto (float)
            - correo (str)
            - comentario (str)
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                WITH ultimo_pago AS (
                SELECT
                    p.cliente_id,
                    MAX(p.fecha_pago) AS ultima_fecha_pago
                FROM pagos p
                GROUP BY p.cliente_id
            )
            SELECT 
                c.id AS cliente_id,
                c.nombre AS nombre_cliente,
                c.inicio AS fecha_inicio,
                COALESCE(up.ultima_fecha_pago, c.inicio) AS fecha_base,
                DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                    '+' || (c.frecuencia / 30) || ' months') AS proximo_pago,
                c.frecuencia,
                ROUND(JULIANDAY('now') - 
                    JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) AS dias_transcurridos,
                CASE 
                    WHEN ROUND(JULIANDAY('now') - 
                            JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= 33 
                    THEN 'En corte'
                    WHEN ROUND(JULIANDAY('now') - 
                            JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) > c.frecuencia 
                    THEN 'Pago pendiente'
                    WHEN ROUND(JULIANDAY('now') - 
                            JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= (c.frecuencia - 3) 
                    THEN 'Cerca'
                    ELSE 'Al día'
                END AS estado_pago,
                s.monto,
                s.correo,
                c.comentario
            FROM clientes c
            LEFT JOIN ultimo_pago up ON c.id = up.cliente_id
            INNER JOIN suscripcion s ON c.id = s.cliente_id
            WHERE c.estado = 'Activo'
            ORDER BY dias_transcurridos DESC;
            ''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error consultando estados de pago: {e}")
            return []
        finally:
            conn.close()
    return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def insertar_pago(cliente_id: int, fecha_pago: str, monto_pagado: int) -> bool:
    """
    Registra un nuevo pago y actualiza el saldo pendiente y saldo neto del cliente,
    utilizando como cuota la suma de los montos de sus suscripciones (ya que un cliente
    puede tener varias suscripciones). Se valida que la diferencia entre la frecuencia de pago
    y los días transcurridos desde el último pago (o la fecha de inicio si no hay pagos previos)
    sea de 3 días o menos. Si la diferencia es mayor, se rechaza el pago y se requiere actualizar
    la fecha de inicio del cliente (reiniciar el contrato).

    Args:
        cliente_id (int): ID del cliente.
        fecha_pago (str): Fecha del pago en formato 'YYYY-MM-DD'.
        monto_pagado (int): Monto abonado en el pago.

    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
    import datetime, sqlite3

    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Obtener datos del cliente y la suma de los montos de sus suscripciones
            cursor.execute('''
                SELECT c.nombre, c.inicio, c.frecuencia, COALESCE(SUM(s.monto),0) AS cuota, c.saldo_pendiente
                FROM clientes c
                JOIN suscripcion s ON c.id = s.cliente_id
                WHERE c.id = ?
                GROUP BY c.id, c.nombre, c.inicio, c.frecuencia, c.saldo_pendiente
            ''', (cliente_id,))
            resultado = cursor.fetchone()
            if not resultado:
                raise ValueError("Cliente o suscripciones no encontradas")
            nombre_cliente, fecha_inicio, frecuencia, cuota, saldo_pendiente = resultado
            
            # Convertir las fechas a objetos datetime.
            fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_pago_obj = datetime.datetime.strptime(fecha_pago, '%Y-%m-%d')
            
            # Obtener la fecha del último pago realizado por el cliente.
            cursor.execute('''
                SELECT MAX(fecha_pago)
                FROM pagos
                WHERE cliente_id = ?
            ''', (cliente_id,))
            ultima_fecha_pago = cursor.fetchone()[0]
            
            if ultima_fecha_pago:
                fecha_base_obj = datetime.datetime.strptime(ultima_fecha_pago, '%Y-%m-%d')
            else:
                fecha_base_obj = fecha_inicio_obj
            
            # Calcular los días transcurridos desde la fecha base hasta la fecha de pago.
            dias_transcurridos = (fecha_pago_obj - fecha_base_obj).days
            
            # Calcular la diferencia entre la frecuencia de pago y los días transcurridos.
            diferencia = abs(frecuencia - dias_transcurridos)
            
            # Validar que la diferencia sea de 3 días o menos.
            if diferencia > 3:
                raise ValueError("La diferencia entre la frecuencia de pago y los días transcurridos es mayor a 3 días. "
                                 "Por favor, actualice la fecha de inicio del cliente para reiniciar el contrato.")
            
            # Calcular el total a pagar en el período actual.
            total_a_pagar = cuota + saldo_pendiente
            
            # Calcular el nuevo saldo pendiente (lo que no se cubre del total a pagar).
            nuevo_saldo_pendiente = max(0, total_a_pagar - monto_pagado)
            # El saldo neto se actualiza como la suma de la cuota y el nuevo saldo pendiente.
            nuevo_saldo_neto = cuota + nuevo_saldo_pendiente
            
            # Registrar el pago en la tabla 'pagos' (sin almacenar el nombre, ya que se relaciona por cliente_id).
            cursor.execute('''
                INSERT INTO pagos (cliente_id, fecha_pago)
                VALUES (?, ?)
            ''', (cliente_id, fecha_pago))
            
            # Actualizar el registro del cliente con el nuevo saldo pendiente y saldo neto.
            cursor.execute('''
                UPDATE clientes
                SET saldo_pendiente = ?, saldo_neto = ?
                WHERE id = ?
            ''', (nuevo_saldo_pendiente, nuevo_saldo_neto, cliente_id))
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            print(f"Error insertando pago: {e}")
            return False
        except ValueError as e:
            print(f"Error de validación: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_estado_pago_cliente(cliente_id: int):
    """
    Obtiene el estado de pago para un cliente específico.
    
    Args:
        cliente_id (int): ID del cliente

    Returns:
        tuple: Datos del cliente o None si no existe.
               Se espera que la consulta retorne los siguientes campos:
               0: id, 1: nombre, 2: inicio, 3: whatsapp, 4: estado, 5: frecuencia, 
               6: monto, 7: correo, 8: comentario, 9: fecha_base, 10: proximo_pago,
               11: días_transcurridos, 12: estado_pago, 13: saldo_pendiente, 14: saldo_neto
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = '''
                WITH ultimo_pago AS (
                SELECT cliente_id, MAX(fecha_pago) AS ultima_fecha_pago
                FROM pagos 
                WHERE cliente_id = :cid
                GROUP BY cliente_id
            ),
            sus AS (
                SELECT cliente_id, 
                    SUM(monto) AS pago_mensual,
                    group_concat(correo, ', ') AS correos
                FROM suscripcion
                WHERE cliente_id = :cid
                GROUP BY cliente_id
            )
            SELECT 
                c.id,
                c.nombre,
                c.inicio,
                c.whatsapp,
                c.estado,
                c.frecuencia,
                IFNULL(s.pago_mensual, 0) AS pago_mensual,
                IFNULL(s.correos, '') AS correos,
                c.comentario,
                COALESCE(up.ultima_fecha_pago, c.inicio) AS fecha_base,
                DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                    '+' || (c.frecuencia / 30) || ' months') AS proximo_pago,
                ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) AS dias_transcurridos,
                CASE 
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= 33 
                        THEN 'En corte'
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) > c.frecuencia 
                        THEN 'Pendiente'
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= (c.frecuencia - 3) 
                        THEN 'Cerca'
                    ELSE 'Al día'
                END AS estado_pago,
                c.saldo_pendiente,
                c.saldo_neto
            FROM clientes c
            LEFT JOIN ultimo_pago up ON c.id = up.cliente_id
            LEFT JOIN sus s ON c.id = s.cliente_id
            WHERE c.id = :cid;
            '''
            cursor.execute(query, {"cid": cliente_id})
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error consultando cliente: {e}")
            return None
        finally:
            conn.close()
    return None
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def insertar_cliente(nombre: str, whatsapp: str, fecha_inicio: str, estado: str, 
                     frecuencia: int, comentario: str) -> bool:
    """
    Inserta un nuevo cliente en la base de datos.

    Args:
        nombre (str): Nombre del cliente
        whatsapp (str): Número de WhatsApp
        fecha_inicio (str): Fecha de inicio (YYYY-MM-DD)
        estado (str): Estado del cliente (Activo/Inactivo)
        frecuencia (int): Frecuencia de pago en días
        monto (float): Monto del pago
        correo (str): Dirección de correo electrónico
        comentario (str): Comentario adicional

    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clientes (nombre, whatsapp, inicio, estado, frecuencia, comentario)
                VALUES (?, ?, ?, ?, ?, ?)
            ''', (nombre, whatsapp, fecha_inicio, estado, frecuencia, comentario))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error insertando cliente: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_whatsapp_by_id(cliente_id: int) -> str:
    """
    Obtiene el número de WhatsApp de un cliente por su ID.
    
    Args:
        cliente_id (int): ID del cliente en la base de datos
        
    Returns:
        str: Número de WhatsApp del cliente o None si no existe
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT whatsapp 
                FROM clientes 
                WHERE id = ?
            """, (cliente_id,))
            result = cursor.fetchone()
            return result[0] if result else None
        except sqlite3.Error as e:
            print(f"Error consultando WhatsApp: {e}")
            return None
        finally:
            conn.close()
    return None
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def obtener_clientes_por_estado(estado: str):
    """
    Obtiene los clientes activos filtrados por el estado de pago especificado.

    Args:
        estado (str): Estado de pago para filtrar ('En corte', 'Pago pendiente', 'Cerca', 'Al día').

    Returns:
        list: Lista de listas con:
            - nombre (str)
            - whatsapp (str)
            - monto (float)
            - correo (str)
            - comentario (str)
            - ultimo_pago (str)
            - proximo_pago (str)
            - estado (str): Estado de pago según los criterios definidos
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
            WITH ultimo_pago AS (
            SELECT
                cliente_id,
                MAX(fecha_pago) AS ultima_fecha_pago
            FROM pagos
            GROUP BY cliente_id
        )
        SELECT 
            c.nombre,
            c.whatsapp,
            s.monto,
            s.correo,
            c.comentario,
            COALESCE(up.ultima_fecha_pago, c.inicio) AS ultimo_pago,
            DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                '+' || (c.frecuencia / 30) || ' months') AS proximo_pago,
            CASE 
                WHEN ROUND(JULIANDAY('now') - 
                        JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= 33 
                THEN 'En corte'
                WHEN ROUND(JULIANDAY('now') - 
                        JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) > c.frecuencia 
                THEN 'Pago pendiente'
                WHEN ROUND(JULIANDAY('now') - 
                        JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= (c.frecuencia - 3) 
                THEN 'Cerca'
                ELSE 'Al día'
            END AS estado
        FROM clientes c
        LEFT JOIN ultimo_pago up ON c.id = up.cliente_id
        LEFT JOIN suscripcion s ON c.id = s.cliente_id
        WHERE c.estado = 'Activo' 
        AND (
            CASE 
                WHEN ROUND(JULIANDAY('now') - 
                        JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= 33 
                THEN 'En corte'
                WHEN ROUND(JULIANDAY('now') - 
                        JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) > c.frecuencia 
                THEN 'Pago pendiente'
                WHEN ROUND(JULIANDAY('now') - 
                        JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= (c.frecuencia - 3) 
                THEN 'Cerca'
                ELSE 'Al día'
            END = ?  -- Aquí se filtra por estado dinámicamente
        )
        ORDER BY CASE estado 
            WHEN 'En corte' THEN 1
            WHEN 'Pago pendiente' THEN 2
            WHEN 'Cerca' THEN 3
            ELSE 4
        END;
            """
            cursor.execute(query, (estado,))
            clientes = cursor.fetchall()
            # Convertir tupla a lista para devolver como lista
            return [list(cliente) for cliente in clientes]
        except sqlite3.Error as e:
            print(f"Error consultando estados de pago: {e}")
            return []
        finally:
            conn.close()
    return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def obtener_todos_los_clientes():
    """
    Obtiene todos los clientes activos sin filtro de estado.

    Returns:
        list: Lista de listas con la información de todos los clientes activos.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                WITH ultimo_pago AS (
                SELECT
                    cliente_id,
                    MAX(fecha_pago) AS ultima_fecha_pago
                FROM pagos
                GROUP BY cliente_id
            )
            SELECT 
                c.nombre,
                c.whatsapp,
                s.monto,
                s.correo,
                c.comentario,
                COALESCE(up.ultima_fecha_pago, c.inicio) AS ultimo_pago,
                DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                    '+' || (c.frecuencia / 30) || ' months') AS proximo_pago,
                CASE 
                    WHEN ROUND(JULIANDAY('now') - 
                            JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= 33 
                    THEN 'En corte'
                    WHEN ROUND(JULIANDAY('now') - 
                            JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) > c.frecuencia 
                    THEN 'Pago pendiente'
                    WHEN ROUND(JULIANDAY('now') - 
                            JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= (c.frecuencia - 3) 
                    THEN 'Cerca'
                    ELSE 'Al día'
                END AS estado
            FROM clientes c
            LEFT JOIN ultimo_pago up ON c.id = up.cliente_id
            LEFT JOIN suscripcion s ON c.id = s.cliente_id
            WHERE c.estado = 'Activo'
            ORDER BY CASE estado 
                WHEN 'En corte' THEN 1
                WHEN 'Pago pendiente' THEN 2
                WHEN 'Cerca' THEN 3
                ELSE 4
            END;

            ''')
            clientes = cursor.fetchall()
            # Convertir tupla a lista para devolver como lista
            return [list(cliente) for cliente in clientes]
        except sqlite3.Error as e:
            print(f"Error obteniendo todos los clientes: {e}")
            return []
        finally:
            conn.close()
    return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def obtener_credenciales():
    """
    Obtiene las credenciales de correo desde la base de datos utilizando connect_to_database.

    Returns:
        tuple: Una tupla con (sender_email, sender_password, receiver_email), o None si falla.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT sender_email, sender_password, receiver_email FROM correo LIMIT 1")
            credenciales = cursor.fetchone()
            return credenciales  # Devuelve una tupla (sender_email, sender_password, receiver_email)
        except sqlite3.Error as e:
            print(f"Error al obtener credenciales: {e}")
            return None
        finally:
            conn.close()
    return None
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def actualizar_credenciales(sender_email: str, sender_password: str, receiver_email: str) -> bool:
    """
    Actualiza las credenciales de correo en la base de datos utilizando connect_to_database.

    Args:
        sender_email (str): Correo del remitente.
        sender_password (str): Contraseña del remitente.
        receiver_email (str): Correo del destinatario.

    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Verifica si ya existen credenciales
            cursor.execute("SELECT COUNT(*) FROM correo")
            existe = cursor.fetchone()[0]

            if existe:
                # Actualiza las credenciales existentes
                cursor.execute("""
                    UPDATE correo
                    SET sender_email = ?, sender_password = ?, receiver_email = ?
                """, (sender_email, sender_password, receiver_email))
            else:
                # Inserta nuevas credenciales si no existen
                cursor.execute("""
                    INSERT INTO correo (sender_email, sender_password, receiver_email)
                    VALUES (?, ?, ?)
                """, (sender_email, sender_password, receiver_email))
            
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar credenciales: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def obtener_numeros_whatsapp():
    """Obtiene la lista de números de WhatsApp de la base de datos."""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT whatsapp FROM clientes WHERE whatsapp IS NOT NULL")
            numeros = [row[0] for row in cursor.fetchall()]
            return numeros
        except sqlite3.Error as e:
            print(f"Error obteniendo números de WhatsApp: {e}")
            return []
        finally:
            conn.close()
    return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_correos_clientes():
    """Obtiene una lista de correos únicos de la tabla clientes."""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT DISTINCT correo FROM clientes WHERE correo IS NOT NULL")
            resultados = [row[0] for row in cursor.fetchall()]
            return resultados
        except sqlite3.Error as e:
            print(f"Error obteniendo correos: {e}")
            return []
        finally:
            conn.close()
    return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cuentas():
    """Obtiene todos los registros de la tabla cuentas."""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, correo, costo, servicio FROM cuentas")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error obteniendo cuentas: {e}")
            return []
        finally:
            conn.close()
    return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def insertar_cuenta(correo: str, costo: int, servicio: str) -> bool:
    """Inserta una nueva cuenta en la tabla cuentas."""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO cuentas (correo, costo, servicio)
                VALUES (?, ?, ?)
            """, (correo, costo, servicio))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error insertando cuenta: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def actualizar_cuenta(cuenta_id: int, correo: str, costo: int, servicio: str) -> bool:
    """Actualiza los datos de una cuenta existente."""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE cuentas
                SET correo = ?, costo = ?, servicio = ?
                WHERE id = ?
            """, (correo, costo, servicio, cuenta_id))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error actualizando cuenta: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_cliente_por_id(cliente_id: int):
    """
    Obtiene el registro de un cliente a partir de su ID.

    Args:
        cliente_id (int): El ID del cliente a buscar.

    Returns:
        tuple o None: Una tupla con los datos del cliente si se encuentra, o None en caso de error o si no existe.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id = ?", (cliente_id,))
            cliente = cursor.fetchone()
            return cliente
        except sqlite3.Error as e:
            print(f"Error al obtener el cliente con ID {cliente_id}: {e}")
            return None
        finally:
            conn.close()
    return None
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_clientes_autocomplete():
    """
    Obtiene una lista de tuplas (id, nombre) de todos los clientes para usarse en AutoComplete.

    Returns:
        list: Lista de tuplas con (id, nombre) de cada cliente.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT id, nombre FROM clientes")
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error obteniendo clientes para autocomplete: {e}")
            return []
        finally:
            conn.close()
    return []

