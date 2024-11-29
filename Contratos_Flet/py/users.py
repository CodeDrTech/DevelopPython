import flet as ft
from database import connect_to_db
from queries import insertar_nuevo_usuario
from flet import AppView
import datetime


def user_panel(page: ft.Page):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 600
    page.window.resizable = True
    page.padding = 20
    #page.scroll = "auto" # type: ignore
    
    
    
    def tab_insertar_equipo(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from equipment import equipment_panel
        equipment_panel(page)
    
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
                snack_bar = ft.SnackBar(ft.Text("¡Usuario agregado exitosamente!"))
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
                text="Datos de Usuario",
                
                content=ft.Column(
                    [
                        ft.Text("Registrar Usuario", size=20),
                        ft.TextField(label="Nombre", ref=txt_nombre, width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Apellido", ref=txt_apellidos, width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Cedula", ref=txt_cedula, width=200, max_length=11, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.TextField(label="Codigo", ref=txt_numero_empleado,width=200, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.ElevatedButton(text="Guardar", on_click=agregar_usuario, width=200),
                        ft.ElevatedButton(text="equipos", on_click=tab_insertar_equipo, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)
    page.update()