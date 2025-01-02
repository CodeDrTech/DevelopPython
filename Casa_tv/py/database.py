import os
import sys
import sqlite3

def get_base_dir():
    """
    Obtiene el directorio base del proyecto Casa_tv.
    
    Returns:
        str: Ruta absoluta al directorio Casa_tv
    """
    if getattr(sys, 'frozen', False):
        # Si es ejecutable
        return os.path.dirname(sys.executable)
    else:
        # Si es script, obtiene ruta Casa_tv
        current_file = os.path.abspath(__file__)  # Ruta actual database.py
        py_dir = os.path.dirname(current_file)    # Directorio /py
        return os.path.dirname(py_dir)            # Directorio Casa_tv

# Rutas dinámicas
BASE_DIR = get_base_dir()
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_URL = os.path.join(DATA_DIR, "database.db")

def connect_to_database():
    """Conecta a la base de datos SQLite"""
    try:
        if not os.path.exists(DATABASE_URL):
            raise FileNotFoundError(f"Base de datos no encontrada en: {DATABASE_URL}")
        return sqlite3.connect(DATABASE_URL)
    except sqlite3.Error as e:
        print(f"Error conectando a BD: {e}")
        return None

__all__ = ['DATABASE_URL', 'connect_to_database']