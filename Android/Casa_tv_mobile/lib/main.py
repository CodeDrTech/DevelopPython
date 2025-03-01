import flet as ft
import os


from core.database.backup import DatabaseBackup
from core.database.database import connect_to_database
from features.reports.finance_view import create_finance_view
from features.payments.vencimientos_view import create_vencimientos_view
def main(page: ft.Page):
    conn = connect_to_database()
    if conn:
        conn.close()
    
    page.title = "Casa TV Mobile"
    page.theme_mode = ft.ThemeMode.LIGHT
    page.padding = 0
    page.window.width = 400
    
    
    def drawer_selected(e):
        selected_index = e.control.selected_index
        if selected_index == 3:  # Index for Finanzas in drawer
            main_view.content = create_finance_view(page)
            page.drawer.open = False
            page.update()
        elif selected_index == 4:  # Índice para el nuevo botón de backup
            handle_backup(e)
            page.drawer.open = False
            page.update()
    
    main_view = ft.Container(padding=10)
    
    def open_drawer(e):
            page.drawer.open = True
            page.update()
    
    def show_message(message: str):
        snack = ft.SnackBar(
            content=ft.Text(message),
            duration=3000  # Increased duration to 10 seconds
        )
        page.overlay.append(snack)
        snack.open = True
        page.update()
    
    def show_share_dialog(backup_path: str):
        dlg = ft.AlertDialog(
            title=ft.Text("Backup Creado"),
            content=ft.Column(
                controls=[
                    ft.Text("¿Deseas compartir el backup?"),
                    ft.ElevatedButton(
                        text="Abrir para compartir",
                        icon=ft.icons.SHARE,
                        on_click=lambda _: page.launch_url(f"content://{backup_path}")
                    )
                ],
                spacing=10
            ),
            actions=[
                ft.TextButton(
                    text="Cerrar",
                    on_click=lambda e: close_dlg(e, dlg)
                )
            ]
        )
        page.dialog = dlg
        dlg.open = True
        page.update()

    def close_dlg(e, dlg):
        dlg.open = False
        page.update()
    
    def handle_backup(e):
        backup_manager = DatabaseBackup()
        success, result = backup_manager.create_backup()
        
        if success:
            backup_path = result.split("guardado en ")[-1]
            show_message("Backup creado exitosamente")
            show_share_dialog(os.path.join(backup_path, "database.db"))
        else:
            show_message(f"Error: {result}")
    
    # Create drawer with 4 additional menu items.
    page.drawer = ft.NavigationDrawer(
        controls=[
            ft.Container(
                content=ft.Column([
                    ft.Text("Casa TV", size=30, weight="bold"),
                    ft.Text("Menu de opciones")
                ]),
                padding=20,
                bgcolor=ft.Colors.BLUE_100
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.MAIL_OUTLINED,
                label="Envio de correos",
                selected_icon=ft.Icons.MAIL
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.STREAM_OUTLINED,
                label="Cuentas",
                selected_icon=ft.Icons.STREAM
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.SHOP_OUTLINED,
                label="Suplidores",
                selected_icon=ft.Icons.SHOP_SHARP
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.MONETIZATION_ON_OUTLINED,
                label="Finanzas",
                selected_icon=ft.Icons.MONETIZATION_ON
            ),
            ft.NavigationDrawerDestination(
                icon=ft.Icons.BACKUP_OUTLINED,
                label="Crear Backup",
                selected_icon=ft.Icons.BACKUP
            ),
        ],
        on_change=drawer_selected
    )

    # App bar with menu button
    page.appbar = ft.AppBar(
        leading=ft.IconButton(icon=ft.Icons.MENU, on_click=open_drawer),
        title=ft.Text("Casa TV Mobile"),
        bgcolor=ft.Colors.BLUE_500,
        color=ft.Colors.WHITE
    )
    
    
    def change_tab(e):
        selected_index = e.control.selected_index
        if selected_index == 0:            
            main_view.content = create_vencimientos_view(page)
            page.update()
        
    

    # Navegación inferior usando NavigationBar
    navigation = ft.NavigationBar(
        selected_index=0,
        destinations=[
            ft.NavigationBarDestination(
                icon=ft.Icons.HOME_OUTLINED,
                selected_icon=ft.Icons.HOME,
                label="Inicio",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PERSON_ADD_OUTLINED,
                selected_icon=ft.Icons.PERSON_ADD,
                label="Clientes",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.PAYMENT_ROUNDED,
                selected_icon=ft.Icons.PAYMENT,
                label="Pagos",
            ),
            ft.NavigationBarDestination(
                icon=ft.Icons.SUBSCRIPTIONS_OUTLINED,
                selected_icon=ft.Icons.SUBSCRIPTIONS,
                label="Suscrib.",
            ),
        ],
        on_change=change_tab
    )   
    main_view.content = create_vencimientos_view(page)
    
    page.add(
        ft.Column([
            ft.Container(
                content=main_view,
                expand=True
            ),
            navigation  # Navigation bar at the bottom
        ], spacing=0, expand=True)
    )
    page.update()

if __name__ == "__main__":
    ft.app(target=main)