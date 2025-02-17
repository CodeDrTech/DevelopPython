import flet as ft
from flet import ScrollMode, AppView
import datetime, calendar
from consultas import get_empleados, insertar_horas, get_codigo_por_nombre, get_ultimos_registros, actualizar_registro, delete_record, validar_entrada_hora

#Funcion principal para iniciar la ventana con los controles
def registro(page: ft.Page):
    page.title = "Horas Extras Ver. 20250127"
    page.window.alignment = ft.alignment.center
    page.window.width = 600
    page.window.height = 650
    page.window.resizable = False
    page.padding = 20
    page.scroll = True # type: ignore
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def crear_tabla_edicion(registros, on_edit_click):        
        """
        Crea una tabla para editar los registros de horas
        
        Parameters
        ----------
        registros : list
            Registros de horas a editar
        on_edit_click : function
            Función a llamar al hacer clic en el botón de editar
        Returns
        -------
        ft.DataTable
            Tabla con los registros de horas
        """
        def formato_fecha_usuario_tabla(fecha_str):
            """
            Convierte una fecha de formato 'YYYY-MM-DD' a 'DD-MMM-YYYY'.

            Args:
                fecha_str (str): Fecha en formato 'YYYY-MM-DD'.

            Returns:
                str: Fecha en formato 'DD-MMM-YYYY' si la conversión es exitosa, 
                        de lo contrario, devuelve la cadena original.
            """
            """Convierte fecha de YYYY-MM-DD a YYYYMMM-DD"""
            try:
                fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
                meses_abrev = {
                    1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR',
                    5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AGO',
                    9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DIC'
                }
                return f"{fecha.day:02d}-{meses_abrev[fecha.month]}-{fecha.year}"
            except ValueError:
                return fecha_str
        def confirmar_eliminacion(registro_id):
            """
            Muestra un cuadro de diálogo de confirmación para eliminar un registro.
            Args:
                registro_id (int): ID del registro a eliminar.
            """
            def close_dlg(e):
                confirm_dialog.open = False
                page.update()
            def eliminar_registro_confirmado(e):
                """
                Elimina el registro después de la confirmación del usuario.
                """
                try:
                    if delete_record(registro_id):
                        # Actualizar la tabla después de eliminar el registro
                        registros_actualizados = get_ultimos_registros()
                        tabla_edicion.rows = crear_tabla_edicion(registros_actualizados, on_edit_click).rows
                        page.show_snack_bar(ft.SnackBar(content=ft.Text("Registro eliminado"), bgcolor="green", duration=3000))
                    else:
                        page.show_snack_bar(ft.SnackBar(content=ft.Text("Error al eliminar"), bgcolor="red", duration=3000))
                except Exception as error:
                    page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {error}"), bgcolor="red", duration=3000))
                finally:
                    confirm_dialog.open = False
                    page.update()
            # Cuadro de diálogo de confirmación
            confirm_dialog = ft.AlertDialog(
                modal=True,
                title=ft.Text("Confirmar eliminación"),
                content=ft.Text("¿Estás seguro de que deseas eliminar este registro?"),
                actions=[
                    ft.TextButton("Cancelar", on_click=close_dlg),
                    ft.TextButton("Eliminar", on_click=eliminar_registro_confirmado),
                ],
                actions_alignment=ft.MainAxisAlignment.END,
            )
            page.dialog = confirm_dialog
            confirm_dialog.open = True
            page.update()
                
        columns = [
            ft.DataColumn(ft.Text("#")),
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Horas 35%     ")),
            ft.DataColumn(ft.Text("Horas 100%     ")),
            ft.DataColumn(ft.Text("Nocturnas")),
            ft.DataColumn(ft.Text("Editar")),
            ft.DataColumn(ft.Text("Eliminar")),
        ]
        
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(reg[0]))),
                    ft.DataCell(ft.Text(formato_fecha_usuario_tabla(reg[1]))),
                    ft.DataCell(ft.Text(str(reg[2]))),
                    ft.DataCell(ft.Text(reg[3])),
                    ft.DataCell(ft.Text(reg[4])),
                    ft.DataCell(ft.Text(reg[5])),
                    ft.DataCell(ft.Text(reg[6])),
                    ft.DataCell(
                        ft.IconButton(
                            icon=ft.Icons.EDIT,
                            icon_color="blue",
                            tooltip="Editar",
                            data=reg,  # Store record data
                            on_click=lambda e: on_edit_click(e.control.data)
                        )
                    ),
                    ft.DataCell(
                    ft.IconButton(
                        icon=ft.Icons.DELETE,
                        icon_color="red",
                        tooltip="Eliminar",
                        data=reg[0],  # Almacena el ID del registro
                        on_click=lambda e, r=reg[0]: confirmar_eliminacion(r)  # Llama a la función de confirmación
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
        """
        Manejador de eventos para el AutoComplete
        
        Parameters
        ----------
        e : flet.event.Event
            Evento lanzado al seleccionar un empleado en el AutoComplete
        
        Notes
        -----
        Este manejador cambia el valor del campo de texto "Código" con el código
        correspondiente al empleado seleccionado en la base de datos.
        """        
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
        """
        Abre el diálogo del DatePicker para que el usuario seleccione una fecha.
        """ 
        page.overlay.append(date_picker_dialog)
        date_picker_dialog.open = True
        page.update()
    
    def seleccionar_fecha(e):
        """
        Selecciona una fecha desde el DatePicker y actualiza el texto en el campo
        de texto "Fecha" con la fecha seleccionada en formato "YYYY-MM-DD".
        Luego cierra el diálogo del DatePicker.
        """
        fecha_actual = date_picker_dialog.value
        if fecha_actual:
            fecha_solo = formato_fecha_usuario(str(fecha_actual.date()))
            txt_fecha.current.value = fecha_solo #.strftime("%Y-%m-%d")
            date_picker_dialog.open = False
            page.update()  

    # Crea el DatePicker y establece que `seleccionar_fecha` se ejecutará cuando cambie la fecha seleccionada.
    def get_rango_fechas():
        """
        Calcula rango de fechas desde primer día mes anterior hasta último día mes actual.
        
        Returns:
            tuple: (fecha_inicio, fecha_fin)
        """
        fecha_actual = datetime.datetime.now()
        
        # Primer día del mes anterior
        if fecha_actual.month == 1:
            primer_dia = datetime.datetime(fecha_actual.year - 1, 12, 1)
        else:
            primer_dia = datetime.datetime(fecha_actual.year, fecha_actual.month - 1, 1)
        
        # Último día del mes actual
        ultimo_dia = fecha_actual.replace(
            day=calendar.monthrange(fecha_actual.year, fecha_actual.month)[1]
        )
        
        return primer_dia, ultimo_dia

    # En la creación del DatePicker
    fecha_inicio, fecha_fin = get_rango_fechas()

    date_picker_dialog = ft.DatePicker(
        first_date=fecha_inicio,
        last_date=fecha_fin,
        current_date=datetime.datetime.now(),
        on_change=seleccionar_fecha
    )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def format_hora(e):
        """
        Función para formatear entrada de hora en formato HH:MM
        Si el primer dígito es 0, formatea horas de 01-09
        Si el primer dígito es 1, formatea horas de 10-12
        """
        # Quitar caracteres no numéricos y obtener solo los dígitos
        raw = ''.join(filter(str.isdigit, e.control.value))
        
        # Si hay dígitos para procesar
        if raw:
            # Si comienza con 0, esperar dos dígitos para la hora
            if raw[0] == '0':
                if len(raw) == 1:
                    formatted = raw  # Solo mostrar el 0
                else:
                    hours = raw[0:2]
                    minutes = raw[2:4] if len(raw) > 2 else ""
                    formatted = f"{hours}:{minutes}" if minutes else hours
            # Si no comienza con 0
            else:
                if len(raw) == 1:
                    formatted = raw  # Solo mostrar el primer dígito
                else:
                    hours = raw[0:2] if len(raw) >= 2 else raw[0]
                    if len(hours) == 2 and int(hours) > 12:
                        hours = "12"
                    minutes = raw[2:4] if len(raw) > 2 else ""
                    formatted = f"{hours}:{minutes}" if minutes else hours
        else:
            formatted = ""
        
        # Actualizar el campo de texto
        e.control.value = formatted
        e.control.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def limpiar_y_recrear_auto_complete(auto_complete_container, empleados_data):
        """
        Limpia el AutoComplete actual y crea uno nuevo con las sugerencias proporcionadas.

        :param auto_complete_container: Contenedor donde se encuentra el AutoComplete actual.
        :param empleados_data: Lista de empleados para establecer como sugerencias.
        """
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
    def open_dlg_modal(e, mensaje="Ha dejado algun campo vacío"):
        """
        Abre un diálogo modal con un mensaje de error.

        :param e: Instancia de la clase Principal.
        :param mensaje: Mensaje a mostrar en el diálogo. Por defecto, "Ha dejado algun campo vacío".
        """
        dlg_modal.content = ft.Text(mensaje)
        e.control.page.overlay.append(dlg_modal)
        dlg_modal.open = True
        e.control.page.update()
        
    def close_dlg(e):
        """
        Cierra el diálogo modal.
        
        :param e: Instancia de la clase Principal.
        """
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
        """
        Muestra un mensaje en una SnackBar en la parte inferior de la pantalla.

        :param mensaje: El mensaje a mostrar en la SnackBar.
        """
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
    txt_nocturnas = ft.Ref[ft.TextField]()
    
    def agregar_horas(e):
        """
        Agrega un registro a la tabla Horas en la base de datos, validando que los campos obligatorios estén completos y
        que el formato de las horas sea correcto.

        :param e: El evento del botón "Agregar".
        :return: None
        """
        
        try:
            #nonlocal nombre_seleccionado
            fecha = formato_fecha_bd(txt_fecha.current.value)
            codigo = txt_codigo.current.value
            nombre = nombre_seleccionado
            hora35 = txt_hora35.current.value
            hora100 = txt_hora100.current.value
            nocturnas = txt_nocturnas.current.value
            
            

            # Validate hours format
            valido35, mensaje35 = validar_entrada_hora(hora35)
            if not valido35:
                open_dlg_modal(e, f"Error en Hora 35%: {mensaje35}")
                return
                
            valido100, mensaje100 = validar_entrada_hora(hora100)
            if not valido100:
                open_dlg_modal(e, f"Error en Hora 100%: {mensaje100}")
                return
            
            validonoc, mensajenoc = validar_entrada_hora(nocturnas)
            if not validonoc:
                open_dlg_modal(e, f"Error en Hora nocturnas: {mensajenoc}")
                return

            if not fecha or not codigo or not nombre or (not hora35 and not hora100 and not nocturnas):
                open_dlg_modal(e, "Complete los campos obligatorios")

            else:
                # Llama a la función de queries
                insertar_horas(fecha, codigo, nombre, hora35, hora100, nocturnas)

                # Mostrar mensaje de éxito
                show_snackbar("¡Hora agregada exitosamente!")


                # Limpia los campos
                txt_codigo.current.value = ""

                limpiar_y_recrear_auto_complete(auto_complete_container, empleados_data)
            
                txt_hora35.current.value = ""
                txt_hora100.current.value = ""
                txt_nocturnas.current.value = ""
                
                registros = get_ultimos_registros()
                tabla_edicion.rows = crear_tabla_edicion(registros, on_edit_click).rows
                page.update()

        except Exception as error:
            # Muestra un error en snack_bar
            show_snackbar(f"Error: {error}")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def tab_empleados(e):
            """
            Maneja el evento de cambio de tab a "Empleados".

            Limpia la página actual y llama a la función Empleados desde el módulo empleados.py, la
            cual imprime los controles y la tabla de empleados en la página actual.
            """
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from empleados import Empleados
            Empleados(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Funcion para manejar diferentes eventos al seleccionar algunos de los tab
    def tab_reporte(e):
            """
            Maneja el evento de cambio de tab a "Reporte".

            Limpia la página actual y llama a la función reporte desde el módulo reporte.py, la
            cual imprime los controles y la tabla de reporte en la página actual.
            """
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from reporte import reporte
            reporte(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Cambiar tamaño de ventana según tab seleccionado
    def cambio_tamano(e):
        """
        Cambia el tamaño de la ventana según la pestaña seleccionada en mainTab.

        Si se selecciona la pestaña de "Registro", el tamaño de la ventana es de 600x650.
        Si se selecciona la pestaña de "Empleados" o "Reporte", el tamaño de la ventana es de 1250x700.
        """
        if mainTab.selected_index == 1:
            page.window.width = 1250
            page.window.height = 650
            page.update()
        else:
            #page.window.width = 1250
            #page.window.height = 650
            registros = get_ultimos_registros()
            tabla_edicion.rows = crear_tabla_edicion(registros, on_edit_click).rows
            page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def on_edit_click(registro_data):
        """
        Maneja el evento de clic en el botón "Editar" de una fila de la tabla de edición.
        """
        def close_dlg(e):
            edit_dialog.open = False
            page.update()

        def save_changes(e):
            """
            Guarda los cambios realizados en el cuadro de diálogo de edición.
            """
            try:
                nueva_fecha = formato_fecha_bd(txt_edit_fecha.current.value)
                nuevas_horas35 = txt_edit_horas35.current.value
                nuevas_horas100 = txt_edit_horas100.current.value
                nuevas_nocturnas = txt_edit_nocturnas.current.value

                # Validar campos de horas
                valido35, mensaje35 = validar_entrada_hora(nuevas_horas35)
                if not valido35:
                    open_dlg_modal(e, f"Hora 35%: {mensaje35}")
                    return

                valido100, mensaje100 = validar_entrada_hora(nuevas_horas100)
                if not valido100:
                    open_dlg_modal(e, f"Hora 100%: {mensaje100}")
                    return

                validonoc, mensajenoc = validar_entrada_hora(nuevas_nocturnas)
                if not validonoc:
                    open_dlg_modal(e, f"Horas Nocturnas: {mensajenoc}")
                    return
                
                if not nueva_fecha or not nuevas_horas35 or not nuevas_horas100 or not nuevas_nocturnas:
                    open_dlg_modal(e, "Complete los campos obligatorios")
                    return

                # Actualizar registro en la base de datos
                if actualizar_registro(
                    registro_data[0],  # ID del registro
                    nueva_fecha,
                    nuevas_horas35,
                    nuevas_horas100,
                    nuevas_nocturnas
                ):
                    # Actualizar tabla en la interfaz
                    registros = get_ultimos_registros()
                    tabla_edicion.rows = crear_tabla_edicion(registros, on_edit_click).rows
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Registro actualizado"), bgcolor="green", duration=3000))
                    edit_dialog.open = False
                    page.update()
                else:
                    page.show_snack_bar(ft.SnackBar(content=ft.Text("Actualización exitosa!"), bgcolor="green", duration=3000))
            except Exception as error:
                page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {e}"), bgcolor="red", duration=3000))

        def mostrar_datepicker_edit(e):
            """Abre el DatePicker para la edición de la fecha."""
            page.overlay.append(date_picker_edit)
            date_picker_edit.open = True
            page.update()

        def seleccionar_fecha_edit(e):
            """Actualiza la fecha seleccionada en el campo de texto."""
            fecha_seleccionada = date_picker_edit.value
            if fecha_seleccionada:
                fecha_solo = formato_fecha_usuario(str(fecha_seleccionada.date())) #fecha_seleccionada.date()
                txt_edit_fecha.current.value = fecha_solo #.strftime("%Y-%m-%d")
                date_picker_edit.open = False
                page.update()

        # Configuración del DatePicker
        date_picker_edit = ft.DatePicker(
            first_date=fecha_inicio,
            last_date=fecha_fin,
            current_date=datetime.datetime.strptime(registro_data[1], "%Y-%m-%d"),  # Fecha actual del registro
            on_change=seleccionar_fecha_edit
        )

        # Referencias para los TextField
        txt_edit_fecha = ft.Ref[ft.TextField]()
        txt_edit_horas35 = ft.Ref[ft.TextField]()
        txt_edit_horas100 = ft.Ref[ft.TextField]()
        txt_edit_nocturnas = ft.Ref[ft.TextField]()

        # Configuración del cuadro de diálogo de edición
        edit_dialog = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Registro"),
            content=ft.Column([
                ft.TextField(
                    ref=txt_edit_fecha,
                    label="Fecha",
                    value=formato_fecha_usuario(registro_data[1]),  # Fecha del registro
                    width=320,
                    on_click=mostrar_datepicker_edit,
                    read_only=True,
                ),
                ft.TextField(
                    ref=txt_edit_horas35,
                    label="Horas 35%",
                    value=registro_data[4],  # Horas 35%
                    width=320,
                    max_length=4,
                    input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$"),
                    on_change=format_hora
                ),
                ft.TextField(
                    ref=txt_edit_horas100,
                    label="Horas 100%",
                    value=registro_data[5],  # Horas 100%
                    width=320,
                    max_length=4,
                    input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$"),
                    on_change=format_hora
                ),
                ft.TextField(
                    ref=txt_edit_nocturnas,
                    label="Horas Nocturnas",
                    value=registro_data[6],  # Nocturnas
                    width=320,
                    max_length=4,
                    input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$"),
                    on_change=format_hora
                ),
            ]),
            actions=[
                ft.TextButton("Cancelar", on_click=close_dlg),
                ft.TextButton("Guardar", on_click=save_changes),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        # Mostrar el cuadro de diálogo
        page.dialog = edit_dialog
        edit_dialog.open = True
        page.update()


    
    # Get initial data for table
    registros = get_ultimos_registros()
    
    # Create table with data
    tabla_edicion = crear_tabla_edicion(registros, on_edit_click)
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def formato_fecha_usuario(fecha_str):
            """
            Convierte una fecha de formato 'YYYY-MM-DD' a 'DD-MMM-YYYY'.

            Args:
                fecha_str (str): Fecha en formato 'YYYY-MM-DD'.

            Returns:
                str: Fecha en formato 'DD-MMM-YYYY' si la conversión es exitosa, 
                        de lo contrario, devuelve la cadena original.
            """
            """Convierte fecha de YYYY-MM-DD a YYYYMMM-DD"""
            try:
                fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
                meses_abrev = {
                    1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR',
                    5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AGO',
                    9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DIC'
                }
                return f"{fecha.day:02d}-{meses_abrev[fecha.month]}-{fecha.year}"
            except ValueError:
                return fecha_str
            
    def formato_fecha_bd(fecha_str):
        """
        Convierte una fecha de formato 'DD-MMM-YYYY' a 'YYYY-MM-DD'.

        Args:
            fecha_str (str): Fecha en formato 'DD-MMM-YYYY'.

        Returns:
            str: Fecha en formato 'YYYY-MM-DD' si la conversión es exitosa, 
                    de lo contrario, devuelve la cadena original.
        """
        meses_abrev = {
            'ENE': 1, 'FEB': 2, 'MAR': 3, 'ABR': 4,
            'MAY': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8,
            'SEPT': 9, 'OCT': 10, 'NOV': 11, 'DIC': 12
        }
        try:
            dia, mes, año = fecha_str.split('-')
            fecha = datetime.datetime(int(año), meses_abrev[mes], int(dia))
            return fecha.strftime('%Y-%m-%d')
        except ValueError:
            return fecha_str
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
                            ft.TextField(width=320, ref=txt_fecha, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, read_only=True, value=formato_fecha_usuario(str(fecha_actual)), on_click=mostrar_datepicker, icon=ft.Icons.CALENDAR_MONTH),
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
                            ft.Text("Nocturna:", width=100),
                            ft.TextField(width=320, ref=txt_nocturnas, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=5, on_change=format_hora, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Hora 35%:", width=100),
                            ft.TextField(width=320, ref=txt_hora35, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=5, on_change=format_hora, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
                        ]),
                        ft.Row([
                            ft.Text("Hora 100%:", width=100),
                            ft.TextField(width=320, ref=txt_hora100, border=ft.border.all(2, ft.Colors.BLACK), border_radius=10, max_length=5, on_change=format_hora, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9:]*$", replacement_string="")),
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
    page.update()