import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QPushButton, QComboBox, QLineEdit, QTableView
from PyQt5.QtCore import Qt

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Ventas")

        # Definir una hoja de estilo CSS personalizada con verde esmeralda
        self.setStyleSheet('''
            /* Estilo para botones */
            QPushButton {
                background-color: #2ECC71; /* Verde esmeralda */
                color: white;
                border: 2px solid #2ECC71;
                border-radius: 5px;
            }
            
            QPushButton:hover {
                background-color: #27AE60; /* Verde esmeralda más oscuro al pasar el mouse */
            }

            /* Estilo para cajas de texto */
            QLineEdit {
                background-color: #2ECC71; /* Verde esmeralda */
                border: 2px solid #2ECC71;
                border-radius: 5px;
                color: white;
            }

            /* Estilo para ComboBox */
            QComboBox {
                background-color: #2ECC71; /* Verde esmeralda */
                border: 2px solid #2ECC71;
                border-radius: 5px;
                color: white;
            }

            /* Estilo para TableView */
            QTableView {
                background-color: #2ECC71; /* Verde esmeralda */
                color: #333; /* Color de texto más oscuro */
            }
        ''')

        # Agregar controles a la ventana
        button = QPushButton("Botón")
        line_edit = QLineEdit()
        combo_box = QComboBox()
        table_view = QTableView()

        self.setCentralWidget(button)  # Puedes cambiar esto según tu diseño

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ventana = VentanaPrincipal()
    ventana.show()
    sys.exit(app.exec_())
