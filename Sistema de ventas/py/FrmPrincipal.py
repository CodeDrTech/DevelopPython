import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMdiSubWindow
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from FrmEmpleado import VentanaEmpleado
from FrmCategoria import VentanaCategoria
from FrmArticulo import VentanaArticulo
from FrmPresentacion import VentanaPresentacion
from FrmProveedor import VentanaProveedor
from FrmCliente import VentanaCliente

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
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        
        
        self.actionSalir.triggered.connect(self.fn_Salir)
        self.actionEmpleados.triggered.connect(self.abrirFrmEmpleados)
        self.actionCategorias.triggered.connect(self.abrirFrmCategoria)
        self.actionArticulos.triggered.connect(self.abrirFrmArticulo)
        self.actionPresentaciones.triggered.connect(self.abrirFrmPresentacion)
        self.actionProveedores.triggered.connect(self.abrirFrmProveedor)
        self.actionClientes.triggered.connect(self.abrirFrmClientes)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def abrirFrmEmpleados(self):
        self.llamar_venana_Empleado = VentanaEmpleado()
        self.llamar_venana_Empleado.show()
        
    def abrirFrmCategoria(self):
        self.llamar_venana_Categoria = VentanaCategoria()
        self.llamar_venana_Categoria.show()
        
    def abrirFrmPresentacion(self):
        self.llamar_venana_Presentacion = VentanaPresentacion()
        self.llamar_venana_Presentacion.show()
        
    def abrirFrmArticulo(self):
        self.llamar_venana_Articulo = VentanaArticulo()
        self.llamar_venana_Articulo.show()
        
    def abrirFrmProveedor(self):
        self.llamar_venana_Proveedor = VentanaProveedor()
        self.llamar_venana_Proveedor.show()
        
    #def abrirFrmClientes(self):
        #self.llamar_venana_Clientes = VentanaCliente()
        #self.llamar_venana_Clientes.show()
        
        
    def abrirFrmClientes(self):
        frmCliente = VentanaCliente()  # Crea una instancia de VentanaCliente
        subWindow = QMdiSubWindow()  # Crea una ventana secundaria para VentanaCliente
        subWindow.setWidget(frmCliente)  # Establece VentanaCliente como contenido de la ventana secundaria
        subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore # Configura para que la ventana secundaria se elimine al cerrarse
        self.mdiArea.addSubWindow(subWindow)  # Agrega la ventana secundaria al mdiArea
        subWindow.show()  # Muestra la ventana secundaria

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def fn_Salir(self):
        self.close()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.show()
    sys.exit(app.exec_())