import flet as ft
import datetime
from utils import mostrar_mensaje, convertir_formato_fecha, get_estado_color_suplidores
from consultas import (
    get_pagos_suplidores, get_cuentas, insertar_pago_suplidor,
    actualizar_pago_suplidor, eliminar_pago_suplidor, get_estado_pagos_suplidores
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
    def cerrar_dialogo(dlg):
        """Cierra un diálogo modal."""
        dlg.open = False
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def mostrar_dialogo_editar(e, pago):
        txt_fecha = ft.TextField(
            label="Fecha de pago",
            value=convertir_formato_fecha(pago[3]),
            read_only=True
        )

        txt_comentarios = ft.TextField(
            label="Comentarios",
            value=pago[10] if pago[10] else "",
            multiline=True,
            min_lines=3,
            max_lines=3,
            width=400
        )

        def guardar(e):
            try:
                if actualizar_pago_suplidor(pago[0], txt_fecha.value, txt_comentarios.value):
                    mostrar_mensaje("Pago actualizado exitosamente", page)
                    dlg_modal.open = False
                    actualizar_tabla()
                else:
                    mostrar_mensaje("Error al actualizar el pago", page)
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}", page)
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar Pago - {pago[1]}"),
            content=ft.Column([
                txt_fecha,
                txt_comentarios
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dlg_modal)),
                ft.TextButton("Guardar", on_click=guardar)
            ]
        )

        page.dialog = dlg_modal # type: ignore
        dlg_modal.open = True
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def mostrar_dialogo_eliminar(e, pago):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(f"¿Eliminar el pago de {pago[1]}?"),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dlg_modal)),
                ft.TextButton("Eliminar", on_click=lambda e: eliminar_y_cerrar(dlg_modal, pago[0]))
            ]
        )
        page.dialog = dlg_modal # type: ignore
        dlg_modal.open = True
        page.update()

    def eliminar_y_cerrar(dlg, pago_id):
        if eliminar_pago_suplidor(pago_id):
            mostrar_mensaje("Pago eliminado exitosamente", page)
            dlg.open = False
            actualizar_tabla()
        else:
            mostrar_mensaje("Error al eliminar el pago", page)
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def mostrar_dialogo_pago(e, pago):
        txt_fecha = ft.TextField(
            label="Fecha de pago",
            value=datetime.datetime.now().strftime("%Y-%m-%d"),
            read_only=True
        )

        def mostrar_fecha(e):
            date_picker = ft.DatePicker(
                on_change=lambda e: cambiar_fecha(e, txt_fecha)
            )
            page.overlay.append(date_picker)
            date_picker.pick_date()
            page.update()

        def cambiar_fecha(e, txt_field):
            if e.control.value:
                fecha = e.control.value.date()
                txt_field.value = fecha.strftime("%Y-%m-%d")
                page.update()

        txt_fecha.on_click = mostrar_fecha

        txt_comentarios = ft.TextField(
            label="Comentarios",
            multiline=True,
            min_lines=3,
            max_lines=3,
            width=400
        )

        def guardar(e):
            try:
                if insertar_pago_suplidor(pago[0], txt_fecha.value, txt_comentarios.value):
                    mostrar_mensaje("Pago registrado exitosamente", page)
                    dlg_modal.open = False
                    actualizar_tabla()
                else:
                    mostrar_mensaje("Error al registrar el pago", page)
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}", page)
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Registrar Pago - {pago[1]}"),
            content=ft.Column([
                txt_fecha,
                txt_comentarios
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dlg_modal)),
                ft.TextButton("Guardar", on_click=guardar)
            ]
        )

        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def actualizar_tabla():
        """Actualiza la tabla con los pagos actuales."""
        pagos = get_estado_pagos_suplidores()
        rows = []
        
        for pago in pagos:
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
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, p=pago: mostrar_dialogo_editar(e, p)  # Changed to new function
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar",
                                    on_click=lambda e, p=pago: mostrar_dialogo_eliminar(e, p)  # Changed to new function
                                ),
                                ft.IconButton(
                                    icon=ft.icons.PAYMENT,
                                    tooltip="Registrar Pago",
                                    on_click=lambda e, p=pago: mostrar_dialogo_pago(e, p)  # Changed to new function
                                )
                            ])
                        )
                    ]
                )
            )
        
        tabla_container.content.rows = rows # type: ignore
        page.update()

    # Create main content
    contenido = ft.Column([
        ft.Text("Pagos a Suplidores", size=20, weight="bold"), # type: ignore
        tabla_container
    ])

    # Initial table load
    actualizar_tabla()

    return contenido
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

