import flet as ft
from frontend.views.usuarios_view import UsuariosView

def main(page: ft.Page):
    # Configurar propiedades de la ventana
    page.title = "Contratos Flet"
    page.window_width = 800
    page.window_height = 600
    page.scroll = "auto"
    
    # Instanciar y cargar la vista principal
    usuarios_view = UsuariosView()
    page.add(usuarios_view)

# Iniciar la aplicación
if __name__ == "__main__":
    ft.app(target=main)
