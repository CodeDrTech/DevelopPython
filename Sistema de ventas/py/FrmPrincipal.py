import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui
from FrmEmpleado import VentanaEmpleado

class VentanaPrincipal(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmPrincipal.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Sistema de Ventas .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        
        
        self.actionSalir.triggered.connect(self.fn_Salir)
        self.actionEmpleados.triggered.connect(self.abrirFrmEmpleados)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def abrirFrmEmpleados(self):
        self.llamar_venana_Empleado = VentanaEmpleado()
        self.llamar_venana_Empleado.show()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def fn_Salir(self):
        self.close()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())