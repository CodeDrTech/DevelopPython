import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

class Ventana(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('Proyectos/FORMULARIO.ui',self)
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = Ventana()
    GUI.show()
    sys.exit(app.exec_())