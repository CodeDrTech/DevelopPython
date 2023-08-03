import sys, os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui

class VentanaPrincipal(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('CalculoSalario/Principal.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('PANEL PRINCIPAL')
        self.setFixedSize(self.size())
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
                
        #Llamar a los diferentes formularios desde los botones
        self.BtnSalir.clicked.connect(self.fn_Salir)
        #self.BtnAgregar.clicked.connect(self.abrirFrmEmpleados)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
                
    #Funcuion para cerrar la ventana principal.    
    def fn_Salir(self):
        self.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         

        
    #Funcion para llamas al evento show.    
    def showEvent(self, event):        
        super().showEvent(event)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())