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