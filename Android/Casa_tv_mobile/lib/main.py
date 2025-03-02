import flet as ft
import os


from core.database.backup import DatabaseBackup
from core.database.database import connect_to_database
from features.finance.finance_view import create_finance_view
from features.expirations.vencimientos_view import create_vencimientos_view
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
        if selected_index == 3:  # Index for Finanzas in drawer.
            main_view.content = create_finance_view(page)
            page.drawer.open = False
            page.update()
        
    
    main_view = ft.Container(padding=10)
    
    def open_drawer(e):
            page.drawer.open = True
            page.update()
    
    
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