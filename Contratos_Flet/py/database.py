import os
import pyodbc
from dotenv import load_dotenv

# Cargar variables del archivo .env
load_dotenv()

# Conexión a SQL Server
def connect_to_db():
    connection_string = os.getenv("DB_CONNECTION_STRING")
    try:
        conn = pyodbc.connect(connection_string)
        return conn
    except Exception as e:
        print(f"Error al conectar a la base de datos: {e}")
        return None

# Ejemplo de consulta
def get_all_users():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Usuario")
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []
