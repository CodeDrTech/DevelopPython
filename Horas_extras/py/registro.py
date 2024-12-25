from turtle import bgcolor
import flet as ft
from flet import ScrollMode, AppView
import datetime, calendar
from consultas import get_empleados, insertar_horas, get_codigo_por_nombre

#Funcion principal para iniciar la ventana con los controles
def registro(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 700
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
    
    
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
            hora35 = format_hour_for_db(txt_hora35.current.value)
            hora100 = format_hour_for_db(txt_hora100.current.value)
            comentario = txt_comentario.current.value

            # Llama a la función de queries 
            if not fecha or not codigo or not nombre or (not hora35 and not hora100):
                open_dlg_modal(e)

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
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,
        
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
                            ft.TextField(width=320, ref=txt_comentario, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, capitalization=ft.TextCapitalization.CHARACTERS),
                        ]),
                        ft.Row([
                        ft.Text(" ", width=100),
                        ft.ElevatedButton(text="Registrar", width=100, on_click=agregar_horas),
                        ft.ElevatedButton(text="Empleados", width=100, on_click=tab_empleados),
                        ft.ElevatedButton(text="Reportes", width=100),
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)
    page.update()