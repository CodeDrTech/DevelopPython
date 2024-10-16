import sys, os
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from FrmEmpleados import VentanaEmpleados
from FrmDatosReportes import VentanaDatosReportes
from FrmFaltantes import VentanaFaltantes
import Configuracion

class VentanaPrincipal(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('MiniNomina/ui/PanelPrincipal.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('PANEL PRINCIPAL')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/png/folder.png'))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
                
        #Llamar a los diferentes formularios desde los botones
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnAgregar.clicked.connect(self.abrirFrmEmpleados)
        self.BtnRegistrar.clicked.connect(self.abrirFrmFaltanes)
        self.BtnReporte.clicked.connect(self.abrirFrmDatosReportes)
        self.BtnBaseDatos.clicked.connect(self.Configurar_datos)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
                
    #Funcuion para cerrar la ventana principal.    
    def fn_Salir(self):
        self.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    #Funcion para reiniciar el programa
    def reiniciar_programa(self):        
        QApplication.quit()
        os.execv(sys.executable, ['python'] + sys.argv)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
        
    #Funcion para llamas al evento show.    
    def showEvent(self, event):        
        super().showEvent(event)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    
    #Configura la ruta a la base de datos para ser usada por el isstema.    
    def Configurar_datos(self):        
        confirmacion = QMessageBox.question(self, "CONFIGURACION DE DATOS", "SI EL PROGRAMA MUESTRA LOS DATOS NO ES NECESARIO CONFIGURAR LA BASE DE DATOS, QUIERES CONTINUAR?", # type: ignore
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        
                    
        # Si el usuario hace clic en el botón "Sí", configura los datos y reinica el programa.
        if confirmacion == QMessageBox.Yes:
            Configuracion.funcion_de_conexion() 
            self.reiniciar_programa()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
            
                    
    #Funciones para llamar las ventanas secundarias y mostrarlas    
    def abrirFrmEmpleados(self):
        self.llamar_venana_empleados = VentanaEmpleados()
        self.llamar_venana_empleados.show()
        
    def abrirFrmFaltanes(self):
        self.llamar_venana_faltante = VentanaFaltantes()
        self.llamar_venana_faltante.show()
        
    def abrirFrmDatosReportes(self):
        self.llamar_venana_reportes = VentanaDatosReportes()
        self.llamar_venana_reportes.show()
        self.llamar_venana_reportes.Filtro_por_fecha()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())