import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QDate

class VentanaVentas(QMainWindow):
    ventana_abierta = False     
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmVentas.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Ventas .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        # Crear un efecto de sombra y aplicarlo a los QTableView
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))
        self.tbDatos.setGraphicsEffect(shadow)      
        
        tbDetalleIngreso_shadow = QGraphicsDropShadowEffect()
        tbDetalleIngreso_shadow.setBlurRadius(20)
        tbDetalleIngreso_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tbDatos2.setGraphicsEffect(tbDetalleIngreso_shadow)
        
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tabWidget.setGraphicsEffect(tabWidget_shadow)
        
        groupBox_shadow = QGraphicsDropShadowEffect()
        groupBox_shadow.setBlurRadius(20)
        groupBox_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(groupBox_shadow)
        
        groupBox_shadow = QGraphicsDropShadowEffect()
        groupBox_shadow.setBlurRadius(20)
        groupBox_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(groupBox_shadow)
        
        groupBox2_shadow = QGraphicsDropShadowEffect()
        groupBox2_shadow.setBlurRadius(20)
        groupBox2_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_2.setGraphicsEffect(groupBox2_shadow)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Botones del formulario y sus funciones
        self.txtIdCliente.mouseDoubleClickEvent = self.abrirFrmBuscarCliente
        self.txtCodArticulo.mouseDoubleClickEvent = self.abrirFrmBuscarArticulo
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    def abrirFrmBuscarCliente(self, event):
        if event.button() == Qt.LeftButton: # type: ignore
            from FrmBuscarClienteVentas import VentanaBuscarClienteVentas
            if not VentanaBuscarClienteVentas.ventana_abierta:
                VentanaBuscarClienteVentas.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarClienteVentas(self)
                self.llamar_ventana.show()
                
            else:
                #mensaje al usuario
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Ventana duplicada")
                mensaje.setText("La ventana ya esta abierta.")
                mensaje.exec_()

    def abrirFrmBuscarArticulo(self, event):
        if event.button() == Qt.LeftButton: # type: ignore
            from FrmBuscarArticuloVentas import VentanaBuscarArticuloVentas
            if not VentanaBuscarArticuloVentas.ventana_abierta:
                VentanaBuscarArticuloVentas.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarArticuloVentas(self)
                self.llamar_ventana.show()
            
            else:
                #mensaje al usuario
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Ventana duplicada")
                mensaje.setText("La ventana ya esta abierta.")
                mensaje.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def traer_cliente(self, id, nombre, apellido):
        nombre_apellidos = nombre +" "+ apellido 
        
        self.txtIdCliente.setText(str(id))
        self.cmbCliente.clear()
        self.cmbCliente.addItem(str(nombre_apellidos))
        
    def traer_articulo(self, id_articulo, nombre_articulo):
        
        self.txtCodArticulo.setText(str(id_articulo))
        self.cmbArticulo.clear()
        self.cmbArticulo.addItem(str(nombre_articulo))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def closeEvent(self, event):
        VentanaVentas.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        
                
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaVentas()
    GUI.show()
    sys.exit(app.exec_())