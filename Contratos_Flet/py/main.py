import flet as ft
from database import connect_to_db
from flet import AppView
import datetime, time, subprocess

from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
import os


# Función para obtener los datos del query
def get_contract_list():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT
                ROW_NUMBER() OVER (ORDER BY c.fecha DESC) AS NumeroRegistro,
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
            ORDER BY c.numeroContrato DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

# Función para obtener un contrato específico
def get_contract_by_number(numero_contrato):
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            query = """
                SELECT
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
                    c.fecha           -- índice [10]
                FROM Usuario u
                INNER JOIN Equipo e ON u.idUsuario = e.idUsuario
                INNER JOIN Contrato c ON u.idUsuario = c.idUsuario AND e.idEquipo = c.idEquipo
                WHERE c.numeroContrato = ?
            """
            cursor.execute(query, (numero_contrato,))
            row = cursor.fetchone()
            conn.close()
            return row
        return None


def filter_contracts(search_text):
    all_contracts = get_contract_list()
    if not search_text:
        return all_contracts
    filtered_contracts = [
        contrato for contrato in all_contracts
        if search_text.lower() in contrato[1].lower() or  # Nombre
           search_text.lower() in contrato[2].lower() or  # Apellido
           search_text.lower() in contrato[3].lower()      # Cédula
    ]
    return filtered_contracts


def main(page: ft.Page):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 600
    page.window.resizable = True
    page.padding = 20
    page.scroll = "auto" # type: ignore

    #Funcion para generar los PDFs
    def generar_pdf_contrato(e, ultimo_registro=None):
            try:
                if not ultimo_registro:
                    snack_bar = ft.SnackBar(
                        ft.Text("Por favor seleccione un contrato de la lista"), 
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
                Condición: <b>{ultimo_registro[6] or 'N/A'}</b><br/><br/>
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
                    ft.Text(f"PDF del contrato generado y abierto exitosamente"), 
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
    # Función para manejar la selección de fila
    def on_select_row(num_contrato):        
        contrato_data = get_contract_by_number(num_contrato)
        if contrato_data:
            generar_pdf_contrato(None, contrato_data)  # Pasar None como evento            
        else:
            snack_bar = ft.SnackBar(
                ft.Text("No se encontró el contrato seleccionado"), 
                duration=3000
            )
            page.overlay.append(snack_bar)
            snack_bar.open = True
            page.update()

    
    # Crear tabla vacía primero
    tabla_contratos = ft.DataTable(
        columns=[],
        rows=[],
        border=ft.border.all(width=1, color=ft.colors.BLUE_GREY_200),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(width=1, color=ft.colors.BLUE_GREY_200),
        show_checkbox_column=True,
    )
    
    def actualizar_tabla(contracts):
        # Obtener datos
        contratos = get_contract_list()
        
        # Actualizar encabezados
        tabla_contratos.columns = [
            ft.DataColumn(ft.Text("#")),
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

        # Actualizar filas
        tabla_contratos.rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(str(contrato[0]))),
                    ft.DataCell(ft.Text(str(contrato[1]))),
                    ft.DataCell(ft.Text(str(contrato[2]))),
                    ft.DataCell(ft.Text(str(contrato[3]))),
                    ft.DataCell(ft.Text(str(contrato[4]))),
                    ft.DataCell(ft.Text(str(contrato[5]))),
                    ft.DataCell(ft.Text(str(contrato[6]))),
                    ft.DataCell(ft.Text(str(contrato[7]))),
                    ft.DataCell(ft.Text(str(contrato[8]))),
                    ft.DataCell(ft.Text(str(contrato[9]))),
                ],
                on_long_press=lambda e, num_contrato=contrato[8]: on_select_row(num_contrato),
                data=contrato[8]
            ) for contrato in contracts
        ]
        page.update()
        
    
    
    def buscar_contratos(e):
        # Obtener el texto ingresado por el usuario
        texto_busqueda = e.control.value.lower().strip()

        # Filtrar los contratos que coincidan con el nombre
        contratos_filtrados = [
            contrato for contrato in contratos
            if texto_busqueda in contrato[1].lower()  # Comparar con el nombre (índice 1)
        ]

        # Actualizar las filas del DataTable
        actualizar_tabla(contratos_filtrados)

        
    # Obtener datos iniciales
    contratos = get_contract_list()
    actualizar_tabla(contratos)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Modificar la creación de filas para incluir selección y datos
    filas = [
        ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(str(contrato[0]))),
                ft.DataCell(ft.Text(str(contrato[1]))),
                ft.DataCell(ft.Text(str(contrato[2]))),
                ft.DataCell(ft.Text(str(contrato[3]))),
                ft.DataCell(ft.Text(str(contrato[4]))),
                ft.DataCell(ft.Text(str(contrato[5]))),
                ft.DataCell(ft.Text(str(contrato[6]))),
                ft.DataCell(ft.Text(str(contrato[7]))),
                ft.DataCell(ft.Text(str(contrato[8]))),
                ft.DataCell(ft.Text(str(contrato[9]))),
            ],
            on_select_changed=lambda e: on_select_row(e),
            data=contrato[8]  # Guardamos el número de contrato
        ) for contrato in contratos
    ]    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

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

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Obtener datos para la tabla
    contratos = get_contract_list()

    # Crear encabezados
    encabezados = [
        ft.DataColumn(ft.Text("#")),
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
                ft.DataCell(ft.Text(str(contrato[0]))),  # Numero
                ft.DataCell(ft.Text(str(contrato[1]))),  # Nomre
                ft.DataCell(ft.Text(str(contrato[2]))),  # Apellido
                ft.DataCell(ft.Text(str(contrato[3]))),  # Cedula
                ft.DataCell(ft.Text(str(contrato[4]))),  # Empleado
                ft.DataCell(ft.Text(str(contrato[5]))),  # Marca
                ft.DataCell(ft.Text(str(contrato[6]))),  # Modelo
                ft.DataCell(ft.Text(str(contrato[7]))),  # Condicio
                ft.DataCell(ft.Text(str(contrato[8]))),  # NumeroContrato
                ft.DataCell(ft.Text(str(contrato[9]))),  # Fecha
            ]
        ) for contrato in contratos
    ]

    # Crear la tabla
    tabla_contratos = ft.DataTable(columns=encabezados, rows=filas, border=ft.border.all(width=1, color=ft.colors.BLUE_GREY_200), border_radius=10, vertical_lines=ft.border.BorderSide(width=1, color=ft.colors.BLUE_GREY_200))
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Funciones para abrir los modulos y sus controles 
    def tab_insertar_usuario(e):
        # En lugar de iniciar una nueva aplicación, limpiamos la página actual
        page.clean()

        # Importamos y ejecutamos la función y sus controles en la página actual
        from users import user_panel
        user_panel(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Funcion para manejar diferentes eventos al seleccionar algunos de los tab
    def cambio_tab(e):
        # El índice del tab seleccionado está en e.control.selected_index
        indice_seleccionado = e.control.selected_index
        
        # Aquí puedes agregar la lógica que necesites según el tab seleccionado
        if indice_seleccionado == 0:  # Tab Listado
            # Actualizar la lista de contratos
            contratos = get_contract_list()
            # Actualizar las filas de la tabla
            filas = [
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(str(contrato[0]))),  # Numero
                        ft.DataCell(ft.Text(str(contrato[1]))),  # Nomre
                        ft.DataCell(ft.Text(str(contrato[2]))),  # Apellido
                        ft.DataCell(ft.Text(str(contrato[3]))),  # Cedula
                        ft.DataCell(ft.Text(str(contrato[4]))),  # Empleado
                        ft.DataCell(ft.Text(str(contrato[5]))),  # Marca
                        ft.DataCell(ft.Text(str(contrato[6]))),  # Modelo
                        ft.DataCell(ft.Text(str(contrato[7]))),  # Condicio
                        ft.DataCell(ft.Text(str(contrato[8]))),  # NumeroContrato
                        ft.DataCell(ft.Text(str(contrato[9]))),  # Fecha
                    ]
                ) for contrato in contratos
            ]
            tabla_contratos.rows = filas
            page.update()
    
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,
        on_change=cambio_tab,
        #scrollable=True,
        
        
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
                                ft.TextField(label="Buscar Nombre", width=200, on_change=buscar_contratos),                                
                                # Botón de Buscar
                                ft.ElevatedButton(text="Buscar", icon=ft.icons.SEARCH),                                
                                # Botón de Imprimir
                                ft.ElevatedButton(text="Imprimir", icon=ft.icons.PRINT, on_click= lambda e: generar_pdf_contrato(e, None)),                                
                                # Botón de Nuevo
                                ft.ElevatedButton(text="Nuevo", icon=ft.icons.ADD, on_click=tab_insertar_usuario),
                            ],
                        ),
                        tabla_contratos
                    ],
                ),
            ),
        ],
    )
    # Actualizar la tabla con los datos
    actualizar_tabla(contratos)
    
    page.add(mainTab)
    page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#ft.app(main)
#ft.app(target=main, port=8080, view=AppView.WEB_BROWSER)