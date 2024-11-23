import flet as ft
from database import connect_to_db


# Función para obtener los datos del query
def get_contract_list():
    conn = connect_to_db()
    if conn:
        cursor = conn.cursor()
        query = """
            SELECT 
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
    page.window.width =1050
    page.window.height = 600
    
    
    # Obtener datos para la tabla
    contratos = get_contract_list()

    # Crear encabezados
    encabezados = [
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
                ft.DataCell(ft.Text(str(contrato[0]))),  # Nombre
                ft.DataCell(ft.Text(str(contrato[1]))),  # Apellido
                ft.DataCell(ft.Text(str(contrato[2]))),  # Cedula
                ft.DataCell(ft.Text(str(contrato[3]))),  # Empleado
                ft.DataCell(ft.Text(str(contrato[4]))),  # Marca
                ft.DataCell(ft.Text(str(contrato[5]))),  # Modelo
                ft.DataCell(ft.Text(str(contrato[6]))),  # Condicion
                ft.DataCell(ft.Text(str(contrato[7]))),  # NumeroContrato
                ft.DataCell(ft.Text(str(contrato[8]))),  # Fecha
            ]
        ) for contrato in contratos
    ]

    # Crear la tabla
    tabla_contratos = ft.DataTable(columns=encabezados, rows=filas)



    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto
        animation_duration=300,
        expand=True,
        
        # Contenedor de tabs
        tabs=[
            #Tab con el listado de los contratos registraod.............................................
            ft.Tab(
                icon=ft.icons.FORMAT_LIST_NUMBERED,
                text="Listado",
                content=ft.Column(
                    [
                        ft.Text("Listado de Contratos", size=20),
                        tabla_contratos
                    ]
                ),
            ),
            #Tab que contiene los controles para registrar a los usuarios en la tabla Usuario...........
            ft.Tab(
                icon=ft.icons.VERIFIED_USER_OUTLINED,
                text="Datos de Usuario",
                content=ft.Column(
                    [
                        ft.Text("Registrar Usuario"),
                        ft.TextField(label="Nombre", width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Apellido", width=200, capitalization=ft.TextCapitalization.WORDS),
                        ft.TextField(label="Cedula", width=200, max_length=11, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.TextField(label="Codigo", width=200, input_filter=ft.InputFilter(allow=True, regex_string=r"^[0-9]*$", replacement_string="")),
                        ft.ElevatedButton(text="Guardar", on_click=lambda _: print("Buscar")),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=10,
                ),
            ),
            #Tab que contiene los controles para regisrar los datos del equipos en la tabla Equipo..................
            ft.Tab(
                icon=ft.icons.DEVICES,
                text="Datos del Equipo",
                content=ft.Container(
                    content=ft.Text("Datos del Equipo", size=20),
                    padding=20,
                ),
            ),
            #Tab que contiene los controsles para el registro de las imagenes del equipos en la tabla Images.........
            ft.Tab(
                icon=ft.icons.IMAGE,
                text="Imágenes",
                content=ft.Container(
                    content=ft.Text("Imágenes", size=20),
                    padding=20,
                ),
            ),#Tab que contiene los controles para el registro de los contratos en la tabla Contrato.................
            ft.Tab(
                icon=ft.icons.LIST,
                text="Contrato",
                content=ft.Container(
                    content=ft.Text("Contrato", size=20),
                    padding=20,
                ),
            ),
        ],
    )

    page.add(mainTab)
    page.update()

ft.app(main)