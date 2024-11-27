import flet as ft
from database import connect_to_db
from queries import insertar_nuevo_usuario, insertar_nuevo_equipo, insertar_nuevo_contrato
from flet import AppView
import datetime


# Función para obtener los datos del query
def get_contract_list():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT 
                u.nombres AS Nombre,
                u.apellidos AS Apellido,
                u.cedula AS Cedula,
                u.numeroEmpleado AS Empleado,
                e.marca AS Marca,
                e.modelo AS Modelo,
                e.condicion AS Condicion,
                c.numeroContrato AS NumeroContrato,
                FORMAT(c.fecha, 'dd/MM/yyyy') AS Fecha
            FROM Usuario u
            INNER JOIN Equipo e ON u.idUsuario = e.idUsuario
            INNER JOIN Contrato c ON u.idUsuario = c.idUsuario AND e.idEquipo = c.idEquipo
            ORDER BY c.fecha DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

def main(page: ft.Page):
    page.title = "Contratos"
    page.window.width =1080
    page.window.height = 600
    page.window.resizable = False
    
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Función que se ejecuta al seleccionar los archivos
    def previsualizar_imagenes(e):
        # Limpiar las imágenes previas
        imagenes_columna.controls.clear()
        # Asegurarse de que solo se agreguen hasta 3 imágenes
        for i, file in enumerate(e.files[:3]):
            imagen = ft.Image(src=file.path, width=100, height=100)  # Ajustar tamaño de las imágenes
            imagenes_columna.controls.append(imagen)
        page.update()
        
    # Función para abrir el selector de archivos
    def abrir_selector_archivos(e):
        file_picker.pick_files(allow_multiple=True) # Abre el selector de archivos para seleccionar imágenes

    # Contenedor donde se mostrarán las imágenes seleccionadas
    imagenes_columna = ft.Row()  # Usamos Row para mostrar las imágenes en una fila

    # Crear el FilePicker para seleccionar imágenes
    file_picker = ft.FilePicker(on_result=previsualizar_imagenes)

    # Añadir el file_picker a la superposición de la página
    page.overlay.append(file_picker)    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Codigo para insertar datos a la tabla Contrato mediante los controles del tab Contrato
    # Referencias para los campos de texto del tab Contrato
    txt_contrato = ft.Ref[ft.TextField]()
    txt_texto_contrato = ft.Ref[ft.TextField]()
    txt_id_usuario_contrato = ft.Ref[ft.TextField]()
    txt_id_equipo_contrato = ft.Ref[ft.TextField]()
    
    
    def agregar_contrato(e):
        try:
            numero_Contrato = txt_contrato.current.value
            texto_Contrato = txt_texto_contrato.current.value
            id_Usuario = txt_id_usuario_contrato.current.value
            id_Equipo = txt_id_equipo_contrato.current.value
            fecha_Contrato = fecha_actual

            # Llama a la función de queries
            insertar_nuevo_contrato(numero_Contrato, fecha_Contrato, texto_Contrato, id_Usuario, id_Equipo)

            # Muestra un snack_bar al usuario
            snack_bar = ft.SnackBar(ft.Text("¡Usuario agregado exitosamente!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()


            # Limpia los campos
            txt_contrato.current.value = ""
            txt_texto_contrato.current.value = ""
            txt_id_usuario_contrato.current.value = ""
            txt_id_equipo_contrato.current.value = ""
            page.update()

        except Exception as error:
            # Muestra un error en snack_bar
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {error}"), open=True, duration=3000)
            page.update()
    
    def mostrar_datepicker(e):
        page.overlay.append(date_picker_dialog)
        date_picker_dialog.open = True
        page.update()

    def seleccionar_fecha(e):
        fecha_actual = date_picker_dialog.value # Obtiene la fecha seleccionada del DatePicker.
        if fecha_actual:
            fecha_solo = fecha_actual.date() # Convierte a formato solo de fecha sin la hora.
            fecha_texto.value = f"               {fecha_solo}" # Actualiza el texto para mostrar la fecha seleccionada.
            date_picker_dialog.open = False # Cierra el diálogo configurando `open = False`.
            page.update() # Finalmente, actualiza la página para reflejar los cambios.

    # Inicializa la fecha actual y crea un texto para mostrar la fecha seleccionada.
    fecha_actual = datetime.date.today()
    fecha_texto = ft.Text(f"               {fecha_actual}")

    # Crea el DatePicker y establece que `seleccionar_fecha` se ejecutará cuando cambie la fecha seleccionada.
    date_picker_dialog = ft.DatePicker(
        on_change=seleccionar_fecha)
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

            # Llama a la función de queries
            insertar_nuevo_usuario(nombre, apellidos, cedula, numero_empleado)

            # Muestra un snack_bar al usuario
            snack_bar = ft.SnackBar(ft.Text("¡Usuario agregado exitosamente!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()


            # Limpia los campos
            txt_nombre.current.value = ""
            txt_apellidos.current.value = ""
            txt_cedula.current.value = ""
            txt_numero_empleado.current.hint_text = ""
            page.update()

        except Exception as error:
            # Muestra un error en snack_bar
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {error}"), open=True, duration=3000)
            page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Codigo para insertar datos a la tabla Equipo mediante los controles del tab Datos del Equipo
    # Referencias para los campos de texto del tab Datos de Equipo
    txt_id_usuario = ft.Ref[ft.TextField]()
    txt_marca = ft.Ref[ft.TextField]()
    txt_modelo = ft.Ref[ft.TextField]()
    rg_condicion = ft.Ref[ft.RadioGroup]()
    
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

            # Llama a la función de queries para insertar el equipo
            insertar_nuevo_equipo(id_usuario, marca, modelo, condicion)


            # Muestra un snack_bar al usuario
            snack_bar = ft.SnackBar(ft.Text("¡Equipo agregado exitosamente!"))
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
    # Obtener datos para la tabla
    contratos = get_contract_list()

    # Crear encabezados
    encabezados = [
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Apellido")),
        ft.DataColumn(ft.Text("Cedula")),
        ft.DataColumn(ft.Text("Empleado")),
        ft.DataColumn(ft.Text("Marca")),
        ft.DataColumn(ft.Text("Modelo")),
        ft.DataColumn(ft.Text("Condicion")),
        ft.DataColumn(ft.Text("Contrato")),
        ft.DataColumn(ft.Text("Fecha")),
    ]

    # Crear filas de la tabla
    filas = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(contrato[0]))),  # Nombre
                ft.DataCell(ft.Text(str(contrato[1]))),  # Apellido
                ft.DataCell(ft.Text(str(contrato[2]))),  # Cedula
                ft.DataCell(ft.Text(str(contrato[3]))),  # Empleado
                ft.DataCell(ft.Text(str(contrato[4]))),  # Marca
                ft.DataCell(ft.Text(str(contrato[5]))),  # Modelo
                ft.DataCell(ft.Text(str(contrato[6]))),  # Condicion
                ft.DataCell(ft.Text(str(contrato[7]))),  # NumeroContrato
                ft.DataCell(ft.Text(str(contrato[8]))),  # Fecha
            ]
        ) for contrato in contratos
    ]

    # Crear la tabla
    tabla_contratos = ft.DataTable(columns=encabezados, rows=filas, border=ft.border.all(width=1, color=ft.colors.BLUE_GREY_200), border_radius=10, vertical_lines=ft.border.BorderSide(width=1, color=ft.colors.BLUE_GREY_200))
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto
        animation_duration=300,
        expand=True,
        
        
        # Contenedor de tabs
        tabs=[
            #Tab con el listado de los contratos registraod.............................................
            ft.Tab(
                icon=ft.icons.FORMAT_LIST_NUMBERED,
                text="Listado",
                
                #Contenido de columnas que se muestran antes del DataTable con los datos de los contratos
                content=ft.Column(
                    [
                        ft.Text("Listado de Contratos", size=20),
                        
                        #Fila de controles para una busqueda filtrada por nombre.
                        ft.Row(
                            [
                                # TextField para ingresar el nombre
                                ft.TextField(label="Buscar Nombre", width=200),
                                
                                # Botón de Buscar
                                ft.ElevatedButton(text="Buscar"),
                                
                                # Botón de Imprimir
                                ft.ElevatedButton(text="Imprimir"),
                                
                                # Botón de Nuevo
                                ft.ElevatedButton(text="Nuevo"),
                            ],
                        ),
                        tabla_contratos
                    ],
                ),
            ),
            #Tab que contiene los controles para registrar a los usuarios en la tabla Usuario...........
            ft.Tab(
                icon=ft.icons.PERSON,
                text="Datos de Usuario",
                
                content=ft.Column(
                    [
                        ft.Text("Registrar Usuario", size=20),
                        ft.TextField(label="Nombre", ref=txt_nombre, width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Apellido", ref=txt_apellidos, width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Cedula", ref=txt_cedula, width=200, max_length=11, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.TextField(label="Codigo", ref=txt_numero_empleado,width=200, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.ElevatedButton(text="Guardar", on_click=agregar_usuario, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
            #Tab que contiene los controles para regisrar los datos del equipos en la tabla Equipo..................
            ft.Tab(
                icon=ft.icons.DEVICES,
                text="Datos del Equipo",
                
                content=ft.Column(
                    [
                        ft.Text("Registrar Equipo", size=20),
                        ft.TextField(label="ID",ref=txt_id_usuario, width=200,read_only=False),
                        ft.TextField(label="Marca",ref=txt_marca, width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Modelo",ref=txt_modelo, width=200, capitalization=ft.TextCapitalization.WORDS  ),
                        ft.Text("Condicion", width=200),
                        ft.RadioGroup(content=ft.Column([ft.Radio(value="Nuevo", label="Nuevo"), ft.Radio(value="Usado", label="Usado")]),ref=rg_condicion),
                        ft.ElevatedButton(text="Guardar", on_click=agregar_equipo, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
                
            ),
            #Tab que contiene los controsles para el registro de las imagenes del equipos en la tabla Images.........
            ft.Tab(
                icon=ft.icons.IMAGE,
                text="Imágenes",
                content=ft.Column(
                    [
                        ft.Text("Guarda las Imágenes", size=20),
                        ft.ElevatedButton(text="Seleccionar Imágenes", on_click=abrir_selector_archivos, width=200),
                        imagenes_columna,  # Aquí se mostrarán las imágenes
                        ft.ElevatedButton(text="Guardar", on_click=lambda _: print("Guardar imágenes"), width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
            #Tab que contiene los controles para el registro de los contratos en la tabla Contrato.................
            ft.Tab(
                icon=ft.icons.LIST,
                text="Contrato",
                content=ft.Column(
                    [
                        ft.Text("Registrar Contrato", size=20),
                        ft.TextField(label="Contrato", width=200, capitalization=ft.TextCapitalization.WORDS, ref=txt_contrato),
                        ft.TextField(label="Texto", width=200, capitalization=ft.TextCapitalization.WORDS, ref=txt_texto_contrato),
                        ft.TextField(label="Usuario", width=200,read_only=False, ref=txt_id_usuario_contrato),
                        ft.TextField(label="Equipo", width=200,read_only=False, ref=txt_id_equipo_contrato),    
                        fecha_texto,
                        ft.ElevatedButton(text="Fecha", icon=ft.icons.CALENDAR_MONTH, on_click=mostrar_datepicker, width=200),
                        ft.ElevatedButton(text="Guardar", on_click=agregar_contrato, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    page.update()
ft.app(main)
#ft.app(target=main, port=8080, view=AppView.WEB_BROWSER)