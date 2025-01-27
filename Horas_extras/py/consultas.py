import pandas as pd
from database import connect_to_database, DATABASE_URL
import sqlite3
import os
from dotenv import load_dotenv
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def cargar_empleados_excel(ruta_excel):
    """
    Lee empleados desde un archivo Excel con rangos específicos C4:C* y H4:H*.
    Args:
        ruta_excel (str): La ruta del archivo Excel desde el cual se leerán los datos.
    Returns:
        pandas.DataFrame: Un DataFrame que contiene los datos de los empleados con las columnas 'Codigo' y 'Nombre'.
        None: Si ocurre un error al leer el archivo Excel.
    Raises:
        Exception: Si ocurre un error al leer el archivo Excel, se captura y se imprime el mensaje de error.
    """
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
    """
    Inserta o actualiza múltiples empleados en la base de datos.
    Parámetros:
        empleados_df (pandas.DataFrame): DataFrame que contiene los datos de los empleados a insertar o actualizar. 
                                         Debe tener las columnas 'Codigo' y 'Nombre'.
    Retorna:
        bool: True si la operación fue exitosa, False en caso contrario.
    Errores:
        sqlite3.Error: Si ocurre un error durante la operación en la base de datos, se captura y se imprime el mensaje de error.
    """
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
    """
    Importa empleados desde un archivo de Excel y los inserta en la base de datos.

    Args:
        ruta_archivo (str): La ruta del archivo de Excel desde el cual se importarán los empleados.

    Returns:
        bool: True si los empleados se insertaron correctamente, False en caso contrario.
    """
    """Función principal para importar empleados"""
    df = cargar_empleados_excel(ruta_archivo)
    if df is not None:
        return insertar_empleados(df)
    return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def get_empleados():
    """
    Obtiene una lista de nombres de empleados desde la base de datos.
    La función verifica si la base de datos existe en la ruta especificada por `DATABASE_URL`.
    Si la base de datos no se encuentra, imprime un mensaje de error y retorna una lista vacía.
    Si la base de datos existe, se conecta a ella y ejecuta una consulta SQL para obtener
    los nombres de los empleados ordenados alfabéticamente. En caso de error durante la consulta,
    imprime un mensaje de error y retorna una lista vacía. Finalmente, cierra la conexión a la base de datos.
    Returns:
        list: Una lista de nombres de empleados. Si ocurre un error o la base de datos no se encuentra,
              retorna una lista vacía.
    """
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
    """
    Obtiene los primeros 10 empleados de la base de datos.

    Conecta a la base de datos y ejecuta una consulta SQL para obtener los primeros 10 empleados
    ordenados por su código en orden descendente. Si ocurre un error durante la consulta, se imprime
    un mensaje de error. La conexión a la base de datos se cierra al finalizar la operación.

    Returns:
        list: Una lista de tuplas, donde cada tupla contiene el código y el nombre de un empleado.
    """
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
    """
    Valida que el formato de una cadena de hora sea HH:MM.

    Args:
        hora_str (str): Cadena que representa la hora en formato HH:MM.

    Returns:
        str: La hora en formato HH:MM si es válida, "0:00" si la cadena está vacía.
        bool: False si el formato es incorrecto o si los minutos son 60 o más.

    Raises:
        ValueError: Si la cadena no puede ser convertida a enteros.
    """
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
    """
    Inserta un registro en la tabla Horas.
    Args:
        fecha (str): La fecha del registro en formato 'YYYY-MM-DD'.
        codigo (str): El código del empleado.
        nombre (str): El nombre del empleado.
        horas_35 (str): Las horas trabajadas al 35% en formato 'HH:MM'.
        horas_100 (str): Las horas trabajadas al 100% en formato 'HH:MM'.
        destino (str): Comentario sobre el destino de las horas.
    Returns:
        bool: True si la inserción fue exitosa, False en caso contrario.
    """
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
    """
    Obtiene el código de un empleado por su nombre.

    Parámetros:
    nombre (str): El nombre del empleado.

    Retorna:
    int: El código del empleado si se encuentra, de lo contrario None.

    Excepciones:
    sqlite3.Error: Si ocurre un error al ejecutar la consulta SQL.
    """
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
    """
    Obtiene registros de horas entre dos fechas ordenados del más reciente al más antiguo.

    Args:
        fecha_inicio (str): La fecha de inicio en formato 'YYYY-MM-DD'.
        fecha_fin (str): La fecha de fin en formato 'YYYY-MM-DD'.

    Returns:
        list: Una lista de tuplas que contienen los registros de horas. Cada tupla tiene la forma 
              (Fecha, Codigo, Nombre, Horas_35, Horas_100, Destino_Comentario).
              Si ocurre un error, se devuelve una lista vacía.
    """
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
                LIMIT 100
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
    """
    Obtiene registros de horas entre dos fechas ordenados del más reciente al más antiguo.

    Args:
        fecha_inicio (str): La fecha de inicio en formato 'YYYY-MM-DD'.
        fecha_fin (str): La fecha de fin en formato 'YYYY-MM-DD'.

    Returns:
        list: Una lista de tuplas que contienen los registros de horas. Cada tupla tiene la forma 
        (Fecha, Codigo, Nombre, Horas_35, Horas_100, Destino_Comentario).
    """
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
    """
    Obtiene los últimos 15 registros de horas desde la base de datos.

    Conecta a la base de datos, ejecuta una consulta para obtener los últimos
    15 registros de la tabla 'Horas' ordenados por fecha en orden descendente
    y por código en orden ascendente. Los registros obtenidos incluyen la fecha,
    el código, el nombre, las horas al 35%, las horas al 100% y el comentario de destino.

    Returns:
        list: Una lista de tuplas que contienen los últimos 15 registros de horas.
              Cada tupla tiene la siguiente estructura:
              (Fecha, Codigo, Nombre, Horas_35, Horas_100, Destino_Comentario)
    """
    """Obtiene los últimos 15 registros de horas"""
    conn = connect_to_database()
    registros = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT ID, Fecha, Codigo, Nombre, Horas_35, Horas_100, Destino_Comentario 
                FROM Horas 
                ORDER BY Fecha DESC, Codigo ASC 
                LIMIT 100
            """)
            registros = cursor.fetchall()
        except sqlite3.Error as e:
            print(f"Error al obtener registros: {e}")
        finally:
            conn.close()
    return registros
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def actualizar_registro(registro_id, nueva_fecha, horas_35, horas_100, comentario):
    """
    Actualiza un registro específico en la tabla 'Horas' usando el id único del registro.

    Parameters
    ----------
    registro_id : int
        ID único del registro a actualizar.
    nueva_fecha : str
        Nueva fecha.
    horas_35 : float
        Nuevas horas al 35%.
    horas_100 : float
        Nuevas horas al 100%.
    nocturnas : float
        Nuevas horas nocturnas.

    Returns
    -------
    bool
        True si el registro se actualizó correctamente, False en caso contrario.

    Raises
    ------
    Exception
        Si ocurre un error durante la actualización.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                UPDATE Horas
                SET Fecha = ?, Horas_35 = ?, Horas_100 = ?, Destino_Comentario = ?
                WHERE id = ?
            """, (nueva_fecha, horas_35, horas_100, comentario, registro_id))
            conn.commit()
            if cursor.rowcount == 0:
                raise Exception("No se encontró un registro con el ID proporcionado.")
            return True
        except sqlite3.Error as e:
            raise Exception(f"Error al actualizar registro: {e}")
        finally:
            conn.close()
    else:
        raise Exception("No se pudo establecer conexión con la base de datos.")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def delete_record(registro_id):
    """
    Elimina un registro específico de la tabla 'Horas' usando el id único del registro.

    Parameters
    ----------
    registro_id : int
        ID único del registro a eliminar.

    Returns
    -------
    bool
        True si el registro se eliminó correctamente, False en caso contrario.

    Raises
    ------
    Exception
        Si ocurre un error durante la eliminación.
    """
    conn = connect_to_database()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                DELETE FROM Horas
                WHERE id = ?
            """, (registro_id,))
            conn.commit()
            if cursor.rowcount == 0:
                raise Exception("No se encontró un registro con el ID proporcionado.")
            return True
        except sqlite3.Error as e:
            raise Exception(f"Error al eliminar registro: {e}")
        finally:
            conn.close()
    else:
        raise Exception("No se pudo establecer conexión con la base de datos.")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def validar_entrada_hora(hora_str):
    """
    Valida el formato y valor de la hora introducida.
    Args:
        hora_str (str): Cadena de texto que representa la hora en formato H:MM o HH:MM.
    Returns:
        tuple: Una tupla que contiene un booleano y un mensaje de error. 
               El booleano es True si la hora es válida, False en caso contrario.
               El mensaje de error proporciona detalles sobre el motivo de la invalidez.
    """
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