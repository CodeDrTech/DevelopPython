import sys
from PyQt5 import QtWidgets, uic

# Cargamos la ventana diseñada
qtCreatorFile = 'Screen01.ui'
Ui_MainWindow, QtBaseClass = uic.loadUiType(qtCreatorFile)

# Creamos la clase de la aplicación
class MyApp(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.button.clicked.connect(self.saludar)

    def saludar(self):
        # Obtenemos el nombre del usuario
        nombre = self.lineEdit.text()

        # Mostramos un mensaje de bienvenida
        self.label.setText("Hola, " + nombre)

# Creamos la aplicación
app = QtWidgets.QApplication(sys.argv)
window = MyApp()
window.show()
app.exec_()
