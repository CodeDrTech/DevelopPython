import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget

class VentanaFaltantes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Faltantes.ui',self)
        self.setWindowTitle('REGISTRAR FALTANTES')
        self.setFixedSize(self.size())
        
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        
        
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaFaltantes()
    GUI.show()
    sys.exit(app.exec_())