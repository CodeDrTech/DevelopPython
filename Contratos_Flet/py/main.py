import flet as ft

def main(page: ft.Page):
    page.title = "Contratos"
    page.window.width = 800
    page.window.height = 600



    mainTab = ft.Tabs(
        selected_index=1,  # Pestaña seleccionada por defecto
        animation_duration=300,
        expand=True,
        
        # Contenedor de pestañas
        tabs=[
            ft.Tab(
                icon=ft.icons.FORMAT_LIST_NUMBERED,
                text="Listado",
                content=ft.Column(
                    [
                        ft.Text("Listado de Contratos", size=20),
                    ]
                    
                ),
            ),
            ft.Tab(
                icon=ft.icons.VERIFIED_USER_OUTLINED,
                text="Datos de Usuario",
                content=ft.Column(
                    [
                        
                        ft.Text("Registrar Usuario"),
                        ft.TextField(label="Nombre", width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Apellido", width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Cedula", width=200, max_length=11, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.TextField(label="Codigo", width=200, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.ElevatedButton(text="Guardar", on_click=lambda _: print("Buscar")),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
            ),
            ft.Tab(
                icon=ft.icons.DEVICES,
                text="Datos del Equipo",
                content=ft.Container(
                    content=ft.Text("Datos del Equipo", size=20),
                    padding=20,
                ),
            ),
            ft.Tab(
                icon=ft.icons.IMAGE,
                text="Imágenes",
                content=ft.Container(
                    content=ft.Text("Imágenes", size=20),
                    padding=20,
                ),
            ),
            ft.Tab(
                icon=ft.icons.LIST,
                text="Contrato",
                content=ft.Container(
                    content=ft.Text("Contrato", size=20),
                    padding=20,
                ),
            ),
        ],
    )

    page.add(mainTab)
    page.update()

ft.app(main)