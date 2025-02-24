import flet as ft
import datetime
from utils import mostrar_mensaje, convertir_formato_fecha
from consultas import (
    get_pagos_suplidores, get_cuentas, insertar_pago_suplidor,
    actualizar_pago_suplidor, eliminar_pago_suplidor
)

def crear_tab_pagos_suplidores(page: ft.Page):
    """Crea el tab para gestionar pagos a suplidores."""
    
    # Estados de pago disponibles
    ESTADOS_PAGO = ["Pendiente", "Pagado", "Cancelado"]
    
    # Contenedor para la tabla
    tabla_container = ft.Container(
        content=ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Servicio")),
                ft.DataColumn(ft.Text("Correo")),
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Estado")),
                ft.DataColumn(ft.Text("Comentarios")),
                ft.DataColumn(ft.Text("Acciones"))
            ],
            rows=[]
        ),
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10
    )

    def actualizar_tabla():
        """Actualiza la tabla con los pagos actuales."""
        pagos = get_pagos_suplidores()
        rows = []
        
        for pago in pagos:
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(pago[1])),  # servicio
                        ft.DataCell(ft.Text(pago[2])),  # correo
                        ft.DataCell(ft.Text(convertir_formato_fecha(pago[3]))),  # fecha
                        ft.DataCell(ft.Text(f"${pago[4]}")),  # monto
                        ft.DataCell(ft.Text(pago[5])),  # estado
                        ft.DataCell(ft.Text(pago[6] or "")),  # comentarios
                        ft.DataCell(
                            ft.Row([
                                ft.IconButton(
                                    icon=ft.icons.EDIT,
                                    tooltip="Editar",
                                    on_click=lambda e, p=pago: editar_pago(e, p)
                                ),
                                ft.IconButton(
                                    icon=ft.icons.DELETE,
                                    tooltip="Eliminar",
                                    on_click=lambda e, p=pago: confirmar_eliminar(e, p)
                                )
                            ])
                        )
                    ]
                )
            )
        
        tabla_container.content.rows = rows
        page.update()

    def mostrar_dialogo_nuevo(e):
        """Muestra el diálogo para nuevo pago."""
        cuentas = get_cuentas()
        
        dropdown_cuenta = ft.Dropdown(
            label="Cuenta/Servicio",
            options=[
                ft.dropdown.Option(
                    key=str(c[0]),
                    text=f"{c[3]} ({c[1]})"
                ) for c in cuentas
            ],
            width=400
        )

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
            txt_field.value = e.date.strftime("%Y-%m-%d")
            page.update()

        txt_fecha.on_click = mostrar_fecha

        txt_monto = ft.TextField(
            label="Monto $",
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*\.?[0-9]*$")
        )

        dropdown_estado = ft.Dropdown(
            label="Estado",
            options=[ft.dropdown.Option(estado) for estado in ESTADOS_PAGO],
            width=400
        )

        txt_comentarios = ft.TextField(
            label="Comentarios",
            multiline=True,
            min_lines=3,
            max_lines=3,
            width=400
        )

        def guardar(e):
            try:
                if not all([dropdown_cuenta.value, txt_fecha.value, txt_monto.value, dropdown_estado.value]):
                    raise ValueError("Todos los campos son obligatorios excepto comentarios")
                
                if insertar_pago_suplidor(
                    int(dropdown_cuenta.value),
                    txt_fecha.value,
                    float(txt_monto.value),
                    dropdown_estado.value,
                    txt_comentarios.value
                ):
                    mostrar_mensaje("Pago registrado exitosamente", page)
                    dlg_modal.open = False
                    actualizar_tabla()
                else:
                    mostrar_mensaje("Error al registrar el pago", page)
            except ValueError as ex:
                mostrar_mensaje(str(ex), page)
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nuevo Pago a Suplidor"),
            content=ft.Column([
                dropdown_cuenta,
                txt_fecha,
                txt_monto,
                dropdown_estado,
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

    def editar_pago(e, pago):
        """Muestra el diálogo para editar un pago existente."""
        txt_fecha = ft.TextField(
            label="Fecha de pago",
            value=pago[3],
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
            txt_field.value = e.date.strftime("%Y-%m-%d")
            page.update()

        txt_fecha.on_click = mostrar_fecha

        txt_monto = ft.TextField(
            label="Monto $",
            value=str(pago[4]),
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*\.?[0-9]*$")
        )

        dropdown_estado = ft.Dropdown(
            label="Estado",
            options=[ft.dropdown.Option(estado) for estado in ESTADOS_PAGO],
            value=pago[5],
            width=400
        )

        txt_comentarios = ft.TextField(
            label="Comentarios",
            value=pago[6] or "",
            multiline=True,
            min_lines=3,
            max_lines=3,
            width=400
        )

        def guardar(e):
            try:
                if not all([txt_fecha.value, txt_monto.value, dropdown_estado.value]):
                    raise ValueError("Fecha, monto y estado son obligatorios")
                
                if actualizar_pago_suplidor(
                    pago[0],  # id
                    txt_fecha.value,
                    float(txt_monto.value),
                    dropdown_estado.value,
                    txt_comentarios.value
                ):
                    mostrar_mensaje("Pago actualizado exitosamente", page)
                    dlg_modal.open = False
                    actualizar_tabla()
                else:
                    mostrar_mensaje("Error al actualizar el pago", page)
            except ValueError as ex:
                mostrar_mensaje(str(ex), page)
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Editar Pago - {pago[1]}"),
            content=ft.Column([
                ft.Text(f"Servicio: {pago[1]}"),
                ft.Text(f"Correo: {pago[2]}"),
                txt_fecha,
                txt_monto,
                dropdown_estado,
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

    def confirmar_eliminar(e, pago):
        """Muestra diálogo de confirmación para eliminar un pago."""
        def eliminar(e):
            if eliminar_pago_suplidor(pago[0]):
                mostrar_mensaje("Pago eliminado exitosamente", page)
                dlg_modal.open = False
                actualizar_tabla()
            else:
                mostrar_mensaje("Error al eliminar el pago", page)
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                f"¿Está seguro de eliminar el pago?\n\n"
                f"Servicio: {pago[1]}\n"
                f"Fecha: {convertir_formato_fecha(pago[3])}\n"
                f"Monto: ${pago[4]}"
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dlg_modal)),
                ft.TextButton("Eliminar", on_click=eliminar)
            ]
        )

        page.dialog = dlg_modal
        dlg_modal.open = True
        page.update()

    def cerrar_dialogo(dlg):
        """Cierra un diálogo."""
        dlg.open = False
        page.update()

    # Crear el contenido principal
    contenido = ft.Column([
        ft.Row([
            ft.Text("Pagos a suplidores", size=20, weight=ft.FontWeight.BOLD),
            ft.ElevatedButton(
                "Nuevo Pago",
                on_click=mostrar_dialogo_nuevo,
                icon=ft.icons.ADD
            )
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        tabla_container
    ])

    # Cargar datos iniciales
    actualizar_tabla()

    return contenido