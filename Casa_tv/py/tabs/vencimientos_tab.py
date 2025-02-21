import flet as ft
from utils import convertir_formato_fecha, mostrar_mensaje
from consultas import get_estado_pagos
from consultas import get_total_pagos_mes_actual



def crear_tabla_vencimientos(page: ft.Page):
        """
        Crea tabla de vencimientos con filtros combinados:
        - AutoComplete para filtrar por nombre
        - Dropdown para filtrar por estado (En corte/Pendiente/Cerca/Todos)
        """
        
        
        
        datos_pagos = None  # Referencia a datos_pagos
        # Variables globales
        registros = get_estado_pagos()
        nombre_seleccionado = None
        estado_seleccionado = "Todos"
        tabla_container = ft.Container()
        
        # Suma de los montos
        total_montos = sum(reg[8] for reg in registros)
        total_montos_format = "{:,}".format(total_montos)
        
        # Obtener la suma de pagos del mes actual
        total_montos = get_total_pagos_mes_actual()
        total_pagado_mes = "{:,}".format(total_montos)
        
        # Utilidad total del mes actual.s
        calculo_utilidad = float(total_pagado_mes.replace(",", "")) - float(total_montos_format.replace(",", ""))
        #Utilidad = "{:,}".format(total_pagado_mes) - "{:,}".format(total_montos_format)
        Utilidad = "{:,}".format(calculo_utilidad)
        
        
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
            
        def reiniciar_tabla_vencimientos(e=None):
            """Actualiza la tabla de vencimientos con datos frescos"""
            # Recargar datos frescos
            nonlocal registros, tabla_container, nombre_seleccionado, auto_complete
            registros = get_estado_pagos()
            
            # Reset nombre_seleccionado
            nombre_seleccionado = None
            
            # Actualizar AutoComplete con nombres frescos
            nombres = sorted(set(reg[1] for reg in registros))
            auto_complete.suggestions = [
                ft.AutoCompleteSuggestion(key=nombre, value=nombre) 
                for nombre in nombres
            ]
            auto_complete.value = ""
            
            # Recalcular totales
            total_montos = sum(reg[8] for reg in registros)
            total_montos_format = "{:,}".format(total_montos)
            total_pagado = get_total_pagos_mes_actual()
            total_pagado_mes = "{:,}".format(total_pagado)
            calculo_utilidad = float(total_pagado_mes.replace(",", "")) - float(total_montos_format.replace(",", ""))
            Utilidad = "{:,}".format(calculo_utilidad)
            
            # Actualizar tabla
            actualizar_tabla(registros)
            page.update()
            
        # Botón refresh
        btn_refresh = ft.IconButton(
            icon=ft.Icons.REFRESH,
            tooltip="Actualizar tabla",
            on_click=reiniciar_tabla_vencimientos
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
            ft.DataColumn(ft.Text("Saldo pendiente", width=70, text_align=ft.TextAlign.LEFT)),
            ft.DataColumn(ft.Text("Días")),
            ft.DataColumn(ft.Text("Estado")),
            ft.DataColumn(ft.Text("Pago    mensual", width=70, text_align=ft.TextAlign.LEFT)),
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
                    ft.DataColumn(ft.Text("Saldo pendiente", width=70, text_align=ft.TextAlign.LEFT)),
                    ft.DataColumn(ft.Text("Días")),
                    ft.DataColumn(ft.Text("Estado")),
                    ft.DataColumn(ft.Text("Pago    mensual", width=70, text_align=ft.TextAlign.LEFT)),
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
                            ft.DataCell(ft.Text(f"${reg[5]}")),
                            ft.DataCell(ft.Text(int(reg[6]))),
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
            ft.Text("Busqueda por nombre", size=20, weight="bold"),
            ft.Row([
                auto_complete_container,
                dropdown_estado,
                btn_refresh,
            ft.Row([ft.Text(f"Deuda total: ${total_montos_format}", size=15, color=ft.Colors.RED)]),
            ft.Row([ft.Text(f"Pagado este mes: ${total_pagado_mes}", size=15, color=ft.Colors.BLUE)]),
            ft.Row([ft.Text(f"Ganancia: ${Utilidad}", size=15, color=ft.Colors.GREEN)]),
            ]),            
            tabla_container
        ])