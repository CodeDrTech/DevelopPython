import flet as ft
from database import connect_to_db
from queries import insertar_nueva_imagen
from flet import AppView
import datetime


def image_panel(page: ft.Page):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 600
    page.window.resizable = True
    page.padding = 20
    #page.scroll = "auto" # type: ignore
    
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
        file_picker.pick_files(allow_multiple=True, allowed_extensions=["jpg", "png", "jpeg"]) # Abre el selector de archivos para seleccionar imágenes

    # Contenedor donde se mostrarán las imágenes seleccionadas
    imagenes_columna = ft.Row()  # Usamos Row para mostrar las imágenes en una fila

    # Crear el FilePicker para seleccionar imágenes
    file_picker = ft.FilePicker(on_result=previsualizar_imagenes)

    # Añadir el file_picker a la superposición de la página
    page.overlay.append(file_picker)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def obtener_numero_contrato(id_equipo):
        query = """
        SELECT c.numeroContrato
        FROM Contrato c
        INNER JOIN Equipo e ON c.idEquipo = e.idEquipo
        WHERE e.idEquipo = ?
        """
        conexion = connect_to_db()
        with conexion.cursor() as cursor:
            cursor.execute(query, (id_equipo,))
            result = cursor.fetchone()
        return result[0] if result else None

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    txt_id_equipo = ft.Ref[ft.TextField]()

    def agregar_imagen(e):
        try:
            id_equipo = txt_id_equipo.current.value
            imagenes = imagenes_columna  # Asegúrate de que contenga las imágenes cargadas

            # Validaciones iniciales
            if not id_equipo:
                raise ValueError("Debe proporcionar un ID de equipo.")
            if not imagenes or len(imagenes) == 0:
                raise ValueError("Debe cargar al menos una imagen.")

            # Obtener el número de contrato asociado al idEquipo
            numero_contrato = obtener_numero_contrato(id_equipo)
            if not numero_contrato:
                raise ValueError(f"No se encontró un contrato asociado al ID de equipo {id_equipo}.")

            # Procesar e insertar imágenes con nombres basados en el número de contrato
            for idx, imagen in enumerate(imagenes):
                nombre_imagen = f"{numero_contrato}_{idx + 1}.jpg" if idx > 0 else f"{numero_contrato}.jpg"
                insertar_nueva_imagen(id_equipo, nombre_imagen, imagen)

            # Notificar éxito al usuario
            snack_bar = ft.SnackBar(ft.Text("¡Imagen(es) agregadas exitosamente!"))
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

            # Limpiar campos
            txt_id_equipo.current.value = ""
            imagenes_columna.clear()
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
                        ft.TextField(label="ID",ref=txt_id_equipo, width=200,read_only=False),
                        ft.ElevatedButton(text="Seleccionar Imágenes", on_click=abrir_selector_archivos, width=200),
                        imagenes_columna,  # Aquí se mostrarán las imágenes
                        ft.ElevatedButton(text="Guardar", on_click=agregar_imagen, width=200),
                        ft.ElevatedButton(text="Contrato", on_click=tab_insertar_contrato, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
            ],
    )
    page.add(mainTab)
    page.update()