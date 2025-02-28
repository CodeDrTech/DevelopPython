import flet as ft
from core.database.consultas import get_vencimientos

def create_vencimientos_view(page: ft.Page):
    print("Creating vencimientos view...")
    """Vista de vencimientos adaptada para móvil."""
    
    
    container = ft.Container(
        padding=10,
        content=ft.Column([
            # Header with title and refresh button
            ft.Row([
                ft.Text("Vencimientos", size=20, weight="bold"),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    on_click=lambda _: print("Refresh clicked")
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            
            # Divider
            ft.Divider(),
            
            # Simple list of cards
            ft.ListView(
                height=400,  # Fixed height
                spacing=10,
                auto_scroll=True
            )
        ])
    )
    
    list_view = container.content.controls[2]
    
    def mostrar_mensaje(mensaje: str):
        snack = ft.SnackBar(content=ft.Text(mensaje), duration=3000)
        page.overlay.append(snack)
        snack.open = True
        page.update()
    
    # Contenedor principal con scroll
    main_container = ft.Container(
        content=ft.Column(
            controls=[],
            scroll=ft.ScrollMode.AUTO,
            expand=True,
            spacing=10
        ),
        padding=10
    )

    # Indicador de carga
    progress_ring = ft.ProgressRing()
    main_container.content.controls.append(progress_ring)
    
    vencimientos_list = ft.ListView(
        expand=1,
        spacing=10,
        padding=10,
        height=500
    )
    
    # Cargar datos de vencimientos
    vencimientos = get_vencimientos()
    print(f"Loaded {len(vencimientos)} vencimientos")
    
    
    # Crear tarjetas de vencimientos
    vencimientos_list = ft.ListView(
        spacing=10,
        padding=20,
        height=page.window.height - 180,  # Fixed height with room for navigation
        auto_scroll=True
    )
    
    # Add cards to the list
    for v in vencimientos:
        vencimientos_list.controls.append(
            ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Text(v[0], weight="bold"),
                        ft.Text(v[1]),
                        ft.Text(v[2]),
                        ft.Text(v[3], 
                            color=ft.colors.RED if v[3] == "En corte"
                            else ft.colors.ORANGE if v[3] == "Pendiente"
                            else ft.colors.BLUE if v[3] == "Cerca"
                            else ft.colors.GREEN
                        )
                    ])
                )
            )
        )
    
    return ft.Column([
        ft.Row([
            ft.Text("Vencimientos", size=20, weight="bold"),
            ft.IconButton(
                icon=ft.Icons.REFRESH,
                on_click=lambda _: print("Refresh clicked")
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        vencimientos_list
    ])

    # Botón de actualizar
    refresh_button = ft.IconButton(
        icon=ft.Icons.REFRESH,
        icon_size=30,
        on_click=lambda _: mostrar_mensaje("Actualizando vencimientos...")
    )

    # Mostrar contenido
    main_container.content.controls = [
        ft.Container(
            content=ft.Row([
                ft.Text("Vencimientos", size=20, weight="bold"),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    on_click=lambda _: print("Refresh clicked")
                )
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.only(bottom=10)
        ),
        vencimientos_list,
    ]

    return main_container