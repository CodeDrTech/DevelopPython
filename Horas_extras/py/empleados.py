import flet as ft
from flet import ScrollMode
from consultas import get_empleados, importar_empleados_desde_excel
from tkinter import filedialog
import tkinter as tk
import os


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


    def importar_excel(e):
        """Importar empleados desde una ruta fija sin diálogo."""
        # Obtener la ruta del directorio raíz del proyecto
        ruta_proyecto = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        archivo = os.path.join(ruta_proyecto, "Empleados.xlsm")     # Ruta del archivo Excel

        if os.path.exists(archivo):  # Verificar que el archivo exista
            if importar_empleados_desde_excel(archivo):
                # Actualizar la lista de empleados
                empleados_data = get_empleados()
                suggestions = [
                    ft.AutoCompleteSuggestion(key=emp, value=emp) 
                    for emp in empleados_data
                ]
                auto_complete.suggestions = suggestions
                page.update()
                page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Empleados importados correctamente"), duration=3000)

                )
            else:
                page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Error al importar empleados"), duration=3000)
                )
        else:
            page.show_snack_bar(
                ft.SnackBar(content=ft.Text("Archivo Excel no encontrado en la ruta predeterminada"), duration=3000)
            )

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
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=10,
    )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Funcion para manejar diferentes eventos al seleccionar algunos de los tab
    def tab_panel(e):
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
        
        # Contenedor de tabs
        tabs=[
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
                            ft.Text("Cargar Empleados:", width=100),
                            ft.ElevatedButton(text="Cargar", icon=ft.Icons.UPLOAD, width=100, on_click=importar_excel),
                            ft.ElevatedButton(text="Atras", icon=ft.Icons.ARROW_BACK, width=100, on_click=tab_panel),
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)
    page.update()