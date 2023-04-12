import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5 import QtWidgets, QtGui
from FrmEmpleados import VentanaEmpleados
from FrmFiltrar import VentanaReportes
from FrmFaltantes import VentanaFaltantes
from FrmDatos import VentanaDatos



class VentanaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/PanelPrincipal.ui',self)
        
        # Configuraiones de la ventana principal.
        self.setWindowTitle('PANEL PRINCIPAL')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        

        
        #Para darle funiones a los botones del PANEL PRINCIPAL
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnAgregar.clicked.connect(self.abrirFrmEmpleados)
        self.BtnRegistrar.clicked.connect(self.abrirFrmFaltanes)
        self.BtnReporte.clicked.connect(self.abrirFrmFiltrar)
        
        
        
        
        
        
        
    #Funcuion para cerrar la ventana principal a travez del boton Salir    
    def fn_Salir(self):
        self.close()
        
        

    #Funciones para llamar las ventanas secundarias y mostrarlas    
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