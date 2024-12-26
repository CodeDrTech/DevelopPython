import flet as ft
from flet import ScrollMode
from consultas import get_horas_por_fecha
import os, datetime, calendar
from datetime import date


#Funcion principal para iniciar la ventana con los controles.
def reporte(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 900
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Funcion para manejar diferentes eventos al seleccionar algunos de los tab
    def tab_registro(e):
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from registro import registro
            registro(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------    
    # funciones y control para abrir cuadro de dialogo para avisar al usuario que faltan datos en tab Registrar Usuario.
    def open_dlg_modal(e):
        e.control.page.overlay.append(dlg_modal)
        dlg_modal.open = True
        e.control.page.update()
        
    def close_dlg(e):
        dlg_modal.open = False
        e.control.page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Falta información"),
        content=ft.Text("Ha dejado algun campo vacío"),
        actions=[
                    ft.TextButton("Ok", on_click=close_dlg),
                ],
        actions_alignment=ft.MainAxisAlignment.END,
        #on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    
    # Initialize SnackBar at start
    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),
        action="OK"
    )
    
    # Make nombre_seleccionado accessible
    nombre_seleccionado = None
    
    def show_snackbar(mensaje):
        if not page.snack_bar:
            page.snack_bar = ft.SnackBar(content=ft.Text(mensaje))
        else:
            page.snack_bar.content.value = mensaje
        page.snack_bar.open = True
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Inicializa las fechas actuales para ambos TextField
    fecha_actual1 = datetime.date.today()
    fecha_actual2 = datetime.date.today()

    # Referencias para los campos de texto
    txt_fecha1 = ft.Ref[ft.TextField]()
    txt_fecha2 = ft.Ref[ft.TextField]()

    # Traer el número del día actual como un entero
    hoy = datetime.date.today()
    num_dia_actual = int(hoy.strftime("%d"))

    # Configuración de `fecha_actual1`
    if num_dia_actual < 15:
        fecha_actual1 = fecha_actual1.replace(day=1)
    else:
        fecha_actual1 = fecha_actual1.replace(day=15)

    # Configuración de `fecha_actual2`
    if num_dia_actual < 15:
        fecha_actual2 = fecha_actual2.replace(day=1)
    else:
        fecha_actual2 = fecha_actual2.replace(day=15)

    # Función para mostrar el DatePicker del primer TextField
    def mostrar_datepicker(e):
        page.overlay.append(date_picker_dialog1)
        date_picker_dialog1.open = True
        page.update()

    # Función para mostrar el DatePicker del segundo TextField
    def mostrar_datepicker2(e):
        page.overlay.append(date_picker_dialog2)
        date_picker_dialog2.open = True
        page.update()

    # Función para seleccionar la fecha del primer TextField
    def seleccionar_fecha1(e):
        fecha_seleccionada = date_picker_dialog1.value
        if fecha_seleccionada:
            fecha_solo = fecha_seleccionada.date()
            txt_fecha1.current.value = fecha_solo.strftime("%Y-%m-%d")
            date_picker_dialog1.open = False
            page.update()

    # Función para seleccionar la fecha del segundo TextField
    def seleccionar_fecha2(e):
        fecha_seleccionada = date_picker_dialog2.value
        if fecha_seleccionada:
            fecha_solo = fecha_seleccionada.date()
            txt_fecha2.current.value = fecha_solo.strftime("%Y-%m-%d")
            date_picker_dialog2.open = False
            page.update()

    # DatePicker para el primer TextField
    date_picker_dialog1 = ft.DatePicker(
        first_date=fecha_actual1.replace(day=1),
        last_date=fecha_actual1.replace(day=calendar.monthrange(fecha_actual1.year, fecha_actual1.month)[1]),
        current_date=datetime.datetime.now(),
        on_change=seleccionar_fecha1
    )

    # DatePicker para el segundo TextField
    date_picker_dialog2 = ft.DatePicker(
        first_date=fecha_actual2.replace(day=1),
        last_date=fecha_actual2.replace(day=calendar.monthrange(fecha_actual2.year, fecha_actual2.month)[1]),
        current_date=datetime.datetime.now(),
        on_change=seleccionar_fecha2
    )

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_tabla_horas(registros):
        """Crea DataTable con registros de horas"""
        columns = [
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Horas 35%")),
            ft.DataColumn(ft.Text("Horas 100%")),
            ft.DataColumn(ft.Text("Comentario")),
        ]
        
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(reg[0])),  # Fecha
                    ft.DataCell(ft.Text(str(reg[1]))),  # Código
                    ft.DataCell(ft.Text(reg[2])),  # Nombre
                    ft.DataCell(ft.Text(reg[3])),  # Horas 35
                    ft.DataCell(ft.Text(reg[4])),  # Horas 100
                    ft.DataCell(ft.Text(reg[5])),  # Comentario
                ],
            ) for reg in registros
        ]
        
        return ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),
        )
    # Contenedor para la tabla
    tabla_container = ft.Container(content=crear_tabla_horas([]))
    def actualizar_tabla(e):
        fecha_inicio = txt_fecha1.current.value
        fecha_fin = txt_fecha2.current.value

        # Validar si la fecha inicial es mayor a la fecha final
        if fecha_inicio > fecha_fin:
            show_snackbar("La fecha inicial no puede ser mayor que la fecha final.")
            return  # Salir de la función si las fechas no son válidas

        # Obtener los registros y actualizar la tabla
        registros = get_horas_por_fecha(fecha_inicio, fecha_fin)
        nueva_tabla = crear_tabla_horas(registros)
        tabla_container.content = nueva_tabla
        page.update()

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    mainTab = ft.Tabs(
        selected_index=1,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,        
        
        # Contenedor de tabs
        tabs=[
            ft.Tab(
                icon=ft.Icons.LIST_ALT_OUTLINED,
                text="Reportes",
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Text("Fecha inicial"),
                            ft.TextField(ref=txt_fecha1, value=fecha_actual1.strftime("%Y-%m-%d"), width=200, read_only=True, on_click=mostrar_datepicker),
                            ft.Text("Fecha final"),
                            ft.TextField(ref=txt_fecha2, value=fecha_actual2.strftime("%Y-%m-%d"), width=200, read_only=True, on_click=mostrar_datepicker2),
                        ]),
                        ft.Row([
                            ft.ElevatedButton(text="Atras", icon=ft.Icons.ARROW_BACK, width=150, on_click=tab_registro),
                            ft.ElevatedButton(text="Buscar", icon=ft.Icons.UPLOAD, width=150, on_click=actualizar_tabla),
                        ]),
                        tabla_container,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)
    page.update()