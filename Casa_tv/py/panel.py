import flet as ft
from flet import ScrollMode, AppView
from consultas import get_clientes, actualizar_cliente, get_estado_pagos, insertar_pago, get_estado_pago_cliente,\
insertar_cliente, obtener_todos_los_clientes, obtener_clientes_por_estado, obtener_credenciales, actualizar_credenciales,\
obtener_numeros_whatsapp

import datetime
import time
import pywhatkit
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


def mostrar_mensaje_whatsapp(mensaje: str, page: ft.Page):
    """
    Muestra un mensaje en SnackBar.

    Args:
        mensaje (str): Texto a mostrar.
        page (ft.Page): Página de la aplicación.
    """
    snack = ft.SnackBar(content=ft.Text(mensaje), duration=5000)
    page.overlay.append(snack)
    snack.open = True
    page.update()

def enviar_mensajes(numeros, mensaje, page, intervalo=10):
    """
    Envía mensajes de WhatsApp a una lista de números.

    Args:
        numeros (list): Lista de números de WhatsApp.
        mensaje (str): Mensaje a enviar.
        page (ft.Page): Página de la aplicación.
        intervalo (int): Tiempo en segundos entre mensajes (por defecto, 10 segundos).
    """
    if not mensaje.strip():
        mostrar_mensaje_whatsapp("El mensaje no puede estar vacío.", page)
        return
    
    if not numeros:
        mostrar_mensaje_whatsapp("No se encontraron números para enviar mensajes.", page)
        return

    for numero in numeros:
        try:
            pywhatkit.sendwhatmsg_instantly(f"+{numero}", mensaje)
            mostrar_mensaje_whatsapp(f"Mensaje enviado a {numero}.", page)
            time.sleep(intervalo)  # Esperar antes de enviar el siguiente mensaje
        except Exception as e:
            mostrar_mensaje_whatsapp(f"Error enviando mensaje a {numero}: {e}", page)

def main(page: ft.Page):
    page.title = "TV en casa  Ver.20250109"
    page.window.alignment = ft.alignment.center
    page.window.width = 1300
    page.window.height = 800
    page.window.resizable = False
    page.padding = 20
    page.scroll = "adaptive" # type: ignore
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
    
#------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------
    def enviar_click(e):
        mensaje = mensaje_textbox.value
        numeros = obtener_numeros_whatsapp()
        enviar_mensajes(numeros, mensaje, page)

    mensaje_textbox = ft.TextField(
        width=320,
        multiline=True,
        border=ft.border.all(2, ft.Colors.BLACK),
        border_radius=10,
        max_length=200,
        capitalization=ft.TextCapitalization.SENTENCES,
    )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def convertir_formato_fecha(fecha_str):
        """
        Convierte una fecha de formato 'YYYY-MM-DD' a 'DD-mes-YYYY'.

        Args:
            fecha_str (str): Fecha en formato 'YYYY-MM-DD'.

        Returns:
            str: Fecha en formato 'DD-mes-YYYY' con el mes en abreviatura de tres letras en español.
                    Si la fecha no es válida, se devuelve el string original.
        """
        """Convierte fecha de YYYY-MM-DD a DD-mes-YYYY"""
        try:
            fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
            meses = {
                1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR',
                5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AGO',
                9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DIC'
            }
            return f"{fecha.day}-{meses[fecha.month]}-{fecha.year}"
        except ValueError:
            return fecha_str
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def abrir_dialogo_credenciales(e):
        """Abre un diálogo para editar las credenciales de correo."""
        credenciales = obtener_credenciales()
        sender_email_edit = ft.TextField(label="Correo Emisor", value=credenciales[0])
        sender_password_edit = ft.TextField(label="Contraseña", value=credenciales[1], password=True)
        receiver_email_edit = ft.TextField(label="Correo Receptor", value=credenciales[2])

        def guardar_cambios_credenciales(e):
            """Guarda los cambios en las credenciales."""
            actualizar_credenciales(
                sender_email_edit.value,
                sender_password_edit.value,
                receiver_email_edit.value
            )
            dlg_modal.open = False
            page.update()
            mostrar_mensaje("Credenciales actualizadas con éxito")

        def cerrar_dialogo(e):
            """Cierra el diálogo sin guardar cambios."""
            dlg_modal.open = False
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Actualizar Credenciales"),
            content=ft.Column([
                sender_email_edit,
                sender_password_edit,
                receiver_email_edit
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=cerrar_dialogo),
                ft.TextButton("Guardar", on_click=guardar_cambios_credenciales)
            ]
        )
        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def envio_estados():        
        """
        Función principal del panel de TV en casa.
        
        Genera el contenido principal de la aplicación, que incluye un dropdown con los estados de los clientes,
        un botón para enviar un correo electrónico con la lista de clientes filtrados por el estado actualmente seleccionado
        y una tabla que muestra la información de los clientes.
        
        Parameters
        ----------
        page: ft.Page
            Página principal de la aplicación.
        
        Returns
        -------
        ft.Column
            Contenedor que contiene todos los elementos de la interfaz de usuario.
        """
        
        def get_estado_color_css(estado: str) -> str:
                """
                Retorna el color correspondiente al estado del pago en formato CSS.
                
                Args:
                    estado (str): Estado del pago (En corte/Pendiente/Cerca/Al día)
                
                Returns:
                    str: Color en formato CSS (hexadecimal) para el estado.
                """
                estado_colores = {
                    "En corte": "#FF0000",     # Rojo
                    "Pendiente": "#FF8C00",   # Naranja oscuro
                    "Cerca": "#007FFF",       # Azul
                    "Al día": "#008000"       # Verde
                }
                return estado_colores.get(estado, "#000000")  # Negro como predeterminado

        def mostrar_mensaje_correo(mensaje: str):
            """
            Muestra un mensaje en SnackBar..
            
            Args:
                mensaje (str): Texto a mostrar
            """
            snack = ft.SnackBar(content=ft.Text(mensaje), duration=5000)
            page.overlay.append(snack)
            snack.open = True
            page.update()
            
        def actualizar_estados(e=None):
            """
            Actualiza la tabla de clientes según el estado actualmente seleccionado en el dropdown.
            
            Parameters
            ----------
            e: Optional[Event]
                Evento que lo desencadena. No se utiliza en este caso.
            
            Notes
            -----
            La función utiliza el valor actual del dropdown para determinar qué clientes mostrar.
            Si el valor es "Todos", se muestran todos los clientes.
            Si el valor es distinto de "Todos", se muestran solo los clientes con ese estado.
            La función utiliza la función obtener_clientes_por_estado para obtener la lista de clientes.
            La función utiliza la función obtener_todos_los_clientes para obtener la lista de todos los clientes.
            La función crea una tabla con las columnas "Nombre", "WhatsApp", "Último Pago", "Próximo Pago" y "Estado".
            La función llena la tabla con los clientes correspondientes al estado seleccionado.
            La función actualiza la página para que los cambios sean visibles.
            """
            estado_seleccionado = dropdown.value
            if estado_seleccionado == "Todos":
                clientes = obtener_todos_los_clientes()
            else:
                clientes = obtener_clientes_por_estado(estado_seleccionado)
            
            tabla_container.content = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("WhatsApp")),
                    ft.DataColumn(ft.Text("Último Pago")),
                    ft.DataColumn(ft.Text("Próximo Pago")),
                    ft.DataColumn(ft.Text("Estado")),
                    ft.DataColumn(ft.Text("Monto")),
                    ft.DataColumn(ft.Text("Correo")),
                    ft.DataColumn(ft.Text("Comentario")),
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(cliente[0])),
                            ft.DataCell(ft.Text(cliente[1])),
                            ft.DataCell(ft.Text(convertir_formato_fecha(cliente[5]))),
                            ft.DataCell(ft.Text(convertir_formato_fecha(cliente[6]))),
                            ft.DataCell(ft.Text(cliente[7])),
                            ft.DataCell(ft.Text(f"${cliente[2]}")),
                            ft.DataCell(ft.Text(cliente[3])),
                            ft.DataCell(ft.Text(cliente[4])),
                        ]
                    ) for cliente in clientes
                ],
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400)
            )
            page.update()

        def enviar_correo(e):
            """
            Envia un correo electrónico con la lista de clientes filtrados por el estado actualmente seleccionado.
            
            Parameters
            ----------
            e: Event
                No se utiliza en esta función, se incluye solo para mantener la consistencia con las funciones de los botones.
            
            """
            credenciales = obtener_credenciales()
            sender_email = credenciales[0]
            sender_password = credenciales[1]
            receiver_email = credenciales[2]
            
            
            #mostrar_mensaje_correo("Enviando correo...")  # Mostrar mensaje de envío
            estado_seleccionado = dropdown.value  # Obtener el estado seleccionado en el momento del envío
            if estado_seleccionado == "Todos":
                clientes = obtener_todos_los_clientes()
            else:
                clientes = obtener_clientes_por_estado(estado_seleccionado)
            
            
            asunto = 'Estados de clientes'
            
            # Formatear los datos para el correo
            body = "Lista de clientes:<br><br>"
            for cliente in clientes:
                primer_nombre = cliente[0].split()[0]
                numero_limpio = ''.join(filter(str.isdigit, cliente[1]))
                enlace_whatsapp = f"https://wa.me/1{numero_limpio}?text=Hola.%20Mensaje%20de%20alerta%20de%20pago."
                body += (
                        f"<b>Nombre: {cliente[0]}</b><br>"                        
                        f"Correo: {cliente[3]}<br>"
                        f"WhatsApp: <a href='{enlace_whatsapp}'>{cliente[1]}</a><br>"
                        f"Último pago: {convertir_formato_fecha(cliente[5])}<br>"
                        f"Próximo pago: {convertir_formato_fecha(cliente[6])}<br>"
                        f"Monto: ${cliente[2]}<br>"
                        f"Estado: <span style='color: {get_estado_color_css(cliente[7])}'>{cliente[7]}</span><br>"
                        f"Comentario: {cliente[4]}<br><br>"                        
                    )

            message = MIMEMultipart()
            message['From'] = sender_email
            message['To'] = receiver_email
            message['Subject'] = asunto
            message.attach(MIMEText(body, 'html'))  # Especificamos 'html' para que los enlaces funcionen

            try:
                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, sender_password)
                text = message.as_string()
                server.sendmail(sender_email, receiver_email, text)
                server.quit()
                mostrar_mensaje_correo("Correo enviado con éxito")
            except Exception as ex:
                mostrar_mensaje_correo("Error al enviar el correo:", ex)

        estados = ['Todos', 'En corte', 'Pago pendiente', 'Cerca', 'Al día']
        
        dropdown = ft.Dropdown(
            value="Todos",
            options=[ft.dropdown.Option(text=estado) for estado in estados],
            on_change=actualizar_estados,
            width=200
        )

        columns = [
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("WhatsApp")),
            ft.DataColumn(ft.Text("Último Pago")),
            ft.DataColumn(ft.Text("Próximo Pago")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Monto")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Comentario")),
        ]

        tabla_container = ft.Container(
            content=ft.DataTable(
                columns=columns,  
                rows=[]
            )
        )

        # Botón para enviar correo
        enviar_correo_button = ft.ElevatedButton("Enviar correo estado", icon=ft.Icons.EMAIL, on_click=enviar_correo)
        
        # Botón para actializar los datos de las credenciales de correo para enviar el correo
        btn_actualizar_credenciales = ft.ElevatedButton("Actualizar credenciales", icon=ft.Icons.UPDATE, on_click=abrir_dialogo_credenciales)

        content = ft.Column([
            ft.Row(
                [
                dropdown,
                enviar_correo_button,
                btn_actualizar_credenciales,
                ]),              
            tabla_container
        ])
        
        actualizar_estados()  # Mostrar los datos de "Todos" al cargar
        return content
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Referencias para controles
    txt_nombre = ft.Ref[ft.TextField]()
    txt_whatsapp = ft.Ref[ft.TextField]()
    txt_fecha_inicio = ft.Ref[ft.TextField]()
    dd_estado = ft.Ref[ft.Dropdown]()
    txt_frecuencia = ft.Ref[ft.TextField]()
    txt_monto = ft.Ref[ft.TextField]()
    txt_correo = ft.Ref[ft.TextField]()
    txt_comentario = ft.Ref[ft.TextField]()    
    
    tabla_vencimientos = None  # Referencia a tabla_vencimientos
    clientes = None  # Referencia a clientes
    
    def mostrar_datepicker_inicio(e):
        """Muestra DatePicker para fecha inicio"""
        date_picker = ft.DatePicker(
            first_date=datetime.datetime.now() - datetime.timedelta(days=365),
            last_date=datetime.datetime.now() + datetime.timedelta(days=365),
            on_change=lambda e: seleccionar_fecha_inicio(e),            
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
        txt_monto.current.value = ""
        txt_correo.current.value = ""
        txt_comentario.current.value = ""
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
                txt_frecuencia.current.value,
                txt_monto.current.value,
                txt_correo.current.value
            ]):
                raise ValueError("Algunos campos son requeridos")

            # Insertar cliente
            if insertar_cliente(
                txt_nombre.current.value,
                txt_whatsapp.current.value,
                txt_fecha_inicio.current.value,
                dd_estado.current.value,
                int(txt_frecuencia.current.value),
                int(txt_monto.current.value),
                txt_correo.current.value,
                txt_comentario.current.value
            ):
                mostrar_mensaje("Cliente guardado correctamente")
                limpiar_campos()
                
                # Actualizar tabla de vencimientos
                nonlocal tabla_vencimientos
                tabla_vencimientos = crear_tabla_vencimientos()
                mainTab.tabs[0].content = tabla_vencimientos                
                
                # Actualizar datos
                nonlocal clientes
                clientes = crear_tabla_clientes()
                mainTab.tabs[1].content = clientes
                page.update()
                
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
        Crea tabla de vencimientos con filtros combinados:
        - AutoComplete para filtrar por nombre
        - Dropdown para filtrar por estado (En corte/Pendiente/Cerca/Todos)
        """
        
        
        
        # Variables globales
        registros = get_estado_pagos()
        nombre_seleccionado = None
        estado_seleccionado = "Todos"
        tabla_container = ft.Container()
        
        # Suma de los montos
        total_montos = sum(reg[8] for reg in registros)
        total_montos_format = "{:,}".format(total_montos)
                
        def filtrar_registros():
            """
            Aplica filtros combinados y actualiza tabla.
            Recarga datos frescos de la BD antes de filtrar.
            """
            # Recargar datos frescos
            nonlocal registros
            registros = get_estado_pagos()
            filtrados = registros

            # Filtrar por nombre si hay selección
            if nombre_seleccionado:
                filtrados = [
                    reg for reg in filtrados 
                    if reg[1].lower() == nombre_seleccionado.lower()
                ]
            
            # Filtrar por estado si no es "Todos"
            if estado_seleccionado != "Todos":
                filtrados = [
                    reg for reg in filtrados 
                    if reg[7] == estado_seleccionado
                ]
            
            
            
            # Actualizar tabla con resultados
            actualizar_tabla(filtrados)
            page.update()

        # Botón refresh
        btn_refresh = ft.IconButton(
            icon=ft.Icons.REFRESH,
            tooltip="Actualizar tabla",
            on_click=lambda _: filtrar_registros()
        )
        
        def on_estado_change(e):
            """Maneja cambio en dropdown de estado"""
            nonlocal estado_seleccionado
            estado_seleccionado = e.control.value
            filtrar_registros()
        
        def on_autocomplete_selected(e):
            """Maneja selección en AutoComplete."""
            nonlocal nombre_seleccionado
            nombre_seleccionado = e.selection.value
            filtrar_registros()        
            
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
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Monto")),
            ft.DataColumn(ft.Text("Correo")),
            ft.DataColumn(ft.Text("Comentario"))
        ]
        
        def get_estado_color(estado):
            """Define color según estado de pago"""
            if estado == "En corte":
                return ft.Colors.RED
            elif estado == "Pago pendiente":
                return ft.Colors.ORANGE_700
            elif estado == "Cerca":
                return ft.Colors.BLUE_700
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
                    ft.DataColumn(ft.Text("Estado")),
                    ft.DataColumn(ft.Text("Monto")),
                    ft.DataColumn(ft.Text("Correo")),
                    ft.DataColumn(ft.Text("Comentario"))
                ],
                rows=[
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(reg[0]))),
                            ft.DataCell(ft.Text(reg[1])),
                            ft.DataCell(ft.Text(convertir_formato_fecha(reg[2]))),
                            ft.DataCell(ft.Text(convertir_formato_fecha(reg[3]))),
                            ft.DataCell(ft.Text(convertir_formato_fecha(reg[4]))),
                            ft.DataCell(ft.Text(f"{reg[5]} días")),
                            ft.DataCell(ft.Text(str(reg[6]))),
                            ft.DataCell(ft.Text(
                                reg[7],
                                color=get_estado_color(reg[7])
                            )),
                            ft.DataCell(ft.Text(str(f"${reg[8]}"))),
                            ft.DataCell(ft.Text(reg[9])),
                            ft.DataCell(ft.Text(reg[10]))
                        ],
                    ) for reg in registros_filtrados
                ],
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=10,
                vertical_lines=ft.border.BorderSide(1, ft.Colors.GREY_400),
                horizontal_lines=ft.border.BorderSide(1, ft.Colors.GREY_400)
            )
            page.update()

        # Crear Dropdown estados
        dropdown_estado = ft.Dropdown(
            width=200,
            label="Filtrar por estado",
            options=[
                ft.dropdown.Option("Todos"),
                ft.dropdown.Option("Al día"),
                ft.dropdown.Option("En corte"),
                ft.dropdown.Option("Pago pendiente"),
                ft.dropdown.Option("Cerca")
            ],
            value="Todos",
            on_change=on_estado_change
        )
        
        
        # Crear AutoComplete
        nombres = sorted(set(reg[1] for reg in registros))
        auto_complete = ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key=nombre, value=nombre) 
                for nombre in nombres
            ],
            on_select=on_autocomplete_selected,
            
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
            ft.Row([
                auto_complete_container,
                dropdown_estado,
                btn_refresh,
            ft.Row([ft.Text(f"Monto total: ${total_montos_format}", size=20, color=ft.Colors.GREEN)]),
            ]),            
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
            monto_edit = ft.TextField(label="Monto", value=str(cliente[6]))
            correo_edit = ft.TextField(label="Correo", multiline=True, value=cliente[7])
            comentario_edit = ft.TextField(label="Comentario", multiline=True, value=cliente[8])

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
                        condicion_edit.value,
                        int(frecuencia_edit.value),
                        int(monto_edit.value),
                        correo_edit.value,
                        comentario_edit.value
                    ):
                        dlg_modal.open = False
                        
                        # Actualizar datos
                        nonlocal clientes
                        clientes = get_clientes()
                        actualizar_tabla(clientes)
                        actualizar_autocomplete()
                        
                        # Limpia y recrea el AutoComplete
                        limpiar_y_recrear_auto_complete(auto_complete_container, clientes)
                        
                        # Actualizar tabla de vencimientos
                        nonlocal tabla_vencimientos
                        tabla_vencimientos = crear_tabla_vencimientos()
                        mainTab.tabs[0].content = tabla_vencimientos
                        
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
                    monto_edit,
                    correo_edit,
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
            tabla_container.content = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nombre")),
                    ft.DataColumn(ft.Text("Inicio")),
                    ft.DataColumn(ft.Text("WhatsApp")),
                    ft.DataColumn(ft.Text("Condicion")),
                    ft.DataColumn(ft.Text("Frecuencia")),
                    ft.DataColumn(ft.Text("Monto")),
                    ft.DataColumn(ft.Text("Correo")),
                    ft.DataColumn(ft.Text("Comentario")),
                    ft.DataColumn(ft.Text("Acciones"))
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
                            ft.DataCell(ft.Text(str(f"${cliente[6]}"))),
                            ft.DataCell(ft.Text(cliente[7])),
                            ft.DataCell(ft.Text(cliente[8])),
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
            return ft.Colors.RED
        elif estado == "Pendiente":
            return ft.Colors.ORANGE_700
        elif estado == "Cerca":
            return ft.Colors.BLUE_700
        return ft.Colors.GREEN

    def mostrar_mensaje(mensaje: str):
        """
        Muestra un mensaje en SnackBar..
        
        Args:
            mensaje (str): Texto a mostrar
        """
        snack = ft.SnackBar(content=ft.Text(mensaje), duration=5000)
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
        
        def limpiar_y_recrear_auto_complete_pago(auto_complete_container, clientes):
            """
            Limpia y recrea el AutoComplete después de aplicar un pago.
            
            Args:
                auto_complete_container: Contenedor del AutoComplete
                clientes: Lista actualizada de clientes
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
            
            Args:
                e: Evento del botón
            """
            date_picker = ft.DatePicker(
                first_date=datetime.datetime.now() - + datetime.timedelta(days=365),
                last_date=datetime.datetime.now() + datetime.timedelta(days=365),
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
                            ft.Text(f"Último pago: {convertir_formato_fecha(cliente[9])}"),
                            ft.Text(f"Próximo pago: {convertir_formato_fecha(cliente[10])}"),
                            ft.Text(f"Días transcurridos: {cliente[11]}"),
                            ft.Text(
                                f"Estado: {cliente[12]}", 
                                color=get_estado_color(cliente[12])
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
                    limpiar_y_recrear_auto_complete_pago(auto_complete_container, get_clientes())
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
                ]),
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
                            ft.Text("Condicion:", width=100),
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
                            ft.Text("Monto:", width=100),
                            ft.TextField(width=320, ref=txt_monto, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=4, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Correo:", width=100),
                            ft.TextField(width=320, ref=txt_correo, multiline=True, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10),
                        ]),
                        ft.Row([
                            ft.Text("Comentario:", width=100),
                            ft.TextField(width=320, ref=txt_comentario, multiline=True, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=100, capitalization=ft.TextCapitalization.WORDS),
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
            ft.Tab(
                icon=ft.Icons.MAIL,
                text="Envio de estados",
                content=ft.Column([
                    ft.Text("Envio de estados", size=20),
                    envio_estados(),                    
                ])
            ),
            #ft.Tab(
            #    icon=ft.Icons.MESSAGE,
            #    text="Whatsapp",
            #    content=ft.Column([
            #        ft.Text("Envio de mensajes por whatsapp", size=20),
            #        ft.Row([
            #                ft.Text("Mensaje:", width=100),
            #                mensaje_textbox,
            #            ]),
            #        ft.ElevatedButton(text="Enviar", width=100, on_click=enviar_click),
            #    ])
            #),
        ],
    )
    page.add(mainTab)
    
ft.app(main)