from turtle import bgcolor
import flet as ft
from flet import ScrollMode, AppView
import datetime, calendar
from consultas import get_empleados, insertar_horas, get_codigo_por_nombre, get_ultimos_registros, actualizar_registro, validar_entrada_hora

#Funcion principal para iniciar la ventana con los controles
def main(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 700
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def crear_tabla_edicion(registros, on_edit_click):
        columns = [
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Horas 35%     ")),
            ft.DataColumn(ft.Text("Horas 100%     ")),
            ft.DataColumn(ft.Text("Comentario")),
            ft.DataColumn(ft.Text("Editar")),
        ]
        
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(reg[0])),
                    ft.DataCell(ft.Text(str(reg[1]))),
                    ft.DataCell(ft.Text(reg[2])),
                    ft.DataCell(ft.Text(reg[3])),
                    ft.DataCell(ft.Text(reg[4])),
                    ft.DataCell(ft.Text(reg[5] if reg[5] else "")),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color="blue",
                            tooltip="Editar",
                            data=reg,  # Store record data
                            on_click=lambda e: on_edit_click(e.control.data)
                        )
                    ),
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
    # Cargar los empleados desde la base de datos
    empleados_data = get_empleados()  # Obtener la lista de empleados
    
    nombre_seleccionado = None
    def on_autocomplete_selected(e):
        nonlocal nombre_seleccionado
        nombre_seleccionado = e.selection.value        

        # Busca el código del empleado seleccionado en la base de datos
        # y lo muestra en el campo de texto "Código"
        codigo_db = get_codigo_por_nombre(nombre_seleccionado)
        if codigo_db:
            txt_codigo.current.value = str(codigo_db)
            page.update()
    
    # Crear sugerencias para el AutoComplete
    suggestions = [
        ft.AutoCompleteSuggestion(key=emp, value=emp) for emp in empleados_data
    ]
    
    # Crear el AutoComplete
    auto_complete = ft.AutoComplete(
        suggestions=suggestions,
        on_select=on_autocomplete_selected,
    )
    
    # Usar un Container para establecer un ancho específico
    auto_complete_container = ft.Container(
        content=auto_complete,
        width=320,  # Establecer el ancho deseado
        border=ft.border.all(1, ft.Colors.BLACK),
        border_radius=10,
        
    )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Inicializa la fecha actual y crea un texto para mostrar la fecha seleccionada.
    fecha_actual = datetime.date.today()
    
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
    def format_hora(e):
        """
        Función para formatear entrada de hora en formato H:MM o HH:MM
        """
        # Quitar caracteres no numéricos
        raw = ''.join(filter(str.isdigit, e.control.value))
        
        # Limitar a 4 dígitos máximo (2 para hora, 2 para minutos)
        raw = raw[:4]
        
        # Aplicar formato HH:MM
        formatted = ''
        for i, char in enumerate(raw):
            if i == 1:  # Añadir ":" después del primer o segundo dígito
                formatted += ':'
            formatted += char
        
        # Actualizar el campo de texto
        e.control.value = formatted
        e.control.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def limpiar_y_recrear_auto_complete(auto_complete_container, empleados_data):
        nonlocal nombre_seleccionado
        nombre_seleccionado = None  # Limpia la selección previa

        # Borra el contenido actual
        auto_complete_container.content = None
        auto_complete_container.update()

        # Crea un nuevo AutoComplete
        auto_complete = ft.AutoComplete(
            suggestions=[
                ft.AutoCompleteSuggestion(key=emp, value=emp) for emp in empleados_data
            ],
            on_select=on_autocomplete_selected  # Reconectar el manejador de eventos
        )

        # Agrega el nuevo AutoComplete al contenedor
        auto_complete_container.content = auto_complete
        auto_complete_container.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def format_hour_for_db(hour_str):
        """Formatea la entrada de hora para la base de datos para siempre incluya :00 en caso de no tenerlo."""
        if not hour_str:
            return ""
        
        # Si es solo un número, añadir :00
        if hour_str.isdigit():
            return f"{hour_str}:00"
        
        return hour_str
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------    
    # funciones y control para abrir cuadro de dialogo para avisar al usuario que faltan datos en tab Registrar Usuario.
    def open_dlg_modal(e, mensaje="Ha dejado algun campo vacío"):
        dlg_modal.content = ft.Text(mensaje)  # Update dialog content
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
    # Codigo para insertar datos a la tabla usuario mediante los controles del tab Datos Usuario
    # Referencias para los campos de texto del tab Datos de Usuario
    txt_fecha = ft.Ref[ft.TextField]()
    txt_codigo = ft.Ref[ft.TextField]()
    txt_hora35 = ft.Ref[ft.TextField]()
    txt_hora100 = ft.Ref[ft.TextField]()
    txt_comentario = ft.Ref[ft.TextField]()
    def agregar_horas(e):
        try:
            #nonlocal nombre_seleccionado
            fecha = txt_fecha.current.value
            codigo = txt_codigo.current.value
            nombre = nombre_seleccionado
            hora35 = txt_hora35.current.value
            hora100 = txt_hora100.current.value
            comentario = txt_comentario.current.value

            # Validate hours format
            valido35, mensaje35 = validar_entrada_hora(hora35)
            if not valido35:
                open_dlg_modal(e, f"Error en Hora 35%: {mensaje35}")
                return
                
            valido100, mensaje100 = validar_entrada_hora(hora100)
            if not valido100:
                open_dlg_modal(e, f"Error en Hora 100%: {mensaje100}")
                return

            if not fecha or not codigo or not nombre or not comentario or (not hora35 and not hora100):
                open_dlg_modal(e, "Complete los campos obligatorios")

            else:
                # Llama a la función de queries
                insertar_horas(fecha, codigo, nombre, hora35, hora100, comentario)

                # Mostrar mensaje de éxito
                show_snackbar("¡Hora agregada exitosamente!")


                # Limpia los campos
                txt_codigo.current.value = ""

                limpiar_y_recrear_auto_complete(auto_complete_container, empleados_data)
            
                txt_hora35.current.value = ""
                txt_hora100.current.value = ""
                txt_comentario.current.value = ""
                page.update()

        except Exception as error:
            # Muestra un error en snack_bar
            show_snackbar(f"Error: {error}")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def tab_empleados(e):
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from empleados import Empleados
            Empleados(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Funcion para manejar diferentes eventos al seleccionar algunos de los tab
    def tab_reporte(e):
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from reporte import reporte
            reporte(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Cambiar tamaño de ventana según tab seleccionado
    def cambio_tamano(e):
        if mainTab.selected_index == 0:
            page.window.width = 700
            page.window.height = 700
            page.update()
        else:
            page.window.width = 1250
            page.window.height = 700
            page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    
    def on_edit_click(registro_data):
        def close_dlg(e):
            edit_dialog.open = False
            page.update()

        def save_changes(e):
            try:
                nueva_fecha = txt_edit_fecha.current.value
                nuevas_horas35 = txt_edit_horas35.current.value
                nuevas_horas100 = txt_edit_horas100.current.value
                nuevo_comentario = txt_edit_comentario.current.value
                
                # Obtenemos valores originales de registro_data
                horas_35_original = registro_data[3]  # Índice 3 para Horas_35
                horas_100_original = registro_data[4]  # Índice 4 para Horas_100
                
                valido35, mensaje35 = validar_entrada_hora(nuevas_horas35)
                if not valido35:
                    open_dlg_modal(e, f"Hora 35%: {mensaje35}")
                    return
                    
                valido100, mensaje100 = validar_entrada_hora(nuevas_horas100)
                if not valido100:
                    open_dlg_modal(e, f"Hora 100%: {mensaje100}")
                    return

                if actualizar_registro(
                    registro_data[0],  # fecha original
                    registro_data[1],  # código
                    nueva_fecha,
                    nuevas_horas35,
                    nuevas_horas100,
                    nuevo_comentario,
                    horas_35_original,
                    horas_100_original
                ):
                    # Actualizar tabla
                    registros = get_ultimos_registros()
                    tabla_edicion.rows = crear_tabla_edicion(registros, on_edit_click).rows
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Registro actualizado"), duration=3000))
                    close_dlg(e)
                else:
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Error al actualizar"), duration=3000))
            except Exception as error:
                page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {error}"), duration=3000))

        txt_edit_fecha = ft.Ref[ft.TextField]()
        txt_edit_horas35 = ft.Ref[ft.TextField]()
        txt_edit_horas100 = ft.Ref[ft.TextField]()
        txt_edit_comentario = ft.Ref[ft.TextField]()

        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Registro"),
            content=ft.Column([
                ft.TextField(
                    ref=txt_edit_fecha,
                    label="Fecha",
                    value=registro_data[0],
                    width=320
                ),
                ft.TextField(
                    ref=txt_edit_horas35,
                    label="Horas 35%",
                    value=registro_data[3],
                    width=320,
                    max_length=4,
                    input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$"),
                    on_change=format_hora
                ),
                ft.TextField(
                    ref=txt_edit_horas100,
                    label="Horas 100%",
                    value=registro_data[4],
                    width=320,
                    max_length=4,
                    input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$"),
                    on_change=format_hora
                ),
                ft.TextField(
                    ref=txt_edit_comentario,
                    label="Comentario",
                    value=registro_data[5],
                    multiline=True,
                    max_length=90,
                    capitalization=ft.TextCapitalization.CHARACTERS,
                    width=320
                ),
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                ft.TextButton("Guardar", on_click=save_changes),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()
    
    # Get initial data for table
    registros = get_ultimos_registros()
    
    # Create table with data
    tabla_edicion = crear_tabla_edicion(registros, on_edit_click)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,
        on_change=cambio_tamano,        
        # Contenedor de tabs
        tabs=[
            ft.Tab(
                icon=ft.Icons.LOCK_CLOCK,
                text="Horas",
                content=ft.Column(
                    [
                        ft.Text("Registro de horas"),
                        ft.Row([
                            ft.Text("Fecha:", width=100),
                            ft.TextField(width=320, ref=txt_fecha, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, read_only=True, value=fecha_actual.strftime("%Y-%m-%d"), on_click=mostrar_datepicker, icon=ft.Icons.CALENDAR_MONTH),
                        ]),
                        ft.Row([
                            ft.Text("Código:", width=100),
                            ft.TextField(width=320, ref=txt_codigo, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, read_only=True, max_length=3, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Nombre:", width=100),
                            auto_complete_container,
                        ]),
                        ft.Row([
                            ft.Text("Hora 35%:", width=100),
                            ft.TextField(width=320, ref=txt_hora35, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=4, on_change=format_hora, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Hora 100%:", width=100),
                            ft.TextField(width=320, ref=txt_hora100, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=4, on_change=format_hora, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Destino/Comentario:", width=100),
                            ft.TextField(width=320, multiline=True, max_length=90, ref=txt_comentario, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, capitalization=ft.TextCapitalization.CHARACTERS),
                        ]),
                        ft.Row([
                        ft.Text(" ", width=100),
                        ft.ElevatedButton(text="Registrar", width=100, on_click=agregar_horas),
                        ft.ElevatedButton(text="Empleados", width=100, on_click=tab_empleados),
                        ft.ElevatedButton(text="Reportes", width=100, on_click=tab_reporte),
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
            ft.Tab(
                icon=ft.Icons.EDIT,
                text="Edicion",
                content=ft.Column([
                    ft.Text("Editar registro de horas"),
                    tabla_edicion,
                ])
            )
        ],
    )
    page.add(mainTab)
ft.app(main)
#ft.app(target=main, port=8080, view=AppView.WEB_BROWSER)