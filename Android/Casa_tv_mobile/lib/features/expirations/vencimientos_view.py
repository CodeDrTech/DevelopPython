import flet as ft
import os

from core.utils.date_utils import convertir_formato_fecha
from core.database.consultas import get_estado_pagos
from core.database.backup import DatabaseBackup

def create_vencimientos_view(page: ft.Page):    
    """Vista de vencimientos adaptada para móvil."""
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def handle_backup(e):
        backup_manager = DatabaseBackup()
        success, result = backup_manager.create_backup()
        
        if success:
            backup_path = result.split("guardado en ")[-1]
            full_path = os.path.join(backup_path, "database.db")
            
            # First show the dialog, then the message
            show_share_dialog(full_path)
            mostrar_mensaje("Backup creado exitosamente")
        else:
            mostrar_mensaje(f"Error: {result}")

    def show_share_dialog(backup_path: str):
        # Create a more prominent share button
        share_button = ft.ElevatedButton(
            "Compartir Backup",
            icon=ft.Icons.SHARE,
            on_click=lambda e: page.launch_url(f"file://{backup_path}")
        )
        
        dlg = ft.AlertDialog(
            modal=True,
            title=ft.Text("Backup Creado"),
            content=ft.Column(
                controls=[
                    ft.Text("El backup se ha guardado exitosamente."),
                    share_button
                ],
                spacing=10,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            actions=[
                ft.TextButton("Cerrar", on_click=lambda e: close_dialog(e, dlg))
            ],
        )
        
        def close_dialog(e, dlg):
            dlg.open = False
            page.update()
        
        page.dialog = dlg
        dlg.open = True
        page.update()
    
    def mostrar_mensaje(mensaje: str):
        snack = ft.SnackBar(content=ft.Text(mensaje), duration=3000)
        page.overlay.append(snack)
        snack.open = True
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Cargar datos de pagos
    pagos = get_estado_pagos()
    
    # Extraer nombres únicos para el dropdown
    nombres_clientes = ["Todos"]
    for p in pagos:
        if p[1] not in nombres_clientes:  # p[1] es el nombre del cliente
            nombres_clientes.append(p[1])
    
    # Crear contenedor para las tarjetas
    cards_container = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        spacing=10,
    )
    
    def actualizar_tarjetas(cliente_seleccionado="Todos"):
        # Limpiar tarjetas existentes
        cards_container.controls.clear()
        
        # Filtrar pagos por cliente seleccionado
        pagos_filtrados = pagos
        if cliente_seleccionado != "Todos":
            pagos_filtrados = [p for p in pagos if p[1] == cliente_seleccionado]
        
        # Crear tarjetas para cada pago
        for p in pagos_filtrados:
            card = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Text(p[1], size=16, weight="bold"),  # Nombre del servicio
                        ft.Text(f"Cliente: {p[1]}"),            # Nombre del cliente
                        ft.Text(f"Próximo pago: {convertir_formato_fecha(p[4])}"),       # Fecha próximo pago
                        ft.Text(f"Pago mensual: ${p[8]}"),     # Pago mensual
                        ft.Container(
                            padding=5,
                            border_radius=5,
                            bgcolor=ft.Colors.RED if p[7] == "En corte"
                                   else ft.Colors.ORANGE if p[7] == "Pendiente"
                                   else ft.Colors.BLUE if p[7] == "Cerca"
                                   else ft.Colors.GREEN,
                            content=ft.Text(p[7], color=ft.Colors.WHITE)  # Estado
                        )
                    ], spacing=5)
                )
            )
            cards_container.controls.append(card)
        
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Estados disponibles para filtrar
    estados = ["Todos", "En corte", "Pendiente", "Cerca", "Al día"]    
    
    # Dropdown para filtrar por cliente
    search_box = ft.TextField(
        label="Buscar cliente",
        hint_text="Escribe para filtrar",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: filter_clients(e.control.value),
        expand=True
    )
    
    estado_dropdown = ft.Dropdown(
        label="Estado",
        width=120,
        options=[ft.dropdown.Option(estado) for estado in estados],
        value="Todos",
        on_change=lambda e: apply_filters(search_box.value, e.control.value)
    )
    
    def apply_filters(search_text, estado_seleccionado="Todos"):
        # Limpiar tarjetas existentes
        cards_container.controls.clear()
        
        # Aplicar filtros
        filtered_pagos = pagos
        
        # Filtrar por texto de búsqueda
        if search_text:
            search_text = search_text.lower()
            filtered_pagos = [p for p in filtered_pagos if search_text in p[1].lower()]
        
        # Filtrar por estado
        if estado_seleccionado != "Todos":
            filtered_pagos = [p for p in filtered_pagos if p[7] == estado_seleccionado]
        
        # Crear tarjetas para cada pago que coincida
        for p in filtered_pagos:
            card = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Text(p[1], size=16, weight="bold"),  # Nombre del servicio
                        ft.Text(f"Cliente: {p[1]}"),            # Nombre del cliente
                        ft.Text(f"Próximo pago: {convertir_formato_fecha(p[4])}"),       # Fecha próximo pago
                        ft.Text(f"Pago mensual: ${p[8]}"),     # Pago mensual
                        ft.Container(
                            padding=5,
                            border_radius=5,
                            bgcolor=ft.Colors.RED if p[7] == "En corte"
                                   else ft.Colors.ORANGE if p[7] == "Pendiente"
                                   else ft.Colors.BLUE if p[7] == "Cerca"
                                   else ft.Colors.GREEN,
                            content=ft.Text(p[7], color=ft.Colors.WHITE)  # Estado
                        )
                    ], spacing=5)
                )
            )
            cards_container.controls.append(card)
        
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def filter_clients(search_text):
        if not search_text:
            actualizar_tarjetas("Todos")
            return
            
        search_text = search_text.lower()
        # Buscar coincidencias parciales en los nombres de clientes
        matching_clients = [p for p in pagos if search_text in p[1].lower()]
        
        # Limpiar tarjetas existentes
        cards_container.controls.clear()
        
        # Crear tarjetas para cada pago que coincida
        for p in matching_clients:
            card = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Text(p[10], size=16, weight="bold"),  # Nombre del servicio
                        ft.Text(f"Cliente: {p[1]}"),            # Nombre del cliente
                        ft.Text(f"Próximo pago: {convertir_formato_fecha(p[4])}"),       # Fecha próximo pago
                        ft.Text(f"Cuota mensual: ${p[8]}"),     # Pago mensual
                        ft.Container(
                            padding=5,
                            border_radius=5,
                            bgcolor=ft.Colors.RED if p[7] == "En corte"
                                   else ft.Colors.ORANGE if p[7] == "Pendiente"
                                   else ft.Colors.BLUE if p[7] == "Cerca"
                                   else ft.Colors.GREEN,
                            content=ft.Text(p[7], color=ft.Colors.WHITE)  # Estado
                        )
                    ], spacing=5)
                )
            )
            cards_container.controls.append(card)
        
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    content = ft.Column(
        scroll=ft.ScrollMode.AUTO,
        height=page.window.height - 180,
        spacing=10
    )
    
    content.controls.append(
        ft.Row([
            ft.Text("Vencimientos", size=20, weight="bold"),
            ft.Row([
                ft.IconButton(
                    icon=ft.Icons.BACKUP,
                    tooltip="Crear Backup",
                    on_click=handle_backup
                ),
                ft.IconButton(
                    icon=ft.Icons.REFRESH,
                    on_click=lambda _: mostrar_mensaje("Actualizando vencimientos...")
                )
            ])
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
    )
    
    content.controls.append(
        ft.Row([
            search_box,
            estado_dropdown
        ], spacing=10)
    )
    content.controls.append(ft.Divider())
    content.controls.append(cards_container)
    
    # Cargar tarjetas iniciales
    apply_filters("", "Todos")

    return ft.Container(
        content=content,
        padding=10,
        expand=False
    )