import pandas as pd
from database import connect_to_database, DATABASE_URL, obtener_ruta_recurso
import sqlite3
import os
from dotenv import load_dotenv
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
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
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
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
            return True
        except sqlite3.Error as e:
            print(f"Error en base de datos: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def importar_empleados_desde_excel(ruta_archivo):
    """Función principal para importar empleados"""
    df = cargar_empleados_excel(ruta_archivo)
    if df is not None:
        return insertar_empleados(df)
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_empleados():
    """Obtiene lista de empleados desde la base de datos"""
    if not os.path.exists(DATABASE_URL):
        print(f"Base de datos no encontrada en: {DATABASE_URL}")
        return []
        
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute('SELECT Nombre FROM Empleados ORDER BY Nombre')
            return [row[0] for row in cursor.fetchall()]
        except sqlite3.Error as e:
            print(f"Error consultando empleados: {e}")
            return []
        finally:
            conn.close()
    return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_primeros_10_empleados():
    """Obtiene los primeros 10 empleados de la base de datos."""
    conn = connect_to_database()
    empleados = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Codigo, Nombre FROM Empleados ORDER BY Codigo DESC LIMIT 5") 
            empleados = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener empleados: {e}")
        finally:
            conn.close()
    return empleados
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def validar_formato_hora(hora_str):
    """Valida que el formato de hora sea HH:MM"""
    try:
        if not hora_str:
            return "0:00"
        if ":" not in hora_str:
            return False
        horas, minutos = map(int, hora_str.split(":"))
        if minutos >= 60:
            return False
        return f"{horas}:{minutos:02d}"
    except ValueError:
        return False

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def insertar_horas(fecha, codigo, nombre, horas_35, horas_100, destino):
    """Inserta registro en tabla Horas"""
    conn = connect_to_database()
    if conn:
        try:
            # Validar formato de horas
            h35 = validar_formato_hora(horas_35)
            h100 = validar_formato_hora(horas_100)
            if not h35 or not h100:
                return False

            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO Horas (Fecha, Codigo, Nombre, Horas_35, Horas_100, Destino_Comentario)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (fecha, codigo, nombre, h35, h100, destino))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al insertar horas: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_codigo_por_nombre(nombre):
    """Obtiene el código de un empleado por su nombre"""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT Codigo FROM Empleados WHERE Nombre = ?", (nombre,))
            resultado = cursor.fetchone()
            return resultado[0] if resultado else None
        except sqlite3.Error as e:
            print(f"Error al obtener código: {e}")
            return None
        finally:
            conn.close()
    return None
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_horas_por_fecha_tabla(fecha_inicio, fecha_fin):
    """Obtiene registros de horas entre dos fechas ordenados del más reciente al más antiguo."""
    conn = connect_to_database()
    registros = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Fecha, Codigo, Nombre, Horas_35, Horas_100, Destino_Comentario 
                FROM Horas 
                WHERE Fecha BETWEEN ? AND ? 
                ORDER BY Fecha DESC, Codigo ASC
                LIMIT 15
            """, (fecha_inicio, fecha_fin))
            registros = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener registros: {e}")
        finally:
            conn.close()
    return registros
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_horas_por_fecha_pdf(fecha_inicio, fecha_fin):
    """Obtiene registros de horas entre dos fechas ordenados del más reciente al más antiguo."""
    conn = connect_to_database()
    registros = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Fecha, Codigo, Nombre, Horas_35, Horas_100, Destino_Comentario 
                FROM Horas 
                WHERE Fecha BETWEEN ? AND ? 
                ORDER BY Fecha DESC, Codigo ASC
            """, (fecha_inicio, fecha_fin))
            registros = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener registros: {e}")
        finally:
            conn.close()
    return registros
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_ultimos_registros():
    """Obtiene los últimos 15 registros de horas"""
    conn = connect_to_database()
    registros = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT Fecha, Codigo, Nombre, Horas_35, Horas_100, Destino_Comentario 
                FROM Horas 
                ORDER BY Fecha DESC, Codigo ASC 
                LIMIT 15
            """)
            registros = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener registros: {e}")
        finally:
            conn.close()
    return registros
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def actualizar_registro(fecha_original, codigo, nueva_fecha, horas_35, horas_100, comentario, horas_35_original, horas_100_original):
    """Actualiza un registro específico de horas"""
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Horas 
                SET Fecha = ?, Horas_35 = ?, Horas_100 = ?, Destino_Comentario = ?
                WHERE Fecha = ? 
                AND Codigo = ? 
                AND Horas_35 = ?
                AND Horas_100 = ?
            """, (nueva_fecha, horas_35, horas_100, comentario, 
                  fecha_original, codigo, horas_35_original, horas_100_original))
            conn.commit()
            return True
        except sqlite3.Error as e:
            print(f"Error al actualizar registro: {e}")
            return False
        finally:
            conn.close()
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def validar_entrada_hora(hora_str):
    """Valida el formato y valor de la hora introducida"""
    if not hora_str:
        return True, ""
    
    if len(hora_str) < 4:
        return False, "Formato inválido. Use H:MM o HH:MM"
        
    if ":" not in hora_str:
        return False, "Formato inválido. Falta ':'"
        
    try:
        horas, minutos = map(int, hora_str.split(":"))
        if minutos >= 60:
            return False, "Los minutos no pueden ser mayores o iguales a 60"
        return True, ""
    except ValueError:
        return False, "Formato inválido"