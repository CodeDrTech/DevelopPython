import os
import shutil
import sqlite3
from datetime import datetime

class DatabaseBackup:
    def __init__(self):
        self.is_android = os.path.exists("/data/user/0/")
        if self.is_android:
            self.db_path = "/data/user/0/com.flet.lib/files/casa_tv.db"
        else:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
            self.db_path = os.path.join(base_dir, "data", "casa_tv.db")

    def create_backup(self):
        try:
            if self.is_android:
                backup_dir = "/storage/emulated/0/Download/CasaTVBackups"
            else:
                base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
                backup_dir = os.path.join(base_dir, "backups")

            if not os.path.exists(backup_dir):
                os.makedirs(backup_dir)

            backup_file = os.path.join(backup_dir, "database.db")

            if not os.path.exists(self.db_path):
                return False, "No se encontró la base de datos original"

            shutil.copy2(self.db_path, backup_file)
            
            if os.path.exists(backup_file):
                return True, f"Backup guardado en {backup_dir}"
            else:
                return False, "No se pudo crear el archivo de backup"

        except Exception as e:
            return False, f"Error al crear backup: {str(e)}"

    def get_backups_list(self):
        """Obtener lista de backups disponibles"""
        try:
            if not os.path.exists(self.backup_dir):
                return []
            
            backups = []
            for file in os.listdir(self.backup_dir):
                if file.startswith("casa_tv_backup_") and file.endswith(".db"):
                    file_path = os.path.join(self.backup_dir, file)
                    size = os.path.getsize(file_path)
                    date = datetime.fromtimestamp(os.path.getctime(file_path))
                    backups.append({
                        "name": file,
                        "path": file_path,
                        "size": size,
                        "date": date
                    })
            
            return sorted(backups, key=lambda x: x["date"], reverse=True)
        except Exception:
            return []

    def restore_backup(self, backup_path):
        """Restaurar un backup específico"""
        try:
            if not os.path.exists(backup_path):
                return False, "Archivo de backup no encontrado"

            # Crear backup del actual antes de restaurar
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            temp_backup = os.path.join(self.backup_dir, f"pre_restore_backup_{timestamp}.db")
            shutil.copy2(self.db_path, temp_backup)

            # Restaurar el backup
            shutil.copy2(backup_path, self.db_path)

            return True, "Backup restaurado exitosamente"
        except Exception as e:
            return False, f"Error en restauración: {str(e)}"