import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5 import QtWidgets, QtGui

class VentanaReportes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Filtrar.ui',self)
        self.setWindowTitle('FILTRAR REPORTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        
        
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaReportes()
    GUI.show()
    sys.exit(app.exec_())