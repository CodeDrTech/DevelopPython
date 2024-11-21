import flet as ft

def main(page: ft.Page):
    page.title = "Basic elevated buttons"
    page.add(
        ft.Row(
            [
                ft.ElevatedButton("Elevated button"),
                ft.OutlinedButton("Outlined button"),
                ft.FilledButton("Filled button"),
                ft.ElevatedButton(text="Elevated button", color="BLUE_100", bgcolor="blue"),
                ft.ElevatedButton("Disabled button", disabled=True),
                ft.IconButton(
                    icon=ft.icons.PAUSE_CIRCLE_FILLED_ROUNDED,
                    icon_color="blue400",
                    icon_size=20,
                    tooltip="Pause record",)
            ],
            alignment=ft.MainAxisAlignment.START,
        ),
        
        
    )

ft.app(main)