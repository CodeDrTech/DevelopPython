from dotenv import load_dotenv
import os, sqlite3

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(BASE_DIR, "data")
DATABASE_URL = os.path.join(DATA_DIR, "HorasExtras.db")

def connect_to_database():
    """Conecta a la base de datos existente"""
    if not os.path.exists(DATABASE_URL):
        raise FileNotFoundError(f"Base de datos no encontrada en: {DATABASE_URL}")
    
    try:
        return sqlite3.connect(DATABASE_URL)
    except sqlite3.Error as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

__all__ = ['DATABASE_URL', 'connect_to_database']