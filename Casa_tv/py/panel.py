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
        Crea tabla de vencimientos de pagos con estado y días transcurridos.
        
        Returns:
            ft.DataTable: Tabla con columnas:
                - ID Cliente
                - Nombre
                - Fecha Inicio
                - Base (último pago)
                - Próximo Pago
                - Frecuencia
                - Días Transcurridos
                - Estado
        """
        registros = get_estado_pagos()
        
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
        
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(reg[0]))),      # ID
                    ft.DataCell(ft.Text(reg[1])),           # Nombre
                    ft.DataCell(ft.Text(reg[2])),           # Fecha inicio
                    ft.DataCell(ft.Text(reg[3])),           # Fecha base
                    ft.DataCell(ft.Text(reg[4])),           # Próximo pago
                    ft.DataCell(ft.Text(f"{reg[5]} días")), # Frecuencia
                    ft.DataCell(ft.Text(str(reg[6]))),      # Días transcurridos
                    ft.DataCell(ft.Text(                    # Estado
                        reg[7],
                        color=get_estado_color(reg[7])
                    )),
                ],
            ) for reg in registros
        ]
        
        return ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
        )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def crear_tabla_clientes():
        """
        Crea una tabla DataTable con los clientes y botones de edición.
        Permite editar los datos de cada cliente mediante un diálogo modal.
        """
        def editar_cliente(e, cliente_id):
            """Abre diálogo modal para editar cliente"""
            dlg_modal.client_id = cliente_id
            nombre_edit.value = e.control.data["nombre"]
            whatsapp_edit.value = e.control.data["whatsapp"]
            estado_edit.value = e.control.data["estado"]
            frecuencia_edit.value = str(e.control.data["frecuencia"])
            dlg_modal.open = True
            page.update()

        def mostrar_mensaje(mensaje: str):
            """
            Muestra mensaje en SnackBar usando nueva API.
            
            Args:
                mensaje (str): Texto a mostrar
            """
            snack = ft.SnackBar(content=ft.Text(mensaje))
            page.overlay.append(snack)
            page.open = snack # type: ignore

        def guardar_cambios(e):
            """Guarda cambios y actualiza tabla"""
            try:
                if actualizar_cliente(
                    dlg_modal.client_id,
                    nombre_edit.value,
                    whatsapp_edit.value,
                    estado_edit.value,
                    int(frecuencia_edit.value)
                ):
                    dlg_modal.open = False
                    actualizar_tabla()
                    mostrar_mensaje("Cliente actualizado")
                else:
                    mostrar_mensaje("Error al actualizar cliente")
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}")
            page.update()

        clientes = get_clientes()
        
        columns = [
            ft.DataColumn(ft.Text("Numero cliente")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Inicio")),
            ft.DataColumn(ft.Text("WhatsApp")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Frecuencia")),
            ft.DataColumn(ft.Text("Acciones"))
        ]
        
        rows = [
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
                            data={
                                "nombre": cliente[1],
                                "whatsapp": cliente[3],
                                "estado": cliente[4],
                                "frecuencia": cliente[5]
                            },
                            on_click=lambda e, id=cliente[0]: editar_cliente(e, id)
                        )
                    )
                ]
            ) for cliente in clientes
        ]

        # Campos del diálogo de edición
        nombre_edit = ft.TextField(label="Nombre", capitalization=ft.TextCapitalization.WORDS)
        whatsapp_edit = ft.TextField(label="WhatsApp", max_length=10, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string=""))
        estado_edit = ft.Dropdown(
            label="Estado",
            options=[
                ft.dropdown.Option("Activo"),
                ft.dropdown.Option("Inactivo")
            ]
        )
        frecuencia_edit = ft.TextField(
            label="Frecuencia (días)",
            input_filter=ft.InputFilter(regex_string=r"[0-9]"),
            max_length=2
        )
        
        def close_dlg(e):
            """Cierra el diálogo modal"""
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Cliente"),
            content=ft.Column([
                nombre_edit,
                whatsapp_edit,
                estado_edit,
                frecuencia_edit
            ], tight=True),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                ft.TextButton("Guardar", on_click=guardar_cambios)
            ]
        )

        # Agregar diálogo a overlay en lugar de page.dialog
        page.overlay.append(dlg_modal)
        
        return ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400)
        )

    def actualizar_tabla():
        """
        Actualiza el contenido de la tabla de clientes 
        después de modificar datos.
        """
        # Obtener tab de listado
        listado_tab = mainTab.tabs[1]
        # Obtener columna dentro del tab
        column = listado_tab.content
        # Actualizar tabla en segunda posición
        column.controls[1] = crear_tabla_clientes()
        page.update()
    # Contenedor principal de la tabla
    #tabla_container = ft.Container(content=crear_tabla_clientes(), expand=True)
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
        snack = ft.SnackBar(content=ft.Text(mensaje))
        page.overlay.append(snack)
        snack.open = True
        page.update()

    
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
    
    def crear_tab_pagos():
        """
        Crea tab para aplicar pagos individuales a clientes.
        Permite seleccionar cliente, fecha de pago y muestra información relevante.
        """
        # Contenedor para info del cliente
        info_container = ft.Container()
        
        def on_cliente_change(e):
            """Actualiza información cuando se selecciona un cliente"""
            cliente_id = e.control.value
            if cliente_id:
                cliente = get_estado_pago_cliente(int(cliente_id))
                if cliente:
                    info_container.content = ft.Column([
                        ft.Text(f"Último pago: {cliente[3]}"),
                        ft.Text(f"Próximo pago: {cliente[4]}"),
                        ft.Text(f"Días transcurridos: {cliente[6]}"),
                        ft.Text(f"Estado: {cliente[7]}", 
                            color=get_estado_color(cliente[7]))
                    ])
                    page.update()

        def aplicar_pago(e):
            """Registra el pago del cliente"""
            try:
                if not cliente_dropdown.value:
                    raise ValueError("Seleccione un cliente")
                if not txt_fecha_pago.current.value:
                    raise ValueError("Seleccione fecha de pago")

                if insertar_pago(
                    int(cliente_dropdown.value),
                    txt_fecha_pago.current.value
                ):
                    mostrar_mensaje("Pago registrado correctamente")
                    on_cliente_change(e)  # Actualizar info
                else:
                    mostrar_mensaje("Error registrando pago")
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}")

        # Obtener clientes para dropdown
        clientes = get_clientes()
        cliente_dropdown = ft.Dropdown(
            label="Seleccionar cliente",
            width=320,
            options=[
                ft.dropdown.Option(key=str(c[0]), text=c[1])
                for c in clientes
            ],
            on_change=on_cliente_change,
            border=ft.border.all(2, ft.Colors.BLACK),
            border_radius=10
        )

        fecha_pago = ft.TextField(
            ref=txt_fecha_pago,
            label="Fecha de pago",
            width=320,
            read_only=True,
            icon=ft.Icons.CALENDAR_MONTH,
            on_click = mostrar_datepicker_pago,
            border=ft.border.all(2, ft.Colors.BLACK),
            border_radius=10
        )

        return ft.Tab(
            text="Aplicar Pagos",
            icon=ft.Icons.PAYMENTS,
            content=ft.Column([
                ft.Text("Registrar Pago", size=20),
                cliente_dropdown,
                fecha_pago,
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
                    ft.Text("Listado de venvimientos", size=20),
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