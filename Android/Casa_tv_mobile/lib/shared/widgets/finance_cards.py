import flet as ft

def create_summary_card(title: str, amount: float, color: str) -> ft.Card:
    """Crea una tarjeta de resumen financiero."""
    return ft.Card(
        content=ft.Container(
            content=ft.Column([
                ft.Text(title, size=14, weight="bold"),
                ft.Text(
                    f"${int(amount):,}",
                    size=20,
                    color=color,
                    weight="bold"
                )
            ], alignment=ft.MainAxisAlignment.CENTER),
            padding=15,
        ),
        elevation=3,
    )