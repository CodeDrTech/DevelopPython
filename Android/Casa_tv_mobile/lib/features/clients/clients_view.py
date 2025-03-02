import flet as ft
import datetime
from core.database.consultas import get_clientes, eliminar_cliente_db, tiene_pagos, eliminar_pagos, insertar_cliente
from core.database.consultas import tiene_suscripciones, eliminar_suscripciones, actualizar_cliente
from core.utils.date_utils import convertir_formato_fecha

def create_clients_view(page: ft.Page):
    """
    Crea la vista de clientes adaptada para móvil.
    """
    # Variables globales
    clientes = get_clientes()
    
    # Contenedor principal para la lista de clientes
    clients_list = ft.ListView(
        expand=True,
        spacing=10,
        padding=10,
    )
    
    # Contador de clientes
    contador_clientes = ft.Text(
        f"Total: {len(clientes)}", 
        size=14,
        weight=ft.FontWeight.BOLD,
        color=ft.Colors.BLUE
    )
    
    # Barra de búsqueda
    search_box = ft.TextField(
        label="Buscar cliente",
        prefix_icon=ft.Icons.SEARCH,
        on_change=lambda e: filtrar_clientes(e.control.value),
        expand=True
    )
    
    def mostrar_mensaje(mensaje: str):
        """Muestra un mensaje en la parte inferior de la pantalla"""
        snack = ft.SnackBar(content=ft.Text(mensaje), duration=3000)
        page.overlay.append(snack)
        snack.open = True
        page.update()
    
    def filtrar_clientes(texto_busqueda):
        """Filtra la lista de clientes según el texto de búsqueda"""
        if not texto_busqueda:
            actualizar_lista_clientes(clientes)
            return
            
        texto_busqueda = texto_busqueda.lower()
        filtrados = [c for c in clientes if texto_busqueda in c[1].lower()]
        actualizar_lista_clientes(filtrados)
    
    def actualizar_lista_clientes(clientes_filtrados):
        """Actualiza la lista de clientes mostrada"""
        contador_clientes.value = f"Total: {len(clientes_filtrados)}"
        
        clients_list.controls.clear()
        
        for cliente in clientes_filtrados:
            # Crear tarjeta para cada cliente
            card = ft.Card(
                content=ft.Container(
                    padding=10,
                    content=ft.Column([
                        ft.Row([
                            ft.Text(cliente[1], size=16, weight="bold", expand=True),
                            ft.Container(
                                padding=5,
                                border_radius=5,
                                bgcolor=ft.Colors.GREEN if cliente[4] == "Activo" else ft.Colors.RED,
                                content=ft.Text(cliente[4], color=ft.Colors.WHITE, size=12)
                            )
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.CALENDAR_TODAY, size=16),
                            ft.Text(f"Inicio: {convertir_formato_fecha(cliente[2])}", size=14),
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.PHONE, size=16),
                            ft.Text(f"WhatsApp: {cliente[3]}", size=14),
                        ]),
                        ft.Row([
                            ft.Icon(ft.Icons.COMMENT, size=16),
                            ft.Text(f"Comentario: {cliente[6]}", size=14),
                        ]),
                        ft.Row([
                            ft.IconButton(
                                icon=ft.Icons.EDIT,
                                tooltip="Editar",
                                on_click=lambda e, id=cliente[0]: editar_cliente(e, id)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.DELETE,
                                tooltip="Eliminar",
                                icon_color="red",
                                on_click=lambda e, id=cliente[0]: eliminar_cliente(e, id)
                            ),
                            ft.IconButton(
                                icon=ft.Icons.PHONE,
                                tooltip="WhatsApp",
                                icon_color="green",
                                on_click=lambda e, tel=cliente[3]: page.launch_url(f"https://wa.me/52{tel}")
                            ),
                        ], alignment=ft.MainAxisAlignment.END)
                    ])
                )
            )
            clients_list.controls.append(card)
        
        page.update()
    
    def eliminar_cliente(e, cliente_id):
        """Elimina un cliente después de verificar y eliminar sus pagos y suscripciones."""
        cliente = next(c for c in clientes if c[0] == cliente_id)
        
        def confirmar_eliminacion(e):
            try:
                # Verificar y eliminar pagos
                if tiene_pagos(cliente_id):
                    eliminar_pagos(cliente_id)
                
                # Verificar y eliminar suscripciones
                if tiene_suscripciones(cliente_id):
                    eliminar_suscripciones(cliente_id)
                
                # Eliminar el cliente
                if eliminar_cliente_db(cliente_id):
                    mostrar_mensaje("Cliente eliminado correctamente")
                    
                    # Actualizar la lista de clientes
                    nonlocal clientes
                    clientes = get_clientes()
                    actualizar_lista_clientes(clientes)
                    
                    page.update()
                else:
                    mostrar_mensaje("Error al eliminar cliente")
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}")
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
    
    def nuevo_cliente(e):
        """Abre diálogo para crear nuevo cliente"""
        nombre_edit = ft.TextField(label="Nombre", capitalization=ft.TextCapitalization.WORDS)
        whatsapp_edit = ft.TextField(
            label="WhatsApp", 
            max_length=10, 
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        fecha_edit = ft.TextField(
            label="Fecha inicio",
            value=datetime.date.today().strftime("%Y-%m-%d"),
            read_only=True,
            on_click=lambda _: mostrar_datepicker_nuevo()
        )
        condicion_edit = ft.Dropdown(
            label="Condición",
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
                    clientes = get_clientes()
                    actualizar_lista_clientes(clientes)
                    
                    page.update()
                    mostrar_mensaje("Cliente creado")
                else:
                    mostrar_mensaje("Error al crear")
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}")
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
            ], scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                ft.TextButton("Guardar", on_click=guardar_nuevo)
            ]
        )
        
        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()
    
    def editar_cliente(e, cliente_id):
        """Abre diálogo para editar cliente"""
        cliente = next(c for c in clientes if c[0] == cliente_id)
        
        nombre_edit = ft.TextField(label="Nombre", value=cliente[1])
        whatsapp_edit = ft.TextField(
            label="WhatsApp", 
            value=cliente[3], 
            max_length=10, 
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
        )
        fecha_edit = ft.TextField(
            label="Fecha inicio",
            value=cliente[2],
            read_only=True,
            on_click=lambda _: mostrar_datepicker_edit()
        )
        condicion_edit = ft.Dropdown(
            label="Condición",
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

        def seleccionar_fecha_edit(e):
            if e.control.value:
                fecha = e.control.value.date()
                fecha_edit.value = fecha.strftime("%Y-%m-%d")
                e.control.open = False
                page.update()
        
        def mostrar_datepicker_edit():
            date_picker = ft.DatePicker(
                first_date=datetime.datetime.now() - datetime.timedelta(days=30),
                last_date=datetime.datetime.now() + datetime.timedelta(days=365),
                on_change=seleccionar_fecha_edit
            )
            page.overlay.append(date_picker)
            date_picker.open = True
            page.update()

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
                    clientes = get_clientes()
                    actualizar_lista_clientes(clientes)
                    
                    page.update()
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
                condicion_edit,
                frecuencia_edit,
                comentario_edit
            ], scroll=ft.ScrollMode.AUTO),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                ft.TextButton("Guardar", on_click=guardar_cambios)
            ]
        )
        
        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()
    
    # Inicializar la lista de clientes
    actualizar_lista_clientes(clientes)
    
    # Crear el contenido principal
    content = ft.Column([
        ft.Row([
            ft.Text("Clientes", size=20, weight="bold"),
            contador_clientes
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        ft.Row([
            search_box,
            ft.IconButton(
                icon=ft.Icons.ADD_CIRCLE,
                tooltip="Nuevo Cliente",
                on_click=nuevo_cliente
            )
        ]),
        clients_list
    ], spacing=10)
    
    return ft.Container(
        content=content,
        padding=10,
        expand=True
    )