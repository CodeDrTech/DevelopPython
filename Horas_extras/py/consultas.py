import pandas as pd
from database import connect_to_database
import sqlite3

def cargar_empleados_excel(ruta_excel):
    """Lee empleados desde Excel con rangos específicos C4:C* y H4:H*"""
    try:
        # Leer rangos específicos del Excel
        df_codigo = pd.read_excel(ruta_excel, usecols="C", skiprows=3)
        df_nombre = pd.read_excel(ruta_excel, usecols="H", skiprows=3)
        
        # Combinar en un solo DataFrame
        df = pd.DataFrame({
            'Codigo': df_codigo.iloc[:, 0],
            'Nombre': df_nombre.iloc[:, 0]
        }).dropna()  # Eliminar filas vacías
        
        return df
    except Exception as e:
        print(f"Error leyendo Excel: {e}")
        return None

def insertar_empleados(empleados_df):
    """Inserta o actualiza múltiples empleados"""
    conn = connect_to_database()
    if conn and not empleados_df.empty:
        try:
            cursor = conn.cursor()
            for _, row in empleados_df.iterrows():
                cursor.execute('''
                    INSERT OR REPLACE INTO Empleados (Codigo, Nombre)
                    VALUES (?, ?)
                ''', (int(row['Codigo']), row['Nombre']))
            
            conn.commit()
            print(f"Se cargaron {len(empleados_df)} empleados")
            return True
        except sqlite3.Error as e:
            print(f"Error en base de datos: {e}")
            return False
        finally:
            conn.close()
    return False

def importar_empleados_desde_excel(ruta_archivo):
    """Función principal para importar empleados"""
    df = cargar_empleados_excel(ruta_archivo)
    if df is not None:
        return insertar_empleados(df)
    return False


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