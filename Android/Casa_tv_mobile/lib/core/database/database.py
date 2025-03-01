import sqlite3
import os
import shutil

def get_database_path():
    db_name = "casa_tv.db"
    
    is_android = os.path.exists("/data/user/0/")
    
    if is_android:
        app_files_dir = "/data/user/0/com.flet.lib/files"
        db_path = os.path.join(app_files_dir, db_name)
        
        if not os.path.exists(db_path):
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
                        break
                    except Exception:
                        continue
        
        return db_path
    else:
        return os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))), 
                            "data", db_name)



# Update global variable to use the function
DATABASE_PATH = get_database_path()

def connect_to_database():
    try:
        global DATABASE_PATH
        DATABASE_PATH = get_database_path()
        return sqlite3.connect(DATABASE_PATH)
    except sqlite3.Error:
        return None