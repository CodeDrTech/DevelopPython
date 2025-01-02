from database import connect_to_database
import sqlite3

def get_clientes():
    """
    Obtiene todos los clientes ordenados por nombre.

    Esta función se conecta a la base de datos, ejecuta una consulta para obtener 
    todos los clientes ordenados por su nombre y devuelve los resultados.

    Returns:
        list: Una lista de tuplas, donde cada tupla contiene los datos de un cliente 
        (id_cliente, nombre, fecha_inicio, whatsapp, estado, ultimo_pago, frecuencia_pago).
        Si ocurre un error durante la consulta, se devuelve una lista vacía.
    """
    """Obtiene todos los clientes ordenados por nombre"""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id_cliente, nombre, fecha_inicio, whatsapp, 
                       estado, ultimo_pago, frecuencia_pago 
                FROM Clientes 
                ORDER BY nombre
            ''')
            return cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error consultando clientes: {e}")
            return []
        finally:
            conn.close()
    return []

def actualizar_cliente(cliente_id: int, nombre: str, whatsapp: str, estado: str, frecuencia: int) -> bool:
    """
    Actualiza los datos de un cliente en la base de datos.

    Args:
        cliente_id (int): ID del cliente a actualizar
        nombre (str): Nuevo nombre del cliente
        whatsapp (str): Nuevo número de WhatsApp
        estado (str): Nuevo estado (Activo/Inactivo)
        frecuencia (int): Nueva frecuencia de pago en días

    Returns:
        bool: True si la actualización fue exitosa, False en caso contrario

    Raises:
        ValueError: Si los parámetros no son válidos
        sqlite3.Error: Si hay error en la base de datos
    """
    # Validar parámetros
    if not all([cliente_id, nombre, whatsapp, estado, frecuencia]):
        raise ValueError("Todos los campos son obligatorios")
    
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
                    frecuencia_pago = ?
                WHERE id_cliente = ?
            ''', (nombre, whatsapp, estado, frecuencia, cliente_id))
            
            conn.commit()
            return cursor.rowcount > 0
            
        except sqlite3.Error as e:
            print(f"Error actualizando cliente: {e}")
            return False
        finally:
            conn.close()
    return False
