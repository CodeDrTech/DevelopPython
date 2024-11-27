import pyodbc
from database import connect_to_db  # Asegúrate de que esta función esté implementada correctamente
import flet as ft


# Función genérica para insertar datos
def insertar_dato_generico(tabla, columnas, valores):
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        columnas_str = ', '.join(columnas)
        valores_str = ', '.join(['?'] * len(columnas))
        query = f"INSERT INTO {tabla} ({columnas_str}) VALUES ({valores_str})"
        cursor.execute(query, valores)
        conn.commit()
    except Exception as e:
        raise Exception(f"Error al insertar en {tabla}: {e}")
    finally:
        if conn:
            conn.close()


# Función específica para insertar un usuario
def insertar_nuevo_usuario(nombre, apellidos, cedula, numero_empleado):
    # Inserta el nuevo usuario en la base de datos
    insertar_dato_generico('Usuario',['nombres', 'apellidos', 'cedula', 'numeroEmpleado'],[nombre, apellidos, cedula, numero_empleado])

def insertar_nuevo_equipo(equipo_id, marca, modelo, condicion):
    #Llamada a insertar_dato_generico para la tabla 'Equipo'
    insertar_dato_generico('Equipo',['idUsuario', 'marca', 'modelo', 'condicion'],[equipo_id, marca, modelo, condicion],)

