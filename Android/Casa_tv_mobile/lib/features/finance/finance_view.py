import flet as ft
from core.database.consultas import get_estado_pagos, get_total_pagos_mes_actual
from shared.widgets.finance_cards import create_summary_card

def create_finance_view(page: ft.Page):
    """Vista de finanzas adaptada para móvil."""
    
    def mostrar_mensaje(mensaje: str):
        snack = ft.SnackBar(content=ft.Text(mensaje), duration=3000)
        page.overlay.append(snack)
        snack.open = True
        page.update()
    
    def load_financial_data():
        registros = get_estado_pagos()
        deuda_total = sum(reg[8] for reg in registros)
        pagos_mes = get_total_pagos_mes_actual()
        ganancia = pagos_mes - deuda_total
        return int(deuda_total), pagos_mes, ganancia

    # Contenedor principal con scroll
    main_container = ft.Container(
        content=ft.Column([], scroll=ft.ScrollMode.AUTO),
        padding=10
    )

    # Indicador de carga
    progress_ring = ft.ProgressRing()
    main_container.content.controls.append(progress_ring)
    
    # Cargar datos
    deuda_total, pagos_mes, ganancia = load_financial_data()
    
    # Crear tarjetas de resumen
    summary_cards = ft.GridView(
        expand=1,
        runs_count=2,
        max_extent=200,
        child_aspect_ratio=1.0,
        spacing=20,
        run_spacing=20,
        controls=[
            create_summary_card("Deuda Total", deuda_total, ft.Colors.RED_400),
            create_summary_card("Pagado este Mes", pagos_mes, ft.Colors.BLUE_400),
            create_summary_card("Ganancia", ganancia, ft.Colors.GREEN_400)
        ]
    )

    # Botón de actualizar con gesto pull-to-refresh
    refresh_button = ft.IconButton(
        icon=ft.Icons.REFRESH,
        icon_size=30,
        on_click=lambda _: mostrar_mensaje("Actualizando datos...")
    )

    # Eliminar indicador de carga y mostrar contenido
    main_container.content.controls = [
        ft.Container(
            content=ft.Row([
                ft.Text("Resumen Financiero", size=24, weight="bold"),
                refresh_button
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            padding=ft.padding.only(top=25, bottom=5)  # Add padding top and bottom
        ),
        summary_cards
    ]

    return main_container