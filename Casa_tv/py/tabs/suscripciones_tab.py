import flet as ft
from utils import mostrar_mensaje
from tabs.vencimientos_tab import crear_tabla_vencimientos
from consultas import (
    get_suscripcion_by_id,
    get_cliente_by_nombre,
    get_cuenta_by_servicio,
    eliminar_suscripcion_db,
    get_suscripciones,
    get_clientes,
    get_cuentas,
    insertar_suscripcion,
    actualizar_suscripcion
)

def cerrar_dialogo(dialog, page):
        """Cierra el diálogo y actualiza la página."""
        dialog.open = False
        page.update()
def  crear_tab_suscripciones(page: ft.Page, mainTab: ft.Tabs):
    """
    Crea el tab "Suscripciones" con funcionalidad similar al tab de cuentas
    """
    def actualizar_vencimientos():
            """Updates the vencimientos tab content"""
            mainTab.tabs[0].content = crear_tabla_vencimientos(page)
            page.update()
    
    # Contenedor principal para la tabla
    tabla_container = ft.Container()
    correo_seleccionado = None
    suscripcion_seleccionada = None
    suscripciones_auto_complete = None
    
    def eliminar_suscripcion(e, suscripcion_id):
        """Elimina una suscripción después de confirmar con el usuario."""
        try:
            suscripcion = get_suscripcion_by_id(suscripcion_id)
            if not suscripcion:
                mostrar_mensaje("Error: No se encontró la suscripción", page)
                return
            
            # Get related data with safe checks
            cliente = get_cliente_by_nombre(suscripcion[1])
            cuenta = get_cuenta_by_servicio(suscripcion[2])
            
            # Safe access to data with fallbacks
            cliente_nombre = cliente[1] if cliente else "Cliente no encontrado"
            servicio_nombre = cuenta[3] if cuenta else "Servicio no encontrado"
            correo = suscripcion[4] if suscripcion[4] else "Sin correo"
            
            def confirmar_eliminacion(e):
                try:
                    if eliminar_suscripcion_db(suscripcion_id):
                        mostrar_mensaje("Suscripción eliminada correctamente", page)
                        actualizar_autocomplete()
                        actualizar_tabla_suscripciones()
                        actualizar_vencimientos()
                    else:
                        mostrar_mensaje("Error al eliminar suscripción", page)
                except Exception as ex:
                    mostrar_mensaje(f"Error: {str(ex)}", page)
                dlg_confirmacion.open = False
                page.update()

            def cancelar_eliminacion(e):
                dlg_confirmacion.open = False
                page.update()

            dlg_confirmacion = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar eliminación"),
                content=ft.Text(
                    f"¿Está seguro que desea eliminar la suscripción?\n"
                    f"Cliente: {cliente_nombre}\n"
                    f"Servicio: {servicio_nombre}\n"
                    f"Correo: {correo}"
                ),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar_eliminacion),
                    ft.TextButton("Eliminar", on_click=confirmar_eliminacion)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            
            page.overlay.append(dlg_confirmacion)
            dlg_confirmacion.open = True
            page.update()
        except Exception as ex:
            mostrar_mensaje(f"Error al preparar eliminación: {str(ex)}", page)
        
    def actualizar_autocomplete():
        """Actualiza las sugerencias del autocomplete con los correos de suscripciones"""
        suscripciones = get_suscripciones()
        if auto_complete and auto_complete_container:
            correos = sorted(set(s[4] for s in suscripciones))  # Índice 4 es el correo
            auto_complete.suggestions = [
                ft.AutoCompleteSuggestion(key=correo, value=correo) 
                for correo in correos
            ]
            auto_complete_container.content = auto_complete
            auto_complete_container.update()

    def actualizar_tabla_suscripciones(suscripciones_filtradas=None):
        """Actualiza la tabla con los datos de suscripciones"""
        suscripciones_list = suscripciones_filtradas if suscripciones_filtradas is not None else get_suscripciones()
        rows = []
        
        for suscripcion in suscripciones_list:
            # suscripcion[0] = id
            # suscripcion[1] = nombre del cliente
            # suscripcion[2] = servicio
            # suscripcion[3] = monto
            # suscripcion[4] = correo
            
            editar_btn = ft.IconButton(
                icon=ft.Icons.EDIT,
                tooltip="Editar suscripción",
                on_click=lambda e, id=suscripcion[0]: editar_suscripcion(e, id, page)
            )
            eliminar_btn = ft.IconButton(
                icon=ft.Icons.DELETE,
                tooltip="Eliminar suscripción",
                icon_color="red",
                on_click=lambda e, id=suscripcion[0]: eliminar_suscripcion(e, id)
            )
            
            rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(suscripcion[0]))),
                        ft.DataCell(ft.Text(suscripcion[1])),
                        ft.DataCell(ft.Text(suscripcion[2])),  # Nombre del servicio
                        ft.DataCell(ft.Text(f"${int(suscripcion[3])}")),
                        ft.DataCell(ft.Text(suscripcion[4])),
                        ft.DataCell(editar_btn),
                        ft.DataCell(eliminar_btn)
                    ]
                )
            )
        
        tabla_container.content = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("ID")),
                ft.DataColumn(ft.Text("Cliente")),
                ft.DataColumn(ft.Text("Servicio")),
                ft.DataColumn(ft.Text("Pago mens.")),
                ft.DataColumn(ft.Text("Correo")),
                ft.DataColumn(ft.Text("Editar")),
                ft.DataColumn(ft.Text("Eliminar"))
            ],
            rows=rows,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400)
        )
        page.update()


    def abrir_dialogo_nuevo(e):
        """Diálogo para nueva suscripción"""
        clientes = get_clientes()
        cuentas = get_cuentas()
        
        # Dropdown para clientes
        dropdown_cliente = ft.Dropdown(
            options=[ft.dropdown.Option(key=str(c[0]), text=c[1]) for c in clientes],
            label="Cliente",
            expand=True
        )
        
        # Dropdown para cuentas
        dropdown_cuenta = ft.Dropdown(
            options=[ft.dropdown.Option(key=str(c[0]), text=f"{c[3]} ({c[1]})") for c in cuentas],
            label="Cuenta",
            expand=True
        )
        
        txt_monto = ft.TextField(
            label="Monto (DOP)",
            expand=True,
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        
        txt_correo = ft.TextField(label="Correo", expand=True)

        def guardar_nueva_suscripcion(e):
            try:
                if not dropdown_cliente.value:
                    mostrar_mensaje("Seleccione un cliente", page)
                    return
                if not dropdown_cuenta.value:
                    mostrar_mensaje("Seleccione una cuenta", page)
                    return
                if not txt_monto.value:
                    mostrar_mensaje("Ingrese un monto válido", page)
                    return
                if not txt_correo.value:
                    mostrar_mensaje("Ingrese un correo", page)
                    return
                
                if txt_correo.value != [c[1] for c in cuentas if c[0] == int(dropdown_cuenta.value)][0]:
                    mostrar_mensaje("El correo no coincide con el de la cuenta", page)
                    return

                if insertar_suscripcion(
                    int(dropdown_cliente.value),
                    int(dropdown_cuenta.value),
                    int(txt_monto.value),
                    txt_correo.value
                ):
                    mostrar_mensaje("Suscripción creada!", page)
                    dialogo_nuevo.open = False
                    actualizar_autocomplete()
                    actualizar_tabla_suscripciones()
                    actualizar_vencimientos()
                else:
                    mostrar_mensaje("Error al crear suscripción", page)
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}", page)
            page.update()

        dialogo_nuevo = ft.AlertDialog(
            modal=True,
            title=ft.Text("Nueva Suscripción"),
            content=ft.Column([
                dropdown_cliente,
                dropdown_cuenta,
                txt_monto,
                txt_correo
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dialogo_nuevo, page)),
                ft.TextButton("Guardar", on_click=guardar_nueva_suscripcion)
            ]
        )
        page.overlay.append(dialogo_nuevo)
        dialogo_nuevo.open = True
        page.update()
        
    
        
    def editar_suscripcion(e, suscripcion_id, page):
        """Diálogo para editar suscripción existente"""
        suscripcion = get_suscripcion_by_id(suscripcion_id)
        clientes = get_clientes()
        cuentas = get_cuentas()

        dropdown_cliente = ft.Dropdown(
            options=[ft.dropdown.Option(key=str(c[0]), text=c[1]) for c in clientes],
            value=str(suscripcion[1]),
            label="Cliente",
            expand=True
        )
        
        dropdown_cuenta = ft.Dropdown(
            options=[ft.dropdown.Option(key=str(c[0]), text=f"{c[3]} ({c[1]})") for c in cuentas],
            value=str(suscripcion[2]),
            label="Cuenta",
            expand=True
        )
        
        txt_monto = ft.TextField(
            value=str(suscripcion[3]), 
            label="Monto (DOP)",
            expand=True,
            input_filter=ft.NumbersOnlyInputFilter()
        )
        
        txt_correo = ft.TextField(value=suscripcion[4], label="Correo", expand=True)

        def guardar_cambios(e):
            try:
                if not dropdown_cliente.value:
                    mostrar_mensaje("Seleccione un cliente", page)
                    return
                if not dropdown_cuenta.value:
                    mostrar_mensaje("Seleccione una cuenta", page)
                    return
                if not txt_monto.value:
                    mostrar_mensaje("Ingrese un monto válido", page)
                    return
                if not txt_correo.value:
                    mostrar_mensaje("Ingrese un correo", page)
                    return
                
                if txt_correo.value != [c[1] for c in cuentas if c[0] == int(dropdown_cuenta.value)][0]:
                    mostrar_mensaje("El correo no coincide con el de la cuenta", page)
                    return
                
                if actualizar_suscripcion(
                    suscripcion_id,
                    int(dropdown_cliente.value),
                    int(dropdown_cuenta.value),
                    int(txt_monto.value),
                    txt_correo.value
                ):
                    mostrar_mensaje("Suscripción actualizada!", page)
                    dlg_modal.open = False
                    actualizar_autocomplete()
                    actualizar_tabla_suscripciones()
                    actualizar_vencimientos()
                else:
                    mostrar_mensaje("Error al actualizar", page)
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}", page)
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Suscripción"),
            content=ft.Column([
                dropdown_cliente,
                dropdown_cuenta,
                txt_monto,
                txt_correo
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dlg_modal, page)),
                ft.TextButton("Guardar", on_click=guardar_cambios)
            ]
        )
        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()

    # Componentes UI
    btn_nuevo = ft.ElevatedButton(
        text="Nueva suscripción",
        icon=ft.Icons.ADD,
        on_click=abrir_dialogo_nuevo
    )

    # Autocomplete para correos
    suscripciones = get_suscripciones()
    auto_complete = ft.AutoComplete(
        suggestions=[
            ft.AutoCompleteSuggestion(key=s[4], value=s[4])
            for s in suscripciones
        ],
        on_select=lambda e: actualizar_tabla_suscripciones(
            [s for s in suscripciones if s[4] == e.selection.value]
        ),
        suggestions_max_height=150
    )

    auto_complete_container = ft.Container(
        content=auto_complete,
        width=320,
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=10
    )

    
    contenido_tab = ft.Column([
        ft.Text("Listado de Suscripciones", size=20, weight="bold"),
        ft.Row([auto_complete_container, btn_nuevo], alignment=ft.MainAxisAlignment.START),
        tabla_container
    ], spacing=20)

    actualizar_tabla_suscripciones()
    return contenido_tab