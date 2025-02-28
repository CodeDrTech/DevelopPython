import sqlite3
import os

# Define the path to your database file
DATABASE_PATH = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 
                            "data", "casa_tv.db")

def connect_to_database():
    """
    Establishes a connection to the SQLite database.
    
    Returns:
        sqlite3.Connection: A connection object or None if connection fails
    """
    try:
        conn = sqlite3.connect(DATABASE_PATH)
        return conn
    except sqlite3.Error as e:
        print(f"Error al conectar con la base de datos: {e}")
        return None