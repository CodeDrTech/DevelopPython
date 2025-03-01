import sqlite3
import os
import shutil

def get_database_path():
    db_name = "casa_tv.db"
    
    is_android = os.path.exists("/data/user/0/")
    
    if is_android:
        app_files_dir = "/data/user/0/com.flet.lib/files"
        db_path = os.path.join(app_files_dir, db_name)
        
        print(f"Android environment detected. Using path: {db_path}")
        
        if not os.path.exists(db_path):
            print(f"Database not found at {db_path}, attempting to copy...")
            
            possible_paths = [
                os.path.join(app_files_dir, "flet", "app", "data", db_name),
                os.path.join(app_files_dir, "assets", "data", db_name),
                os.path.join(app_files_dir, "flet", "app", "assets", "data", db_name),
                os.path.join(app_files_dir, "flet", "app", db_name)
            ]
            
            for path in possible_paths:
                if os.path.exists(path):
                    try:
                        shutil.copy2(path, db_path)
                        print(f"Database copied from {path} to {db_path}")
                        break
                    except Exception as e:
                        print(f"Error copying from {path}: {e}")
        
        return db_path
    else:
        db_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 
                            "data", db_name)
        print(f"Development environment detected. Using path: {db_path}")
        return db_path



# Update global variable to use the function
DATABASE_PATH = get_database_path()

def connect_to_database():
    try:
        global DATABASE_PATH
        DATABASE_PATH = get_database_path()
        
        # Agregar más información de diagnóstico
        if os.path.exists("/data/user/0/"):
            print("\n=== Información de la base de datos en Android ===")
            possible_locations = [
                "/data/user/0/com.flet.lib/files/casa_tv.db",
                "/data/user/0/com.flet.lib/files/flet/app/casa_tv.db",
                "/data/user/0/com.flet.lib/files/flet/app/data/casa_tv.db"
            ]
            
            for loc in possible_locations:
                exists = os.path.exists(loc)
                size = os.path.getsize(loc) if exists else 0
                print(f"Ubicación: {loc}")
                print(f"¿Existe?: {exists}")
                print(f"Tamaño: {size} bytes\n")
        
        print(f"Usando base de datos en: {DATABASE_PATH}")
        print(f"¿Existe?: {os.path.exists(DATABASE_PATH)}")
        print(f"Tamaño: {os.path.getsize(DATABASE_PATH) if os.path.exists(DATABASE_PATH) else 0} bytes")
        
        conn = sqlite3.connect(DATABASE_PATH)
        
        # Check if the database has the necessary tables
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
        tables = cursor.fetchall()
        print(f"Tables in the database: {tables}")
        
        if tables:
            cursor.execute("SELECT COUNT(*) FROM clientes")
            count = cursor.fetchone()[0]
            print(f"Number of clients in the database: {count}")
        
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None