import sys  
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication

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
        self.BtnAgregar.clicked.connect(self.Calculos)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
                
    #Funcuion para cerrar la ventana principal.    
    def fn_Salir(self):
        self.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

    def Calculos(self):
        a=1
        
        
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