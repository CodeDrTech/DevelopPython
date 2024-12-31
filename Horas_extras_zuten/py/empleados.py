import flet as ft
from flet import ScrollMode
from consultas import get_empleados, importar_empleados_desde_excel, get_primeros_10_empleados
from database import connect_to_database, DATABASE_URL, get_base_dir
import os, sys
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def crear_tabla_empleados():
    """
    Crea y retorna un DataTable con los primeros 10 empleados.
    La tabla contiene las siguientes columnas:
    - Código: El código del empleado.
    - Nombre: El nombre del empleado.
    Las filas de la tabla se generan a partir de los datos de los primeros 10 empleados obtenidos 
    mediante la función `get_primeros_10_empleados`.
    Returns:
        ft.DataTable: Un objeto DataTable con las columnas y filas definidas, y con estilos de borde 
        y líneas verticales y horizontales.
    """
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
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

def actualizar_tabla(tabla_empleados):
    """
    Actualiza los datos de la tabla de empleados.
    Args:
        tabla_empleados (ft.DataTable): La tabla de empleados que se actualizará.
    Returns:
        None
    """
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
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    
    # Crear tabla inicialmente
    tabla_empleados = crear_tabla_empleados()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def on_cancel(e):
        """
        Función para ejecutar si se cancela la importación de empleados.
        
        Cierra el diálogo de carga y muestra un SnackBar con un mensaje 
        indicando que no se importaron empleados.
        """
        carga_modal.open = False  # Cierra el diálogo
        # Mostrar SnackBar
        snackbar = ft.SnackBar(
            content=ft.Text("No se importaron empleados"),
            duration=3000,
        )
        page.snack_bar = snackbar
        snackbar.open = True
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def importar_excel(e):
        """
        Importar empleados desde un archivo Excel ubicado en una ruta fija y mostrar mensajes de SnackBar durante el proceso.
        Args:
            e: Evento que dispara la función (no utilizado en el cuerpo de la función).
        Funcionalidad:
            - Cierra el diálogo modal de carga.
            - Muestra un mensaje inicial indicando el inicio de la importación.
            - Verifica la existencia del archivo Excel en la ruta especificada.
            - Si el archivo existe:
                - Muestra un mensaje indicando que el archivo fue encontrado.
                - Intenta importar los empleados desde el archivo Excel.
                - Si la importación es exitosa:
                    - Actualiza la lista de empleados y las sugerencias de autocompletado.
                    - Muestra un mensaje de éxito.
                - Si la importación falla:
                    - Muestra un mensaje de error.
            - Si el archivo no existe:
                - Muestra un mensaje indicando que el archivo no fue encontrado.
            - Captura y muestra cualquier excepción que ocurra durante el proceso.
        """
        """Importar empleados desde una ruta fija con mensajes de SnackBar."""
        carga_modal.open = False  # Cierra el diálogo
        page.update()  # Actualiza la UI para cerrar el diálogo

        try:
            # Mostrar mensaje inicial
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text("Iniciando la importación desde Excel..."),
                    duration=300
                )
            )

            # Obtener la ruta al archivo Excel en la carpeta 'data'
            archivo = os.path.join(get_base_dir(), "data", "Empleados_zuten.xlsm")

            if os.path.exists(archivo):
                # Mensaje de archivo encontrado
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Archivo Excel encontrado. Cargando datos..."),
                        duration=3000
                    )
                )
                page.update()

                # Importar empleados desde Excel
                if importar_empleados_desde_excel(archivo):
                    # Actualizar la lista de empleados
                    empleados_data = get_empleados()
                    suggestions = [
                        ft.AutoCompleteSuggestion(key=emp, value=emp)
                        for emp in empleados_data
                    ]
                    auto_complete.suggestions = suggestions
                    page.update()

                    # Mensaje de éxito
                    page.show_snack_bar(
                        ft.SnackBar(
                            content=ft.Text("Empleados importados correctamente."),
                            duration=3000
                        )
                    )
                else:
                    # Mensaje de error en la importación
                    page.show_snack_bar(
                        ft.SnackBar(
                            content=ft.Text("Error al importar empleados."),
                            duration=3000
                        )
                    )
            else:
                # Mensaje de archivo no encontrado
                page.show_snack_bar(
                    ft.SnackBar(
                        content=ft.Text("Archivo Excel no encontrado."),
                        duration=3000
                    )
                )
        except Exception as e:
            # Mensaje de error general
            page.show_snack_bar(
                ft.SnackBar(
                    content=ft.Text(f"Error: {str(e)}"),
                    duration=3000
                )
            )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Crear el diálogo de confirmación
    carga_modal = ft.AlertDialog(
        title=ft.Text("¿Estás seguro?"),
        content=ft.Text("Esta acción no se puede deshacer."),
        actions=[
            ft.TextButton("Sí", on_click=importar_excel),
            ft.TextButton("No", on_click=on_cancel),
        ],
        modal=True,
    )

    # Botón para mostrar el diálogo
    def show_carga_modal(e):
        """
        Muestra el diálogo de confirmación para importar empleados desde Excel.
        
        Args:
            e: Evento que dispara la función (no utilizado en el cuerpo de la función).
        """
        page.dialog = carga_modal
        carga_modal.open = True
        page.update()
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
    
    def tab_registro(e):
            """
            Maneja el evento de cambio de tab a "Registro".

            Limpia la página actual y llama a la función registro desde el módulo registro.py, la
            cual imprime los controles y la tabla de registro en la página actual.
            """
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
                            ft.ElevatedButton(text="Cargar", icon=ft.Icons.UPLOAD, width=150, on_click=show_carga_modal),
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