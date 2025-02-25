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
    def registrar_pago_suplidor(e, pago):
        """Abre diálogo para registrar nuevo pago de suplidor"""
        
        txt_fecha = ft.TextField(
            label="Fecha de pago",
            value=datetime.datetime.now().strftime("%Y-%m-%d"),
            read_only=True,
            icon=ft.Icons.CALENDAR_MONTH
        )

        def mostrar_fecha(e):
            date_picker = ft.DatePicker(
                on_change=lambda e: cambiar_fecha(e, txt_fecha)
            )
            page.overlay.append(date_picker)
            date_picker.open = True
            page.update()

        def cambiar_fecha(e, txt_field):
            txt_field.value = e.control.value.date().strftime("%Y-%m-%d")
            page.update()

        txt_fecha.on_click = mostrar_fecha

        txt_comentarios = ft.TextField(
            label="Comentarios",
            multiline=True,
            min_lines=2,
            max_lines=3,
            width=400
        )

        def guardar_pago(e):
            try:
                if not txt_fecha.value:
                    raise ValueError("La fecha es obligatoria")
                
                if insertar_pago_suplidor(
                    cuenta_id=pago[0],  # ID de la cuenta
                    fecha_pago=txt_fecha.value,
                    comentarios=txt_comentarios.value
                ):
                    mostrar_mensaje("Pago registrado exitosamente", page)
                    dlg_modal.open = False
                    actualizar_vencimientos()
                    filtrar_tabla(dropdown_correos.value)  # Actualizar la tabla con el filtro actual
                else:
                    mostrar_mensaje("Error al registrar el pago", page)
            except ValueError as ex:
                mostrar_mensaje(str(ex), page)
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Registrar Pago - {pago[1]}"),  # Nombre del servicio
            content=ft.Column([
                ft.Text(f"Servicio: {pago[1]}"),
                ft.Text(f"Correo: {pago[2]}"),
                ft.Text(f"Monto a pagar: ${pago[8]}"),  # Muestra el monto pero no es editable
                txt_fecha,
                txt_comentarios
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", 
                            on_click=lambda e: setattr(dlg_modal, 'open', False) or page.update()),
                ft.TextButton("Guardar", on_click=guardar_pago)
            ]
        )

        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()
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
                icon_color="red",
                tooltip="Eliminar",
                
            )
            
            pay_button = ft.IconButton(
                icon=ft.icons.PAYMENT,
                icon_color="green",
                tooltip="Registrar Pago",
                on_click=lambda e, p=pago: registrar_pago_suplidor(e, p)
                
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

