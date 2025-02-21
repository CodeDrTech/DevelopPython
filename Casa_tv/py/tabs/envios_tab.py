import flet as ft
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib
from utils import (
    convertir_formato_fecha,
    mostrar_mensaje,
    get_estado_color
)
from consultas import (
    obtener_todos_los_clientes,
    obtener_clientes_por_estado,
    obtener_credenciales,
    actualizar_credenciales
)



def envio_estados(page: ft.Page, mainTab: ft.Tabs):        
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
                mostrar_mensaje("Credenciales actualizadas con éxito", page)

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
        
        def get_estado_color_css(estado: str) -> str:
                """
                Retorna el color correspondiente al estado del pago en formato CSS.
                
                Args:
                    estado (str): Estado del pago (En corte/Pendiente/Cerca/Al día)
                
                Returns:
                    str: Color en formato CSS (hexadecimal) para el estado.
                """
                estado_colores = {
                    "En corte": "#FF0000",    # Rojo
                    "Pendiente": "#FF8C00",   # Naranja oscuro
                    "Cerca": "#007FFF",       # Azul
                    "Al día": "#008000"       # Verde
                }
                return estado_colores.get(estado, "#000000")  # Negro como predeterminado

        def mostrar_mensaje_correo(mensaje: str, page: ft.Page = None):
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
                    ft.DataColumn(ft.Text("Pago mens.")),
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
                enlace_whatsapp = f"https://wa.me/1{numero_limpio}?text=Hola.%20Bendiciones%0A%0AEl%20pago%20de%20su%20cuota%20es%0Aen%20fecha%20{convertir_formato_fecha(cliente[6])}.%0A%0AFavor%20pagar%20dentro%20de%203%0Adias%20para%20evitar%20corte.%0A%0AGracias."

                
                # Convertir cliente[8] (deuda pendiente) y cliente[2] (pago mensual) a enteros,
                # usando 0 si son None.
                deuda_pendiente = int(cliente[8]) if cliente[8] is not None else 0
                pago_mensual = int(cliente[2]) if cliente[2] is not None else 0
                deuda_total = pago_mensual + deuda_pendiente

                body += (
                    f"<b>Nombre: {cliente[0]}</b><br>"                        
                    f"Correo: {cliente[3]}<br>"
                    f"WhatsApp: <a href='{enlace_whatsapp}'>{cliente[1]}</a><br>"
                    f"Último pago: {convertir_formato_fecha(cliente[5])}<br>"
                    f"Próximo pago: {convertir_formato_fecha(cliente[6])}<br>"
                    f"Deuda pendiente: ${deuda_pendiente}<br>"
                    f"Pago mensual: ${pago_mensual}<br>"
                    f"Deuda total: ${deuda_total}<br>"
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
                mostrar_mensaje_correo("Correo enviado con éxito", page)
            except Exception as ex:
                mostrar_mensaje_correo(f"Error al enviar el correo: {str(ex)}", page)

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
            ft.DataColumn(ft.Text("Pago mens.")),
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
        enviar_correo_button = ft.ElevatedButton("Enviar correo", icon=ft.Icons.EMAIL, on_click=enviar_correo)
        
        # Botón para actializar los datos de las credenciales de correo para enviar el correo
        btn_actualizar_credenciales = ft.ElevatedButton("Actualizar credenciales", icon=ft.Icons.UPDATE, on_click=abrir_dialogo_credenciales)

        content = ft.Column([
            ft.Text("Envio de estados por correo", size=20, weight="bold"),
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