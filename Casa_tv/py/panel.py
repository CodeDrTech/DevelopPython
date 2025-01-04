import flet as ft
from flet import ScrollMode, AppView
from consultas import get_clientes, actualizar_cliente, get_estado_pagos, insertar_pago, get_estado_pago_cliente, insertar_cliente
import datetime




def main(page: ft.Page):
    page.title = "TV en casa"
    page.window.alignment = ft.alignment.center
    page.window.width = 1050
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = False # type: ignore
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    
    # Referencias globales
    txt_fecha_pago = ft.Ref[ft.TextField]()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Referencias para controles
    txt_nombre = ft.Ref[ft.TextField]()
    txt_whatsapp = ft.Ref[ft.TextField]()
    txt_fecha_inicio = ft.Ref[ft.TextField]()
    dd_estado = ft.Ref[ft.Dropdown]()
    txt_frecuencia = ft.Ref[ft.TextField]()

    def mostrar_datepicker_inicio(e):
        """Muestra DatePicker para fecha inicio"""
        date_picker = ft.DatePicker(
            first_date=datetime.datetime.now(),
            last_date=datetime.datetime.now() + datetime.timedelta(days=30),
            on_change=lambda e: seleccionar_fecha_inicio(e)
        )
        page.overlay.append(date_picker)
        date_picker.open = True
        page.update()

    def seleccionar_fecha_inicio(e):
        """Actualiza TextField con fecha seleccionada"""
        if e.control.value:
            fecha = e.control.value.date()
            txt_fecha_inicio.current.value = fecha.strftime("%Y-%m-%d")
            e.control.open = False
            page.update()

    def limpiar_campos():
        """Limpia todos los campos del formulario"""
        txt_nombre.current.value = ""
        txt_whatsapp.current.value = ""
        txt_fecha_inicio.current.value = ""
        dd_estado.current.value = "Activo"
        txt_frecuencia.current.value = ""
        page.update()

    def guardar_cliente(e):
        """Valida y guarda nuevo cliente"""
        try:
            # Validar campos requeridos
            if not all([
                txt_nombre.current.value,
                txt_whatsapp.current.value,
                txt_fecha_inicio.current.value,
                dd_estado.current.value,
                txt_frecuencia.current.value
            ]):
                raise ValueError("Todos los campos son requeridos")

            # Insertar cliente
            if insertar_cliente(
                txt_nombre.current.value,
                txt_whatsapp.current.value,
                txt_fecha_inicio.current.value,
                dd_estado.current.value,
                int(txt_frecuencia.current.value)
            ):
                mostrar_mensaje("Cliente guardado correctamente")
                limpiar_campos()
            else:
                mostrar_mensaje("Error al guardar cliente")
        except ValueError as e:
            mostrar_mensaje(f"Error: {str(e)}")
        except Exception as e:
            mostrar_mensaje(f"Error inesperado: {str(e)}")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_tabla_vencimientos():
        """
        Crea tabla de vencimientos con filtro por nombre cliente.
        Permite filtrar usando AutoComplete con nombres de la BD.
        """
        # Variables globales
        registros = get_estado_pagos()
        nombre_seleccionado = None
        tabla_container = ft.Container()
        
        def on_autocomplete_selected(e):
            """Maneja selección en AutoComplete."""
            nonlocal nombre_seleccionado
            nombre_seleccionado = e.selection.value
            
            # Filtrar registros por nombre
            if nombre_seleccionado:
                registros_filtrados = [
                    reg for reg in registros 
                    if reg[1].lower() == nombre_seleccionado.lower()
                ]
                actualizar_tabla(registros_filtrados)
            else:
                actualizar_tabla(registros)
        
        # Mantener columnas existentes
        columns = [
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Inicio")),
            ft.DataColumn(ft.Text("Ultimo pago")),
            ft.DataColumn(ft.Text("Proximo pago")),
            ft.DataColumn(ft.Text("Frecuencia")),
            ft.DataColumn(ft.Text("Días")),
            ft.DataColumn(ft.Text("Estado"))
        ]
        
        def get_estado_color(estado):
            """Define color según estado de pago"""
            if estado == "En corte":
                return ft.Colors.RED_600
            elif estado == "Pago pendiente":
                return ft.Colors.ORANGE_700
            elif estado == "Cerca":
                return ft.Colors.YELLOW_700
            return ft.Colors.GREEN

        def actualizar_tabla(registros_filtrados):
            """Actualiza contenido de la tabla."""
            tabla_container.content = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("Inicio")),
                    ft.DataColumn(ft.Text("Ultimo pago")),
                    ft.DataColumn(ft.Text("Proximo pago")),
                    ft.DataColumn(ft.Text("Frecuencia")),
                    ft.DataColumn(ft.Text("Días")),
                    ft.DataColumn(ft.Text("Estado"))
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(reg[0]))),
                            ft.DataCell(ft.Text(reg[1])),
                            ft.DataCell(ft.Text(reg[2])),
                            ft.DataCell(ft.Text(reg[3])),
                            ft.DataCell(ft.Text(reg[4])),
                            ft.DataCell(ft.Text(f"{reg[5]} días")),
                            ft.DataCell(ft.Text(str(reg[6]))),
                            ft.DataCell(ft.Text(
                                reg[7],
                                color=get_estado_color(reg[7])
                            )),
                        ],
                    ) for reg in registros_filtrados
                ],
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400)
            )
            page.update()

        # Crear AutoComplete
        nombres = sorted(set(reg[1] for reg in registros))
        auto_complete = ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key=nombre, value=nombre) 
                for nombre in nombres
            ],
            on_select=on_autocomplete_selected
        )

        # Contenedor para AutoComplete
        auto_complete_container = ft.Container(
            content=auto_complete,
            width=320,
            border=ft.border.all(1, ft.Colors.BLACK),
            border_radius=10
        )

        # Mostrar todos inicialmente
        actualizar_tabla(registros)

        return ft.Column([
        auto_complete_container,
        tabla_container
        ])
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_tabla_clientes():
        """
        Crea tabla de clientes con:
        - Filtro por nombre con AutoComplete
        - Edición completa de datos incluyendo fecha
        - Actualización en tiempo real
        """
        # Variables globales
        clientes = get_clientes()
        nombre_seleccionado = None
        tabla_container = ft.Container()
        auto_complete = None
        auto_complete_container = None

        def editar_cliente(e, cliente_id):
            """Abre diálogo para editar cliente"""
            cliente = next(c for c in clientes if c[0] == cliente_id)
            
            nombre_edit = ft.TextField(label="Nombre", value=cliente[1])
            whatsapp_edit = ft.TextField(label="WhatsApp", value=cliente[3])
            fecha_edit = ft.TextField(
                label="Fecha inicio",
                value=cliente[2],
                read_only=True,
                icon=ft.Icons.CALENDAR_MONTH,
                on_click=lambda _: mostrar_datepicker_edit()
            )
            estado_edit = ft.Dropdown(
                label="Estado",
                options=[
                    ft.dropdown.Option("Activo"),
                    ft.dropdown.Option("Inactivo")
                ],
                value=cliente[4]
            )
            frecuencia_edit = ft.TextField(
                label="Frecuencia",
                value=str(cliente[5]),
                input_filter=ft.InputFilter(regex_string=r"[0-9]")
            )

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
                        estado_edit.value,
                        int(frecuencia_edit.value)
                    ):
                        dlg_modal.open = False
                        # Actualizar datos
                        nonlocal clientes
                        clientes = get_clientes()
                        actualizar_tabla(clientes)
                        actualizar_autocomplete()
                        
                        # Limpia y recrea el AutoComplete
                        limpiar_y_recrear_auto_complete(auto_complete_container, clientes)
                        
                        
                        mostrar_mensaje("Cliente actualizado")
                    else:
                        mostrar_mensaje("Error al actualizar")
                except Exception as ex:
                    mostrar_mensaje(f"Error: {str(ex)}")
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
                    estado_edit,
                    frecuencia_edit
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
            """Actualiza contenido de la tabla"""
            tabla_container.content = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("Inicio")),
                    ft.DataColumn(ft.Text("WhatsApp")),
                    ft.DataColumn(ft.Text("Estado")),
                    ft.DataColumn(ft.Text("Frecuencia")),
                    ft.DataColumn(ft.Text("Acciones"))
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(cliente[0]))),
                            ft.DataCell(ft.Text(cliente[1])),
                            ft.DataCell(ft.Text(cliente[2])),
                            ft.DataCell(ft.Text(cliente[3])),
                            ft.DataCell(ft.Text(cliente[4])),
                            ft.DataCell(ft.Text(f"{cliente[5]} días")),
                            ft.DataCell(
                                ft.IconButton(
                                    icon=ft.Icons.EDIT,
                                    data=cliente,
                                    on_click=lambda e, id=cliente[0]: 
                                        editar_cliente(e, id)
                                )
                            )
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
            auto_complete_container,
            tabla_container
        ])
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def get_estado_color(estado: str) -> str:
        """
        Retorna el color correspondiente al estado del pago.
        
        Args:
            estado (str): Estado del pago (En corte/Pendiente/Cerca/Al día)
        
        Returns:
            str: Color en formato flet para el estado
        """
        if estado == "En corte":
            return ft.Colors.RED_600
        elif estado == "Pendiente":
            return ft.Colors.ORANGE
        elif estado == "Cerca":
            return ft.Colors.YELLOW_700
        return ft.Colors.GREEN

    def mostrar_mensaje(mensaje: str):
        """
        Muestra un mensaje en SnackBar.
        
        Args:
            mensaje (str): Texto a mostrar
        """
        snack = ft.SnackBar(content=ft.Text(mensaje), duration=3000)
        page.overlay.append(snack)
        snack.open = True
        page.update()    

    
    
    def crear_tab_pagos():
        """
        Crea tab para aplicar pagos con AutoComplete y fecha.
        Permite seleccionar cliente, establecer fecha y registrar pago.
        """
        # Variables de estado
        info_container = ft.Container()
        cliente_seleccionado = None
        clientes = get_clientes()
        txt_fecha_pago = ft.Ref[ft.TextField]()
        tabla_vencimientos = None  # Referencia a tabla_vencimientos

        def mostrar_datepicker_pago(e):
            """
            Muestra el DatePicker para seleccionar fecha de pago.
            
            Args:
                e: Evento del botón
            """
            date_picker = ft.DatePicker(
                first_date=datetime.datetime.now() - + datetime.timedelta(days=60),
                last_date=datetime.datetime.now() + datetime.timedelta(days=60),
                on_change=lambda e: seleccionar_fecha_pago(e),
            )
            page.overlay.append(date_picker)
            date_picker.open = True
            page.update()
            
        def seleccionar_fecha_pago(e):
            """
            Actualiza TextField con fecha seleccionada.
            
            Args:
                e: Evento del DatePicker
                txt_field: TextField a actualizar
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
            txt_fecha_pago.value = ""
            page.update()
            
            
        # Crear controles
        campo_fecha = ft.TextField(
            ref=txt_fecha_pago,
            label="Fecha de pago",
            width=320,
            read_only=True,
            icon=ft.Icons.CALENDAR_MONTH,
            on_click=mostrar_datepicker_pago
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
                        info_container.content = ft.Column([
                            ft.Text(f"Último pago: {cliente[3]}"),
                            ft.Text(f"Próximo pago: {cliente[4]}"),
                            ft.Text(f"Días transcurridos: {cliente[6]}"),
                            ft.Text(
                                f"Estado: {cliente[7]}", 
                                color=get_estado_color(cliente[7])
                            )
                        ])
                        page.update()
        
        def aplicar_pago(e):
            """Registra pago y limpia selección"""
            try:
                if not cliente_seleccionado:
                    raise ValueError("Seleccione un cliente")
                if not txt_fecha_pago.current.value:
                    raise ValueError("Seleccione fecha de pago")

                cliente_id = next(
                    (c[0] for c in clientes if c[1] == cliente_seleccionado), 
                    None
                )
                
                if insertar_pago(cliente_id, txt_fecha_pago.current.value):
                    mostrar_mensaje("Pago registrado correctamente")
                    limpiar_seleccion()
                    txt_fecha_pago.current.value = ""
                    
                    # Actualizar tabla de vencimientos
                    nonlocal tabla_vencimientos
                    tabla_vencimientos = crear_tabla_vencimientos()
                    mainTab.tabs[0].content = tabla_vencimientos
                    page.update()
                else:
                    mostrar_mensaje("Error registrando pago")
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}")

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

        return ft.Tab(
            text="Aplicar Pagos",
            icon=ft.Icons.PAYMENT,
            content=ft.Column([
                ft.Text("Registrar Pago", size=20),
                auto_complete_container,
                campo_fecha,
                info_container,
                ft.ElevatedButton(
                    "Aplicar Pago",
                    on_click=aplicar_pago,
                    icon=ft.Icons.SAVE
                )
            ])
        )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,        
        # Contenedor de tabs
        tabs=[
            ft.Tab(
                icon=ft.Icons.HOME,
                text="Vencimientos",
                content=ft.Column([
                    ft.Text("Busqueda por nombre", size=20),
                    crear_tabla_vencimientos(),
                ])
            ),
            ft.Tab(
                icon=ft.Icons.LIST,
                text="Listado de clientes",
                content=ft.Column([
                    ft.Text("Clientes", size=20),
                    crear_tabla_clientes(),
                ])
            ),
            ft.Tab(
                icon=ft.Icons.PERSON_ADD,
                text="Agregar clientes",
                content=ft.Column(
                    [
                        ft.Text("Registrar clientes", size=20),
                        ft.Row([
                            ft.Text("Nombre:", width=100),
                            ft.TextField(width=320, ref=txt_nombre, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, capitalization=ft.TextCapitalization.WORDS),
                        ]),
                        ft.Row([
                            ft.Text("Fecha de inicio:", width=100),
                            ft.TextField(width=320, ref=txt_fecha_inicio, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, read_only=True, icon=ft.Icons.CALENDAR_MONTH, on_click=mostrar_datepicker_inicio),
                            
                        ]),
                        ft.Row([
                            ft.Text("Whatsapp:", width=100),
                            ft.TextField(width=320, ref=txt_whatsapp, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=10, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Estado:", width=100),
                            ft.Dropdown(
                            width=320,
                            ref=dd_estado,
                            value="Activo",
                            options=[
                                ft.dropdown.Option("Activo"),
                                ft.dropdown.Option("Inactivo"),
                            ],
                            border=ft.border.all(2, ft.Colors.BLACK),
                            border_radius=10,
                        ),
                        ]),
                        ft.Row([
                        ft.Text("Frecuencia de pago:", width=100),
                        ft.Dropdown(
                            width=320,
                            ref=txt_frecuencia,
                            value="30",
                            options=[
                                ft.dropdown.Option("1"),
                                ft.dropdown.Option("15"),
                                ft.dropdown.Option("30"),
                            ],
                            border=ft.border.all(2, ft.Colors.BLACK),
                            border_radius=10,
                        ),
                        ]),
                        ft.Row([
                        ft.Text(" ", width=100),
                        ft.ElevatedButton(text="Registrar", width=100, on_click=guardar_cliente),
                        ft.ElevatedButton(text="Empleados", width=100),
                        ft.ElevatedButton(text="Reportes", width=100),
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
            crear_tab_pagos(),
        ],
    )
    page.add(mainTab)
    
ft.app(main)