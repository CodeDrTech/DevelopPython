import flet as ft
from database import connect_to_db
from flet import AppView


def login(page: ft.Page):
    page.title = "Inicio de Sesión"
    page.window.alignment = ft.alignment.center
    page.window.width = 400
    page.window.height = 300
    page.window.resizable = False
    
    

    def iniciar_sesion(e):
        usuario = txt_usuario.value
        contrasena = txt_contrasena.value
        
        conn = connect_to_db()
        if conn:
            cursor = conn.cursor()
            query = "SELECT * FROM Login WHERE usuario = ? AND contrasena = ?"
            cursor.execute(query, (usuario, contrasena))
            result = cursor.fetchone()
            conn.close()

            if result:
                lbl_mensaje.value = "¡Inicio de sesión exitoso!"
                lbl_mensaje.color = ft.colors.GREEN
                lbl_mensaje.update()
            
                # En lugar de iniciar una nueva aplicación, limpiamos la página actual
                page.clean()
                
                # Importamos y ejecutamos la función main en la página actual
                from main import main
                main(page)

            else:
                lbl_mensaje.value = "Usuario o contraseña incorrectos."
                lbl_mensaje.color = ft.colors.RED
                txt_usuario.value = ""
                txt_contrasena.value = ""
                txt_usuario.update()
                txt_contrasena.update()
                txt_usuario.focus()

            lbl_mensaje.update()

    txt_usuario = ft.TextField(label="Usuario", width=300)
    txt_contrasena = ft.TextField(label="Contraseña", password=True, width=300)
    btn_iniciar = ft.ElevatedButton("Iniciar Sesión", on_click=iniciar_sesion)
    lbl_mensaje = ft.Text(value="", size=14)
    
    page.add(
        ft.Column(
            [
                ft.Text("Inicio de Sesión", size=24, weight=ft.FontWeight.BOLD),
                txt_usuario,
                txt_contrasena,
                btn_iniciar,
                lbl_mensaje,
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=15,
        )
    )
    txt_usuario.focus()
ft.app(login)
#ft.app(target=login, port=8080, view=AppView.WEB_BROWSER)
