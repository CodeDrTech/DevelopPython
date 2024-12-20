import flet as ft
from flet import ScrollMode
import datetime
from database import connect_to_database


def get_empleados():
    """Obtiene la lista de empleados de la base de datos."""
    conn = connect_to_database()
    empleados = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT codigo, nombre FROM Empleados")
            rows = cursor.fetchall()
            for row in rows:
                empleados.append({"codigo": row[0], "nombre": row[1]})
        except sqlite3.Error as e:
            print(f"Error al obtener empleados: {e}")
        finally:
            conn.close()
    return empleados

#Funcion principal para iniciar la ventana con los controles.
def main(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 800
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE
    
    
    # Cargar los empleados desde la base de datos
    empleados_data = get_empleados()  # Obtener la lista de empleados

    # Crear opciones para el dropdown
    dropdown_options = [ft.dropdown.Option(emp["nombre"]) for emp in empleados_data]
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def mostrar_datepicker(e):
        # Abre el diálogo del DatePicker para que el usuario seleccione una fecha.
        page.overlay.append(date_picker_dialog)
        date_picker_dialog.open = True
        page.update()

    def seleccionar_fecha(e):
        # Obtiene la fecha seleccionada del DatePicker.
        fecha_actual = date_picker_dialog.value
        if fecha_actual:
            # Convierte a formato solo de fecha sin la hora.
            fecha_solo = fecha_actual.date()
            # Actualiza el texto para mostrar la fecha seleccionada.
            fecha_texto.value = f"               {fecha_solo}"
            # Cierra el diálogo configurando `open = False`.
            date_picker_dialog.open = False
            # Finalmente, actualiza la página para reflejar los cambios.
            page.update()

    # Inicializa la fecha actual y crea un texto para mostrar la fecha seleccionada.
    fecha_actual = datetime.date.today()
    fecha_texto = ft.Text(f"               {fecha_actual}")

    # Crea el DatePicker y establece que `seleccionar_fecha` se ejecutará cuando cambie la fecha seleccionada.
    date_picker_dialog = ft.DatePicker(
        on_change=seleccionar_fecha)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,    
        
        # Contenedor de tabs
        tabs=[
            ft.Tab(
                icon=ft.Icons.LOCK_CLOCK,
                text="Horas",
                content=ft.Column(
                    [
                        ft.Text("      Registrar Horas", size=20),
                        fecha_texto,
                        ft.ElevatedButton(
                            text=           "Fecha",
                            icon=           ft.Icons.CALENDAR_TODAY,
                            on_click=       mostrar_datepicker,
                            width=          200
                        ),
                        ft.TextField(label="Codigo", width=200, max_length=3, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.Dropdown(label="Nombre", width=200, options=[ft.dropdown.Option("Juan")]),
                        ft.TextField(label="Hora 35%", width=200, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ft.TextField(label="Hora 100%", width=200, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ft.TextField(label="Destino/Comentario",width=200),
                        ft.ElevatedButton(text="Registrar", width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
            ft.Tab(
                icon=ft.Icons.PEOPLE,
                text="Empleados",
                content=ft.Column(
                    [
                        ft.TextField(label="Codigo", width=200, max_length=3, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.Dropdown(label="Nombre", width=200, options=dropdown_options),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                )
            ),
        ],
    )
    page.add(mainTab)    
ft.app(main)