from kivymd.app import MDApp
from kivymd.uix.screen import MDScreen
from kivymd.uix.button import MDRaisedButton

class MiAplicacionMD(MDApp):
    def build(self):
        pantalla = MDScreen()
        boton = MDRaisedButton(
            text="Iniciar",
            pos_hint={"center_x": 0.5, "center_y": 0.5},
            on_release=self.iniciar
        )
        pantalla.add_widget(boton)
        return pantalla

    def iniciar(self, instance):
        print("Iniciando aplicación con Material Design...")

if __name__ == "__main__":
    MiAplicacionMD().run()
