import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui

class VentanaCliente(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/Frmmdiarea.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Clientes .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
class Frmmdiarea(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("Frmmdiarea.ui", self)
        
        # Agregar FrmPrincipal como un subformulario en el área MDI
        self.mdiArea.addSubWindow(VentanaCliente())
        
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCliente()
    GUI.show()
    sys.exit(app.exec_())