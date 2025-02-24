import flet as ft
import datetime
import time
from utils import convertir_formato_fecha, mostrar_mensaje
from consultas import get_clientes, eliminar_cliente_db, tiene_pagos, eliminar_pagos, insertar_cliente
from consultas import tiene_suscripciones, eliminar_suscripciones, actualizar_cliente
from tabs.vencimientos_tab import crear_tabla_vencimientos
from tabs.pagos_tab import crear_tab_pagos

def crear_tabla_clientes(page: ft.Page, mainTab: ft.Tabs):
        """
        Crea tabla de clientes con:
        - Agregar nuevo cliente
        - Filtro por nombre con AutoComplete
        - Edición completa de datos incluyendo fecha
        - Actualización en tiempo real
        """
        def actualizar_vencimientos():
            """Updates the vencimientos tab content"""
            mainTab.tabs[0].content = crear_tabla_vencimientos(page)
            page.update()
        
        def actualizar_pagos():
            """Updates the pagos tab content"""
            mainTab.tabs[2].content = crear_tab_pagos(page, mainTab)
            page.update()
        
        # Variables globales
        clientes = get_clientes()
        nombre_seleccionado = None
        tabla_container = ft.Container()
        auto_complete = None
        auto_complete_container = None
        
        contador_clientes = ft.Text(
            f"Total clientes registrados: {len(clientes)}", 
            size=16,
            weight=ft.FontWeight.BOLD,
            color=ft.colors.BLUE
        )
        
        # -----------------------------------------------
        # Función para ELIMINAR CLIENTE
        # -----------------------------------------------
        def eliminar_cliente(e, cliente_id):
            """Elimina un cliente después de verificar y eliminar sus pagos y suscripciones."""
            cliente = next(c for c in clientes if c[0] == cliente_id)
            
            def confirmar_eliminacion(e):
                try:
                    # Check and delete payments
                    if tiene_pagos(cliente_id):
                        eliminar_pagos(cliente_id)
                    
                    # Check and delete subscriptions
                    if tiene_suscripciones(cliente_id):
                        eliminar_suscripciones(cliente_id)
                    
                    # Delete the client
                    if eliminar_cliente_db(cliente_id):
                        mostrar_mensaje("Cliente eliminado correctamente", page)
                        
                        # Update the client list and table
                        nonlocal clientes
                        clientes = get_clientes()
                        actualizar_tabla(clientes)
                        actualizar_autocomplete()
                        
                        # Update the vencimientos table                        
                        actualizar_vencimientos()
                        actualizar_pagos()
                        
                        page.update()
                    else:
                        mostrar_mensaje("Error al eliminar cliente", page)
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
                content=ft.Text(f"¿Está seguro que desea eliminar al cliente {cliente[1]}?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar_eliminacion),
                    ft.TextButton("Eliminar", on_click=confirmar_eliminacion)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            
            page.overlay.append(dlg_confirmacion)
            dlg_confirmacion.open = True
            page.update()
        # -----------------------------------------------
        # Función para NUEVO CLIENTE
        # -----------------------------------------------
        def nuevo_cliente(e):
            """Abre diálogo para crear nuevo cliente"""
            nombre_edit = ft.TextField(label="Nombre", capitalization=ft.TextCapitalization.WORDS)
            whatsapp_edit = ft.TextField(label="WhatsApp", max_length=10, 
                        input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
            fecha_edit = ft.TextField(
                label="Fecha inicio",
                value=datetime.date.today().strftime("%Y-%m-%d"),
                read_only=True,
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda _: mostrar_datepicker_nuevo()
            )
            condicion_edit = ft.Dropdown(
                label="Condicion",
                options=[
                    ft.dropdown.Option("Activo"),
                    ft.dropdown.Option("Inactivo")
                ],
                value="Activo"
            )
            frecuencia_edit = ft.Dropdown(
                label="Frecuencia",
                options=[
                    ft.dropdown.Option("30"),
                    ft.dropdown.Option("15"),
                    ft.dropdown.Option("1"),
                ],
                value="30"
            )
            comentario_edit = ft.TextField(label="Comentario", multiline=True, max_length=100)

            def seleccionar_fecha_nuevo(e):
                if e.control.value:
                    fecha = e.control.value.date()
                    fecha_edit.value = fecha.strftime("%Y-%m-%d")
                    e.control.open = False
                    page.update()

            def mostrar_datepicker_nuevo():
                date_picker = ft.DatePicker(
                    first_date=datetime.datetime.now() - datetime.timedelta(days=30),
                    last_date=datetime.datetime.now() + datetime.timedelta(days=365),
                    on_change=seleccionar_fecha_nuevo
                )
                page.overlay.append(date_picker)
                date_picker.open = True
                page.update()

            def guardar_nuevo(e):
                try:
                    # Validar campos requeridos
                    if not all([
                        nombre_edit.value,
                        whatsapp_edit.value,
                        fecha_edit.value,
                        condicion_edit.value,
                        frecuencia_edit.value
                    ]):
                        dlg_modal.open = False
                        raise ValueError("Todos los campos son requeridos")
                    
                    if insertar_cliente(
                        nombre_edit.value,
                        whatsapp_edit.value,
                        fecha_edit.value,
                        condicion_edit.value,
                        int(frecuencia_edit.value),
                        comentario_edit.value
                    ):
                        dlg_modal.open = False
                        
                        # Actualizar datos
                        nonlocal clientes
                        limpiar_y_recrear_auto_complete(auto_complete_container, clientes)
                        
                        clientes = get_clientes()
                        actualizar_tabla(clientes)
                        actualizar_autocomplete()  
                        
                        # Actualizar tabla de vencimientos
                        actualizar_vencimientos()
                        actualizar_pagos()
                        
                        page.update()
                        mostrar_mensaje("Cliente creado", page)
                    else:
                        mostrar_mensaje("Error al crear", page)
                except Exception as ex:
                    mostrar_mensaje(f"Error: {str(ex)}", page)
                page.update()

            def close_dlg(e):
                """Cierra el diálogo modal"""
                dlg_modal.open = False
                e.control.page.update()
            
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Nuevo Cliente"),
                content=ft.Column([
                    nombre_edit,
                    whatsapp_edit,
                    fecha_edit,
                    condicion_edit,
                    frecuencia_edit,
                    comentario_edit
                ]),
                actions=[
                    ft.TextButton("Cancelar", on_click=close_dlg),
                    ft.TextButton("Guardar", on_click=guardar_nuevo)
                ]
            )
            
            page.overlay.append(dlg_modal)
            dlg_modal.open = True
            page.update()
        # -----------------------------------------------
        # Función para EDITAR CLIENTE
        # -----------------------------------------------
        def editar_cliente(e, cliente_id):
            """Abre diálogo para editar cliente"""
            cliente = next(c for c in clientes if c[0] == cliente_id)
            
            nombre_edit = ft.TextField(label="Nombre", value=cliente[1])
            whatsapp_edit = ft.TextField(label="WhatsApp", value=cliente[3], max_length=10, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
            fecha_edit = ft.TextField(
                label="Fecha inicio",
                value=cliente[2],
                read_only=True,
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda _: mostrar_datepicker_edit()
            )
            condicion_edit = ft.Dropdown(
                label="Condicion",
                options=[
                    ft.dropdown.Option("Activo"),
                    ft.dropdown.Option("Inactivo")
                ],
                value=cliente[4]
            )
            frecuencia_edit = ft.TextField(
                label="Frecuencia",
                value=str(cliente[5]),
                input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
            )
            comentario_edit = ft.TextField(label="Comentario", multiline=True, value=cliente[6])

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
                    first_date=datetime.datetime.now() - datetime.timedelta(days=30),
                    last_date=datetime.datetime.now() + datetime.timedelta(days=365),
                    on_change=lambda e: seleccionar_fecha_edit(e, fecha_edit)
                )
                page.overlay.append(date_picker)
                date_picker.open = True
                page.update()
                
            # Usar en el diálogo de edición:
            fecha_edit = ft.TextField(
                label="Fecha inicio",
                value=cliente[2],
                read_only=True,
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda _: mostrar_datepicker_edit()
            )

            def guardar_cambios(e):
                """Guarda cambios del cliente"""
                try:
                    if actualizar_cliente(
                        cliente_id,
                        nombre_edit.value,
                        whatsapp_edit.value,
                        fecha_edit.value,
                        condicion_edit.value,
                        int(frecuencia_edit.value),
                        comentario_edit.value
                    ):
                        dlg_modal.open = False
                        
                        nonlocal clientes                        
                        # Limpia y recrea el AutoComplete
                        limpiar_y_recrear_auto_complete(auto_complete_container, clientes)
                        
                        
                        clientes = get_clientes()
                        actualizar_tabla(clientes)
                        actualizar_autocomplete()
                        
                        # Actualizar tabla de vencimientos
                        actualizar_vencimientos()
                        actualizar_pagos()
                        
                        page.update()
                        
                        
                        mostrar_mensaje("Cliente actualizado", page)
                    else:
                        mostrar_mensaje("Error al actualizar", page)
                except Exception as ex:
                    mostrar_mensaje(f"Error: {str(ex)}", page)
                page.update()

            def close_dlg(e):
                """Cierra el diálogo modal"""
                dlg_modal.open = False
                e.control.page.update()
            
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar Cliente"),
                content=ft.Column([
                    nombre_edit,
                    whatsapp_edit,
                    fecha_edit,
                    condicion_edit,
                    frecuencia_edit,
                    comentario_edit
                ]),
                actions=[
                    ft.TextButton("Cancelar", 
                        on_click=close_dlg),
                    ft.TextButton("Guardar", 
                        on_click=guardar_cambios)
                ]
            )            
            page.overlay.append(dlg_modal)
            dlg_modal.open = True
            page.update()
        
        
        def actualizar_tabla(registros_filtrados):
            """Actualiza contenido de la tabla."""
            
            # Update counter
            contador_clientes.value = f"Total clientes registrados: {len(clientes)}"
            
            tabla_container.content = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("Inicio")),
                    ft.DataColumn(ft.Text("WhatsApp")),
                    ft.DataColumn(ft.Text("Condicion")),
                    ft.DataColumn(ft.Text("Frecuencia")),
                    ft.DataColumn(ft.Text("Comentario")),
                    ft.DataColumn(ft.Text("Editar")),
                    ft.DataColumn(ft.Text("Eliminar")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(cliente[0]))),
                            ft.DataCell(ft.Text(cliente[1])),
                            ft.DataCell(ft.Text(convertir_formato_fecha(cliente[2]))),
                            ft.DataCell(ft.Text(cliente[3])),
                            ft.DataCell(ft.Text(cliente[4])),
                            ft.DataCell(ft.Text(f"{cliente[5]} días")),
                            ft.DataCell(ft.Text(cliente[6])),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    data=cliente,
                                    on_click=lambda e, id=cliente[0]: 
                                        editar_cliente(e, id)
                                )
                            ),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.DELETE,
                                    icon_color="red",
                                    data=cliente,
                                    on_click=lambda e, id=cliente[0]:
                                        eliminar_cliente(e, id)
                                )
                            ),
                        ]
                    ) for cliente in registros_filtrados
                ],
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400)
            )
            page.update()

        def on_autocomplete_selected(e):
            """Filtra tabla por nombre seleccionado"""
            nonlocal nombre_seleccionado
            nombre_seleccionado = e.selection.value
            if nombre_seleccionado:
                filtrados = [c for c in clientes 
                            if c[1].lower() == nombre_seleccionado.lower()]
                actualizar_tabla(filtrados)
            else:
                actualizar_tabla(clientes)

        # Crear AutoComplete
        nombres = sorted(set(c[1] for c in clientes))
        auto_complete = ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key=nombre, value=nombre) 
                for nombre in nombres
            ],
            on_select=on_autocomplete_selected
        )

        auto_complete_container = ft.Container(
            content=auto_complete,
            width=320,
            border=ft.border.all(1, ft.Colors.BLACK),
            border_radius=10
        )
        
        def actualizar_autocomplete():
            """Actualiza sugerencias del AutoComplete."""
            if auto_complete and auto_complete_container:
                nombres = sorted(set(c[1] for c in clientes))
                auto_complete.suggestions = [
                    ft.AutoCompleteSuggestion(key=nombre, value=nombre) 
                    for nombre in nombres
                ]
                auto_complete_container.content = auto_complete
                auto_complete_container.update()
            
        # Inicializar componentes
        def limpiar_y_recrear_auto_complete(auto_complete_container, clientes):
            """
            Limpia y recrea el AutoComplete después de actualizar cliente.
            Mantiene el filtro por nombre y actualiza la tabla.

            Args:
                auto_complete_container: Contenedor del AutoComplete
                clientes: Lista actualizada de clientes
            """
            nonlocal nombre_seleccionado

            # Obtener cliente actualizado
            cliente_actualizado = next(
                (c for c in clientes if c[1].lower() == nombre_seleccionado.lower()),
                None
            ) if nombre_seleccionado else None

            # Crear sugerencias
            if cliente_actualizado:
                # Mostrar solo el cliente actualizado
                sugerencias = [
                    ft.AutoCompleteSuggestion(
                        key=cliente_actualizado[1],
                        value=cliente_actualizado[1]
                    )
                ]
                # Actualizar tabla filtrada
                actualizar_tabla([cliente_actualizado])
            else:
                # Mostrar todos los clientes
                nombres = sorted(set(c[1] for c in clientes))
                sugerencias = [
                    ft.AutoCompleteSuggestion(key=nombre, value=nombre)
                    for nombre in nombres
                ]
                # Actualizar tabla completa
                actualizar_tabla(clientes)

            # Recrear AutoComplete
            auto_complete = ft.AutoComplete(
                suggestions=sugerencias,
                on_select=on_autocomplete_selected,
                suggestions_max_height=150
            )

            # Actualizar contenedor
            auto_complete_container.content = auto_complete
            auto_complete_container.update()

        actualizar_tabla(clientes)       
        
        return ft.Column([
            ft.Text("Clientes", size=20, weight="bold"),
            ft.Row([
                auto_complete_container,
                ft.ElevatedButton(
                    "Nuevo Cliente",
                    icon=ft.Icons.ADD,
                    on_click=nuevo_cliente
                ),
                contador_clientes
            ], alignment=ft.MainAxisAlignment.START),
            tabla_container
        ])