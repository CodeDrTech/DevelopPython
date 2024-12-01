import flet as ft
from database import connect_to_db
from queries import insertar_nuevo_contrato
from flet import AppView
import datetime

def get_last_records():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT TOP 1
                u.idUsuario,
                u.nombres,
                u.apellidos,
                e.idEquipo,
                e.marca,
                e.modelo,
                e.condicion,
                c.numeroContrato
            FROM            Usuario u
            LEFT JOIN      Equipo e ON u.idUsuario = e.idUsuario
            CROSS APPLY   (SELECT TOP 1 numeroContrato 
                          FROM   Contrato 
                          ORDER  BY idContrato DESC) c
            ORDER BY      u.idUsuario DESC
        """
        cursor.execute(query)
        row = cursor.fetchone()
        conn.close()
        return row
    return None

#Funcion para generar el numero de contrato siguiente SL00001+1=SL00002
def incrementar_numero_contrato(ultimo_contrato=None):
    try:
        # Si no hay contrato previo o es None, empezar con SL00001
        if not ultimo_contrato:
            return "SL00001"
            
        # Si hay contrato previo, incrementar
        letras = ''.join(filter(str.isalpha, ultimo_contrato))  # Obtiene "SL"
        numeros = ''.join(filter(str.isdigit, ultimo_contrato)) # Obtiene "00012"
        
        siguiente_numero = int(numeros) + 1
        nuevo_numero = str(siguiente_numero).zfill(len(numeros))
        nuevo_contrato = f"{letras}{nuevo_numero}"
        
        return nuevo_contrato
        
    except Exception as e:
        print(f"Error al incrementar número de contrato: {e}")
        return "SL00001"  # En caso de error, también empezar con SL00001

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
    # Obtener todos los últimos registros
    ultimo_registro = get_last_records()
    
    if not ultimo_registro[7]:
        Siguiente_contrato = "SL00000"
    else:
        Siguiente_contrato = incrementar_numero_contrato(ultimo_registro[7])
        
    #Siguiente_contrato = incrementar_numero_contrato(ultimos_registros[2] if ultimos_registros else "SL00000")
    
    mainTab = ft.Tabs(
        selected_index=    0,
        animation_duration=300,
        expand=           True,
        tabs=[
            ft.Tab(
                icon=    ft.icons.LIST,
                text=    "Contrato",
                content= ft.Column(
                    controls=[
                        # Fila con el título y la información del usuario y equipo
                        ft.Row(
                            controls=[
                                ft.Text("Registre el Contrato", size=20),
                                ft.Column([
                                    ft.Text(f"Nombre: {ultimo_registro[1]} {ultimo_registro[2]}", size=14) if ultimo_registro else ft.Text(""),
                                    ft.Text(f"Equipo: {ultimo_registro[4]} {ultimo_registro[5]} {ultimo_registro[6]}", size=14) if ultimo_registro and ultimo_registro[4] else ft.Text("")
                                ])
                            ],                                
                            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        ),
                        
                        # Columna con los controles del formulario
                        ft.Container(
                            content=ft.Column(
                                controls=[
                                    ft.TextField(
                                        label=          "Contrato",
                                        ref=            txt_contrato,
                                        width=          200,
                                        capitalization= ft.TextCapitalization.CHARACTERS,
                                        value=          Siguiente_contrato
                                    ),
                                    ft.TextField(
                                        label=          "Texto",
                                        ref=            txt_texto_contrato,
                                        width=          200,
                                        capitalization= ft.TextCapitalization.WORDS
                                    ),
                                    ft.TextField(
                                        label=          "Usuario",
                                        ref=            txt_id_usuario_contrato,
                                        width=          200,
                                        read_only=      True,
                                        value=          ultimo_registro[0] if ultimo_registro else ""
                                    ),
                                    ft.TextField(
                                        label=          "Equipo",
                                        ref=            txt_id_equipo_contrato,
                                        width=          200,
                                        read_only=      True,
                                        value=          ultimo_registro[3] if ultimo_registro else ""
                                    ),
                                    fecha_texto,
                                    ft.ElevatedButton(
                                        text=           "Fecha",
                                        icon=           ft.icons.CALENDAR_MONTH,
                                        on_click=       mostrar_datepicker,
                                        width=          200
                                    ),
                                    ft.ElevatedButton(
                                        text=           "Guardar",
                                        on_click=       agregar_contrato,
                                        width=          200
                                    ),
                                    ft.ElevatedButton(
                                        text=           "Listado",
                                        on_click=       main_panel,
                                        width=          200
                                    ),
                                ],
                                spacing=    15,
                                alignment= ft.MainAxisAlignment.START
                            )
                        )
                    ]
                )
            )
        ]
    )
    page.add(mainTab)
    txt_texto_contrato.current.focus()
    page.update()