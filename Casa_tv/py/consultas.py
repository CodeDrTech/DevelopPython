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
                ORDER BY nombre ASC
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
def get_clientes_pagos():
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
                WHERE estado = 'Activo'
                ORDER BY date(inicio) DESC;
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
    Actualiza los datos de un cliente en la base de datos. Si la fecha de inicio se actualiza,
    también se actualiza el último pago (en la tabla pagos) con esa misma fecha, ya que se reinicia el contrato.
    """
    if not all([cliente_id, nombre, whatsapp, fecha_inicio, estado, frecuencia]):
        raise ValueError("Todos los campos son requeridos")
    
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # Obtener la fecha de inicio actual del cliente
            cursor.execute("SELECT inicio FROM clientes WHERE id = ?", (cliente_id,))
            row = cursor.fetchone()
            if not row:
                raise ValueError(f"No se encontró el cliente con ID {cliente_id}")
            
            old_fecha_inicio = row[0]

            # Actualizar los datos del cliente
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
            
            # Si la fecha de inicio cambió, se actualiza el último pago registrado
            if old_fecha_inicio != fecha_inicio:
                cursor.execute('''
                    SELECT id, fecha_pago 
                    FROM pagos
                    WHERE cliente_id = ?
                    ORDER BY fecha_pago DESC
                    LIMIT 1
                ''', (cliente_id,))
                last_payment = cursor.fetchone()
                
                if last_payment:
                    last_payment_id = last_payment[0]
                    cursor.execute(
                        "UPDATE pagos SET fecha_pago = ? WHERE id = ?", 
                        (fecha_inicio, last_payment_id)
                    )
            
            conn.commit()
            return True
            
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Error SQL actualizando cliente: {str(e)}")
            raise Exception(f"Error actualizando cliente en la base de datos: {str(e)}")
        except Exception as e:
            conn.rollback()
            print(f"Error general actualizando cliente: {str(e)}")
            raise
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
                c.id AS cliente_id,                                  -- índice 0
                c.nombre AS nombre_cliente,                          -- índice 1
                c.inicio AS fecha_inicio,                            -- índice 2
                COALESCE(up.ultima_fecha_pago, c.inicio) AS fecha_base,  -- índice 3
                DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                    '+' || (c.frecuencia / 30) || ' months') AS proximo_pago,  -- índice 4
                c.frecuencia,                                        -- índice 5
                ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) AS dias_transcurridos,  -- índice 6
                CASE 
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > 33 
                        THEN 'En corte'
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > c.frecuencia 
                        THEN 'Pago pendiente'
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) >= (c.frecuencia - 3) 
                        THEN 'Cerca'
                    ELSE 'Al día'
                END AS estado_pago,                                -- índice 7
                IFNULL(SUM(s.monto), 0) AS monto,                   -- índice 8
                IFNULL(GROUP_CONCAT(s.correo, ', '), '') AS correo, -- índice 9
                c.comentario                                      -- índice 10
            FROM clientes c
            LEFT JOIN ultimo_pago up ON c.id = up.cliente_id
            INNER JOIN suscripcion s ON c.id = s.cliente_id
            WHERE c.estado = 'Activo'
            GROUP BY c.id
            ORDER BY nombre DESC;
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
def get_total_pagos_mes_actual():
    """
    Obtiene la suma de los pagos realizados en el mes actual.
    
    Returns:
        float: Suma de los montos de pagos del mes actual. 
               Retorna 0 si no hay pagos o hay un error.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT COALESCE(SUM(s.monto) - SUM(c.saldo_pendiente), 0) AS utilidad
                FROM pagos p
                INNER JOIN suscripcion s ON p.cliente_id = s.cliente_id
                INNER JOIN clientes c ON p.cliente_id = c.id
                WHERE strftime('%Y-%m', p.fecha_pago) = strftime('%Y-%m', 'now')
                AND c.estado = 'Activo';
            ''')
            total = cursor.fetchone()[0]
            return total
        except sqlite3.Error as e:
            print(f"Error consultando pagos del mes actual: {e}")
            return 0
        finally:
            conn.close()
    return 0
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def insertar_pago(cliente_id: int, fecha_pago: str, monto_pagado: int) -> bool:
    """Registra un nuevo pago y actualiza el saldo pendiente y saldo neto del cliente.
    
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
            
            # ... validación de fechas y días transcurridos ...
            
            # Calcular el total a pagar y nuevos saldos
            total_a_pagar = cuota + saldo_pendiente
            nuevo_saldo_pendiente = max(0, total_a_pagar - monto_pagado)
            nuevo_saldo_neto = cuota + nuevo_saldo_pendiente
            
            # Registrar el pago con todos los campos
            cursor.execute('''
                INSERT INTO pagos (cliente_id, fecha_pago, monto_pagado, deuda_pendiente, saldo_neto)
                VALUES (?, ?, ?, ?, ?)
            ''', (cliente_id, fecha_pago, monto_pagado, nuevo_saldo_pendiente, nuevo_saldo_neto))
            
            # Actualizar saldos del cliente
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
                    GROUP_CONCAT(correo, ', ') AS correos
                FROM suscripcion
                WHERE cliente_id = :cid
                GROUP BY cliente_id
            )
            SELECT 
                c.id,                                                    -- índice 0
                c.nombre,                                                -- índice 1
                c.inicio,                                                -- índice 2
                c.whatsapp,                                              -- índice 3
                c.estado,                                                -- índice 4
                c.frecuencia,                                            -- índice 5
                IFNULL(s.pago_mensual, 0) AS pago_mensual,               -- índice 6
                IFNULL(s.correos, '') AS correos,                        -- índice 7
                c.comentario,                                            -- índice 8
                COALESCE(up.ultima_fecha_pago, c.inicio) AS fecha_base,   -- índice 9
                DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                    '+' || (c.frecuencia / 30) || ' months') AS proximo_pago,  -- índice 10
                ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) AS dias_transcurridos,  -- índice 11
                CASE 
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > 33 
                        THEN 'En corte'
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > c.frecuencia 
                        THEN 'Pago pendiente'
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) >= (c.frecuencia - 3) 
                        THEN 'Cerca'
                    ELSE 'Al día'
                END AS estado_pago,                                    -- índice 12
                c.saldo_pendiente,                                       -- índice 13
                c.saldo_neto                                             -- índice 14
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
            SELECT cliente_id, MAX(fecha_pago) AS ultima_fecha_pago
            FROM pagos
            GROUP BY cliente_id
        )
        SELECT 
            c.nombre,                                           -- índice 0
            c.whatsapp,                                         -- índice 1
            IFNULL(SUM(s.monto), 0) AS monto,                     -- índice 2 (suma de montos de suscripciones)
            IFNULL(GROUP_CONCAT(s.correo, ', '), '') AS correo,   -- índice 3 (todos los correos concatenados)
            c.comentario,                                       -- índice 4
            COALESCE(up.ultima_fecha_pago, c.inicio) AS ultimo_pago,  -- índice 5
            DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                '+' || (c.frecuencia / 30) || ' months') AS proximo_pago,  -- índice 6
            CASE 
                WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > 33 
                    THEN 'En corte'
                WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > c.frecuencia 
                    THEN 'Pago pendiente'
                WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) >= (c.frecuencia - 3) 
                    THEN 'Cerca'
                ELSE 'Al día'
            END AS estado,                                     -- índice 7
            c.saldo_pendiente AS deuda                         -- índice 8
        FROM clientes c
        LEFT JOIN ultimo_pago up ON c.id = up.cliente_id
        LEFT JOIN suscripcion s ON c.id = s.cliente_id
        WHERE c.estado = 'Activo'
        AND (
            CASE 
                WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > 33 
                    THEN 'En corte'
                WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > c.frecuencia 
                    THEN 'Pago pendiente'
                WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) >= (c.frecuencia - 3) 
                    THEN 'Cerca'
                ELSE 'Al día'
            END = ?
        )
        GROUP BY c.id, c.nombre, c.whatsapp, c.inicio, c.estado, c.frecuencia, c.comentario, c.saldo_pendiente
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
                SELECT cliente_id, MAX(fecha_pago) AS ultima_fecha_pago
                FROM pagos
                GROUP BY cliente_id
            )
            SELECT 
                c.nombre,                                           -- índice 0
                c.whatsapp,                                         -- índice 1
                IFNULL(SUM(s.monto), 0) AS monto,                     -- índice 2 (suma de montos de suscripciones)
                IFNULL(group_concat(s.correo, ', '), '') AS correo,   -- índice 3 (todos los correos concatenados)
                c.comentario,                                       -- índice 4
                COALESCE(up.ultima_fecha_pago, c.inicio) AS ultimo_pago,  -- índice 5
                DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                    '+' || (c.frecuencia / 30) || ' months') AS proximo_pago,  -- índice 6
                CASE 
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > 33 
                        THEN 'En corte'
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) > c.frecuencia 
                        THEN 'Pago pendiente'
                    WHEN ROUND(JULIANDAY('now') - JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio)) - 1) >= (c.frecuencia - 3) 
                        THEN 'Cerca'
                    ELSE 'Al día'
                END AS estado,                                     -- índice 7
                c.saldo_pendiente AS deuda                         -- índice 8
            FROM clientes c
            LEFT JOIN ultimo_pago up ON c.id = up.cliente_id
            LEFT JOIN suscripcion s ON c.id = s.cliente_id
            WHERE c.estado = 'Activo'
            GROUP BY c.id, c.nombre, c.whatsapp, c.inicio, c.estado, c.frecuencia, c.comentario, c.saldo_pendiente
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
            cursor.execute("SELECT id, correo, costo, servicio FROM cuentas ORDER by correo")
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
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_suscripciones():
    """
    Obtiene todas las suscripciones con joins para el nombre del cliente y el servicio.
    
    Returns:
        list: Lista de tuplas con (suscripcion.id, cliente.nombre, cuenta.servicio, suscripcion.monto, suscripcion.correo)
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            query = """
                SELECT s.id, cl.nombre, cu.servicio, s.monto, s.correo
                FROM suscripcion s
                JOIN clientes cl ON s.cliente_id = cl.id
                JOIN cuentas cu ON s.cuenta_id = cu.id
                ORDER BY cl.nombre;
            """
            cursor.execute(query)
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error obteniendo suscripciones: {e}")
            return []
        finally:
            conn.close()
    return []

def get_cliente_by_nombre(nombre_id: int):
    """
    Obtiene los datos de un cliente por su ID.
    
    Args:
        nombre (int): El ID del cliente.
        
    Returns:
        tuple or None: Los datos del cliente o None si no se encuentra.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM clientes WHERE id = ?", (nombre_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error obteniendo cliente: {e}")
            return None
        finally:
            conn.close()
    return None

def get_cuenta_by_servicio(servicio_id: int):
    """
    Obtiene los datos de una cuenta por su ID.
    
    Args:
        servicio (int): El ID de la cuenta.
        
    Returns:
        tuple or None: Los datos de la cuenta o None si no se encuentra.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM cuentas WHERE id = ?", (servicio_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error obteniendo cuenta: {e}")
            return None
        finally:
            conn.close()
    return None

def insertar_suscripcion(cliente_id: int, cuenta_id: int, monto: int, correo: str) -> bool:
    """
    Inserta una nueva suscripción.
    
    Args:
        cliente_id (int): ID del cliente.
        cuenta_id (int): ID de la cuenta.
        monto (int): Monto asignado a la suscripción.
        correo (str): Correo asociado a la suscripción.
    
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO suscripcion (cliente_id, cuenta_id, monto, correo)
                VALUES (?, ?, ?, ?)
            """, (cliente_id, cuenta_id, monto, correo))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error insertando suscripcion: {e}")
            return False
        finally:
            conn.close()
    return False

def actualizar_suscripcion(suscripcion_id: int, cliente_id: int, cuenta_id: int, monto: int, correo: str) -> bool:
    """
    Actualiza los datos de una suscripción existente.
    
    Args:
        suscripcion_id (int): ID de la suscripción a actualizar.
        cliente_id (int): Nuevo ID del cliente.
        cuenta_id (int): Nuevo ID de la cuenta.
        monto (int): Nuevo monto asignado.
        correo (str): Nuevo correo asociado.
        
    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE suscripcion
                SET cliente_id = ?, cuenta_id = ?, monto = ?, correo = ?
                WHERE id = ?
            """, (cliente_id, cuenta_id, monto, correo, suscripcion_id))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error actualizando suscripcion: {e}")
            return False
        finally:
            conn.close()
    return False

def get_suscripcion_by_id(suscripcion_id: int):
    """
    Obtiene una suscripción específica por su ID.
    
    Args:
        suscripcion_id (int): El ID de la suscripción.
        
    Returns:
        tuple or None: Los datos de la suscripción o None si no se encuentra.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM suscripcion WHERE id = ?", (suscripcion_id,))
            return cursor.fetchone()
        except sqlite3.Error as e:
            print(f"Error obteniendo suscripcion: {e}")
            return None
        finally:
            conn.close()
    return None
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def eliminar_cliente_db(cliente_id: int) -> bool:
    """
    Elimina un cliente de la base de datos.

    Args:
        cliente_id (int): ID del cliente a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = ?", (cliente_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error eliminando cliente: {e}")
            return False
        finally:
            conn.close()
    return False

def tiene_pagos(cliente_id: int) -> bool:
    """
    Verifica si un cliente tiene pagos registrados.

    Args:
        cliente_id (int): ID del cliente a verificar.

    Returns:
        bool: True si el cliente tiene pagos, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM pagos 
                WHERE cliente_id = ?
            """, (cliente_id,))
            result = cursor.fetchone()[0]
            return result > 0
        except sqlite3.Error as e:
            print(f"Error verificando pagos del cliente: {e}")
            return False
        finally:
            conn.close()
    return False

def eliminar_pagos(cliente_id: int) -> bool:
    """
    Elimina todos los pagos asociados a un cliente.

    Args:
        cliente_id (int): ID del cliente cuyos pagos se eliminarán.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM pagos WHERE cliente_id = ?", (cliente_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error eliminando pagos del cliente: {e}")
            return False
        finally:
            conn.close()
    return False

def tiene_suscripciones(cliente_id: int) -> bool:
    """
    Verifica si un cliente tiene suscripciones activas.

    Args:
        cliente_id (int): ID del cliente a verificar.

    Returns:
        bool: True si el cliente tiene suscripciones, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COUNT(*) 
                FROM suscripcion 
                WHERE cliente_id = ?
            """, (cliente_id,))
            result = cursor.fetchone()[0]
            return result > 0
        except sqlite3.Error as e:
            print(f"Error verificando suscripciones del cliente: {e}")
            return False
        finally:
            conn.close()
    return False

def eliminar_suscripciones(cliente_id: int) -> bool:
    """
    Elimina todas las suscripciones asociadas a un cliente.

    Args:
        cliente_id (int): ID del cliente cuyas suscripciones se eliminarán.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM suscripcion WHERE cliente_id = ?", (cliente_id,))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error eliminando suscripciones del cliente: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def eliminar_cuenta_db(cuenta_id: int) -> bool:
    """
    Elimina una cuenta de la base de datos y todas sus suscripciones asociadas.

    Args:
        cuenta_id (int): ID de la cuenta a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            # First delete all subscriptions associated with this account
            cursor.execute("DELETE FROM suscripcion WHERE cuenta_id = ?", (cuenta_id,))
            # Then delete the account
            cursor.execute("DELETE FROM cuentas WHERE id = ?", (cuenta_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            conn.rollback()
            print(f"Error eliminando cuenta: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def eliminar_suscripcion_db(suscripcion_id: int) -> bool:
    """
    Elimina una suscripción de la base de datos.

    Args:
        suscripcion_id (int): ID de la suscripción a eliminar.

    Returns:
        bool: True si la eliminación fue exitosa, False en caso contrario.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM suscripcion WHERE id = ?", (suscripcion_id,))
            conn.commit()
            return cursor.rowcount > 0
        except sqlite3.Error as e:
            print(f"Error eliminando suscripción: {e}")
            return False
        finally:
            conn.close()
    return False

