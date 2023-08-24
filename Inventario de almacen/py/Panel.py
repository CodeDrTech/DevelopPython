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

        self.BtnSalir.clicked.connect(self.fn_Salir)
        
    def fn_Salir(self):
        self.close()


if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())