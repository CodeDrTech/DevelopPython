import flet as ft
import datetime

def mostrar_mensaje(mensaje: str, page: ft.Page):
    snack = ft.SnackBar(content=ft.Text(mensaje), duration=5000)
    page.overlay.append(snack)
    snack.open = True
    page.update()

def convertir_formato_fecha(fecha_str):
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

def get_estado_color(estado: str) -> str:
    if estado == "En corte":
        return ft.Colors.RED
    elif estado == "Pago pendiente":
        return ft.Colors.ORANGE_700
    elif estado == "Cerca":
        return ft.Colors.BLUE_700
    return ft.Colors.GREEN