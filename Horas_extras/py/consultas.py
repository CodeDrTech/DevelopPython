from database import connect_to_database


def get_empleados():
    """Obtiene la lista de empleados de la base de datos."""
    conn = connect_to_database()
    empleados = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Nombre FROM Empleados")  # Solo obtener nombres
            rows = cursor.fetchall()
            for row in rows:
                empleados.append(row[0])  # Agregar solo el nombre
        except sqlite3.Error as e:
            print(f"Error al obtener empleados: {e}")
        finally:
            conn.close()
    return empleados