import flet as ft
from database import connect_to_db
from queries import insertar_nuevo_equipo
from flet import AppView
import datetime


def equipment_panel(page: ft.Page):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 600
    page.window.resizable = True
    page.padding = 20
    #page.scroll = "auto" # type: ignore
    
    def tab_inserta_imagen(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from image import image_panel
        image_panel(page)
    
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

            if not id_usuario or not marca or not modelo or not condicion:
                open_dlg_modal(e)
            else:
                # Llama a la función de queries para insertar el equipo
                insertar_nuevo_equipo(id_usuario, marca, modelo, condicion)
                
                #Si el insert se realiza pasa el tab para ingresar datos sobre las imagenes.
                tab_inserta_imagen(e)


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
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,
        #scrollable=True,
        # Contenedor de tabs
        tabs=[
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
                        ft.ElevatedButton(text="Imagenes", on_click=tab_inserta_imagen, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)
    page.update()