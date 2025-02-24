import flet as ft
from utils import mostrar_mensaje
from consultas import (
    get_cuentas,
    insertar_cuenta,
    actualizar_cuenta,
    eliminar_cuenta_db
)
from tabs.vencimientos_tab import crear_tabla_vencimientos
from tabs.clientes_tab import crear_tabla_clientes
from tabs.pagos_tab import crear_tab_pagos
from tabs.suscripciones_tab import crear_tab_suscripciones


def crear_tab_cuentas(page: ft.Page, mainTab: ft.Tabs):
        """
        Crea el tab "Cuentas" que permite agregar nuevas cuentas mediante un diálogo
        y muestra una tabla con los registros actuales, con opción de editar.
        """
        
        def actualizar_vencimientos():
            """Updates the vencimientos tab content"""
            mainTab.tabs[0].content = crear_tabla_vencimientos(page)
            page.update()
            
        def actualizar_clientes():
                """Updates the pagos tab content"""
                mainTab.tabs[1].content = crear_tabla_clientes(page, mainTab)
                page.update()
                
        def actualizar_pagos():
            """Updates the vencimientos tab content"""
            mainTab.tabs[2].content = crear_tab_pagos(page, mainTab)
            page.update()
            
        def actualizar_suscripciones():
                """Updates the pagos tab content"""
                mainTab.tabs[3].content = crear_tab_suscripciones(page, mainTab)
                page.update()
        
        # Contenedor donde se mostrará la tabla de cuentas.
        tabla_container = ft.Container()
        correo_seleccionado = None
        cuenta_seleccionada = None
        cuentas_auto_complete = None
        
        
        def actualizar_autocomplete():
            """Actualiza sugerencias del AutoComplete."""
            cuentas = get_cuentas()
            if auto_complete and auto_complete_container:
                correos = sorted(set(c[1] for c in cuentas))
                auto_complete.suggestions = [
                    ft.AutoCompleteSuggestion(key=correo, value=correo) 
                    for correo in correos
                ]
                auto_complete_container.content = auto_complete
                auto_complete_container.update()
                
        def on_cuenta_selected(e):
            """
            Actualiza la información cuando se selecciona un correo en el AutoComplete de cuentas.
            Filtra la tabla de cuentas para mostrar únicamente aquellas cuyo correo coincide con
            el valor seleccionado.
            """
            nonlocal cuenta_seleccionada, cuentas_auto_complete
            cuenta_seleccionada = e.selection.value
            if cuenta_seleccionada:
                filtrados = [c for c in cuentas_auto_complete if c[1].lower() == cuenta_seleccionada.lower()]
                actualizar_tabla_cuentas(filtrados)
            else:
                actualizar_tabla_cuentas()
            page.update()

        def eliminar_cuenta(e, cuenta_id):
            """Elimina una cuenta después de confirmar con el usuario."""
            cuenta = next(c for c in get_cuentas() if c[0] == cuenta_id)
            
            def confirmar_eliminacion(e):
                try:
                    if eliminar_cuenta_db(cuenta_id):
                        mostrar_mensaje("Cuenta eliminada correctamente", page)
                        actualizar_autocomplete()
                        actualizar_tabla_cuentas()
                        
                        # Actualizar los demas modulos
                        actualizar_vencimientos()
                        actualizar_clientes()
                        actualizar_pagos()
                        actualizar_suscripciones()
                    else:
                        mostrar_mensaje("Error al eliminar cuenta", page)
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
                content=ft.Text(f"¿Está seguro que desea eliminar la cuenta {cuenta[1]}?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=cancelar_eliminacion),
                    ft.TextButton("Eliminar", on_click=confirmar_eliminacion)
                ],
                actions_alignment=ft.MainAxisAlignment.END
            )
            
            page.overlay.append(dlg_confirmacion)
            dlg_confirmacion.open = True
            page.update()
        
        # Función para actualizar la tabla de cuentas; acepta opcionalmente una lista filtrada.
        def actualizar_tabla_cuentas(cuentas_filtradas=None):
            cuentas_list = cuentas_filtradas if cuentas_filtradas is not None else get_cuentas()
            rows = []
            for cuenta in cuentas_list:
                # Se asume que get_cuentas() devuelve registros con: (id, correo, costo, servicio)
                editar_btn = ft.IconButton(
                    icon=ft.Icons.EDIT,
                    tooltip="Editar cuenta",
                    on_click=lambda e, id=cuenta[0]: editar_cuenta(e, id, page)
                )
                eliminar_btn = ft.IconButton(
                    icon=ft.Icons.DELETE,
                    tooltip="Eliminar cuenta",
                    icon_color="red",
                    on_click=lambda e, id=cuenta[0]: eliminar_cuenta(e, id)
                )
                rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(cuenta[0]))),
                            ft.DataCell(ft.Text(cuenta[1])),
                            ft.DataCell(ft.Text(f"${cuenta[2]:.2f}")),
                            ft.DataCell(ft.Text(cuenta[3])),
                            ft.DataCell(editar_btn),
                            ft.DataCell(eliminar_btn)
                        ]
                    )
                )
            tabla_container.content = ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Correo")),
                    ft.DataColumn(ft.Text("Costo")),
                    ft.DataColumn(ft.Text("Servicio")),
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


        # Función para abrir el diálogo "Nuevo" para agregar una cuenta.
        def abrir_dialogo_nuevo(e):            
            
            txt_correo = ft.TextField(label="Correo", width=300)
            
            txt_costo = ft.TextField(
                label="Costo (en DOP)", 
                width=300, 
                input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
            )
            txt_servicio = ft.TextField(label="Servicio (Netflix, HBO)", width=300, capitalization=ft.TextCapitalization.WORDS)
            
            def guardar_nueva_cuenta(e):
                try:
                    # Validación de campos
                    if not txt_correo.value:
                        mostrar_mensaje("El campo correo es requerido.", page)
                        return
                    if not txt_costo.value:
                        mostrar_mensaje("El campo costo es requerido.", page)
                        return
                    if not txt_servicio.value:
                        mostrar_mensaje("El campo servicio es requerido.", page)
                        return

                    # Conversión de tipos
                    try:
                        costo = int(txt_costo.value)
                    except ValueError:
                        mostrar_mensaje("El campo costo debe ser un número válido.", page)
                        return

                    # Llamada a insertar_cuenta
                    if insertar_cuenta(txt_correo.value, costo, txt_servicio.value):
                        mostrar_mensaje("Cuenta agregada correctamente.", page)
                        
                        dialogo_nuevo.open = False
                        
                        actualizar_autocomplete()
                        
                        actualizar_tabla_cuentas()
                        
                        # Actualizar los demas modulos
                        actualizar_vencimientos()
                        actualizar_clientes()
                        actualizar_pagos()
                        actualizar_suscripciones()
                        
                        
                    else:
                        mostrar_mensaje("Error al agregar cuenta.", page)
                except Exception as ex:
                    mostrar_mensaje(f"Error: {str(ex)}", page)                
                page.update()
            
            dialogo_nuevo = ft.AlertDialog(
                modal=True,
                title=ft.Text("Agregar Nueva Cuenta"),
                content=ft.Column([
                    ft.Text("Ingrese los datos de la cuenta:"),
                    txt_correo,
                    txt_costo,
                    txt_servicio,
                ], spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: cerrar_dialogo(dialogo_nuevo, page)),
                    ft.TextButton("Guardar", on_click=guardar_nueva_cuenta)
                ]
            )
            page.overlay.append(dialogo_nuevo)
            dialogo_nuevo.open = True
            page.update()

        
        def editar_cuenta(e, cuenta_id, page):
            """Abre un diálogo modal para editar una cuenta existente, usando TextFields para actualizar los datos."""
            # Obtener la lista actualizada de cuentas y buscar la cuenta a editar.
            cuentas_list = get_cuentas()  # Se asume que get_cuentas() retorna registros con: (id, correo, costo, servicio)
            cuenta = next(c for c in cuentas_list if c[0] == cuenta_id)
            
            # Crear TextFields para cada campo (correo, costo y servicio)
            txt_correo = ft.TextField(label="Correo", value=cuenta[1], width=320, multiline=True)
            txt_costo = ft.TextField(
                label="Costo (en DOP)",
                value=str(cuenta[2]),
                width=320,
                input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")
            )
            txt_servicio = ft.TextField(label="Servicio", value=cuenta[3], width=320)
            
            def guardar_cambios(e):
                nuevo_correo = txt_correo.value.strip() # type: ignore
                nuevo_servicio = txt_servicio.value.strip() # type: ignore
                try:
                    nuevo_costo = int(txt_costo.value.strip()) # type: ignore
                except ValueError:
                    mostrar_mensaje("El costo debe ser un número.", page)
                    return
                
                # Llamar a la función actualizar_cuenta del módulo de consultas, que debe actualizar la cuenta
                # con los nuevos valores: (cuenta_id, correo, costo, servicio).
                if actualizar_cuenta(cuenta_id, nuevo_correo, nuevo_costo, nuevo_servicio):
                    dlg_modal.open = False
                    
                    actualizar_autocomplete()
                    
                    actualizar_tabla_cuentas()  # Se asume que esta función refresca la tabla de cuentas en la UI
                    
                    
                    # Actualizar los demas modulos
                    actualizar_vencimientos()
                    actualizar_clientes()
                    actualizar_pagos()
                    actualizar_suscripciones()
                    
                    page.update()
                    mostrar_mensaje("Cuenta actualizada correctamente.", page)
                else:
                    mostrar_mensaje("Error al actualizar la cuenta.", page)
                page.update()
            
            def close_dlg(e):
                dlg_modal.open = False
                page.update()
            
            dlg_modal = ft.AlertDialog(
                modal=True,
                title=ft.Text("Editar Cuenta"),
                content=ft.Column([
                    txt_correo,
                    txt_costo,
                    txt_servicio,
                ], spacing=10),
                actions=[
                    ft.TextButton("Cancelar", on_click=lambda e: close_dlg(e)),
                    ft.TextButton("Guardar", on_click=guardar_cambios)
                ]
            )
            page.overlay.append(dlg_modal)
            dlg_modal.open = True
            page.update()

        
        def cerrar_dialogo(dialog, page):
            dialog.open = False
            page.update()
        
        # Botón "Nuevo"
        btn_nuevo = ft.ElevatedButton(
            text="Nueva cuenta",
            icon=ft.Icons.ADD,
            on_click=abrir_dialogo_nuevo
        )
        
        # Función para filtrar la tabla por correo, basada en el valor seleccionado en el AutoComplete.
        def on_autocomplete_selected(e):
            nonlocal correo_seleccionado
            correo_seleccionado = e.selection.value  # Se obtiene el correo seleccionado
            if correo_seleccionado:
                cuentas = get_cuentas()  # Obtener la lista completa de cuentas
                filtrados = [c for c in cuentas if c[1].lower() == correo_seleccionado.lower()]
                actualizar_tabla_cuentas(filtrados)
            else:
                actualizar_tabla_cuentas()
        
        # Crear el AutoComplete para correos, usando los datos de get_cuentas().
        # Se extrae el campo "correo" de cada registro.
        correos = get_cuentas()
        auto_complete = ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key=cuenta[1], value=cuenta[1])
                for cuenta in correos
            ],
            on_select=on_autocomplete_selected,
            suggestions_max_height=150,
        )

        auto_complete_container = ft.Container(
            content=auto_complete,
            width=320,
            border=ft.border.all(1, ft.Colors.BLACK),
            border_radius=10
        )
        

        contenido_tab = ft.Column([
            ft.Text("Listado de Cuentas", size=20, weight="bold"), # type: ignore
            ft.Row([auto_complete_container, btn_nuevo], alignment=ft.MainAxisAlignment.START),
            tabla_container
        ], spacing=20)
        
        actualizar_tabla_cuentas()
        return contenido_tab