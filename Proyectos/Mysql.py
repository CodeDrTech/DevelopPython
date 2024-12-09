import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QVBoxLayout, QWidget
import mysql.connector

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Conexión a MySQL")
        self.setGeometry(100, 100, 400, 300)

        layout = QVBoxLayout()
        self.label = QLabel("Estado de la conexión: No conectado")
        layout.addWidget(self.label)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)

        try:
            self.connection = mysql.connector.connect(
                host="tu_host",
                user="tu_usuario",
                password="tu_contraseña",
                database="tu_base_de_datos"
            )
            self.label.setText("Estado de la conexión: Conectado a MySQL")
        except mysql.connector.Error as err:
            self.label.setText(f"Error de conexión: {err}")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
