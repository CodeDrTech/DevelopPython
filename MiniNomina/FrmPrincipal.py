import sys
from PyQt5 import uic
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QIcon
from FrmEmpleados import VentanaEmpleados
from FrmDatosReportes import VentanaDatosReportes
from FrmFaltantes import VentanaFaltantes
import Configuracion

class VentanaPrincipal(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('MiniNomina/FrmDesign/PanelPrincipal.ui',self)
        
        # Configuraiones de la ventana principal.
        self.setWindowTitle('PANEL PRINCIPAL')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/folder.png'))
        
        

        
        #Llamar a los diferentes formularios desde los botones
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnAgregar.clicked.connect(self.abrirFrmEmpleados)
        self.BtnRegistrar.clicked.connect(self.abrirFrmFaltanes)
        self.BtnReporte.clicked.connect(self.abrirFrmDatosReportes)
        self.BtnBaseDatos.clicked.connect(self.Configurar_datos)
              
        
        
        
        
    #Funcuion para cerrar la ventana principal a travez del boton Salir    
    def fn_Salir(self):
        self.close()
        
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)
        
    def Configurar_datos(self):
        Configuracion.funcion_de_conexion()   
        
    #Funciones para llamar las ventanas secundarias y mostrarlas    
    def abrirFrmEmpleados(self):
        self.llamar_venana_empleados = VentanaEmpleados()
        self.llamar_venana_empleados.show()
        
    def abrirFrmFaltanes(self):
        self.llamar_venana_faltante = VentanaFaltantes()
        self.llamar_venana_faltante.show()
        
    def abrirFrmDatosReportes(self):
        self.llamar_venana_reportes = VentanaDatosReportes()
        self.llamar_venana_reportes.show()
        self.llamar_venana_reportes.Filtro_por_fecha()
     
              
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())