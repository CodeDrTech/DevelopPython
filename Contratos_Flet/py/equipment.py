import flet as ft
from database import connect_to_db
from queries import insertar_nuevo_equipo
from flet import AppView, ScrollMode
import datetime
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
# Función para obtener la lista de equipos registrados
# Se utiliza en la sección de equipos para mostrar los equipos existentes
# y en la sección de contratos para seleccionar un equipo
def get_equipment_list():
    # Conectamos a la base de datos
    conn = connect_to_db()
    if conn:
        # Creamos un cursor para realizar la consulta
        cursor = conn.cursor()
        # Creamos la consulta SQL
        query =  """
            SELECT DISTINCT
                u.idUsuario,
                u.nombres,
                u.apellidos,
                e.idEquipo,
                e.marca,
                e.modelo,
                e.condicion,
                e.imei
            FROM Equipo e
            INNER JOIN Usuario u ON e.idUsuario = u.idUsuario
            INNER JOIN Contrato c ON e.idEquipo = c.idEquipo AND e.idUsuario = c.idUsuario
            ORDER BY e.idEquipo DESC
        """
        # Ejecutamos la consulta
        cursor.execute(query)
        # Obtenemos los resultados
        rows = cursor.fetchall()
        # Cerramos la conexión
        conn.close()
        # Devolvemos los resultados
        return rows
    # Si no se puede conectar a la base de datos, devolvemos una lista vacía
    return []
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def actualizar_equipo(id_equipo, marca, modelo, imei, condicion):
    """
    Actualiza los datos de un equipo en la base de datos

    :param id_equipo: Identificador único del equipo
    :param marca: Marca del equipo
    :param modelo: Modelo del equipo
    :param imei: IMEI o serie del equipo
    :param condicion: Condición del equipo (nuevo o usado)
    :return: True si se actualizó correctamente, False en caso contrario
    """
    try:
        # Conectamos a la base de datos
        conn = connect_to_db()
        # Creamos un cursor para realizar la consulta
        cursor = conn.cursor()
        # Creamos la consulta SQL
        query = """
            UPDATE Equipo 
            SET marca = ?, modelo = ?, imei = ?, condicion = ?
            WHERE idEquipo = ?
        """
        # Ejecutamos la consulta
        cursor.execute(query, (marca, modelo, imei, condicion, id_equipo))
        # Confirmamos los cambios
        conn.commit()
        # Cerramos la conexión
        conn.close()
        # Devolvemos True para indicar que se actualizó correctamente
        return True
    except Exception as e:
        # Mostramos un mensaje de error si algo falla
        print(f"Error al actualizar equipo: {e}")
        # Devolvemos False para indicar que hubo un error
        return False
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

def mostrar_dialogo_edicion(e, equipo_data, on_update_callback):
    """
    Muestra un diálogo modal para editar los datos de un equipo.

    :param e: Instancia de la clase Principal
    :param equipo_data: Tupla con los datos del equipo a editar
    :param on_update_callback: Función a llamar cuando el usuario guarde los cambios
    """
    def guardar_cambios(e):
        """
        Guarda los cambios realizados en el diálogo modal y cierra el diálogo.

        :param e: Instancia de la clase Principal
        """
        if actualizar_equipo(
            equipo_data[3],  # idEquipo
            edit_marca.value,
            edit_modelo.value,
            edit_imei.value,
            edit_condicion.value
        ):
            dlg_modal.open = False
            e.page.update()
            # Llamar al callback para actualizar la vista
            if on_update_callback:
                on_update_callback(e)
            e.page.show_snack_bar(ft.SnackBar(content=ft.Text("Datos actualizados correctamente")))
        else:
            e.page.show_snack_bar(ft.SnackBar(content=ft.Text("Error al actualizar datos")))

    edit_marca = ft.TextField(label="Marca", value=equipo_data[4], on_submit=guardar_cambios, capitalization=ft.TextCapitalization.WORDS)
    edit_modelo = ft.TextField(label="Modelo", value=equipo_data[5], on_submit=guardar_cambios, capitalization=ft.TextCapitalization.WORDS)
    edit_imei = ft.TextField(label="IMEI/Serie", value=equipo_data[7], on_submit=guardar_cambios)
    edit_condicion = ft.Dropdown(
        label="Condición",
        value=equipo_data[6],
        options=[
            ft.dropdown.Option("Nuevo"),
            ft.dropdown.Option("Usado")
        ],
    )

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Editar Equipo"),
        content=ft.Column([
            edit_marca,
            edit_modelo,
            edit_imei,
            edit_condicion,
        ], tight=True),
        actions=[
            ft.TextButton("Cancelar", on_click=lambda e: setattr(dlg_modal, 'open', False)),
            ft.TextButton("Guardar", on_click=guardar_cambios),
        ],
    )

    e.page.dialog = dlg_modal
    dlg_modal.open = True
    e.page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

def get_user_list():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT TOP 1
                idUsuario,
                nombres,
                apellidos
            FROM Usuario
            ORDER BY idUsuario DESC
        """
        cursor.execute(query)
        row = cursor.fetchone()  # Usamos fetchone() en lugar de fetchall()
        conn.close()
        return row
    return None
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def equipment_panel(page: ft.Page, llamada: str):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 800
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.AUTO
    
    
    
    
    
    
    def tab_inserta_imagen(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from image import image_panel
        image_panel(page)
        
    # Funciones para abrir los modulos y sus controles 
    def regresar_a_usuarios(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from users import user_panel
        user_panel(page, "equipment")
    
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
    # Codigo para insertar datos a la tabla Equipo mediante los controles del tab Datos del Equipo
    # Referencias para los campos de texto del tab Datos de Equipo
    txt_id_usuario = ft.Ref[ft.TextField]()
    txt_marca = ft.Ref[ft.TextField]()
    txt_modelo = ft.Ref[ft.TextField]()
    rg_condicion = ft.Ref[ft.RadioGroup]()
    txt_imei = ft.Ref[ft.TextField]()
    
    
    
    def agregar_equipo(e):
        try:
            
            # Verificar que la referencia está inicializada
            if rg_condicion.current is None:
                raise ValueError("El control RadioGroup no está inicializado.")

            # Obtener el valor seleccionado
            condicion = rg_condicion.current.value
            if not condicion:
                raise ValueError("Debe seleccionar una condición para el equipo.")
            
            # Obtener los valores de los campos
            id_usuario = txt_id_usuario.current.value
            marca = txt_marca.current.value
            modelo = txt_modelo.current.value
            condicion = rg_condicion.current.value  # Obtener el valor del RadioGroup
            imei = txt_imei.current.value
            
            
            if not id_usuario or not marca or not modelo or not condicion:
                open_dlg_modal(e)
            else:
                # Llama a la función de queries para insertar el equipo
                insertar_nuevo_equipo(id_usuario, marca, modelo, condicion, imei)
                
                #Si el insert se realiza pasa el tab para ingresar datos sobre las imagenes.
                tab_inserta_imagen(e)


                # Muestra un snack_bar al usuario
                snack_bar = ft.SnackBar(ft.Text("¡Equipo agregado exitosamente!"), duration=3000)
                page.overlay.append(snack_bar)
                snack_bar.open = True
                page.update()

                # Limpia los campos
                txt_id_usuario.current.value = ""
                txt_marca.current.value = ""
                txt_modelo.current.value = ""
                rg_condicion.current.value = None  # Restablece la selección
                page.update()

        except ValueError as ve:
            # Manejo específico de validación
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ve}"), open=True, duration=3000)
            page.update()

        except Exception as error:
            # Muestra un error general en el snack_bar
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {error}"), open=True, duration=3000)
            page.overlay.append(page.snack_bar)
            page.update()
            
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Obtener datos del último usuario
    ultimo_usuario = get_user_list()

    #Aun no lo uso
    # Crear contenedor de información del usuario
    info_usuario = ft.Container(
        content=ft.Column([
            ft.Text("Último Usuario Registrado", size=16, weight=ft.FontWeight.BOLD),
            ft.Container(
                content=ft.Column([
                    ft.Text(f"ID: {ultimo_usuario[0]}", size=14) if ultimo_usuario else ft.Text("No hay usuarios registrados"),
                    ft.Text(f"Nombre: {ultimo_usuario[1]} {ultimo_usuario[2]}", size=14) if ultimo_usuario else ft.Text("")
                ]),
                border=ft.border.all(1, ft.colors.GREY_400),
                border_radius=10,
                padding=10
            )
        ]),
        padding=20,
        width=300  # Ancho fijo para el contenedor
    )

    # Actualiza la tabla de equipos con los datos actuales en la base de datos
    #
    # - Llama a la función get_equipment_list para obtener la lista de equipos
    # - Convierte cada equipo en una fila de la tabla (objeto DataRow)
    # - Cada celda (DataCell) tiene un Text con el valor correspondiente
    # - La celda de la columna de Acciones tiene un Row con un IconButton
    #   que cuando se hace clic llama a la función mostrar_dialogo_edicion
    #   pasando como argumento el equipo actual y la función actualizar_tabla_equipos
    #   como callback
    # - Finalmente, se actualiza la página para mostrar los cambios
    def actualizar_tabla_equipos(e=None):
        # Obtener la lista actualizada de equipos
        equipos = get_equipment_list()
        # Actualizar la tabla
        data_table.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(f"{equipo[1]} {equipo[2]}")),  # Nombre completo
                    ft.DataCell(ft.Text(equipo[4])),  # Marca
                    ft.DataCell(ft.Text(equipo[5])),  # Modelo
                    ft.DataCell(ft.Text(equipo[7] or "")),  # IMEI
                    ft.DataCell(ft.Text(equipo[6])),  # Condición
                    ft.DataCell(
                        ft.Row([
                            ft.IconButton(
                                icon=ft.icons.EDIT,
                                icon_color="blue400",
                                tooltip="Editar",
                                on_click=lambda e, eq=equipo: mostrar_dialogo_edicion(e, eq, actualizar_tabla_equipos)
                            )
                        ])
                    ),
                ]
            ) for equipo in equipos
        ]
        page.update()

    # Crea la tabla de datos
    # - columns: define las columnas de la tabla
    # - rows: almacena las filas de la tabla
    #      cada fila es un objeto DataRow con cells que es una lista de DataCell
    #      cada DataCell contiene un Text con el valor de la celda
    data_table = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Usuario")),
            ft.DataColumn(ft.Text("Marca")),
            ft.DataColumn(ft.Text("Modelo")),
            ft.DataColumn(ft.Text("IMEI/Serie")),
            ft.DataColumn(ft.Text("Condición")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        border=ft.border.all(width=1, color=ft.colors.BLUE_GREY_200),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(width=1, color=ft.colors.BLUE_GREY_200),
    )

    # Llamar a la función para cargar los datos inicialmente
    actualizar_tabla_equipos()
    
    
    #Funcion para avanzar al modulo de insertar imagen.
    def handle_siguiente_click(e):
        tab_inserta_imagen(e)
    
    #Boton para avanzar al modulo de insertar imagen desde el modulo de insertar equipo.
    #Solo estará habilitado si se retrocede desde el modulo insertar imagen cuando se quiere actualizar datos de equipo.
    btn_siguiente = ft.ElevatedButton(text="Siguiente", on_click=handle_siguiente_click, width=200, icon=ft.icons.ARROW_FORWARD)
    
    mainTab = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[
            ft.Tab(
                icon=ft.icons.DEVICES,
                text="Datos del equipo",
                #content=ft.Container(
                    content=ft.Column(
                        controls=[
                            # Fila con el título y la información del usuario
                            ft.Row(
                                controls=[
                                    ft.Text("Registre el equipo", size=20),
                                    ft.Text(f"Nombre: {ultimo_usuario[1]} {ultimo_usuario[2]}", size=14) if ultimo_usuario else ft.Text("")
                                ],                                
                                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                            ),
                            
                            # Columna con los controles del formulario.
                            ft.Container(
                                content=ft.Column(
                                    controls=[
                                        ft.TextField(label="ID", ref=txt_id_usuario, width=200, read_only=True, value=ultimo_usuario[0]),
                                        ft.TextField(label="Marca", ref=txt_marca, width=200,capitalization=ft.TextCapitalization.WORDS),
                                        ft.TextField(label="Modelo", ref=txt_modelo, width=200, capitalization=ft.TextCapitalization.WORDS),
                                        ft.TextField(label="IMEI/Serie", ref=txt_imei, width=200, capitalization=ft.TextCapitalization.WORDS),
                                        ft.Text("Condicion", width=200),
                                        ft.RadioGroup(
                                            content=ft.Row(
                                                controls=[
                                                            ft.Radio(value="Nuevo", label="Nuevo"),
                                                            ft.Radio(value="Usado", label="Usado")
                                                        ]
                                                            ),
                                                            ref=rg_condicion
                                        ),
                                        ft.Row(
                                            controls=[
                                                ft.ElevatedButton(text="Guardar", on_click=agregar_equipo, width=200),
                                                ft.ElevatedButton(text="Imagenes", on_click=tab_inserta_imagen, width=200),
                                                ft.ElevatedButton(text="Atras", tooltip="Regresa a usuarios", icon=ft.icons.ARROW_BACK, on_click=regresar_a_usuarios, width=200)
                                            ],
                                            spacing=20
                                        )
                                    ]
                                    
                                ),
                                padding=20
                            )
                        ]
                    ),
                    #padding=20
                #)
            ),
            ft.Tab(
                icon=ft.icons.LIST,
                text="Lista de equipos",
                content=ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text("Equipos registrados", size=20, weight=ft.FontWeight.BOLD),
                        ]),
                        data_table,
                        btn_siguiente,
                    ]),
                    padding=20
                )
            )
            
        ]
    )
    page.add(mainTab)    
    
    # Lógica para habilitar o deshabilitar controles según el módulo que llamó
    if llamada == "contract":
        
        # Establecer el índice de la pestaña activa
        mainTab.selected_index = 1
        
        # Deshabilitar controles de inserción si fue llamado desde el módulo de contratos
        txt_id_usuario.current.read_only = True
        txt_id_usuario.current.color = "red"
        txt_id_usuario.current.value = "Deshabilitado"
        
        txt_marca.current.read_only = True
        txt_marca.current.color = "red"
        txt_marca.current.value = "Deshabilitado"
        
        txt_modelo.current.read_only = True
        txt_modelo.current.color = "red"
        txt_modelo.current.value = "Deshabilitado"
        
        txt_imei.current.read_only = True
        txt_imei.current.color = "red"
        txt_imei.current.value = "Deshabilitado"
        
        rg_condicion.current.disabled = True  # Suponiendo que rg_condicion es un RadioGroup
    else:
        #Deshabilita el boton siguiente para que no avance si no se llenan los datos del usuario
        btn_siguiente.disabled = True
        
        
        txt_marca.current.focus()
    page.update()