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
            - monto (float)
            - correo (str)
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
                    monto,
                    correo,
                    comentario
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

def actualizar_cliente(cliente_id: int, nombre: str, whatsapp: str, fecha_inicio: str, estado: str, frecuencia: int, monto: float, correo: str, comentario: str) -> bool:
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
                    monto = ?,
                    correo = ?,
                    comentario = ?
                WHERE id = ?
            ''', (nombre, whatsapp, fecha_inicio, estado, frecuencia, monto, correo, comentario, cliente_id))
            
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
                    cliente_id,
                    MAX(fecha_pago) AS ultima_fecha_pago
                FROM pagos
                GROUP BY cliente_id
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
                c.monto,
                c.correo,
                c.comentario
            FROM clientes c
            LEFT JOIN ultimo_pago up ON c.id = up.cliente_id
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
    siempre que la diferencia entre la frecuencia de pago y los días transcurridos
    desde el último pago o la fecha de inicio sea de 3 días o menos. Si la diferencia
    es mayor, se rechaza el pago y se requiere actualizar la fecha de inicio del cliente
    (reiniciar el contrato).

    Args:
        cliente_id (int): ID del cliente.
        fecha_pago (str): Fecha del pago en formato 'YYYY-MM-DD'.
        monto_pagado (int): Monto abonado en el pago.

    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Obtener datos del cliente: nombre, fecha de inicio, frecuencia, monto (cuota), saldo_pendiente.
            cursor.execute('''
                SELECT nombre, inicio, frecuencia, monto, saldo_pendiente 
                FROM clientes 
                WHERE id = ?
            ''', (cliente_id,))
            cliente = cursor.fetchone()
            if not cliente:
                raise ValueError("Cliente no encontrado")
                
            nombre_cliente, fecha_inicio, frecuencia, monto, saldo_pendiente = cliente
            
            # Convertir fechas a objetos datetime.
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
                # Si existe un pago previo, usar la fecha del último pago.
                fecha_base_obj = datetime.datetime.strptime(ultima_fecha_pago, '%Y-%m-%d')
            else:
                # Si no hay pagos previos, usar la fecha de inicio.
                fecha_base_obj = fecha_inicio_obj
            
            # Calcular los días transcurridos desde la fecha base hasta la fecha de pago.
            dias_transcurridos = (fecha_pago_obj - fecha_base_obj).days
            
            # Calcular la diferencia entre la frecuencia de pago y los días transcurridos.
            diferencia = abs(frecuencia - dias_transcurridos)
            
            # Verificar si la diferencia es mayor que 3 días.
            if diferencia > 3:
                raise ValueError("La diferencia entre la frecuencia de pago y los días transcurridos "
                                 "es mayor a 3 días. Por favor, actualice la fecha de inicio del cliente "
                                 "para reiniciar el contrato.")
            
            # Calcular el total que debe pagar en el período actual.
            total_a_pagar = monto + saldo_pendiente
            
            # Calcular el nuevo saldo pendiente (lo que no se cubre del total a pagar).
            nuevo_saldo_pendiente = max(0, total_a_pagar - monto_pagado)
            
            # El saldo neto se actualiza como la suma de la cuota fija y el nuevo saldo pendiente.
            nuevo_saldo_neto = monto + nuevo_saldo_pendiente
            
            # Registrar el pago en la tabla 'pagos'.
            cursor.execute('''
                INSERT INTO pagos (cliente_id, nombre_cliente, fecha_pago)
                VALUES (?, ?, ?)
            ''', (cliente_id, nombre_cliente, fecha_pago))
            
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
    Obtiene estado de pago para un cliente específico.
    
    Args:
        cliente_id (int): ID del cliente

    Returns:
        tuple: Datos del cliente o None si no existe
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                WITH ultimo_pago AS (
                    SELECT cliente_id, MAX(fecha_pago) AS ultima_fecha_pago
                    FROM pagos 
                    WHERE cliente_id = ?
                    GROUP BY cliente_id
                )
                SELECT 
                    c.id,
                    c.nombre,
                    c.inicio,
                    c.whatsapp,
                    c.estado,
                    c.frecuencia,
                    c.monto,
                    c.correo,
                    c.comentario,
                    COALESCE(up.ultima_fecha_pago, c.inicio) AS fecha_base,
                    DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                        '+' || (c.frecuencia / 30) || ' months') AS proximo_pago,
                    ROUND(JULIANDAY('now') - 
                        JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) AS dias_transcurridos,
                    CASE 
                        WHEN ROUND(JULIANDAY('now') - 
                                JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= 33 
                        THEN 'En corte'
                        WHEN ROUND(JULIANDAY('now') - 
                                JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) > c.frecuencia 
                        THEN 'Pendiente'
                        WHEN ROUND(JULIANDAY('now') - 
                                JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) >= (c.frecuencia - 3) 
                        THEN 'Cerca'
                        ELSE 'Al día'
                    END AS estado_pago,
                    c.saldo_pendiente,
                    c.saldo_neto
                FROM clientes c
                LEFT JOIN ultimo_pago up ON c.id = up.cliente_id
                WHERE c.id = ?
            ''', (cliente_id, cliente_id))
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
                     frecuencia: int, monto: float, correo: str, comentario: str) -> bool:
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
                INSERT INTO clientes (nombre, whatsapp, inicio, estado, frecuencia, monto, correo, comentario)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, whatsapp, fecha_inicio, estado, frecuencia, monto, correo, comentario))
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
                c.monto,
                c.correo,
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
            WHERE c.estado = 'Activo' AND (
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
            END = ?)
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
                    c.monto,
                    c.correo,
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

