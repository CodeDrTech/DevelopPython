import sys 
import locale 
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
        salario_anualizado = float(salario_texto)
        SalarioAnual = salario_anualizado*12
        renta15 = 0.15
        renta20 = 0.20
        renta25 = 0.25
        
        Ars = 0.0304 #float(ars_texto)
        Afp = 0.0287 #float(afp_texto)        
        Seguros = Ars + Afp
        SalarioAnual2 = salario_anualizado*Seguros
        SalarioAnual3 = salario_anualizado-SalarioAnual2
        SalarioAnual4 = SalarioAnual3*12
        
        if SalarioAnual4 <= 416220.00:
            
            otros_texto = self.txtOtros.text()
        
            
               
            Otros = float(otros_texto)
            Salario = SalarioAnual/12
                
            SeguroNeto = Seguros*Salario
            SalarioNeto = Salario-SeguroNeto
                        
            SalarioQuincenalNeto = (SalarioNeto / 2) - Otros
            
            self.txtIsr.setText("")    
            locale.setlocale(locale.LC_ALL, '')
            
            
            numero_formateado2 = locale.format_string("%.2f", SalarioQuincenalNeto, grouping=True)
            numero_formateado3 = locale.format_string("%.2f", Salario/2, grouping=True)
            numero_formateado4 = locale.format_string("%.2f", Ars*salario_anualizado, grouping=True)
            numero_formateado5 = locale.format_string("%.2f", Afp*salario_anualizado, grouping=True)
            
            self.txtArs.setText(str(numero_formateado4))
            self.txtAfp.setText(str(numero_formateado5))  
            self.txtQuincenal.setText(str(numero_formateado2))
            self.txtMensual.setText(str(numero_formateado3))
        
        
         
        elif SalarioAnual4 >= 416220.01 and SalarioAnual4 <= 624329.00:
            otros_texto = self.txtOtros.text()
               
            Otros = float(otros_texto)
            Salario = SalarioAnual/12
                
            SeguroNeto = Seguros*Salario
            SalarioNeto = Salario-SeguroNeto
            
            excedente = (SalarioNeto*12)-416220.01
            excedente2 = (excedente*renta15)/12
            
            SalarioNeto2 = SalarioNeto-excedente2
                        
            SalarioQuincenalNeto = (SalarioNeto2 / 2) - Otros
            
            
            locale.setlocale(locale.LC_ALL, '')
            
            numero_formateado = locale.format_string("%.2f", excedente2, grouping=True)
            numero_formateado2 = locale.format_string("%.2f", SalarioQuincenalNeto, grouping=True)
            numero_formateado3 = locale.format_string("%.2f", Salario/2, grouping=True)
            numero_formateado4 = locale.format_string("%.2f", Ars*salario_anualizado, grouping=True)
            numero_formateado5 = locale.format_string("%.2f", Afp*salario_anualizado, grouping=True)
            
            
            self.txtArs.setText(str(numero_formateado4))
            self.txtAfp.setText(str(numero_formateado5))
            self.txtIsr.setText(str(numero_formateado))    
            self.txtQuincenal.setText(str(numero_formateado2))
            self.txtMensual.setText(str(numero_formateado3))
        
        elif SalarioAnual4 >= 624329.01 and SalarioAnual4 <= 867123.00:
            otros_texto = self.txtOtros.text()
               
            Otros = float(otros_texto)
            Salario = SalarioAnual/12
                
            SeguroNeto = Seguros*Salario
            SalarioNeto = Salario-SeguroNeto
            
            excedente = (SalarioNeto*12)-624329.01
            excedente2 = ((excedente*renta20)+31216)/12
            
            SalarioNeto2 = SalarioNeto-excedente2
                        
            SalarioQuincenalNeto = (SalarioNeto2 / 2) - Otros
            
            
            locale.setlocale(locale.LC_ALL, '')
            
            numero_formateado = locale.format_string("%.2f", excedente2, grouping=True)
            numero_formateado2 = locale.format_string("%.2f", SalarioQuincenalNeto, grouping=True)
            numero_formateado3 = locale.format_string("%.2f", Salario/2, grouping=True)
            numero_formateado4 = locale.format_string("%.2f", Ars*salario_anualizado, grouping=True)
            numero_formateado5 = locale.format_string("%.2f", Afp*salario_anualizado, grouping=True)
            
            
            self.txtArs.setText(str(numero_formateado4))
            self.txtAfp.setText(str(numero_formateado5))
            self.txtIsr.setText(str(numero_formateado))    
            self.txtQuincenal.setText(str(numero_formateado2))
            self.txtMensual.setText(str(numero_formateado3))
            
            
        elif SalarioAnual4 >= 867123.01:
            otros_texto = self.txtOtros.text()
               
            Otros = float(otros_texto)
            Salario = SalarioAnual/12
                
            SeguroNeto = Seguros*Salario
            SalarioNeto = Salario-SeguroNeto
            
            excedente = (SalarioNeto*12)-867123.01
            excedente2 = ((excedente*renta25)+79776)/12
            
            SalarioNeto2 = SalarioNeto-excedente2
                        
            SalarioQuincenalNeto = (SalarioNeto2 / 2) - Otros
            
            locale.setlocale(locale.LC_ALL, '')
            
            numero_formateado = locale.format_string("%.2f", excedente2, grouping=True)
            numero_formateado2 = locale.format_string("%.2f", SalarioQuincenalNeto, grouping=True)
            numero_formateado3 = locale.format_string("%.2f", Salario/2, grouping=True)
            numero_formateado4 = locale.format_string("%.2f", Ars*salario_anualizado, grouping=True)
            numero_formateado5 = locale.format_string("%.2f", Afp*salario_anualizado, grouping=True)
            
            
            self.txtArs.setText(str(numero_formateado4))
            self.txtAfp.setText(str(numero_formateado5))
            self.txtIsr.setText(str(numero_formateado))    
            self.txtQuincenal.setText(str(numero_formateado2))
            self.txtMensual.setText(str(numero_formateado3))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         

        
    #Funcion para llamas al evento show.    
    def showEvent(self, event):        
        super().showEvent(event)
        self.txtSalario.setFocus()
        #self.txtArs.setText("0.0304")
        #self.txtAfp.setText("0.0287")
        self.txtOtros.setText("0")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())