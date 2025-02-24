import flet as ft
import datetime
from utils import mostrar_mensaje, convertir_formato_fecha, get_estado_color_suplidores
from consultas import (
    get_pagos_suplidores, get_cuentas, insertar_pago_suplidor,
    actualizar_pago_suplidor, eliminar_pago_suplidor, get_estado_pagos_suplidores, get_correos_unicos
)
from tabs.vencimientos_tab import crear_tabla_vencimientos

def crear_tab_pagos_suplidores(page: ft.Page, mainTab: ft.Tabs):
    """Crea el tab para gestionar pagos a suplidores."""
    
    # Estados de pago disponibles
    ESTADOS_PAGO = ["Pendiente", "Pagado", "Cancelado"]
    
    def actualizar_vencimientos():
            """Updates the vencimientos tab content"""
            mainTab.tabs[0].content = crear_tabla_vencimientos(page)
            page.update()
            
    # Dropdown para filtrar por correo
    dropdown_correos = ft.Dropdown(
        label="Filtrar por correo",
        width=300,
        editable=True,
        enable_filter=True,
        enable_search=True,
        max_menu_height=200,
        options=[ft.dropdown.Option("Todos los correos")] + [
            ft.dropdown.Option(correo) for correo in get_correos_unicos()
        ],
        on_change=lambda e: filtrar_tabla(e.control.value)
    )
    
    # Contenedor para la tabla
    tabla_container = ft.Container(
        content=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Servicio")),
                ft.DataColumn(ft.Text("Correo")),
                ft.DataColumn(ft.Text("Fecha Inicial")),
                ft.DataColumn(ft.Text("Último Pago")),
                ft.DataColumn(ft.Text("Próximo Pago")),
                ft.DataColumn(ft.Text("Cuota")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Tarjeta")),
                ft.DataColumn(ft.Text("Comentarios")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[],
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
            #horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400)
        ),
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10
    )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def filtrar_tabla(correo_seleccionado=None):
        """Actualiza la tabla con los pagos actuales."""
        pagos = get_estado_pagos_suplidores()
        rows = []
        
        for pago in pagos:
            # Filter by selected email
            if correo_seleccionado and correo_seleccionado != "Todos los correos" and pago[2] != correo_seleccionado:
                continue
            # Create buttons with proper event handling
            edit_button = ft.IconButton(
                icon=ft.icons.EDIT,
                tooltip="Editar",
                
            )
            
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Eliminar",
                
            )
            
            pay_button = ft.IconButton(
                icon=ft.icons.PAYMENT,
                tooltip="Registrar Pago",
                
            )
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(pago[1])),  # servicio
                        ft.DataCell(ft.Text(pago[2])),  # correo
                        ft.DataCell(ft.Text(convertir_formato_fecha(pago[3]))),  # fecha inicial
                        ft.DataCell(ft.Text(convertir_formato_fecha(pago[4]))),  # último pago
                        ft.DataCell(ft.Text(convertir_formato_fecha(pago[5]))),  # próximo pago
                        ft.DataCell(ft.Text(f"${pago[8]}")),  # cuota
                        ft.DataCell(ft.Text(pago[7], color=get_estado_color_suplidores(pago[7]))),  # estado
                        ft.DataCell(ft.Text(f"*{pago[9]}" if pago[9] else "-")),  # tarjeta
                        ft.DataCell(ft.Text(pago[10] or "")),  # comentarios
                        ft.DataCell(
                            ft.Row(
                                controls=[edit_button, delete_button, pay_button],
                                spacing=0
                            )
                        )
                    ]
                )
            )
        
        if tabla_container.content:
            tabla_container.content.rows = rows # type: ignore
            page.update()

    # Create main content
    contenido = ft.Column([
        ft.Text("Pagos a Suplidores", size=20, weight="bold"), # type: ignore
        dropdown_correos,
        tabla_container
    ])

    # Initial table load
    filtrar_tabla()

    return contenido
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

