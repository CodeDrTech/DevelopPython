import datetime

def convertir_formato_fecha(fecha_str):
    """
    Convierte una fecha en formato 'YYYY-MM-DD' a 'DD-MMM-YYYY' 
    donde MMM es la abreviatura del mes en español.
    
    Args:
        fecha_str (str): Fecha en formato 'YYYY-MM-DD'
        
    Returns:
        str: Fecha formateada como 'DD-MMM-YYYY' o la cadena original si no se puede convertir
    """
    try:
        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
        meses = {
            1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR',
            5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AGO',
            9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DIC'
        }
        return f"{fecha.day}-{meses[fecha.month]}-{fecha.year}"
    except ValueError:
        return fecha_str