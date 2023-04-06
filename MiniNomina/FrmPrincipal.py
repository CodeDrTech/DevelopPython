import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from FrmEmpleados import VentanaEmpleados
from FrmFiltrar import VentanaReportes
from FrmFaltantes import VentanaFaltantes


class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/PanelPrincipal.ui',self)
        self.setWindowTitle('PANEL PRINCIPAL')
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnAgregar.clicked.connect(self.abrirFrmEmpleados)
        
        
        
        
    def fn_Salir(self):
        self.close()
        
    def abrirFrmEmpleados(sefl):
        llamarvenana = VentanaEmpleados()
        llamarvenana.show()
        
               
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())