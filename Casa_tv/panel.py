import flet as ft
from flet import ScrollMode, AppView




def main(page: ft.Page):
    page.title = "TV en casa"
    page.window.alignment = ft.alignment.center
    page.window.width = 600
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = False
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------



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