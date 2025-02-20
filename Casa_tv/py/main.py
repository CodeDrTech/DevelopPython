import flet as ft
from tabs.vencimientos_tab import crear_tabla_vencimientos
from tabs.clientes_tab import crear_tabla_clientes
from tabs.pagos_tab import crear_tab_pagos
from tabs.suscripciones_tab import crear_tab_suscripciones

def main(page: ft.Page):
    page.title = "TV en casa  Ver.20250216"
    page.window.alignment = ft.alignment.center
    page.window.width = 1300
    page.window.height = 800
    page.window.resizable = False
    page.padding = 20
    page.scroll = "adaptive"
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT

    # First create empty mainTab
    mainTab = ft.Tabs(
        selected_index=0,
        animation_duration=300,
        expand=True,
        tabs=[]
    )

    # Create vencimientos content
    vencimientos_content = crear_tabla_vencimientos(page)
    
    # Create clientes content
    clientes_content = crear_tabla_clientes(page, mainTab)
    
    # Create pagos content
    pagos_content = crear_tab_pagos(page, mainTab)
    
    # Create suscripciones content
    suscripciones_content = crear_tab_suscripciones(page, mainTab)

    # Create and add all tabs
    tabs_list = [
        ft.Tab(
            icon=ft.Icons.HOME,
            text="Vencimientos",
            content=vencimientos_content
        ),
        ft.Tab(
            icon=ft.Icons.PERSON_ADD,
            text="Clientes",
            content=clientes_content
        ),
        ft.Tab(
            icon=ft.Icons.PAYMENT,
            text="Aplicar Pagos",
            content=pagos_content
        ),
        ft.Tab(
            icon=ft.Icons.SUBSCRIPTIONS,
            text="Suscripciones",
            content=suscripciones_content
        ),
        ft.Tab(
            icon=ft.Icons.MAIL,
            text="Envio de correos",
        ),
        ft.Tab(
            text="Cuentas",
            icon=ft.Icons.STREAM,
        )
    ]

    # Add tabs to mainTab
    mainTab.tabs = tabs_list
    page.add(mainTab)

if __name__ == "__main__":
    ft.app(target=main)