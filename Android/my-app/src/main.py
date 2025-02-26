import flet as ft
import requests
import datetime
from math import sin, cos, radians

def main(page: ft.Page):
    page.title = "Weather App"
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = 20
    page.bgcolor = "#1a1a1a"

    # Animated background circle
    circle = ft.Container(
        width=40,
        height=40,
        border_radius=20,
        bgcolor=ft.Colors.BLUE_400,
        offset=ft.transform.Offset(0, 0),
        animate_offset=ft.animation.Animation(duration=2000, curve=ft.AnimationCurve.EASE_IN_OUT),
    )

    def animate_position(e):
        current = circle.offset.x if circle.offset else 0
        next_x = sin(radians(current * 10)) * 0.5
        next_y = cos(radians(current * 10)) * 0.5
        circle.offset = ft.transform.Offset(next_x, next_y)
        circle.update()
        page.update()

    circle.on_animation_end = lambda e: animate_position(e)
    
    # Weather search components
    city_input = ft.TextField(
        label="Nombre de la ciudad",
        border_radius=10,
        expand=True,
        text_size=16
    )

    weather_card = ft.Card(
        elevation=5,
        content=ft.Container(
            padding=20,
            content=ft.Column(
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                controls=[
                    ft.Text("Informacion del clima", size=24, weight="bold"), # type: ignore
                    ft.Divider(),
                    ft.Row([
                        ft.Icon(ft.Icons.LOCATION_ON, color=ft.Colors.RED_400),
                        ft.Text("", size=20, weight="500") # type: ignore
                    ], alignment=ft.MainAxisAlignment.CENTER),
                    ft.Text("", size=40, weight="bold"), # type: ignore
                    ft.Text("", size=16),
                    ft.Row([
                        ft.Column([
                            ft.Icon(ft.Icons.WATER_DROP, color=ft.Colors.BLUE_400),
                            ft.Text("", size=14)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                        ft.Column([
                            ft.Icon(ft.Icons.AIR, color=ft.Colors.GREEN_400),
                            ft.Text("", size=14)
                        ], horizontal_alignment=ft.CrossAxisAlignment.CENTER)
                    ], alignment=ft.MainAxisAlignment.SPACE_AROUND)
                ]
            )
        )
    )

    def get_weather(e):
        try:
            API_KEY = "####"
            city = city_input.value
            url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            
            response = requests.get(url)
            data = response.json()

            if response.status_code == 200:
                weather_card.content.content.controls[2].controls[1].value = data['name']
                weather_card.content.content.controls[3].value = f"{int(data['main']['temp'])}°C"
                weather_card.content.content.controls[4].value = data['weather'][0]['description'].capitalize()
                weather_card.content.content.controls[5].controls[0].controls[1].value = f"Humedad: {data['main']['humidity']}%"
                weather_card.content.content.controls[5].controls[1].controls[1].value = f"Vientos: {data['wind']['speed']} m/s"
                weather_card.visible = True
            else:
                weather_card.visible = False
                page.show_snack_bar(ft.SnackBar(content=ft.Text("City not found!")))
        except Exception as e:
            page.show_snack_bar(ft.SnackBar(content=ft.Text(f"Error: {str(e)}")))
        page.update()

    search_button = ft.ElevatedButton(
        "Search",
        icon=ft.Icons.SEARCH,  # Updated from icons to Icons
        on_click=get_weather,
        style=ft.ButtonStyle(
            shape=ft.RoundedRectangleBorder(radius=10),
        )
    )

    # Layout
    page.add(
        ft.Stack([circle]),
        ft.Container(height=20),
        ft.Row([city_input, search_button], alignment=ft.MainAxisAlignment.CENTER),
        ft.Container(height=20),
        weather_card
    )

    animate_position(None)

ft.app(target=main)