import flet as ft
from database import connect_to_db
from queries import insertar_nuevo_contrato
from flet import AppView, ScrollMode
import datetime, time, subprocess


from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os

def get_last_records():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT TOP 1
                u.idUsuario,      -- índice [0]
                u.nombres,        -- índice [1]
                u.apellidos,      -- índice [2]
                e.idEquipo,       -- índice [3]
                e.marca,          -- índice [4]
                e.modelo,         -- índice [5]
                e.condicion,      -- índice [6]
                c.numeroContrato, -- índice [7]
                u.cedula,         -- índice [8]
                u.numeroEmpleado, -- índice [9]
                c.fecha,          -- índice [10]
                e.imei            -- índice [11]
            FROM            Usuario u
            LEFT JOIN      Equipo e ON u.idUsuario = e.idUsuario
            CROSS APPLY   (SELECT TOP 1 numeroContrato, fecha 
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
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.AUTO
    
    
    #Funcion para llamar al panel principal.
    def main_panel(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from main import main
        main(page)
        
    def regresar_a_equipos(e, tabs):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from equipment import equipment_panel
        equipment_panel(page, "contract")
    
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
    txt_id_usuario_contrato = ft.Ref[ft.TextField]()
    txt_id_equipo_contrato = ft.Ref[ft.TextField]()
    
    
    def agregar_contrato(e):
        try:
            numero_Contrato = txt_contrato.current.value
            id_Usuario = txt_id_usuario_contrato.current.value
            id_Equipo = txt_id_equipo_contrato.current.value
            fecha_Contrato = fecha_actual

            if not numero_Contrato or not id_Usuario or not id_Equipo:
                open_dlg_modal(e)
            else:
                # Llama a la función de queries
                insertar_nuevo_contrato(numero_Contrato, fecha_Contrato, id_Usuario, id_Equipo)
                
                #Genera el contrato en PDF
                generar_pdf_contrato(e)
                
                #Si el insert se realiza pasa el tab listado.
                main_panel(e)

                # Muestra un snack_bar al usuario
                snack_bar = ft.SnackBar(ft.Text("¡Contrato agregado exitosamente!"), duration=3000)
                page.overlay.append(snack_bar)
                snack_bar.open = True
                page.update()


                # Limpia los campos
                txt_contrato.current.value = ""
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
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

    def generar_pdf_contrato(e):
        try:
            ultimo_registro = get_last_records()
            if not ultimo_registro:
                snack_bar = ft.SnackBar(
                    ft.Text("No hay datos para generar el PDF"), 
                    duration=3000
                )
                page.overlay.append(snack_bar)
                snack_bar.open = True
                page.update()
                return

            pdf_path = os.path.abspath(f"Contratos_Flet/pdf/Contrato_{ultimo_registro[7]}.pdf")
            os.makedirs("Contratos_Flet/pdf", exist_ok=True)
            doc = SimpleDocTemplate(
                pdf_path,
                pagesize=letter,
                rightMargin=72,
                leftMargin=72,
                topMargin=72,
                bottomMargin=72
            )

            elementos = []
            estilos = getSampleStyleSheet()
            estilos.add(ParagraphStyle(
                name='Justificado',
                parent=estilos['Normal'],
                alignment=4,
                spaceAfter=12,
                fontSize=11
            ))

            # Título y fecha
            titulo = """
            <para align=center><b>CONTRATO DE ENTREGA DE EQUIPO TECNOLÓGICO</b></para>
            """
            elementos.append(Paragraph(titulo, estilos['Heading1']))
            elementos.append(Spacer(1, 12))

            info = f"""
            <para>
            Número de Contrato: {ultimo_registro[7]}<br/>
            Fecha: {ultimo_registro[10]}
            </para>
            """
            elementos.append(Paragraph(info, estilos['Normal']))
            elementos.append(Spacer(1, 12))

            # Partes del contrato
            partes = f"""
            <para>
            Entre <b>SELACT CORP</b>, con domicilio en [dirección de la empresa], en lo sucesivo denominada "La Empresa," 
            y el/la empleado(a) <b>{ultimo_registro[1]} {ultimo_registro[2]}</b>, identificado(a) con la cédula de identidad 
            <b>{ultimo_registro[8]}</b> y el código de empleado <b>{ultimo_registro[9]}</b>, en adelante denominado "El Empleado," 
            se acuerda lo siguiente:
            </para>
            """
            elementos.append(Paragraph(partes, estilos['Justificado']))
            elementos.append(Spacer(1, 12))

            # Cláusula Primera
            clausula_primera = f"""
            <para>
            <b>Cláusula Primera: Entrega del Equipo</b><br/><br/>
            La Empresa hace entrega a El Empleado del siguiente equipo tecnológico:<br/><br/>
            Marca: <b>{ultimo_registro[4] or 'N/A'}</b><br/>
            Modelo: <b>{ultimo_registro[5] or 'N/A'}</b><br/>
            Condición: <b>{ultimo_registro[6] or 'N/A'}</b><br/>
            IMEI/Serie: <b>{ultimo_registro[11] or 'N/A'}</b><br/><br/>
            El equipo entregado es propiedad de La Empresa y será utilizado exclusivamente para actividades relacionadas con sus funciones laborales.
            </para>
            """
            elementos.append(Paragraph(clausula_primera, estilos['Justificado']))
            elementos.append(Spacer(1, 12))

            # Cláusula Segunda
            clausula_segunda = """
            <para>
            <b>Cláusula Segunda: Obligaciones de El Empleado</b><br/><br/>
            El Empleado se compromete a:<br/><br/>
            • Utilizar el equipo de manera responsable y únicamente para los fines establecidos por La Empresa.<br/>
            • Cuidar el equipo y tomar todas las precauciones necesarias para evitar daños, pérdidas o deterioros.<br/>
            • No realizar modificaciones, reparaciones no autorizadas o transferir el equipo a terceros sin el consentimiento previo de La Empresa.<br/><br/>
            En caso de daños al equipo atribuibles a negligencia, mal uso o incumplimiento de estas obligaciones, El Empleado se compromete a cubrir los costos de reparación o reposición del equipo, según corresponda.
            </para>
            """
            elementos.append(Paragraph(clausula_segunda, estilos['Justificado']))
            elementos.append(Spacer(1, 12))

            # Cláusula Tercera
            clausula_tercera = """
            <para>
            <b>Cláusula Tercera: Responsabilidades de La Empresa</b><br/><br/>
            La Empresa se compromete a:<br/><br/>
            • Proveer el equipo en condiciones óptimas de funcionamiento.<br/>
            • Brindar el soporte técnico necesario para el mantenimiento preventivo y correctivo del equipo, siempre que el daño no sea atribuible a El Empleado.<br/>
            • Establecer las políticas internas aplicables a la gestión y uso del equipo tecnológico.
            </para>
            """
            elementos.append(Paragraph(clausula_tercera, estilos['Justificado']))
            elementos.append(Spacer(1, 12))

            # Cláusula Cuarta
            clausula_cuarta = """
            <para>
            <b>Cláusula Cuarta: Devolución del Equipo</b><br/><br/>
            El Empleado deberá devolver el equipo en las mismas condiciones en las que fue recibido, salvo el desgaste natural, en los siguientes casos:<br/><br/>
            • Al término de su relación laboral con La Empresa.<br/>
            • Cuando La Empresa lo solicite.<br/>
            • En caso de pérdida del equipo, El Empleado será responsable de cubrir el costo total de reposición.
            </para>
            """
            elementos.append(Paragraph(clausula_cuarta, estilos['Justificado']))
            elementos.append(Spacer(1, 12))

            # Cláusula Quinta y Firmas
            clausula_quinta = f"""
            <para>
            <b>Cláusula Quinta: Aceptación del Contrato</b><br/><br/>
            Ambas partes declaran que han leído y comprendido el contenido de este contrato, aceptando sus términos y condiciones.
            </para>
            """
            elementos.append(Paragraph(clausula_quinta, estilos['Justificado']))
            elementos.append(Spacer(1, 24))

            # Firmas centradas
            firmas = f"""
            <para align=center>
            
            __________________________<br/>
            Representante autorizado<br/>
            <b>SELACT CORP</b><br/><br/><br/><br/>
            
            
            __________________________<br/>
            <b>{ultimo_registro[1]} {ultimo_registro[2]}</b>
            </para>
            """
            elementos.append(Paragraph(firmas, estilos['Normal']))

            doc.build(elementos)
            
            time.sleep(1)
                
            # Abrir el PDF después de generarlo
            subprocess.Popen([pdf_path], shell=True)
            
            snack_bar = ft.SnackBar(
                ft.Text(f"PDF del contrato generado exitosamente"), 
                duration=3000
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

        except Exception as error:
            snack_bar = ft.SnackBar(
                ft.Text(f"Error al generar PDF: {str(error)}"), 
                duration=3000
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
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
                                        on_submit =     agregar_contrato,
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
                                    ft.ElevatedButton(
                                        text=           "PDF",
                                        on_click=       generar_pdf_contrato,
                                        width=          200
                                    ),
                                    ft.ElevatedButton(text="Atras", tooltip="Regresar a equipos", icon=ft.icons.ARROW_BACK, on_click=lambda e: regresar_a_equipos(e), width=200),
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
    page.update()