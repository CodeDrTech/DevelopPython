import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setGeometry(100, 100, 400, 200)
    window.setWindowTitle('Botón con Efectos')

    button = QPushButton('+', window)
    button.setGeometry(150, 75, 100, 40)

    # Configura un efecto de sombra en el botón
    shadow_effect = QGraphicsDropShadowEffect()
    shadow_effect.setBlurRadius(10)
    shadow_effect.setColor(Qt.black) # type: ignore
    button.setGraphicsEffect(shadow_effect)

    # Cambia el estilo del botón (opcional)
    button.setStyleSheet("background-color: #3498db; color: white;")

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
