from math import exp, trunc
import flet as ft
from database import connect_to_db
from queries import insertar_nueva_imagen
from flet import AppView, ScrollMode, ListView, Container, border
import datetime, os



# Definición de variables globales para la interfaz
lista_equipos = ft.ListView(expand=True)  # Esta línea se eliminará
imagen_frame = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO, alignment=ft.MainAxisAlignment.CENTER, width=300, expand=True)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
def filtrar_equipos_por_nombre(equipos_info, nombre_busqueda):
    # Filtrar equipos cuyo nombre contiene el criterio de búsqueda (insensible a mayúsculas)
    return [
        equipo for equipo in equipos_info
        if nombre_busqueda.lower() in equipo['nombre'].lower()
    ]

def cargar_equipos_filtrados(nombre_busqueda=""):
    equipos_info = obtener_informacion_equipos()  # Obtener información de los equipos
    
    # Filtrar los equipos si se proporcionó un criterio de búsqueda
    if nombre_busqueda:
        equipos_info = filtrar_equipos_por_nombre(equipos_info, nombre_busqueda)
    
    # Crear y devolver el DataTable con los equipos filtrados
    return crear_tabla_equipos(equipos_info)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

# Función para obtener equipos con imágenes
def obtener_informacion_equipos():
    conn = connect_to_db()  # Conectar a la base de datos
    cursor = conn.cursor()
    
    query = """
    SELECT
        e.idEquipo AS id,  -- Reincluir el idEquipo
        c.numeroContrato AS Contrato,
        u.nombres AS nombre,
        u.apellidos AS apellido,
        e.marca AS marca,
        e.modelo AS modelo,
        e.condicion AS condicion
    FROM 
        EquipoImagen ei
    JOIN 
        Equipo e ON ei.idEquipo = e.idEquipo
    JOIN 
        Usuario u ON e.idUsuario = u.idUsuario
    JOIN 
        Contrato c ON e.idEquipo = c.idEquipo  -- Relaciona el equipo con el contrato
    GROUP BY 
        c.numeroContrato, u.nombres, u.apellidos, e.marca, e.modelo, e.condicion, e.idEquipo  -- Asegúrate de agrupar por idEquipo
    ORDER BY 
        c.numeroContrato;  -- Ordenar por el número del contrato
    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()  # Obtener todos los resultados
    conn.close()  # Cerrar la conexión
    
    # Convertir resultados a un formato adecuado (lista de diccionarios)
    equipos_info = [{'id': row[0], 'Contrato': row[1], 'nombre': row[2], 
                     'apellido': row[3], 'marca': row[4], 
                     'modelo': row[5], 'condicion': row[6]} for row in resultados]
    return equipos_info

# Nueva función para crear un DataTable con la información de los equipos
def crear_tabla_equipos(equipos_info):
    columns = [
        ft.DataColumn(ft.Text("Contrato")),
        ft.DataColumn(ft.Text("Nombre")),
        ft.DataColumn(ft.Text("Apellido")),
        ft.DataColumn(ft.Text("Marca")),
        ft.DataColumn(ft.Text("Modelo")),
        ft.DataColumn(ft.Text("Condición")),
    ]
    
    rows = []
    for equipo in equipos_info:
        rows.append(ft.DataRow(cells=[
            ft.DataCell(ft.Text(equipo['Contrato'])),
            ft.DataCell(ft.Text(equipo['nombre'])),
            ft.DataCell(ft.Text(equipo['apellido'])),
            ft.DataCell(ft.Text(equipo['marca'])),
            ft.DataCell(ft.Text(equipo['modelo'])),
            ft.DataCell(ft.Text(equipo['condicion'])),
        ],
        on_long_press=lambda e, equipo=equipo: mostrar_imagenes(equipo)
                            ))
    
    data_table = ft.DataTable(
        columns=columns,
        rows=rows,
        border=ft.border.all(width=1, color=ft.colors.BLUE_GREY_200),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(width=1, color=ft.colors.BLUE_GREY_200),
    )
    
    return data_table

# Función para cargar equipos en el DataTable
def cargar_equipos():
    equipos_info = obtener_informacion_equipos()  # Obtener información de los equipos
    data_table = crear_tabla_equipos(equipos_info)  # Crear el DataTable
    return data_table  # Devolver el DataTable

# Función para obtener imágenes por equipo
def obtener_imagenes_por_equipo(equipo):
    conn = connect_to_db()  # Conectar a la base de datos
    cursor = conn.cursor()
    
    query = """
    SELECT rutaImagen FROM EquipoImagen WHERE idEquipo = ?;
    """
    
    cursor.execute(query, (equipo['id'],))
    resultados = cursor.fetchall()  # Obtener todas las imágenes
    conn.close()  # Cerrar la conexión
    
    # Convertir resultados a un formato adecuado (lista de diccionarios)
    imagenes = [{'rutaImagen': row[0]} for row in resultados]
    return imagenes

def mostrar_imagenes(equipo):
    imagenes = obtener_imagenes_por_equipo(equipo)  # Obtener imágenes por equipo
    imagen_frame.controls.clear()  # Limpiar imágenes anteriores
    for imagen in imagenes:
        # Asegúrate de que la ruta de la imagen sea correcta
        imagen_frame.controls.append(ft.Image(src=imagen['rutaImagen'], width=200, height=200))
    imagen_frame.update()  # Actualiza el contenedor para mostrar las imágenes
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------  

def image_panel(page: ft.Page):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 800
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.AUTO
    
    # Crear el DataTable y agregarlo a la interfaz
    data_table = cargar_equipos()  # Cargar equipos y obtener el DataTable
    
    # Crear un contenedor para las imágenes
    #imagen_frame = ft.Column(spacing=10, scroll=ft.ScrollMode.AUTO)  # Cambiado a Column para mostrar imágenes verticalmente

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------- 
    # Referencia para el campo de búsqueda
    campo_busqueda = ft.Ref[ft.TextField]()
    
    # Contenedor dinámico para la tabla
    contenedor_tabla = ft.Ref[ft.Column]()
    
    # Función para actualizar la tabla al buscar
    def actualizar_tabla(e):
        criterio = campo_busqueda.current.value
        tabla_actualizada = cargar_equipos_filtrados(criterio)
        contenedor_tabla.current.controls.clear()
        contenedor_tabla.current.controls.append(tabla_actualizada)
        page.update()

    # Inicialmente cargar todos los equipos
    data_table = cargar_equipos_filtrados()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------- 
    
    
    #Funcion para llamar al panel principal.
    def tab_insertar_contrato(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from contract import contract_panel
        contract_panel(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------    
    # funciones y control para abrir cuadro de dialogo para avisar al usuario que faltan datos en tab Registrar Usuario.
    # Función para abrir el cuadro de diálogo
    
    def open_dlg_modal(message):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Información"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Ok", on_click=lambda e: close_dlg(dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg_modal)  # Abre el cuadro de diálogo

    def close_dlg(dialog):
        page.close(dialog)  # Cierra el cuadro de diálogo
        #page.add(ft.Text("El cuadro de diálogo se cerró correctamente."))  # Mensaje opcional

    # Botón para abrir el cuadro de diálogo
    #page.add(ft.ElevatedButton("Mostrar Mensaje", on_click=lambda e: open_dlg_modal("Este es un mensaje de prueba.")))


    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Falta información"),
        content=ft.Text("Ha dejado algun campo vacío"),
        actions=[
                    ft.TextButton("Ok", on_click=lambda e: close_dlg(dlg_modal)),
                ],
        actions_alignment=ft.MainAxisAlignment.END,
    )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Función que se ejecuta al seleccionar los archivos
    # Variable para almacenar las rutas de las imágenes seleccionadas
    rutas_imagenes = []
    
    def previsualizar_imagenes(e):
        # Limpiar las imágenes previas
        imagenes_columna.controls.clear()
        rutas_imagenes.clear()  # Limpiar las rutas anteriores
    
        # Verificar si e.files no es None y tiene elementos
        if e.files and len(e.files) > 0:
            # Asegurarse de que solo se agreguen hasta 3 imágenes
            for i, file in enumerate(e.files[:3]):
                imagen = ft.Image(src=file.path, width=100, height=100)  # Ajustar tamaño de las imágenes
                imagenes_columna.controls.append(imagen)
                rutas_imagenes.append(file.path)  # Guardar la ruta del archivo
        else:
            open_dlg_modal("No se seleccionaron archivos.")  # Mostrar el mensaje en un cuadro de diálogo

        page.update()
        
    # Función para abrir el selector de archivos
    def abrir_selector_archivos(e):
        file_picker.pick_files(allow_multiple=True, allowed_extensions=["jpg", "png", "jpeg"]) # Abre el selector de archivos para seleccionar imágenes

    # Contenedor donde se mostrarán las imágenes seleccionadas
    imagenes_columna = ft.Row()  # Usamos Row para mostrar las imágenes en una fila

    # Crear el FilePicker para seleccionar imágenes
    file_picker = ft.FilePicker(on_result=previsualizar_imagenes)

    # Añadir el file_picker a la superposición de la página
    page.overlay.append(file_picker)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def obtener_ultimo_equipo():
        query = """
        SELECT TOP 1 idEquipo
            FROM Equipo
            ORDER BY idEquipo DESC
        """
        conexion = connect_to_db()
        with conexion.cursor() as cursor:
            cursor.execute(query)
            result = cursor.fetchone()
        return result if result else None
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Definir la carpeta donde se guardarán las imágenes
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))  # Obtiene el directorio del archivo actual
    IMAGES_FOLDER = os.path.join(BASE_DIR, '..', 'static', 'images')  # Ruta a static/images
    os.makedirs(IMAGES_FOLDER, exist_ok=True)  # Crea la carpeta si no existe
    
    PROYECTO = "Contratos_Flet"
    
    txt_id_equipo = ft.Ref[ft.TextField]()
    ultimo_equipo_id = obtener_ultimo_equipo()
    def agregar_imagen(e):
        try:
            id_equipo = txt_id_equipo.current.value
    
            # Validaciones iniciales
            if not id_equipo:
                raise ValueError("Debe proporcionar un ID de equipo.")
            if not rutas_imagenes or len(rutas_imagenes) == 0:
                raise ValueError("Debe cargar al menos una imagen.")
    
            # Obtener el último ID de equipo
            ultimo_equipo_id = obtener_ultimo_equipo()
            if not ultimo_equipo_id:
                raise ValueError(f"No se encontró un equipo con el ID {id_equipo}.")
    
            # Procesar e insertar imágenes con nombres basados en el número de contrato
            for idx, ruta_imagen in enumerate(rutas_imagenes):
                nombre_imagen = f"{ultimo_equipo_id}_{idx + 1}.jpg" if idx > 0 else f"{ultimo_equipo_id}.jpg"
                ruta_destino = os.path.join(IMAGES_FOLDER, nombre_imagen)  # Define IMAGES_FOLDER antes
                
                # Guardar la imagen en el sistema de archivos
                with open(ruta_imagen, "rb") as f:  # Usa la ruta del archivo
                    with open(ruta_destino, "wb") as out_file:  # Abre el archivo de destino
                        out_file.write(f.read())  # Guarda la imagen en el sistema de archivos
                
                
                 # Construir la ruta relativa con el prefijo del proyecto
                ruta_destino_con_prefijo = os.path.join(PROYECTO, 'static', 'images', nombre_imagen)
                
                # Inserta la imagen en la base de datos
                insertar_nueva_imagen(id_equipo, ruta_destino_con_prefijo)
                
                tab_insertar_contrato(e)
    
            # Notificar éxito al usuario
            snack_bar = ft.SnackBar(ft.Text("¡Imagen(es) agregadas exitosamente!"), duration=3000)
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()
    
            # Limpiar campos
            txt_id_equipo.current.value = ""
            imagenes_columna.controls.clear()  # Limpiar las imágenes cargadas
            rutas_imagenes.clear()  # Limpiar las rutas
            page.update()
    
        except ValueError as ve:
            # Manejo de errores específicos
            page.snack_bar = ft.SnackBar(ft.Text(f"Error: {ve}"), open=True, duration=3000)
            page.update()
    
        except Exception as error:
            # Manejo de errores generales
            page.snack_bar = ft.SnackBar(ft.Text(f"Error inesperado: {error}"), open=True, duration=3000)
            page.update()

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,
        
        # Contenedor de tabs
        tabs=[
            #Tab que contiene los controsles para el registro de las imagenes del equipos en la tabla Images.........
            ft.Tab(
                icon=ft.icons.IMAGE,
                text="Imágenes",
                content=ft.Column(
                    [
                        ft.Text("Guarda las Imágenes", size=20),
                        ft.TextField(label="ID",ref=txt_id_equipo, width=200,read_only=True, value=ultimo_equipo_id[0]),
                        ft.ElevatedButton(text="Seleccionar Imágenes", on_click=abrir_selector_archivos, width=200),
                        imagenes_columna,  # Aquí se mostrarán las imágenes
                        ft.ElevatedButton(text="Guardar", on_click=agregar_imagen, width=200),
                        ft.ElevatedButton(text="Contrato", on_click=tab_insertar_contrato, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
            ft.Tab(
                    icon=ft.icons.LIST,
                    text="Equipos con Imágenes",
                    content=ft.Row(
                        controls=[
                            ft.Column(
                                controls=[
                                    # TextField para ingresar el nombre
                                    ft.TextField(label="Buscar Nombre", icon=ft.icons.SEARCH, width=200, on_change=actualizar_tabla, ref=campo_busqueda),
                                    ft.Column(ref=contenedor_tabla, controls=[data_table]),  # Tabla inicial,
                                ],
                                expand=True,  # Hace que el data_table ocupe el espacio necesario
                            ),
                            ft.Column(
                                controls=[
                                    imagen_frame,
                                ],
                                expand=False,  # Hace que las imágenes ocupen solo el espacio requerido
                                alignment=ft.MainAxisAlignment.CENTER,
                            ),
                        ],
                        alignment=ft.MainAxisAlignment.START,  # Alineación horizontal
                        vertical_alignment=ft.CrossAxisAlignment.START,  # Alineación vertical
                        spacing=15,  # Espaciado entre columnas
                    )
                ),
            ],
            
            
    )
    page.add(mainTab)
    page.update()
