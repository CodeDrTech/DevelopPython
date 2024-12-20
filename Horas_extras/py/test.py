import sqlite3
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
database_url = os.getenv("DATABASE_URL")

# Imprimir la URL de la base de datos para verificar
print(f"Conectándose a la base de datos en: {database_url}")

# Verificar si el archivo de la base de datos existe
if not os.path.isfile(database_url):
    print(f"El archivo de la base de datos '{database_url}' no existe.")
else:
    print(f"El archivo de la base de datos '{database_url}' existe.")

def connect_to_database():
    """Establece la conexión a la base de datos SQLite."""
    try:
        # Establecer la conexión a la base de datos
        conn = sqlite3.connect(database_url)
        print("Conexión a la base de datos establecida con éxito.")
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")

def get_empleados():
    """Obtiene la lista de empleados de la base de datos."""
    conn = connect_to_database()
    empleados = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Codigo, Nombre FROM Empleados")
            rows = cursor.fetchall()
            for row in rows:
                empleados.append({"codigo": row[0], "nombre": row[1]})
        except sqlite3.Error as e:
            print(f"Error al obtener empleados: {e}")
        finally:
            conn.close()
    return empleados

# Llamar a la función para verificar que funciona correctamente
empleados = get_empleados()
print(empleados)