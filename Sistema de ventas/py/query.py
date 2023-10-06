from PyQt5.QtWidgets import QApplication, QMainWindow, QFormLayout, QWidget, QTableView, QVBoxLayout, QFrame, QTabWidget, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        layout = QFormLayout(central_widget)

        tab_widget = QTabWidget(self)
        layout.addWidget(tab_widget)

        # Crear una pestaña en el QTabWidget
        tab1 = QWidget()
        tab_widget.addTab(tab1, "Tab 1")

        tab_layout = QVBoxLayout(tab1)

        frame = QFrame(self)
        frame_layout = QVBoxLayout(frame)

        table_view = QTableView(self)
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Columna 1", "Columna 2"])
        for i in range(10):
            row = [QStandardItem(f'Dato {i}, 1'), QStandardItem(f'Dato {i}, 2')]
            model.appendRow(row)
        table_view.setModel(model)

        # Crear un efecto de sombra y aplicarlo al QTableView
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(10)
        shadow.setColor(QColor(200, 200, 200))
        table_view.setGraphicsEffect(shadow)

        frame_layout.addWidget(table_view)
        tab_layout.addWidget(frame)

if __name__ == '__main__':
    app = QApplication([])
    window = MainWindow()
    window.show()
    app.exec()
