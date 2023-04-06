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
        self.setFixedSize(self.size())
        
        #para darle funiones a los botones del PANEL PRINCIPAL
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnAgregar.clicked.connect(self.abrirFrmEmpleados)
        self.BtnRegistrar.clicked.connect(self.abrirFrmFaltanes)
        self.BtnReporte.clicked.connect(self.abrirFrmFiltrar)
        
        
        
    def fn_Salir(self):
        self.close()
        
    def abrirFrmEmpleados(self):
        self.llamar_venana_empleados = VentanaEmpleados()
        self.llamar_venana_empleados.show()
        
    def abrirFrmFaltanes(self):
        self.llamar_venana_faltante = VentanaFaltantes()
        self.llamar_venana_faltante.show()
        
    def abrirFrmFiltrar(self):
        self.llamar_venana_filtrar = VentanaReportes()
        self.llamar_venana_filtrar.show()
        
               
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())