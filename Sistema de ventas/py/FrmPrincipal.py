import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui

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
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())