import flet as ft

def main(page: ft.Page):
    def open_dlg_modal(message):
        dlg_modal = ft.AlertDialog(
            modal=True,
            title=ft.Text("Información"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("Ok", on_click=lambda e: close_dlg(dlg_modal)),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        page.open(dlg_modal)  # Abre el cuadro de diálogo

    def close_dlg(dialog):
        page.close(dialog)  # Cierra el cuadro de diálogo
        page.add(ft.Text("El diálogo se cerró correctamente."))  # Mensaje opcional

    # Botón para abrir el cuadro de diálogo
    page.add(ft.ElevatedButton("Mostrar Mensaje", on_click=lambda e: open_dlg_modal("Este es un mensaje de prueba.")))

# Ejecutar la aplicación
ft.app(target=main)
