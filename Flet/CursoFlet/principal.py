import flet

from flet import IconButton, Page, Row, TextField, icons



def main(page: Page):
    page.title = "Flet counter example"
    page.vertical_alignment = flet.MainAxisAlignment.CENTER

    txt_number = TextField(value="0", text_align=flet.TextAlign.RIGHT, width=100)

    def minus_click(event):
        txt_number.value = int(txt_number.value) - 1
        page.update()

    def plus_click(event):
        txt_number.value = int(txt_number.value) + 1
        page.update()

    page.add(
        Row(
            [
                IconButton(icons.REMOVE, on_click=minus_click),
                txt_number,
                IconButton(icons.ADD, on_click=plus_click),
            ],
            alignment=flet.MainAxisAlignment.CENTER,
        )
    )

# ... existing code ...

# Ejecutar la aplicación en modo web
# ... existing code ...

# Ejecutar la aplicación en modo web
# ... existing code ...

# Ejecutar la aplicación en modo web
flet.app(target=main, port=8080, host="0.0.0.0")