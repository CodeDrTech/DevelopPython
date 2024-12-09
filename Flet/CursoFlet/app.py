import flet as ft


def main(page: ft.Page):
    page.title = "Calc App"
    result = ft.Text(value="0", color=ft.colors.WHITE, size=20)
    current_value = "0"
    operation = None
    
    def button_clicked(e):
        nonlocal current_value, operation
        text = e.control.text
        if text.isdigit() or text == ".":
            if current_value == "0":
                current_value = text
            else:
                current_value += text
        elif text in ["+", "-", "*", "/"]:
            if operation is None:  # Solo cambiar la operación si no hay una en curso
                operation = text
                result.value = current_value  # Guardar el valor actual en el resultado
        elif text == "=":
            try:
                if operation == "+":
                    current_value = str(float(result.value) + float(current_value))
                elif operation == "-":
                    current_value = str(float(result.value) - float(current_value))
                elif operation == "*":
                    current_value = str(float(result.value) * float(current_value))
                elif operation == "/":
                    if float(current_value) == 0:
                        current_value = "Error: División entre cero"
                    else:
                        current_value = str(float(result.value) / float(current_value))
                result.value = current_value
                operation = None
            except (ValueError, ZeroDivisionError):
                current_value = "Error"
        elif text == "AC":
            current_value = "0"
            result.value = "0"
            operation = None
        elif text == "+/-":
            current_value = str(float(current_value) * -1)

        result.value = current_value
        page.update()
    
    
    class CalcButton(ft.ElevatedButton):
        def __init__(self, text, expand=1):
            super().__init__(text=text, expand=expand, on_click=button_clicked)
            self.text = text
            self.expand = expand

    class DigitButton(CalcButton):
        def __init__(self, text, expand=1):
            CalcButton.__init__(self, text, expand)
            self.bgcolor = ft.colors.WHITE24
            self.color = ft.colors.WHITE

    class ActionButton(CalcButton):
        def __init__(self, text):
            CalcButton.__init__(self, text)
            self.bgcolor = ft.colors.ORANGE
            self.color = ft.colors.WHITE

    class ExtraActionButton(CalcButton):
        def __init__(self, text):
            CalcButton.__init__(self, text)
            self.bgcolor = ft.colors.BLUE_GREY_100
            self.color = ft.colors.BLACK

    page.add(
        ft.Container(
            width=350,
            bgcolor=ft.colors.BLACK,
            border_radius=ft.border_radius.all(20),
            padding=20,
            content=ft.Column(
                controls=[
                    ft.Row(controls=[result], alignment="end"),
                    ft.Row(
                        controls=[
                            ExtraActionButton(text="AC"),
                            ExtraActionButton(text="+/-"),
                            ExtraActionButton(text="%"),
                            ActionButton(text="/"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="7"),
                            DigitButton(text="8"),
                            DigitButton(text="9"),
                            ActionButton(text="*"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="4"),
                            DigitButton(text="5"),
                            DigitButton(text="6"),
                            ActionButton(text="-"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="1"),
                            DigitButton(text="2"),
                            DigitButton(text="3"),
                            ActionButton(text="+"),
                        ]
                    ),
                    ft.Row(
                        controls=[
                            DigitButton(text="0", expand=2),
                            DigitButton(text="."),
                            ActionButton(text="="),
                        ]
                    ),
                ]
            ),
        )
    )

ft.app(target=main,  port=8080, view=ft.AppView.WEB_BROWSER)