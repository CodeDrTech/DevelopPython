import sqlite3
import os
from dotenv import load_dotenv

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener la URL de la base de datos desde las variables de entorno
database_url = os.getenv("DATABASE_URL")

def connect_to_database():
    """Establece la conexión a la base de datos SQLite."""
    try:
        # Establecer la conexión a la base de datos
        conn = sqlite3.connect(database_url)

        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar a la base de datos: {e}")