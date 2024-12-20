from turtle import bgcolor
import flet as ft
from flet import ScrollMode
import datetime
from consultas import get_empleados

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
    #Funcion para manejar diferentes eventos al seleccionar algunos de los tab
    def cambio_tab(e):
        # El índice del tab seleccionado está en e.control.selected_index
        indice_seleccionado = e.control.selected_index
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
                        auto_complete_container,
                        ft.TextField(label="Hora 35%", width=200, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ft.TextField(label="Hora 100%", width=200, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ft.TextField(label="Destino/Comentario", width=200, border_radius=5),
                        ft.ElevatedButton(text="Registrar", width=200, color=ft.Colors.BLUE_600),
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
                        auto_complete_container,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)    
ft.app(main)