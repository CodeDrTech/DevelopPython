from kivymd.app import MDApp
from kivymd.uix.tab import MDTabsBase, MDTabs
from kivymd.uix.screen import MDScreen
from kivymd.uix.label import MDLabel
from kivymd.uix.boxlayout import MDBoxLayout


class Tab(MDBoxLayout, MDTabsBase):
    """Clase para crear el contenido de cada pestaña."""
    pass


class MainApp(MDApp):
    def build(self):
        self.theme_cls.theme_style = "Light"  # Cambiar a "Dark" para tema oscuro
        self.theme_cls.primary_palette = "Blue"  # Cambiar color primario

        # Pantalla principal
        screen = MDScreen()

        # Layout principal con las pestañas al final
        layout = MDBoxLayout(orientation="vertical")

        # Contenido principal (parte superior)
        content = MDBoxLayout(size_hint=(1, 0.88))  # Ajuste dinámico para contenido
        content.add_widget(MDLabel(text="Contenido principal", halign="center"))

        # Pestañas
        tabs = MDTabs(size_hint=(1, 0.12))  # Altura de pestañas ajustada para pantallas móviles
        tabs.add_widget(self.create_tab("Vencimientos", "Muestra los vencimientos de pagos.", "home"))
        tabs.add_widget(self.create_tab("Clientes", "Lista de clientes registrados.", "account"))
        tabs.add_widget(self.create_tab("Agregar clientes", "Formulario para añadir clientes nuevos.", "account-plus"))
        tabs.add_widget(self.create_tab("Aplicar pagos", "Registrar pagos de clientes.", "cash"))
        tabs.add_widget(self.create_tab("Envio estado", "Enviar estados por mail.", "gmail"))

        # Agregar contenido y pestañas al layout principal
        layout.add_widget(content)
        layout.add_widget(tabs)

        # Agregar el layout principal a la pantalla
        screen.add_widget(layout)
        return screen

    def create_tab(self, name, text, icon):
        """Crea una pestaña con un nombre y texto descriptivo."""
        tab = Tab(orientation='vertical', padding=10)  # Padding para mejor ajuste en móviles
        
        # Texto alineado a la derecha
        label = MDLabel(
            text=text,
            halign="left",
            theme_text_color="Primary",
            size_hint_y=1,
            height="40dp",  # Ajuste para que no ocupe demasiado espacio
        )
        
        # Agregar texto al tab
        tab.add_widget(label)
        tab.text = name
        tab.icon = icon
        return tab


if __name__ == "__main__":
    MainApp().run()
