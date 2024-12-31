import os
import sqlite3
import sys

def obtener_ruta_recurso(ruta_relativa):
    """Obtiene la ruta del recurso, ya sea en desarrollo o en el ejecutable."""
    try:
        base_path = sys._MEIPASS  # Carpeta temporal creada por PyInstaller
    except AttributeError:
        # Ruta base para desarrollo: carpeta raíz del proyecto
        base_path = os.path.abspath(os.path.dirname(__file__))  # Aquí corriges la ruta
        base_path = os.path.dirname(base_path)  # Retrocede un nivel para incluir "Horas_extras"
    return os.path.join(base_path, ruta_relativa)

# Ajustamos la ruta a la base de datos
DATABASE_URL = obtener_ruta_recurso(os.path.join("data", "HorasExtras.db"))

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
