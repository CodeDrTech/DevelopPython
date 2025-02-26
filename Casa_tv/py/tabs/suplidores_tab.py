import flet as ft
import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib

from utils import mostrar_mensaje, convertir_formato_fecha, get_estado_color_suplidores
from consultas import (
    get_pagos_suplidores, obtener_credenciales, insertar_pago_suplidor,
    actualizar_pago_suplidor, eliminar_pago_suplidor, get_estado_pagos_suplidores, get_correos_unicos
)
from tabs.vencimientos_tab import crear_tabla_vencimientos


def crear_tab_pagos_suplidores(page: ft.Page, mainTab: ft.Tabs):
    """Crea el tab para gestionar pagos a suplidores."""
    
    # Estados de pago disponibles
    ESTADOS_PAGO = ["Pendiente", "Pagado", "Cancelado"]
    
    def cerrar_dialogo(dlg):
        """Cierra un diálogo modal."""
        dlg.open = False
        page.update()
    
    def actualizar_vencimientos():
            """Updates the vencimientos tab content"""
            mainTab.tabs[0].content = crear_tabla_vencimientos(page)
            page.update()
            
    # Dropdown para filtrar por correo
    dropdown_correos = ft.Dropdown(
        label="Filtrar por correo",
        width=300,
        editable=True,
        enable_filter=True,
        enable_search=True,
        max_menu_height=200,
        options=[ft.dropdown.Option("Todos los correos")] + [
            ft.dropdown.Option(correo) for correo in get_correos_unicos()
        ],
        on_change=lambda e: filtrar_tabla(e.control.value)
    )
    
    dropdown_estados = ft.Dropdown(
        label="Filtrar por estado",
        width=300,
        options=[
            ft.dropdown.Option("Todos los estados"),
            ft.dropdown.Option("Pagado"),
            ft.dropdown.Option("Cerca"),
            ft.dropdown.Option("Pago pendiente")
        ]
    )
    
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
    def mostrar_dialogo_pago(e, pago):
        """Abre diálogo para registrar nuevo pago de suplidor"""
        
        txt_fecha = ft.TextField(
            label="Fecha de pago",
            value=datetime.datetime.now().strftime("%Y-%m-%d"),
            read_only=True,
            icon=ft.Icons.CALENDAR_MONTH
        )

        def mostrar_fecha(e):
            date_picker = ft.DatePicker(
                on_change=lambda e: cambiar_fecha(e, txt_fecha)
            )
            page.overlay.append(date_picker)
            date_picker.open = True
            page.update()

        def cambiar_fecha(e, txt_field):
            txt_field.value = e.control.value.date().strftime("%Y-%m-%d")
            page.update()

        txt_fecha.on_click = mostrar_fecha

        txt_comentarios = ft.TextField(
            label="Comentarios",
            multiline=True,
            min_lines=2,
            max_lines=3,
            width=400
        )

        def guardar_pago(e):
            try:
                if not txt_fecha.value:
                    raise ValueError("La fecha es obligatoria")
                
                if insertar_pago_suplidor(
                    cuenta_id=pago[0],  # ID de la cuenta
                    fecha_pago=txt_fecha.value,
                    comentarios=txt_comentarios.value
                ):
                    mostrar_mensaje("Pago registrado exitosamente", page)
                    dlg_modal.open = False
                    actualizar_vencimientos()
                    filtrar_tabla(dropdown_correos.value)  # Actualizar la tabla con el filtro actual
                else:
                    mostrar_mensaje("Error al registrar el pago", page)
            except ValueError as ex:
                mostrar_mensaje(str(ex), page)
            page.update()

        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text(f"Registrar Pago - {pago[1]}"),  # Nombre del servicio
            content=ft.Column([
                ft.Text(f"Servicio: {pago[1]}"),
                ft.Text(f"Correo: {pago[2]}"),
                ft.Text(f"Monto a pagar: ${pago[8]}"),  # Muestra el monto pero no es editable
                txt_fecha,
                txt_comentarios
            ], spacing=10),
            actions=[
                ft.TextButton("Cancelar", 
                            on_click=lambda e: setattr(dlg_modal, 'open', False) or page.update()),
                ft.TextButton("Guardar", on_click=guardar_pago)
            ]
        )

        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def mostrar_dialogo_editar(e, pago):
        """Muestra diálogo para editar un pago existente."""
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
            date_picker.open = True
            page.update()

        def cambiar_fecha(e, txt_field):
            if e.control.value:
                fecha = e.control.value.date()
                txt_field.value = fecha.strftime("%Y-%m-%d")
                page.update()

        txt_fecha.on_click = mostrar_fecha

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
                    actualizar_vencimientos()
                    filtrar_tabla(dropdown_correos.value)  # Actualizar la tabla con el filtro actual
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

        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def mostrar_dialogo_eliminar(e, pago):
        """Muestra diálogo de confirmación para eliminar un pago."""
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Confirmar eliminación"),
            content=ft.Text(
                f"¿Está seguro que desea eliminar el pago?\n"
                f"Servicio: {pago[1]}\n"
                f"Fecha: {convertir_formato_fecha(pago[3])}"
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dlg_modal)),
                ft.TextButton("Eliminar", on_click=lambda e: eliminar_y_cerrar(dlg_modal, pago[0]))
            ]
        )
        page.overlay.append(dlg_modal)
        dlg_modal.open = True
        page.update()

    def eliminar_y_cerrar(dlg, pago_id):
        """Elimina el pago y cierra el diálogo."""
        if eliminar_pago_suplidor(pago_id):
            mostrar_mensaje("Pago eliminado exitosamente", page)
            dlg.open = False
            actualizar_vencimientos()
            filtrar_tabla(dropdown_correos.value)  # Actualizar la tabla con el filtro actual
        else:
            mostrar_mensaje("Error al eliminar el pago", page)
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def enviar_correo_suplidores(pagos_filtrados, page):
        """Envía por correo la lista de pagos a suplidores."""
        credenciales = obtener_credenciales()
        sender_email = credenciales[0]
        sender_password = credenciales[1]
        receiver_email = credenciales[2]
        
        pagos_filtrados = [
            pago for pago in pagos_filtrados 
            if not (str(pago[9]) in ['1234', '0000'] and 
                    pago[9] is not None)
        ]
    
        if not pagos_filtrados:
            mostrar_mensaje("No hay pagos para mostrar después del filtrado", page)
            return
        
        asunto = 'Estado de Pagos a Suplidores'
        
        # Create table header
        body = """
        <html>
        <head>
            <style>
                table { border-collapse: collapse; width: 100%; }
                th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
                th { background-color: #f2f2f2; }
                .estado-pagado { color: green; }
                .estado-cerca { color: blue; }
                .estado-pendiente { color: orange; }
            </style>
        </head>
        <body>
            <h2>Lista de Pagos a Suplidores</h2>
            <table>
                <tr>
                    <th>Servicio</th>
                    <th>Correo</th>
                    <th>Último Pago</th>
                    <th>Próximo Pago</th>
                    <th>Cuota</th>
                    <th>Estado</th>
                    <th>Tarjeta</th>
                    <th>Comentarios</th>
                </tr>
        """
        
        # Add table rows
        for pago in pagos_filtrados:
            estado_class = f"estado-{pago[7].lower().replace(' ', '-')}"
            body += f"""
                <tr>
                    <td>{pago[1]}</td>
                    <td>{pago[2]}</td>
                    <td>{convertir_formato_fecha(pago[4])}</td>
                    <td>{convertir_formato_fecha(pago[5])}</td>
                    <td>${pago[8]:,.2f}</td>
                    <td class="{estado_class}">{pago[7]}</td>
                    <td>{'*'+str(pago[9]) if pago[9] else '-'}</td>
                    <td>{pago[10] or ''}</td>
                </tr>
            """
        
        # Close table and HTML
        body += """
            </table>
        </body>
        </html>
        """

        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = asunto
        message.attach(MIMEText(body, 'html'))

        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, sender_password)
            text = message.as_string()
            server.sendmail(sender_email, receiver_email, text)
            server.quit()
            mostrar_mensaje("Correo enviado con éxito", page)
        except Exception as ex:
            mostrar_mensaje(f"Error al enviar el correo: {str(ex)}", page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def filtrar_tabla(correo_seleccionado=None, estado_seleccionado=None):
        """Actualiza la tabla con los pagos filtrados por correo y estado."""
        pagos = get_estado_pagos_suplidores()
        rows = []
        
        for pago in pagos:
            # Skip if doesn't match correo filter
            if correo_seleccionado and correo_seleccionado != "Todos los correos" and pago[2] != correo_seleccionado:
                continue
                
            # Skip if doesn't match estado filter
            if estado_seleccionado and estado_seleccionado != "Todos los estados" and pago[7] != estado_seleccionado:
                continue

            # Create buttons and row as before...
            edit_button = ft.IconButton(
                icon=ft.icons.EDIT,
                tooltip="Editar",
                on_click=lambda e, p=pago: mostrar_dialogo_editar(e, p)
            )
            
            delete_button = ft.IconButton(
                icon=ft.icons.DELETE,
                tooltip="Eliminar",
                icon_color="red",
                on_click=lambda e, p=pago: mostrar_dialogo_eliminar(e, p)
            )
            
            pay_button = ft.IconButton(
                icon=ft.icons.PAYMENT,
                tooltip="Registrar Pago",
                icon_color="green",
                on_click=lambda e, p=pago: mostrar_dialogo_pago(e, p)
            )
            
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
                            ft.Row(
                                controls=[edit_button, delete_button, pay_button],
                                spacing=0
                            )
                        )
                    ]
                )
            )
        
        if tabla_container.content:
            tabla_container.content.rows = rows # type: ignore
            page.update()
            
    dropdown_correos.on_change = lambda e: filtrar_tabla(
        e.control.value, 
        dropdown_estados.value
    )
    
    dropdown_estados.on_change = lambda e: filtrar_tabla(
        dropdown_correos.value, 
        e.control.value
    )

    # Create main content
    contenido = ft.Column([
        ft.Text("Pagos a Suplidores", size=20, weight="bold"),
        ft.Row([
            dropdown_correos,
            dropdown_estados,
            ft.ElevatedButton(
                "Enviar por correo",
                icon=ft.icons.EMAIL,
                on_click=lambda e: enviar_correo_suplidores(
                    [pago for pago in get_estado_pagos_suplidores()
                     if (dropdown_correos.value == "Todos los correos" or pago[2] == dropdown_correos.value) and
                        (dropdown_estados.value == "Todos los estados" or pago[7] == dropdown_estados.value)
                    ],
                    page
                )
            )
        ], spacing=20),
        tabla_container
    ])

    # Initial table load
    filtrar_tabla()

    return contenido
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

