from database import connect_to_database
import sqlite3

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
