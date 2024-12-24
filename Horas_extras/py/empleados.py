import flet as ft
from flet import ScrollMode
from consultas import get_empleados, importar_empleados_desde_excel, get_primeros_10_empleados
from tkinter import filedialog
import tkinter as tk
import os
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def crear_tabla_empleados():
    """Crea y retorna un DataTable con los primeros 10 empleados"""
    empleados = get_primeros_10_empleados()
    
    # Define las columnas
    columns = [
        ft.DataColumn(ft.Text("Código")),
        ft.DataColumn(ft.Text("Nombre")),
    ]
    
    # Crea las filas con los datos
    rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(emp[0]))),  # Codigo
                ft.DataCell(ft.Text(emp[1])),       # cnombre
            ],
        ) for emp in empleados
    ]
    
    return ft.DataTable(
        columns=columns,
        rows=rows,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
        horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
        show_checkbox_column=True,
    )

def actualizar_tabla(tabla_empleados):
    """Actualiza los datos de la tabla de empleados"""
    empleados = get_primeros_10_empleados()
    
    tabla_empleados.rows = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(emp[0]))),
                ft.DataCell(ft.Text(emp[1])),
            ],
        ) for emp in empleados
    ]
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#Funcion principal para iniciar la ventana con los controles.
def Empleados(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 700
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE
    page.bgcolor = "#00033d"
    #page.theme_mode = ft.ThemeMode.LIGHT
    
    
    # Crear tabla inicialmente
    tabla_empleados = crear_tabla_empleados()
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
    def tab_registro(e):
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from registro import registro
            registro(page)
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
                        ft.Row([
                            tabla_empleados,
                        ]),
                        ft.Row([
                            ft.ElevatedButton(text="Atras", icon=ft.Icons.ARROW_BACK, width=150, on_click=tab_registro),
                            ft.ElevatedButton(text="Cargar", icon=ft.Icons.UPLOAD, width=150, on_click=importar_excel),
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