import flet as ft
from database import connect_to_db
from flet import AppView
import datetime


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
            ORDER BY c.fecha DESC
        """
        cursor.execute(query)
        rows = cursor.fetchall()
        conn.close()
        return rows
    return []

def main(page: ft.Page):
    page.title = "Contratos"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 600
    page.window.resizable = True
    page.padding = 20
    page.scroll = "auto" # type: ignore    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

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
                                ft.TextField(label="Buscar Nombre", width=200),                                
                                # Botón de Buscar
                                ft.ElevatedButton(text="Buscar"),                                
                                # Botón de Imprimir
                                ft.ElevatedButton(text="Imprimir"),                                
                                # Botón de Nuevo
                                ft.ElevatedButton(text="Nuevo", on_click=tab_insertar_usuario),
                            ],
                        ),
                        tabla_contratos
                    ],
                ),
            ),
        ],
    )
    page.add(mainTab)
    page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------

#ft.app(main)
#ft.app(target=main, port=8080, view=AppView.WEB_BROWSER)