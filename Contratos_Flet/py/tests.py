import flet as ft
from flet_model import Model, Router


class First(Model):
    route = 'first'
    vertical_alignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment = ft.CrossAxisAlignment.CENTER

    appbar = ft.AppBar(
        title=ft.Text("First View"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE)
    controls = [
        ft.ElevatedButton("Go to Second Page", on_click="go_second")
    ]

    def go_second(self, e):
        self.page.go('/first/second')


class Second(Model):
    route = 'second'
    title = "Test"
    vertical_alignment = ft.MainAxisAlignment.CENTER
    horizontal_alignment = ft.CrossAxisAlignment.CENTER

    appbar = ft.AppBar(
        title=ft.Text("Second View"),
        center_title=True,
        bgcolor=ft.Colors.SURFACE)
    controls = [
        ft.ElevatedButton("Go to First", on_click="go_first")
    ]

    def go_first(self, e):
        self.page.go('first')


def main(page: ft.Page):
    page.title = "Title"
    page.theme_mode = "light"
    # Initialize router with route mappings
    Router(
        {'first': First(page)},
        {'second': Second(page)}
    )

    page.go(page.route)


ft.app(target=main)