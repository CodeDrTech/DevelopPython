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
        flet.Row(
            [
                flet.IconButton(flet.icons.REMOVE, on_click=minus_click),
                txt_number,
                flet.IconButton(flet.icons.ADD, on_click=plus_click),
            ],
            alignment=flet.MainAxisAlignment.CENTER,
        )
    )

flet.app(target=main, view=flet.web.WEB_BROWSER)