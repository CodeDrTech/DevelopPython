import flet as ft
from flet import ScrollMode
from consultas import get_empleados



#Funcion principal para iniciar la ventana con los controles.
def Empleados(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 700
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def regresar_a_main(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        #from main import main
        #main(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
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
    #Funcion para manejar diferentes eventos al seleccionar algunos de los tab
    def cambio_tab(e):
        # El índice del tab seleccionado está en e.control.selected_index
        indice_seleccionado = e.control.selected_index
        
        if indice_seleccionado == 0:
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from panel import main
            main(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    mainTab = ft.Tabs(
        selected_index=1,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,
        #on_change=cambio_tab,
        
        
        # Contenedor de tabs
        tabs=[
            ft.Tab(
                icon=ft.Icons.LOCK_CLOCK,
                text="Horas",
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
                )
            ),
        ],
    )
    page.add(mainTab)
    page.update()