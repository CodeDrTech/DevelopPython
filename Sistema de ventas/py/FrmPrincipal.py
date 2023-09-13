import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMdiSubWindow, QMessageBox
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
        #self.setFixedSize(self.size())
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
        
        if VentanaEmpleado:
            #mensaje al usuario
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Creacion de PDF")
            mensaje.setText("Documento guardado con exito.")
            mensaje.exec_()
        else:
            frmEmpleado = VentanaEmpleado()
            subWindow = QMdiSubWindow()
            subWindow.setWidget(frmEmpleado)
            subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
            self.mdiArea.addSubWindow(subWindow)
            subWindow.show()
    def abrirFrmCategoria(self):
        frmCategoria = VentanaCategoria()
        subWindow = QMdiSubWindow()
        subWindow.setWidget(frmCategoria)
        subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
        self.mdiArea.addSubWindow(subWindow)
        subWindow.show()
        
    def abrirFrmPresentacion(self):
        frmPresentacion = VentanaPresentacion()
        subWindow = QMdiSubWindow()
        subWindow.setWidget(frmPresentacion)
        subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
        self.mdiArea.addSubWindow(subWindow)
        subWindow.show()
        
    def abrirFrmArticulo(self):
        frmArticulo = VentanaArticulo()
        subWindow = QMdiSubWindow()
        subWindow.setWidget(frmArticulo)
        subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
        self.mdiArea.addSubWindow(subWindow)
        subWindow.show()
        
    def abrirFrmProveedor(self):
        frmProveedor = VentanaProveedor()
        subWindow = QMdiSubWindow()
        subWindow.setWidget(frmProveedor)
        subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
        self.mdiArea.addSubWindow(subWindow)
        subWindow.show()
        
        
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
    GUI.showMaximized()
    sys.exit(app.exec_())