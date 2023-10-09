import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableView
from PyQt5.QtCore import Qt, QAbstractTableModel

class MyTableModel(QAbstractTableModel):
    def __init__(self, data):
        super().__init__()
        self.data = data

    def rowCount(self, parent):
        return len(self.data)

    def columnCount(self, parent):
        return len(self.data[0])

    def data(self, index, role):
        if role == Qt.DisplayRole:
            return str(self.data[index.row()][index.column()])
        return None

class MyWindow(QMainWindow):
    def __init__(self, data):
        super().__init__()
        self.setGeometry(100, 100, 600, 400)
        self.table_view = QTableView(self)
        self.setCentralWidget(self.table_view)

        self.model = MyTableModel(data)
        self.table_view.setModel(self.model)

        self.table_view.doubleClicked.connect(self.double_click_event)

    def double_click_event(self, index):
        # Aquí puedes manejar el evento de doble clic en la celda
        row = index.row()
        column = index.column()
        value = self.model.data[row][column]
        print(f"Doble clic en la celda ({row}, {column}): {value}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    data = [[1, 2, 3], [4, 5, 6], [7, 8, 9]]
    window = MyWindow(data)
    window.show()
    sys.exit(app.exec_())
