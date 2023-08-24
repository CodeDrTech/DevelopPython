import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui

class VentanaPrincipal(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Inventario de almacen/ui/PANEL.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('CONTROL DE INVENTARIO')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Inventario de almacen/png/folder.png'))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        
        #Llamar a los diferentes formularios desde los botones
        self.BtnSalir.clicked.connect(self.fn_Salir)
        #self.BtnAgregar.clicked.connect(self.abrirFrmEmpleados)
        #self.BtnRegistrar.clicked.connect(self.abrirFrmFaltanes)
        #self.BtnReporte.clicked.connect(self.abrirFrmDatosReportes)
        #self.BtnBaseDatos.clicked.connect(self.Configurar_datos)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def fn_Salir(self):
        self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------       
        
    #Funciones para llamar las ventanas secundarias y mostrarlas    
    def abrirFrmEmpleados(self):
        self.llamar_venana_empleados = VentanaEmpleados()
        self.llamar_venana_empleados.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())