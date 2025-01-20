from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase
from kivymd.uix.floatlayout import MDFloatLayout
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.lang import Builder

class Tab(MDFloatLayout, MDTabsBase):
    """Clase para crear el contenido de cada pestaña."""
    pass

class MainScreen(MDBoxLayout):
    pass

class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # Cambiar a "Dark" para tema oscuro
        self.theme_cls.primary_palette = "Blue"  # Cambiar color primario
        return Builder.load_file('App_android/kivy/main.kv')

if __name__ == "__main__":
    MainApp().run()