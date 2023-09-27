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
from FrmIngreso import VentanaIngresoAlmacen
from FrmVentas import VentanaVentas

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
        
    def etiqueta_usuario(self, rol, etiqueta):
        self.lblUsuario.setText(rol + ":")
        self.lblEmpleado.setText(etiqueta)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        
    def administrador(self):
            self.actionSalir.triggered.connect(self.fn_Salir)
            self.actionEmpleados.triggered.connect(self.abrirFrmEmpleados)
            self.actionCategorias.triggered.connect(self.abrirFrmCategoria)
            self.actionArticulos.triggered.connect(self.abrirFrmArticulo)
            self.actionPresentaciones.triggered.connect(self.abrirFrmPresentacion)
            self.actionProveedores.triggered.connect(self.abrirFrmProveedor)
            self.actionClientes.triggered.connect(self.abrirFrmClientes)
            self.actionIngresos.triggered.connect(self.abrirFrmIngresos)
            self.actionVentas.triggered.connect(self.abrirFrmVentas)
            self.actionCambiar_de_usuario.triggered.connect(self.cerrar_sesion)
            #self.menuConsultas
            #self.nemuHerramientas       
            #self.actionCategorias.setEnabled(False)
            
    def vendedor(self):
            self.actionSalir.triggered.connect(self.fn_Salir)
            self.actionEmpleados.setEnabled(False)
            self.actionCategorias.setEnabled(False)
            self.actionArticulos.setEnabled(False)
            self.actionPresentaciones.setEnabled(False)
            self.actionProveedores.setEnabled(False)
            self.actionClientes.triggered.connect(self.abrirFrmClientes)
            self.actionVentas.triggered.connect(self.abrirFrmVentas)
            self.actionIngresos.setEnabled(False)
            self.actionCambiar_de_usuario.triggered.connect(self.cerrar_sesion)
            #self.menuConsultas
            #self.nemuHerramientas
                    
            #self.actionCategorias.setEnabled(False)
            
    def almacen(self):
            self.actionSalir.triggered.connect(self.fn_Salir)
            self.actionEmpleados.setEnabled(False)
            self.actionCategorias.triggered.connect(self.abrirFrmCategoria)
            self.actionArticulos.triggered.connect(self.abrirFrmArticulo)
            self.actionPresentaciones.triggered.connect(self.abrirFrmPresentacion)
            self.actionProveedores.triggered.connect(self.abrirFrmProveedor)
            self.actionClientes.setEnabled(False)
            self.actionVentas.setEnabled(False)
            self.actionIngresos.triggered.connect(self.abrirFrmIngresos)
            self.actionCambiar_de_usuario.triggered.connect(self.cerrar_sesion)
            #self.menuConsultas
            #self.nemuHerramientas
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
    def abrirFrmEmpleados(self):
        
        if not VentanaEmpleado.ventana_abierta:           
            frmEmpleado = VentanaEmpleado()
            VentanaEmpleado.ventana_abierta = True
            subWindow = QMdiSubWindow()
            subWindow.setWidget(frmEmpleado)
            subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
            self.mdiArea.addSubWindow(subWindow)
            subWindow.show()   
            
            
        else:
            #mensaje al usuario
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana duplicada")
            mensaje.setText("La ventana ya esta abierta.")
            mensaje.exec_()
            
            
            
    def abrirFrmCategoria(self):
        
        if not VentanaCategoria.ventana_abierta:
            frmCategoria = VentanaCategoria()
            VentanaCategoria.ventana_abierta = True
            subWindow = QMdiSubWindow()
            subWindow.setWidget(frmCategoria)
            subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
            self.mdiArea.addSubWindow(subWindow)
            subWindow.show()
        else:
            #mensaje al usuario
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana duplicada")
            mensaje.setText("La ventana ya esta abierta.")
            mensaje.exec_()
        
    def abrirFrmPresentacion(self):
        
        if not VentanaPresentacion.ventana_abierta:
            frmPresentacion = VentanaPresentacion()
            VentanaPresentacion.ventana_abierta = True
            subWindow = QMdiSubWindow()
            subWindow.setWidget(frmPresentacion)
            subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
            self.mdiArea.addSubWindow(subWindow)
            subWindow.show()
        else:
            #mensaje al usuario
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana duplicada")
            mensaje.setText("La ventana ya esta abierta.")
            mensaje.exec_()
            
    def abrirFrmIngresos(self):
        
        if not VentanaIngresoAlmacen.ventana_abierta:
            frmIngreso = VentanaIngresoAlmacen()
            VentanaIngresoAlmacen.ventana_abierta = True
            subWindow = QMdiSubWindow()
            subWindow.setWidget(frmIngreso)
            subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
            self.mdiArea.addSubWindow(subWindow)
            subWindow.show()
        else:
            #mensaje al usuario
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana duplicada")
            mensaje.setText("La ventana ya esta abierta.")
            mensaje.exec_()
                
    def abrirFrmArticulo(self):
        
        if not VentanaArticulo.ventana_abierta:
            frmArticulo = VentanaArticulo()
            VentanaArticulo.ventana_abierta = True
            subWindow = QMdiSubWindow()
            subWindow.setWidget(frmArticulo)
            subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
            self.mdiArea.addSubWindow(subWindow)
            subWindow.show()
        else:
            #mensaje al usuario
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana duplicada")
            mensaje.setText("La ventana ya esta abierta.")
            mensaje.exec_()
        
    def abrirFrmProveedor(self):
        
        if not VentanaProveedor.ventana_abierta:
            frmProveedor = VentanaProveedor()
            VentanaProveedor.ventana_abierta = True
            subWindow = QMdiSubWindow()
            subWindow.setWidget(frmProveedor)
            subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
            self.mdiArea.addSubWindow(subWindow)
            subWindow.show()
        else:
            #mensaje al usuario
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana duplicada")
            mensaje.setText("La ventana ya esta abierta.")
            mensaje.exec_()
    
    def abrirFrmVentas(self):
        
        if not VentanaVentas.ventana_abierta:
            frmVentas = VentanaVentas()
            VentanaVentas.ventana_abierta = True
            subWindow = QMdiSubWindow()
            subWindow.setWidget(frmVentas)
            subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore
            self.mdiArea.addSubWindow(subWindow)
            subWindow.show()
        else:
            #mensaje al usuario
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana duplicada")
            mensaje.setText("La ventana ya esta abierta.")
            mensaje.exec_()
        
        
    def abrirFrmClientes(self):
        
        if not VentanaCliente.ventana_abierta:
            frmCliente = VentanaCliente()  # Crea una instancia de VentanaCliente
            VentanaCliente.ventana_abierta = True
            subWindow = QMdiSubWindow()  # Crea una ventana secundaria para VentanaCliente
            subWindow.setWidget(frmCliente)  # Establece VentanaCliente como contenido de la ventana secundaria
            subWindow.setAttribute(Qt.WA_DeleteOnClose)  # type: ignore # Configura para que la ventana secundaria se elimine al cerrarse
            self.mdiArea.addSubWindow(subWindow)  # Agrega la ventana secundaria al mdiArea
            subWindow.show()  # Muestra la ventana secundaria
        else:
            #mensaje al usuario
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana duplicada")
            mensaje.setText("La ventana ya esta abierta.")
            mensaje.exec_()
            
    def cerrar_sesion(self):
        # Cierra la sesión del usuario actual
        from FrmLogin import VentanaLogin
        self.ventana_login = VentanaLogin()
        self.ventana_login.show()
        self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def fn_Salir(self):
        self.close()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPrincipal()
    GUI.showMaximized()
    sys.exit(app.exec_())