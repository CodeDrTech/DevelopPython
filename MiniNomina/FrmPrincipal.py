import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/PanelPrincipal.ui',self)
        self.setWindowTitle('Panel Principal')
        
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())