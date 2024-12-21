from turtle import bgcolor
import flet as ft
from flet import ScrollMode
import datetime
from consultas import get_empleados

#Funcion principal para iniciar la ventana con los controles
def main(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 700
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    
    # Cargar los empleados desde la base de datos
    empleados_data = get_empleados()  # Obtener la lista de empleados

    # Crear sugerencias para el AutoComplete
    suggestions = [
        ft.AutoCompleteSuggestion(key=emp, value=emp) for emp in empleados_data
    ]
    
    # Crear el AutoComplete
    auto_complete = ft.AutoComplete(
        suggestions=suggestions,
    )
    
    # Usar un Container para establecer un ancho específico
    auto_complete_container = ft.Container(
        content=auto_complete,
        width=200,  # Establecer el ancho deseado
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=10,
    )
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
    def Empleados(e):
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from empleados import Empleados
        Empleados(page)
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
                        ft.Text("Registro de horas"),
                        ft.Row([
                            ft.Text("Código:", width=100),
                            ft.TextField(width=200, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=3, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Nombre:", width=100),
                            auto_complete_container,
                        ]),
                        ft.Row([
                            ft.Text("Hora 35%:", width=100),
                            ft.TextField(width=200, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Hora 100%:", width=100),
                            ft.TextField(width=200, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Destino/Comentario:", width=100),
                            ft.TextField(width=200, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10),
                        ]),
                        ft.Row([
                        ft.ElevatedButton(text="Registrar", width=150),
                        ft.ElevatedButton(text="Reportes", width=150),
                        ]),
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
                        ft.Text("Cargar empleados"),
                        ft.Row([
                            ft.Text("Código:", width=100),
                            ft.TextField(width=200, max_length=3, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Nombre:", width=100),
                            auto_complete_container,
                        ]),
                        ft.Row([
                            ft.Text("Cargar:", width=100),
                            ft.ElevatedButton(text="...", icon=ft.Icons.UPLOAD, width=150, on_click=Empleados),
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)    
ft.app(main)