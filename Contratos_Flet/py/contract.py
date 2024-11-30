import flet as ft
from database import connect_to_db
from queries import insertar_nuevo_contrato
from flet import AppView
import datetime

def get_last_ids():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT TOP 1
                u.idUsuario,
                e.idEquipo
            FROM Usuario u
            CROSS APPLY (
                SELECT TOP 1 idEquipo
                FROM Equipo
                ORDER BY idEquipo DESC
            ) e
            ORDER BY u.idUsuario DESC
        """
        cursor.execute(query)
        row = cursor.fetchone()
        conn.close()
        return row
    return None

def contract_panel(page: ft.Page):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 600
    page.window.resizable = True
    page.padding = 20
    #page.scroll = "auto" # type: ignore
    
    def main_panel(e):
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

            if not numero_Contrato or not texto_Contrato or not id_Usuario or not id_Equipo:
                open_dlg_modal(e)
            else:
                # Llama a la función de queries
                insertar_nuevo_contrato(numero_Contrato, fecha_Contrato, texto_Contrato, id_Usuario, id_Equipo)
                
                #Si el insert se realiza pasa el tab listado.
                main_panel(e)

                # Muestra un snack_bar al usuario
                snack_bar = ft.SnackBar(ft.Text("¡Contrato agregado exitosamente!"), duration=3000)
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
        # Abre el diálogo del DatePicker para que el usuario seleccione una fecha.
        page.overlay.append(date_picker_dialog)
        date_picker_dialog.open = True
        page.update()

    def seleccionar_fecha(e):
        # Obtiene la fecha seleccionada del DatePicker.
        fecha_actual = date_picker_dialog.value
        if fecha_actual:
            # Convierte a formato solo de fecha sin la hora.
            fecha_solo = fecha_actual.date()
            # Actualiza el texto para mostrar la fecha seleccionada.
            fecha_texto.value = f"               {fecha_solo}"
            # Cierra el diálogo configurando `open = False`.
            date_picker_dialog.open = False
            # Finalmente, actualiza la página para reflejar los cambios.
            page.update()

    # Inicializa la fecha actual y crea un texto para mostrar la fecha seleccionada.
    fecha_actual = datetime.date.today()
    fecha_texto = ft.Text(f"               {fecha_actual}")

    # Crea el DatePicker y establece que `seleccionar_fecha` se ejecutará cuando cambie la fecha seleccionada.
    date_picker_dialog = ft.DatePicker(
        on_change=seleccionar_fecha)
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Extrae los id del usuario y equipo recien insertados a la base de dato.
    ultimos_ids = get_last_ids()
    
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,
        #scrollable=True,
        
        
        # Contenedor de tabs
        tabs=[#Tab que contiene los controles para el registro de los contratos en la tabla Contrato.................
            ft.Tab(
                icon=ft.icons.LIST,
                text="Contrato",
                content=ft.Column(
                    [
                        ft.Text("Registre el equipo", size=20),
                        ft.TextField(label="Contrato", width=200, capitalization=ft.TextCapitalization.CHARACTERS, ref=txt_contrato),
                        ft.TextField(label="Texto", width=200, capitalization=ft.TextCapitalization.WORDS, ref=txt_texto_contrato),
                        ft.TextField(label="Usuario", width=200,read_only=True, ref=txt_id_usuario_contrato, value=ultimos_ids[0]),
                        ft.TextField(label="Equipo", width=200,read_only=True, ref=txt_id_equipo_contrato, value=ultimos_ids[1]),    
                        fecha_texto,
                        ft.ElevatedButton(text="Fecha", icon=ft.icons.CALENDAR_MONTH, on_click=mostrar_datepicker, width=200),
                        ft.ElevatedButton(text="Guardar", on_click=agregar_contrato, width=200),
                        ft.ElevatedButton(text="Listado", on_click=main_panel, width=200),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)
    txt_contrato.current.focus()
    page.update()