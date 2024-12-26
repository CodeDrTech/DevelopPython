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
    # Inicializa la fecha actual y crea un texto para mostrar la fecha seleccionada.
    fecha_actual = datetime.date.today()
    # Referencias para los campos de texto del tab Datos de Usuario
    txt_fecha = ft.Ref[ft.TextField]()
    
    # Traer el numero del dia actual como un entero
    hoy = fecha_actual.today()
    num_dia_actual = int(hoy.strftime("%d"))
    
    # Si el dia actual es menor a 15, se establece la fecha actual al primer dia del mes
    if num_dia_actual < 15:
        fecha_actual = fecha_actual.replace(day=1)
    else:
        # Si el dia actual es mayor o igual a 15, se establece la fecha_inicio en el dia 15
        fecha_actual = fecha_actual.replace(day=15)
        
    def mostrar_datepicker(e):
        # Abre el diálogo del DatePicker para que el usuario seleccione una fecha.
        page.overlay.append(date_picker_dialog)
        date_picker_dialog.open = True
        page.update()
    
    def seleccionar_fecha(e):
        fecha_actual = date_picker_dialog.value
        if fecha_actual:
            fecha_solo = fecha_actual.date()
            txt_fecha.current.value = fecha_solo.strftime("%Y-%m-%d")
            date_picker_dialog.open = False
            page.update()  

    # Crea el DatePicker y establece que `seleccionar_fecha` se ejecutará cuando cambie la fecha seleccionada.
    date_picker_dialog = ft.DatePicker(
        first_date=fecha_actual.replace(day=1),
        last_date=fecha_actual.replace(day=calendar.monthrange(fecha_actual.year, fecha_actual.month)[1]),
        current_date=datetime.datetime.now(),
        on_change=seleccionar_fecha)
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
        fecha_inicio = txt_fecha.current.value
        fecha_fin = txt_fecha.current.value
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
                            ft.TextField(ref=txt_fecha, value=fecha_actual.strftime("%Y-%m-%d"), width=200),
                            ft.Text("Fecha final"),
                            ft.TextField(ref=txt_fecha, value=fecha_actual.strftime("%Y-%m-%d"), width=200),
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