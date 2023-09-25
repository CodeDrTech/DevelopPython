import sys
from PyQt5.QtWidgets import QApplication
from FrmLogin import VentanaLogin
from FrmPrincipal import VentanaPrincipal


    
def FrmPrincipal():
    ventana_principal = VentanaPrincipal()
    ventana_login = VentanaLogin()
    
    ventana_principal.show()
    
    ventana_login.fn_Salir()
    
def LoginCambiarUsuario():
    ventana_principal = VentanaPrincipal()
    ventana_login = VentanaLogin()
    
    
    ventana_principal.fn_Salir()
    ventana_login.show()
    
    
    
