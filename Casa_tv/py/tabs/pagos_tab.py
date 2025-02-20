import flet as ft
import datetime
from utils import convertir_formato_fecha, mostrar_mensaje, get_estado_color
from consultas import get_clientes_pagos, get_estado_pago_cliente, insertar_pago

def crear_tab_pagos(page: ft.Page, mainTab: ft.Tabs):
        """
        Crea tab para aplicar pagos con AutoComplete y fecha.
        Permite seleccionar cliente, establecer fecha y registrar pago.
        """
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
                    
                    # Actualizar tabla de vencimientos (si aplica)
                    nonlocal tabla_vencimientos
                    tabla_vencimientos = crear_tabla_vencimientos()
                    mainTab.tabs[0].content = tabla_vencimientos
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
            ft.Text("Registrar Pago", size=20, weight="bold"),
            auto_complete_container,
            campo_fecha,
            campo_pago,
            info_container,
            ft.ElevatedButton(
                "Aplicar Pago",
                on_click=aplicar_pago,
                icon=ft.Icons.SAVE
            )
        ])