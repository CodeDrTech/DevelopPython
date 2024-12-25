import flet as ft
from flet import ScrollMode
from consultas import get_empleados, importar_empleados_desde_excel, get_primeros_10_empleados
from tkinter import filedialog
import tkinter as tk
import os


#Funcion principal para iniciar la ventana con los controles.
def reporte(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 700
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = ScrollMode.ADAPTIVE
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Funcion para manejar diferentes eventos al seleccionar algunos de los tab
    def tab_registro(e):
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from registro import registro
            registro(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    mainTab = ft.Tabs(
        selected_index=1,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,        
        
        # Contenedor de tabs
        tabs=[
            ft.Tab(
                icon=ft.Icons.LIST_ALT_OUTLINED,
                text="Reportes",
                content=ft.Column(
                    [
                        ft.Row([
                            
                        ]),
                        ft.Row([
                            ft.ElevatedButton(text="Atras", icon=ft.Icons.ARROW_BACK, width=150, on_click=tab_registro),
                            ft.ElevatedButton(text="Cargar", icon=ft.Icons.UPLOAD, width=150),
                        ]),
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    page.add(mainTab)
    page.update()