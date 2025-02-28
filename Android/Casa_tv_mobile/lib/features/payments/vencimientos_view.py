import flet as ft
from core.database.consultas import get_vencimientos

def create_vencimientos_view(page: ft.Page):
    
    """Vista de vencimientos adaptada para móvil."""
    
    content = ft.Column([
        ft.Text("Vencimientos", size=24, weight="bold"),
        ft.Divider(),
    ])  
    
    def mostrar_mensaje(mensaje: str):
        snack = ft.SnackBar(content=ft.Text(mensaje), duration=3000)
        page.overlay.append(snack)
        snack.open = True
        page.update()
        
    content = ft.Column(
        scroll=ft.ScrollMode.AUTO,  # Make it scrollable
        height=page.window.height - 180,  # Fixed height with room for navigation
        spacing=10
    )
    
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
    
    content.controls.append(
        ft.Row([
            ft.Text("Vencimientos", size=20, weight="bold"),
            ft.IconButton(
                icon=ft.Icons.REFRESH,
                on_click=lambda _: mostrar_mensaje("Actualizando vencimientos...")
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )
    
    content.controls.append(ft.Divider())
    
    # Cargar datos de vencimientos
    vencimientos = get_vencimientos()
    
    
    # Add cards to the list
    for v in vencimientos:
        card = ft.Card(
            content=ft.Container(
                padding=10,
                content=ft.Column([
                    ft.Text(v[0], size=16, weight="bold"),
                    ft.Text(f"Cliente: {v[1]}"),
                    ft.Text(f"Vence: {v[2]}"),
                    ft.Container(
                        padding=5,
                        border_radius=5,
                        bgcolor=ft.Colors.RED if v[3] == "En corte"
                               else ft.Colors.ORANGE if v[3] == "Pendiente"
                               else ft.Colors.BLUE if v[3] == "Cerca"
                               else ft.Colors.GREEN,
                        content=ft.Text(v[3], color=ft.Colors.WHITE)
                    )
                ], spacing=5)
            )
        )
        content.controls.append(card)    
    

    return ft.Container(
        content=content,
        padding=10,
        expand=False  # Important: don't expand to fill all space
    )