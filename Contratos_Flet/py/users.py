import flet as ft
from database import connect_to_db
from queries import insertar_nuevo_usuario
from flet import AppView, ScrollMode
import datetime, time

def actualizar_usuario(id_usuario, nombres, apellidos, cedula, numero_empleado):
    """
    Actualiza los datos de un usuario en la base de datos
    Recibe:
        id_usuario (int): Identificador del usuario
        nombres (str): Nombres del usuario
        apellidos (str): Apellidos del usuario
        cedula (str): C dula del usuario
        numero_empleado (str): N mero de empleado del usuario
    Retorna:
        bool: True si se actualiz  correctamente, False en caso contrario
    """
    try:
        conn = connect_to_db()
        cursor = conn.cursor()
        query = """
            UPDATE Usuario 
            SET nombres = ?, apellidos = ?, cedula = ?, numeroEmpleado = ?
            WHERE idUsuario = ?
        """
        cursor.execute(query, (nombres, apellidos, cedula, numero_empleado, id_usuario))
        conn.commit()
        conn.close()
        return True
    except Exception as e:
        print(f"Error al actualizar usuario: {e}")
        return False


def get_user_list():
    """
    Obtiene la lista de usuarios registrados
    Retorna:
        list: Lista de usuarios con sus respectivos datos
    """
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT idUsuario, nombres, apellidos, cedula, numeroEmpleado
            FROM Usuario
            ORDER BY idUsuario DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []


def user_panel(page: ft.Page):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 600
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.AUTO
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def mostrar_dialogo_edicion_usuario(e, usuario_data, on_update_callback):
        """
        Muestra un diálogo modal para editar los datos de un usuario.

        :param e: Instancia de la clase Principal
        :param usuario_data: Tupla con los datos del usuario a editar
        :param on_update_callback: Función a llamar cuando el usuario guarde los cambios
        """
        
        def format_cedula_edit(e):
            """
            Función específica para formatear la cédula en el diálogo de edición
            """
            # Quitar caracteres no numéricos
            raw = ''.join(filter(str.isdigit, e.control.value))
            
            # Aplicar formato deseado para la cédula (XXX-XXXXXXX-X)
            formatted = ''
            for i, char in enumerate(raw):
                if i == 3 or i == 10:  # Añadir guion después de la tercera y décima posición
                    formatted += '-'
                formatted += char
                
            # Actualizar el campo de texto directamente
            e.control.value = formatted
            e.control.update()
            
        def guardar_cambios(e):
            """
            Guarda los cambios realizados en el diálogo modal y cierra el diálogo.

            :param e: Instancia de la clase Principal
            """
            if actualizar_usuario(
                usuario_data[0],  # idUsuario
                edit_nombres.value,
                edit_apellidos.value,
                edit_cedula.value,
                edit_numero_empleado.value
            ):
                dlg_modal_edit.open = False
                e.page.update()
                if on_update_callback:
                    on_update_callback()
            else:
                e.page.show_snack_bar(
                    ft.SnackBar(content=ft.Text("Error al actualizar el usuario"))
                )

        edit_nombres = ft.TextField(
            label="Nombres",
            value=usuario_data[1],
            width=300,
            capitalization=ft.TextCapitalization.WORDS,
            on_submit=guardar_cambios
        )
        edit_apellidos = ft.TextField(
            label="Apellidos",
            value=usuario_data[2],
            width=300,
            capitalization=ft.TextCapitalization.WORDS,
            on_submit=guardar_cambios
        )
        edit_cedula = ft.TextField(
            label="Cédula",
            value=usuario_data[3],
            width=300,
            on_submit=guardar_cambios,
            on_change=format_cedula_edit,
            max_length=13,
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")
        )
        edit_numero_empleado = ft.TextField(
            label="Número de Empleado",
            value=usuario_data[4],
            width=300,
            on_submit=guardar_cambios,
            input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string="")
        )

        dlg_modal_edit = ft.AlertDialog(
            modal=True,
            title=ft.Text("Editar Usuario"),
            content=ft.Column(
                controls=[
                    edit_nombres,
                    edit_apellidos,
                    edit_cedula,
                    edit_numero_empleado,
                ],
                tight=True,
            ),
            actions=[
                ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg_modal_edit, 'open', False)),
                ft.TextButton("Guardar", on_click=guardar_cambios),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )

        e.page.dialog = dlg_modal_edit
        dlg_modal_edit.open = True
        e.page.update()

    def actualizar_lista_usuarios():
        """
        Actualiza la lista de usuarios en la interfaz

        Retorna:
            None
        """
        usuarios = get_user_list()
        tabla_usuarios.rows.clear()
        
        for usuario in usuarios:
            tabla_usuarios.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(usuario[1])),  # nombres
                        ft.DataCell(ft.Text(usuario[2])),  # apellidos
                        ft.DataCell(ft.Text(usuario[3])),  # cedula
                        ft.DataCell(ft.Text(usuario[4])),  # numero_empleado
                        ft.DataCell(
                            ft.Row(
                                controls=[
                                    ft.IconButton(
                                        icon=ft.icons.EDIT,
                                        icon_color="blue400",
                                        tooltip="Editar",
                                        data=usuario,
                                        on_click=lambda e: mostrar_dialogo_edicion_usuario(
                                            e, e.control.data, actualizar_lista_usuarios
                                        ),
                                    ),
                                ]
                            )
                        ),
                    ],
                )
            )
        page.update()

    # Crear tabla de usuarios
    tabla_usuarios = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombres")),
            ft.DataColumn(ft.Text("Apellidos")),
            ft.DataColumn(ft.Text("Cédula")),
            ft.DataColumn(ft.Text("Número de Empleado")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[]
    )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------  
    def tab_insertar_equipo(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from equipment import equipment_panel
        equipment_panel(page)
        
    def regresar_a_main(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from main import main
        main(page)
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
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------- 
    #Funcion para crear el formato a la cedula agragando giones
    def format_cedula(e):
        # Quitar caracteres no numéricos
        raw = ''.join(filter(str.isdigit, e.control.value))
        
        # Aplicar formato deseado para la cédula (XXX-XXXXXXX-X)
        formatted = ''
        for i, char in enumerate(raw):
            if i == 3 or i == 10:  # Añadir guion después de la tercera y décima posición
                formatted += f'-'
            formatted += char
            
        # Actualizar el campo de texto
        txt_cedula.current.value = formatted
        txt_cedula.current.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------- 
    # Codigo para insertar datos a la tabla usuario mediante los controles del tab Datos Usuario
    # Referencias para los campos de texto del tab Datos de Usuario
    txt_nombre = ft.Ref[ft.TextField]()
    txt_apellidos = ft.Ref[ft.TextField]()
    txt_cedula = ft.Ref[ft.TextField]()
    txt_numero_empleado = ft.Ref[ft.TextField]()
    def agregar_usuario(e):
        try:
            nombre = txt_nombre.current.value
            apellidos = txt_apellidos.current.value
            cedula = txt_cedula.current.value
            numero_empleado = txt_numero_empleado.current.value

            if not nombre or not apellidos or not cedula or not numero_empleado:
                open_dlg_modal(e)

            else:
                # Llama a la función de queries
                insertar_nuevo_usuario(nombre, apellidos, cedula, numero_empleado)
                
                #Si el insert se realiza pasa el tab para ingresar datos sobre el equipo.
                tab_insertar_equipo(e)

                # Muestra un snack_bar al usuario
                snack_bar = ft.SnackBar(ft.Text("¡Usuario agregado exitosamente!"), duration=3000)
                page.overlay.append(snack_bar)
                snack_bar.open = True
                page.update()


                # Limpia los campos
                txt_nombre.current.value = ""
                txt_apellidos.current.value = ""
                txt_cedula.current.value = ""
                txt_numero_empleado.current.value = ""
                page.update()

        except Exception as error:
            # Muestra un error en snack_bar
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {error}"), open=True, duration=3000)
            page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,
        #on_change=cambio_tab,
        #scrollable=True
        
        tabs=[
        #Tab que contiene los controles para registrar a los usuarios en la tabla Usuario...........
            ft.Tab(
                icon=ft.icons.PERSON,
                text="Datos del usuario",
                
                content=ft.Column(
                    [
                        ft.Text("Registre al usuario", size=20),
                        ft.TextField(label="Nombre", ref=txt_nombre, width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Apellido", ref=txt_apellidos, width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Cedula", ref=txt_cedula, width=200, max_length=13, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9-]*$", replacement_string=""), on_change=format_cedula),
                        ft.TextField(label="Codigo", on_submit=agregar_usuario, ref=txt_numero_empleado,width=200, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.ElevatedButton(text="Guardar", on_click=agregar_usuario, width=200),
                        ft.ElevatedButton(text="equipos", on_click=tab_insertar_equipo, width=200),
                        ft.ElevatedButton(text="Atras", tooltip="reguresa al menu principal", icon=ft.icons.ARROW_BACK, on_click=regresar_a_main, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
            # Nueva pestaña para lista de usuarios
            ft.Tab(
                icon=ft.icons.LIST,
                text="Lista de Usuarios",
                content=ft.Column(
                    controls=[
                        ft.Text("Usuarios Registrados", size=20, weight=ft.FontWeight.BOLD),
                        tabla_usuarios,
                    ],
                    scroll=ft.ScrollMode.AUTO,
                ),
            ),
        ],
    )
    # Inicializar la lista de usuarios
    actualizar_lista_usuarios()
    page.add(mainTab)
    #Lleva el foco el textFiled usuaro al cargar el formulario
    txt_nombre.current.focus()
    page.update()