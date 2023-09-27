import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui
from FrmProductos import VentanaProductos
from FrmClientes import Ventanaclientes
from FrmProveedores import Ventanaproveedores
from FrmCompras import VentanaCompras
from FrmSalidas import VentanaSalidas
from FrmInventario import VentanaInventario
from FrmHistorial import VentanaHistorial
from FrmBaseSalidas import VentanaBaseSalidas
from FrmBaseCompras import VentanaBaseCompras

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
        self.btnCompras.clicked.connect(self.abrirFrmCompras)
        self.btnSalidas.clicked.connect(self.abrirFrmSalidas)
        self.btnInventario.clicked.connect(self.abrirFrmInventario)
        self.btnHistorial.clicked.connect(self.abrirFrmHistorial)
        self.btnBaseSalidas.clicked.connect(self.abrirFrmBaseSalidas)
        self.bntBaseCompras.clicked.connect(self.abrirFrmBaseCompras)
                
        
        
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
        
    def abrirFrmCompras(self):
        self.llamar_venana_compras = VentanaCompras()
        self.llamar_venana_compras.show()
        
    def abrirFrmSalidas(self):
        self.llamar_venana_salidas = VentanaSalidas()
        self.llamar_venana_salidas.show()
        
    def abrirFrmInventario(self):
        self.llamar_venana_inventario = VentanaInventario()
        self.llamar_venana_inventario.show()
        
    def abrirFrmHistorial(self):
        self.llamar_venana_historial = VentanaHistorial()
        self.llamar_venana_historial.show()
        
    def abrirFrmBaseSalidas(self):
        self.llamar_venana_base_salidas = VentanaBaseSalidas()
        self.llamar_venana_base_salidas.show()
        
    def abrirFrmBaseCompras(self):
        self.llamar_venana_base_compras = VentanaBaseCompras()
        self.llamar_venana_base_compras.show()
        

if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())