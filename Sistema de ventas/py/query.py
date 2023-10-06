from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QGraphicsColorizeEffect
from PyQt5.QtGui import QColor
from PyQt5.QtCore import QPropertyAnimation

def colorize_animation(widget):
    # Creamos un efecto de cambio de color
    colorize_effect = QGraphicsColorizeEffect()
    widget.setGraphicsEffect(colorize_effect)

    # Creamos una animación para cambiar gradualmente el color
    animation = QPropertyAnimation(colorize_effect, b"color")
    animation.setDuration(10000)  # Duración de la animación en milisegundos (2 segundos)
    animation.setStartValue(QColor(255, 255, 255))  # Color inicial (blanco)
    animation.setEndValue(QColor(255, 0, 0))        # Color final (rojo)


    # Iniciamos la animación
    animation.start()

if __name__ == '__main__':
    app = QApplication([])
    window = QMainWindow()
    button = QPushButton("Animar Color")
    window.setCentralWidget(button)

    button.clicked.connect(lambda: colorize_animation(window))  # Aplicar la animación al hacer clic en el botón

    window.show()
    app.exec()
