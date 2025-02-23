import flet as ft
import datetime
from utils import convertir_formato_fecha, mostrar_mensaje, get_estado_color
from consultas import get_clientes_pagos, get_estado_pago_cliente, insertar_pago, get_pagos_cliente, eliminar_pago, actualizar_pago
from tabs.vencimientos_tab import crear_tabla_vencimientos

def crear_tab_pagos(page: ft.Page, mainTab: ft.Tabs):
        """
        Crea tab para aplicar pagos con AutoComplete y fecha.
        Permite seleccionar cliente, establecer fecha y registrar pago.
        """
        
        # Add after info_container definition
        tabla_pagos = ft.Container(
        content=ft.DataTable(  # Contenido inicial vacío
            columns=[
                ft.DataColumn(ft.Text("Fecha")),
                ft.DataColumn(ft.Text("Monto")),
                ft.DataColumn(ft.Text("Editar")),
                ft.DataColumn(ft.Text("Eliminar"))
            ],
            rows=[]
        ),
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=10
        )
        
        def actualizar_tabla_pagos(cliente_id):
            """Actualiza la tabla de pagos del cliente."""
            pagos = get_pagos_cliente(cliente_id)
            tabla_pagos.content = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Fecha")),
                    ft.DataColumn(ft.Text("Monto")),
                    ft.DataColumn(ft.Text("Editar")),
                    ft.DataColumn(ft.Text("Eliminar"))
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(convertir_formato_fecha(pago[2]))),
                            ft.DataCell(ft.Text(f"${pago[3]}")),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.EDIT,
                                        tooltip="Editar",
                                        on_click=lambda e, p=pago: editar_pago(e, p)
                                    )
                                ])
                            ),
                            ft.DataCell(
                                ft.Row([
                                    ft.IconButton(
                                        icon=ft.Icons.DELETE,
                                        icon_color="red",
                                        tooltip="Eliminar",
                                        on_click=lambda e, p=pago: confirmar_eliminar_pago(e, p)
                                    ) if index == 0 else ft.Text("")  # Solo mostrar en el primer registro (último pago)
                                ])
                            )
                        ]
                    ) for index, pago in enumerate(pagos)  # Añadimos index para rastrear la posición
                ]
            )
            page.update()
        
        
        
        def confirmar_eliminar_pago(e, pago):
            def eliminar(e):
                if eliminar_pago(pago[0]):
                    mostrar_mensaje("Pago eliminado", page)
                    actualizar_tabla_pagos(pago[0])
                    actualizar_vencimientos()
                dlg_modal.open = False
                page.update()

            def cancelar(e):
                dlg_modal.open = False
                page.update()

            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar eliminación"),
                content=ft.Text(f"¿Eliminar el pago de ${pago[3]} del {convertir_formato_fecha(pago[2])}?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.TextButton("Eliminar", on_click=eliminar)
                ]
            )
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        def editar_pago(e, pago):
            
            def seleccionar_fecha_edit(e, txt_field):
                """
                Actualiza TextField con la fecha seleccionada en el DatePicker.
                
                Args:
                    e: Evento del DatePicker con la fecha seleccionada
                    txt_field: TextField a actualizar con la nueva fecha
                """
                if e.control.value:
                    fecha = e.control.value.date()
                    txt_field.value = fecha.strftime("%Y-%m-%d")
                    e.control.open = False
                    page.update()
            
            def mostrar_datepicker_edit():
                """Muestra DatePicker para editar fecha"""
                date_picker = ft.DatePicker(
                    first_date=datetime.datetime.now() - datetime.timedelta(days=365),
                    last_date=datetime.datetime.now() + datetime.timedelta(days=365),
                    on_change=lambda e: seleccionar_fecha_edit(e, fecha_edit)
                )
                page.overlay.append(date_picker)
                date_picker.open = True
                page.update()
                
            fecha_edit = ft.TextField(
                label="Fecha",
                value=pago[2],
                read_only=True,
                on_click=lambda _: mostrar_datepicker_edit()
            )
            monto_edit = ft.TextField(
                label="Monto",
                value=str(pago[3])
            )

            def guardar(e):
                try:
                    if actualizar_pago(pago[0], fecha_edit.value, int(monto_edit.value)):
                        mostrar_mensaje("Pago actualizado", page)
                        # Actualizar tabla de pagos
                        actualizar_tabla_pagos(pago[0])
                        # Actualizar vencimientos
                        actualizar_vencimientos()
                        # Actualizar controles de pago
                        if cliente_seleccionado:
                            cliente_id = next(
                                (c[0] for c in clientes if c[1] == cliente_seleccionado), 
                                None
                            )
                            if cliente_id:
                                cliente = get_estado_pago_cliente(cliente_id)
                                if cliente:
                                    info_container.content = ft.Column([
                                        ft.Text(f"Informacion sobre : {cliente[1]}", size=20),
                                        ft.Text(f"Último pago: {convertir_formato_fecha(cliente[9])}"),
                                        ft.Text(f"Próximo pago: {convertir_formato_fecha(cliente[10])}"),
                                        ft.Text(f"Pago mensual de: $ {cliente[6]}"),
                                        ft.Text(f"Deuda pendiente: $ {cliente[13]}"),
                                        ft.Text(f"Monto a pagar: $ {cliente[6]+cliente[13]}"),
                                        ft.Text(f"Días transcurridos: {cliente[11]}"),
                                        ft.Text(
                                            f"Estado: {cliente[12]}", 
                                            color=get_estado_color(cliente[12])
                                        )
                                    ])
                        dlg_modal.open = False
                        page.update()
                except ValueError as ex:
                    mostrar_mensaje(f"Error: {str(ex)}", page)

            def cancelar(e):
                dlg_modal.open = False
                page.update()

            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar pago"),
                content=ft.Column([fecha_edit, monto_edit]),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar),
                    ft.TextButton("Guardar", on_click=guardar)
                ]
            )
            page.dialog = dlg_modal
            dlg_modal.open = True
            page.update()

        
        
        def actualizar_vencimientos():
            """Updates the vencimientos tab content"""
            mainTab.tabs[0].content = crear_tabla_vencimientos(page)
            page.update()
        
        # Variables de estado
        info_container = ft.Container()
        cliente_seleccionado = None
        clientes = get_clientes_pagos()  # Se obtiene la lista de clientes actualizada
        txt_fecha_pago = ft.Ref[ft.TextField]()
        txt_campo_pago = ft.Ref[ft.TextField]()
        tabla_vencimientos = None  # Referencia a tabla_vencimientos
        
        
        def limpiar_y_recrear_auto_complete_pago(auto_complete_container, clientes):
            """
            Limpia y recrea el AutoComplete después de aplicar un pago.
            """
            nonlocal cliente_seleccionado
            cliente_seleccionado = None
            # Obtener nombres actualizados
            nombres = sorted(set(c[1] for c in clientes))
            # Recrear AutoComplete limpio
            auto_complete = ft.AutoComplete(
                suggestions=[
                    ft.AutoCompleteSuggestion(key=nombre, value=nombre)
                    for nombre in nombres
                ],
                on_select=on_cliente_selected
            )
            # Actualizar contenedor
            auto_complete_container.content = auto_complete
            auto_complete_container.update()
            # Limpiar otros campos
            info_container.content = None
            txt_fecha_pago.current.value = ""
            page.update()

        def mostrar_datepicker_pago(e):
            """
            Muestra el DatePicker para seleccionar fecha de pago.
            """
            date_picker = ft.DatePicker(
                first_date=datetime.datetime.now() - datetime.timedelta(days=365),
                last_date=datetime.datetime.now() + datetime.timedelta(days=365),
                on_change=lambda e: seleccionar_fecha_pago(e),
            )
            page.overlay.append(date_picker)
            date_picker.open = True
            page.update()
                
        def seleccionar_fecha_pago(e):
            """
            Actualiza TextField con la fecha seleccionada.
            """
            if e.control.value:
                fecha = e.control.value.date()
                txt_fecha_pago.current.value = fecha.strftime("%Y-%m-%d")
                e.control.open = False
                page.update()
            
        def limpiar_seleccion():
            """Limpia selección y campos"""
            nonlocal cliente_seleccionado
            cliente_seleccionado = None
            info_container.content = None
            txt_fecha_pago.current.value = ""
            page.update()
                
        # Crear controles
        campo_fecha = ft.TextField(
            ref=txt_fecha_pago,
            label="Fecha de pago",
            width=320,
            read_only=True,
            on_click=mostrar_datepicker_pago
        )
        campo_pago = ft.TextField(
            ref=txt_campo_pago,
            label="Monto a pagar $",
            width=320,
            read_only=False,
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
            
        def on_cliente_selected(e):
            """Actualiza información cuando se selecciona cliente"""
            nonlocal cliente_seleccionado
            cliente_seleccionado = e.selection.value
            if cliente_seleccionado:
                cliente_id = next(
                    (c[0] for c in clientes if c[1] == cliente_seleccionado), 
                    None
                )
                if cliente_id:
                    cliente = get_estado_pago_cliente(cliente_id)
                    if cliente:
                        
                        # Los índices corresponden a la nueva consulta de get_estado_pago_cliente
                        info_container.content = ft.Column([
                            ft.Text(f"Informacion sobre : {cliente[1]}", size=20),
                            ft.Text(f"Último pago: {convertir_formato_fecha(cliente[9])}"),
                            ft.Text(f"Próximo pago: {convertir_formato_fecha(cliente[10])}"),
                            ft.Text(f"Pago mensual de: $ {cliente[6]}"),
                            ft.Text(f"Deuda pendiente: $ {cliente[13]}"),
                            ft.Text(f"Monto a pagar: $ {cliente[6]+cliente[13]}"),
                            ft.Text(f"Días transcurridos: {cliente[11]}"),
                            ft.Text(
                                f"Estado: {cliente[12]}", 
                                color=get_estado_color(cliente[12])
                            )
                        ])
                        actualizar_tabla_pagos(cliente_id)
                        page.update()
        def aplicar_pago(e):
            """Registra pago y limpia selección"""
            try:
                if not cliente_seleccionado:
                    raise ValueError("Seleccione un cliente")
                if not txt_fecha_pago.current.value:
                    raise ValueError("Seleccione fecha de pago")
                if not txt_campo_pago.current.value:
                    raise ValueError("Coloca el monto a pagar")
                
                cliente_id = next(
                    (c[0] for c in clientes if c[1] == cliente_seleccionado), 
                    None
                )
                
                # Convertir monto a entero
                monto_pagado = int(txt_campo_pago.current.value)
                
                if insertar_pago(cliente_id, txt_fecha_pago.current.value, monto_pagado):
                    mostrar_mensaje("Pago registrado correctamente", page)
                    limpiar_y_recrear_auto_complete_pago(auto_complete_container, get_clientes_pagos())
                    txt_fecha_pago.current.value = ""
                    txt_campo_pago.current.value = ""
                    
                    # actualizar tabla de vencimientos
                    actualizar_vencimientos()
                    
                    page.update()
                else:
                    mostrar_mensaje("Error registrando pago", page)
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}", page)

        # AutoComplete para selección de cliente
        nombres = sorted(set(c[1] for c in clientes))
        auto_complete = ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key=nombre, value=nombre)
                for nombre in nombres
            ],
            on_select=on_cliente_selected
        )
            
        # Contenedor para AutoComplete
        auto_complete_container = ft.Container(
            content=auto_complete,
            width=320,
            border=ft.border.all(1, ft.Colors.BLACK),
            border_radius=10
        )

        return ft.Column([
            ft.Text("Registrar pago", size=20, weight="bold"),
            ft.Row([
                ft.Column([
                    auto_complete_container,
                    campo_fecha,
                    campo_pago,
                    ft.Column([  # Nueva columna independiente para info_container
                        info_container
                    ], expand=True),
                    ft.ElevatedButton(
                        "Aplicar Pago",
                        on_click=aplicar_pago,
                        icon=ft.Icons.SAVE
                    )
                ], spacing=10, expand=1),  # Expand para ocupar el espacio restante
                
                ft.Column([
                    ft.Text("Historial de pago del cliente", size=20, weight="bold"),
                    tabla_pagos
                ], alignment=ft.MainAxisAlignment.START)  # Asegura que la tabla no se mueva
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ])

