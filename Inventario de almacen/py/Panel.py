import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui
from FrmProductos import VentanaProductos
from FrmClientes import Ventanaclientes
from FrmProveedores import Ventanaproveedores

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
        
        #Llamar a los diferentes formularios desde los botones
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnProductos.clicked.connect(self.abrirFrmProductos)
        self.btnClientes.clicked.connect(self.abrirFrmClientes)
        self.btnProveedores.clicked.connect(self.abrirFrmProveedores)
        #self.BtnBaseDatos.clicked.connect(self.Configurar_datos)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def fn_Salir(self):
        self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------       
        
    #Funciones para llamar las ventanas secundarias y mostrarlas    
    def abrirFrmProductos(self):
        self.llamar_venana_productos = VentanaProductos()
        self.llamar_venana_productos.show()
        
    def abrirFrmClientes(self):
        self.llamar_venana_cliente = Ventanaclientes()
        self.llamar_venana_cliente.show()

    def abrirFrmProveedores(self):
        self.llamar_venana_proveedores = Ventanaproveedores()
        self.llamar_venana_proveedores.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())