import flet as ft
from flet import ScrollMode


#Funcion principal para iniciar la ventana con los controles.
def main(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 1250
    page.window.height = 800
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE
    
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    mainTab = ft.Tabs(
        selected_index=0,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,    
        
        # Contenedor de tabs
        tabs=[
            ft.Tab(
                icon=ft.Icons.HOUSE_ROUNDED,
                text="Horas",
            ),
            ft.Tab(
                icon=ft.Icons.IMAGE,
                text="Equipos con Imágenes",
            ),
        ],
    )
    page.add(mainTab)    
ft.app(main)