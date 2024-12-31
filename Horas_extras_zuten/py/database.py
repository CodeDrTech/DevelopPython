import os
import sys
import sqlite3

def get_base_dir():
    """
    Obtiene la carpeta base del ejecutable o del script.

    Returns:
        str: La ruta de la carpeta base. Si el script está congelado como un ejecutable,
        devuelve la ruta del directorio del ejecutable. Si el script se está ejecutando
        en un entorno de desarrollo, devuelve la ruta del directorio raíz del proyecto.
    """
    """Obtiene la carpeta base del ejecutable o del script."""
    if getattr(sys, 'frozen', False):  # Ejecutable
        return os.path.dirname(sys.executable)
    else:  # Desarrollo
        # Go up one level from py directory to reach project root
        return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Rutas dinámicas
BASE_DIR = get_base_dir()
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_URL = os.path.join(DATA_DIR, "HorasExtras.db")

def connect_to_database():
    """
    Conecta a la base de datos existente.
    Si la base de datos no existe en la ruta especificada por DATABASE_URL, 
    se lanza una excepción FileNotFoundError.
    Returns:
        sqlite3.Connection: Objeto de conexión a la base de datos si la conexión es exitosa.
        None: Si ocurre un error al intentar conectar a la base de datos.
    Raises:
        FileNotFoundError: Si la base de datos no se encuentra en la ruta especificada.
    """
    """Conecta a la base de datos existente."""
    if not os.path.exists(DATABASE_URL):
        raise FileNotFoundError(f"Base de datos no encontrada en: {DATABASE_URL}")
    
    try:
        return sqlite3.connect(DATABASE_URL)
    except sqlite3.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

__all__ = ['DATABASE_URL', 'connect_to_database']
