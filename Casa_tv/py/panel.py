import flet as ft
from flet import ScrollMode, AppView
from consultas import get_clientes




def main(page: ft.Page):
    page.title = "TV en casa"
    page.window.alignment = ft.alignment.center
    page.window.width = 900
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = False # type: ignore
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_tabla_clientes():
        """
        Crea y retorna una tabla DataTable con los clientes.
        
        Returns:
            ft.DataTable: Tabla con columnas y filas de datos de clientes.
        """
        clientes = get_clientes()
        
        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Inicio")),
            ft.DataColumn(ft.Text("WhatsApp")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Último Pago")),
            ft.DataColumn(ft.Text("Frecuencia"))
        ]
        
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(cliente[0]))),
                    ft.DataCell(ft.Text(cliente[1])),
                    ft.DataCell(ft.Text(cliente[2])),
                    ft.DataCell(ft.Text(cliente[3])),
                    ft.DataCell(ft.Text(cliente[4])),
                    ft.DataCell(ft.Text(cliente[5])),
                    ft.DataCell(ft.Text(f"{cliente[6]} días")),
                ],
            ) for cliente in clientes
        ]
        
        return ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
        )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,        
        # Contenedor de tabs
        tabs=[
            ft.Tab(
                icon=ft.Icons.LIST,
                text="Listado",
                content=ft.Column([
                    ft.Text("Listado de clientes", size=20),
                    crear_tabla_clientes(),
                ])
            ),
            ft.Tab(
                icon=ft.Icons.SUPERVISED_USER_CIRCLE_SHARP,
                text="Clientes",
                content=ft.Column(
                    [
                        ft.Text("Registrar clientes", size=20),
                        ft.Row([
                            ft.Text("No.:", width=100),
                            ft.TextField(width=320, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, read_only=True),
                        ]),
                        ft.Row([
                            ft.Text("Nombre:", width=100),
                            ft.TextField(width=320, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, capitalization=ft.TextCapitalization.WORDS),
                        ]),
                        ft.Row([
                            ft.Text("Fecha de inicio:", width=100),
                            ft.TextField(width=320, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, read_only=True, icon=ft.Icons.CALENDAR_MONTH),
                            
                        ]),
                        ft.Row([
                            ft.Text("Whatsapp:", width=100),
                            ft.TextField(width=320, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=12, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Estado:", width=100),
                            ft.Dropdown(
                            width=320,
                            value="Activo",
                            options=[
                                ft.dropdown.Option("Activo"),
                                ft.dropdown.Option("Inactivo"),
                            ],
                            border=ft.border.all(2, ft.Colors.BLACK),
                            border_radius=10,
                        ),
                        ]),
                        ft.Row([
                            ft.Text("Ultimo pago:", width=100),
                            ft.TextField(width=320, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, read_only=True, icon=ft.Icons.CALENDAR_MONTH),
                        ]),
                        ft.Row([
                        ft.Text("Frecuencia de pago:", width=100),
                        ft.Dropdown(
                            width=320,
                            value="30",
                            options=[
                                ft.dropdown.Option("1"),
                                ft.dropdown.Option("15"),
                                ft.dropdown.Option("30"),
                            ],
                            border=ft.border.all(2, ft.Colors.BLACK),
                            border_radius=10,
                        ),
                        ]),
                        ft.Row([
                        ft.Text(" ", width=100),
                        ft.ElevatedButton(text="Registrar", width=100),
                        ft.ElevatedButton(text="Empleados", width=100),
                        ft.ElevatedButton(text="Reportes", width=100),
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