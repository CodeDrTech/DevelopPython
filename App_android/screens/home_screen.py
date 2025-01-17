from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.button import MDRaisedButton  # Importar desde kivymd.uix.button

class Tab(MDBoxLayout, MDTabsBase):
    """Clase para crear el contenido de cada pestaña."""
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # Cambiar a "Dark" para tema oscuro
        self.theme_cls.primary_palette = "Blue"  # Cambiar color primario

        # Pantalla principal
        screen = MDScreen()

        # Pestañas
        tabs = MDTabs()
        tabs.add_widget(self.create_tab("Vencimientos", "Busqueda por nombre.", "home"))
        tabs.add_widget(self.create_tab("Clientes", "Lista de clientes registrados.", "account"))
        tabs.add_widget(self.create_tab("Agregar clientes", "Formulario para añadir clientes nuevos.", "account-plus"))
        tabs.add_widget(self.create_tab("Aplicar pagos", "Registrar pagos de clientes.", "cash"))
        tabs.add_widget(self.create_tab("Envio estado", "Enviar estados por WhatsApp.", "send"))

        # Agregar las pestañas a la pantalla
        screen.add_widget(tabs)
        return screen

    def create_tab(self, name, text, icon):
        """Crea una pestaña con un nombre y texto descriptivo."""
        tab = Tab(orientation='vertical')
        
        # Contenedor para el texto alineado a la derecha en la parte superior
        top_layout = MDBoxLayout(size_hint_y=None, height="48dp", padding=[0, 10, 10, 0])
        label = MDLabel(text=text, halign="left", theme_text_color="Primary")
        top_layout.add_widget(label)
        
        # Agregar el contenedor de texto y el icono
        tab.add_widget(top_layout)
        tab.text = name
        tab.icon = icon
        return tab


if __name__ == "__main__":
    MainApp().run()
