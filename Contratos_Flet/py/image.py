from math import trunc
import flet as ft
from database import connect_to_db
from queries import insertar_nueva_imagen
from flet import AppView, ScrollMode, ListView, Container, border
import datetime, os



# Definición de variables globales para la interfaz
lista_equipos = ListView()  # Lista para mostrar equipos
imagen_frame = Container()   # Contenedor para mostrar imágenes

# Variables y referencias
txt_id_equipo = ft.Ref[ft.TextField]()
lista_equipos = ft.ListView(expand=True)
imagen_frame = ft.Row(spacing=10, scroll=ft.ScrollMode.AUTO)

# Función para obtener equipos con imágenes
def obtener_equipos_con_imagenes():
    conn = connect_to_db()  # Conectar a la base de datos
    cursor = conn.cursor()
    
    query = """
    SELECT e.idEquipo, e.marca
    FROM Equipo e
    JOIN EquipoImagen ei ON e.idEquipo = ei.idEquipo
    GROUP BY e.idEquipo, e.marca;

    """
    
    cursor.execute(query)
    resultados = cursor.fetchall()  # Obtener todos los resultados
    conn.close()  # Cerrar la conexión
    
    # Convertir resultados a un formato adecuado (lista de diccionarios)
    equipos = [{'id': row[0], 'nombre': row[1]} for row in resultados]
    return equipos

# Función para cargar equipos en el ListView
def cargar_equipos():
    equipos = obtener_equipos_con_imagenes()
    lista_equipos.controls.clear()
    for equipo in equipos:
        lista_equipos.controls.append(ft.ListTile(title=ft.Text(equipo["nombre"]), on_click=lambda e, equipo=equipo: mostrar_imagenes(equipo)))
    # Actualizar el componente SOLO después de que esté agregado al árbol
    lista_equipos.update()

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
    imagen_frame.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------  
def image_panel(page: ft.Page):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 600
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.AUTO
    
    global lista_equipos
    
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
    # Función que se ejecuta al seleccionar los archivos
    # Variable para almacenar las rutas de las imágenes seleccionadas
    rutas_imagenes = []
    
    def previsualizar_imagenes(e):
        # Limpiar las imágenes previas
        imagenes_columna.controls.clear()
        rutas_imagenes.clear()  # Limpiar las rutas anteriores
    
        # Asegurarse de que solo se agreguen hasta 3 imágenes
        for i, file in enumerate(e.files[:3]):
            imagen = ft.Image(src=file.path, width=100, height=100)  # Ajustar tamaño de las imágenes
            imagenes_columna.controls.append(imagen)
            rutas_imagenes.append(file.path)  # Guardar la ruta del archivo
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
                
                # Inserta la imagen en la base de datos
                insertar_nueva_imagen(id_equipo, ruta_destino)
                
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
                content=ft.Column(
                    [
                        ft.Text("Lista de Equipos", size=20),
                        lista_equipos,  # Usar la lista definida
                        ft.Text("Imágenes del equipo seleccionado:", size=16),
                        imagen_frame,    # Usar el contenedor definido
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                                ),
                )
            ],
            
            
    )
    page.add(mainTab)
    cargar_equipos()
    page.update()
