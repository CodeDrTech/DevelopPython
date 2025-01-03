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
                    frecuencia
                FROM Clientes 
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

def actualizar_cliente(cliente_id: int, nombre: str, whatsapp: str, estado: str, frecuencia: int) -> bool:
    """
    Actualiza los datos de un cliente en la base de datos.

    Args:
        cliente_id (int): ID del cliente a modificar
        nombre (str): Nombre del cliente
        whatsapp (str): Número de WhatsApp
        estado (str): Estado del cliente (Activo/Inactivo)
        frecuencia (int): Frecuencia de pago en días

    Returns:
        bool: True si la actualización fue exitosa, False si hubo error

    Raises:
        ValueError: Si los datos no son válidos
        sqlite3.Error: Si hay error en la base de datos
    """
    # Validar datos
    if not all([cliente_id, nombre, whatsapp, estado, frecuencia]):
        raise ValueError("Todos los campos son requeridos")
    
    if estado not in ['Activo', 'Inactivo']:
        raise ValueError("Estado debe ser 'Activo' o 'Inactivo'")
    
    if frecuencia <= 0:
        raise ValueError("Frecuencia debe ser mayor a 0")

    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                UPDATE Clientes 
                SET nombre = ?,
                    whatsapp = ?,
                    estado = ?,
                    frecuencia = ?
                WHERE id = ?
            ''', (nombre, whatsapp, estado, frecuencia, cliente_id))
            
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
    """
    conn = connect_to_database()  # Reemplazar con tu función de conexión
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
                         '+' || c.frecuencia || ' days') AS proximo_pago,
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
                    END AS estado_pago
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
import datetime
import sqlite3

def insertar_pago(cliente_id: int, fecha_pago: str) -> bool:
    """
    Inserta un nuevo pago manteniendo la secuencia de fechas original del cliente.

    Args:
        cliente_id (int): ID del cliente que realiza el pago
        fecha_pago (str): Fecha del pago actual en formato 'YYYY-MM-DD'

    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            
            # Obtener datos del cliente
            cursor.execute('''
                SELECT nombre, inicio, frecuencia 
                FROM clientes 
                WHERE id = ?
            ''', (cliente_id,))
            
            cliente = cursor.fetchone()
            if not cliente:
                raise ValueError("Cliente no encontrado")
                
            nombre_cliente, fecha_inicio, frecuencia = cliente
            # Validar que frecuencia sea un número positivo
            if frecuencia <= 0:
                raise ValueError("La frecuencia debe ser mayor a cero")
            
            # Convertir fechas a objetos datetime
            fecha_inicio_obj = datetime.datetime.strptime(fecha_inicio, '%Y-%m-%d')
            fecha_pago_obj = datetime.datetime.strptime(fecha_pago, '%Y-%m-%d')
            
            # Calcular cuántos períodos han pasado (en días)
            dias_transcurridos = (fecha_pago_obj - fecha_inicio_obj).days
            
            # Verificar si la fecha de pago está alineada con la frecuencia
            if dias_transcurridos % frecuencia != 0:
                raise ValueError("La fecha de pago no está alineada con la frecuencia del cliente")
            
            # Insertar el pago
            cursor.execute('''
                INSERT INTO pagos (cliente_id, nombre_cliente, fecha_pago)
                VALUES (?, ?, ?)
            ''', (cliente_id, nombre_cliente, fecha_pago))
            
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
                    FROM pagos WHERE cliente_id = ?
                    GROUP BY cliente_id
                )
                SELECT 
                    c.id,
                    c.nombre,
                    c.inicio,
                    COALESCE(up.ultima_fecha_pago, c.inicio) AS fecha_base,
                    DATE(COALESCE(up.ultima_fecha_pago, c.inicio), 
                         '+' || c.frecuencia || ' days') AS proximo_pago,
                    c.frecuencia,
                    ROUND(JULIANDAY('now') - 
                          JULIANDAY(COALESCE(up.ultima_fecha_pago, c.inicio))) 
                          AS dias_transcurridos,
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
                    END AS estado_pago
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
def insertar_cliente(nombre: str, whatsapp: str, fecha_inicio: str, estado: str, frecuencia: int) -> bool:
    """
    Inserta un nuevo cliente en la base de datos.

    Args:
        nombre (str): Nombre del cliente
        whatsapp (str): Número de WhatsApp
        fecha_inicio (str): Fecha de inicio (YYYY-MM-DD)
        estado (str): Estado del cliente (Activo/Inactivo)
        frecuencia (int): Frecuencia de pago en días

    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO clientes (nombre, whatsapp, inicio, estado, frecuencia)
                VALUES (?, ?, ?, ?, ?)
            ''', (nombre, whatsapp, fecha_inicio, estado, frecuencia))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error insertando cliente: {e}")
            return False
        finally:
            conn.close()
    return False
