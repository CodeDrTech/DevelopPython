import sys
from PyQt5.QtWidgets import QApplication, QPushButton, QGraphicsDropShadowEffect, QMainWindow
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # Crear el botón
        self.button = QPushButton("Botón Con Sombra", self)
        
        # Aplicar el estilo CSS al botón
        self.button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                border-radius: 15px;
                padding: 10px 20px;
                font-size: 16px;
            }

            QPushButton:hover {
                background-color: #45a049;
            }

            QPushButton:pressed {
                background-color: #388e3c;
                padding-left: 12px;
                padding-top: 12px;
            }
        """)

        # Crear el efecto de sombra
        shadow_effect = QGraphicsDropShadowEffect()
        shadow_effect.setBlurRadius(10)
        shadow_effect.setXOffset(10)
        shadow_effect.setYOffset(10)
        shadow_effect.setColor(Qt.black)

        # Asignar el efecto de sombra al botón
        self.button.setGraphicsEffect(shadow_effect)

        # Configurar la ventana principal
        self.setWindowTitle("Ventana Principal")
        self.setGeometry(100, 100, 400, 300)

# Inicializar la aplicación
if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    # Crear y mostrar la ventana principal
    main_window = MainWindow()
    main_window.show()

    # Ejecutar el bucle de la aplicación
    sys.exit(app.exec_())
