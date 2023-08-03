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
                
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnCalcular.clicked.connect(self.Calculos)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
                
    #Funcuion para cerrar la ventana principal.    
    def fn_Salir(self):
        self.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

    def Calculos(self):
        salario_texto = self.txtSalario.text()
        ars_texto = self.txtArs.text()
        afp_texto = self.txtAfp.text()
        otros_texto = self.txtOtros.text()
        
        Ars = float(ars_texto)
        Afp = float(afp_texto)        
        Seguros = Ars + Afp
        
        Otros = float(otros_texto)
        Salario = float(salario_texto)
        
        SeguroNeto = Seguros*Salario
        SalarioNeto = Salario-SeguroNeto
        
        
        SalarioQuincenalNeto = (SalarioNeto / 2) - Otros
        
        self.txtQuincenal.setText(str(SalarioQuincenalNeto))
        self.txtMensual.setText(str(SalarioNeto))
        
        

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         

        
    #Funcion para llamas al evento show.    
    def showEvent(self, event):        
        super().showEvent(event)
        self.txtSalario.setFocus()
        self.txtArs.setText("0.0304")
        self.txtAfp.setText("0.0287")
        self.txtOtros.setText("0")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())