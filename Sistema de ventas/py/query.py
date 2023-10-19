from PyQt5.QtCore import QUrl
from PyQt5.QtQuick import QQuickView
from PyQt5.QtWidgets import QApplication

app = QApplication([])

view = QQuickView()
view.setSource(QUrl.fromLocalFile('C:/Users/acer/OneDrive/Documentos/UntitledProject/UntitledProject.qml'))
view.show()

app.exec_()
