import flet as ft

def main(page: ft.Page):
    page.title = "Contratos"
    page.window_width = 800
    page.window.height = 600
    page.scroll = "auto"

    mainTab = ft.Tabs(
        selected_index=1,  # Pestaña seleccionada por defecto
        animation_duration=300,
        expand=True,
        
        # contenedor de pestañas
        tabs=[
            ft.Tab(
                icon=ft.icons.FORMAT_LIST_NUMBERED,
                text="Listado",
                content=ft.Column(
                    [
                        ft.Text("Listado de Contratos", size=20),  # Label
                    ]
                    
                ),
            ),
            ft.Tab(
                icon=ft.icons.VERIFIED_USER_OUTLINED,
                text="Datos de Usuario",
                content=ft.Column(
                    [
                        ft.Text("Listado de Contratos"),
                        ft.TextField(label="Buscar contrato", width=150),  # Ajusta el ancho según sea necesario
                        ft.ElevatedButton(text="Buscar", on_click=lambda _: print("Buscar")),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=100,
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