import flet as ft
import sys

def main(page: ft.Page):
    page.title = "Registro de Horas Extras"
    
    # Elementos de la interfaz
    horas_input = ft.TextField(label="Horas Extras", keyboard_type=ft.KeyboardType.NUMBER)
    registrar_btn = ft.ElevatedButton(text="Registrar", on_click=lambda e: registrar_horas(horas_input.value))
    
    page.add(horas_input, registrar_btn)
    print("Ruta del intérprete:", sys.executable)

def registrar_horas(horas):
    print(f"Horas extra registradas: {horas}")

if __name__ == "__main__":
    ft.app(target=main)