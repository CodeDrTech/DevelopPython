import flet as ft
from backend.database import get_all_users

def UsuariosView():
    # Obtener datos de usuarios
    data = get_all_users()
    rows = [ft.DataRow(cells=[
        ft.DataCell(ft.Text(str(row.idUsuario))),
        ft.DataCell(ft.Text(row.nombres)),
        ft.DataCell(ft.Text(row.apellidos)),
        ft.DataCell(ft.Text(row.cedula or "N/A")),
        ft.DataCell(ft.Text(row.numeroEmpleado or "N/A")),
    ]) for row in data]

    return ft.View(
        "/usuarios",
        controls=[
            ft.AppBar(title=ft.Text("Usuarios")),
            ft.DataTable(
                columns=[
                    ft.DataColumn(ft.Text("ID")),
                    ft.DataColumn(ft.Text("Nombres")),
                    ft.DataColumn(ft.Text("Apellidos")),
                    ft.DataColumn(ft.Text("Cédula")),
                    ft.DataColumn(ft.Text("N° Empleado")),
                ],
                rows=rows
            )
        ]
    )
