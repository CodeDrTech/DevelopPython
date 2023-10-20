import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QDate

class VentanaCotizaciones(QMainWindow):
    ventana_abierta = False     
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmCotizacion.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Cotizaciones .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        # Crear un efecto de sombra        
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tabWidget.setGraphicsEffect(tabWidget_shadow)
        
        groupBox_shadow = QGraphicsDropShadowEffect()
        groupBox_shadow.setBlurRadius(20)
        groupBox_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(groupBox_shadow)
        
        groupBox3_shadow = QGraphicsDropShadowEffect()
        groupBox3_shadow.setBlurRadius(20)
        groupBox3_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_3.setGraphicsEffect(groupBox3_shadow)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Botones del formulario y sus funciones
        self.txtIdCliente.mouseDoubleClickEvent = self.abrirFrmBuscarCliente
        self.txtCodArticulo.mouseDoubleClickEvent = self.abrirFrmBuscarArticulo
        
        self.cmbCliente.mouseDoubleClickEvent = self.abrirFrmBuscarCliente
        self.cmbArticulo.mouseDoubleClickEvent = self.abrirFrmBuscarArticulo
        
        self.cmbArticulo.currentIndexChanged.connect(self.cargar_precios_venta)
        self.cmbArticulo.currentIndexChanged.connect(self.actualizar_existencia_producto)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def abrirFrmBuscarCliente(self, event):
        if event.button() == Qt.LeftButton: # type: ignore
            from FrmBuscarClienteCotizacion import VentanaBuscarClienteCotizacion
            if not VentanaBuscarClienteCotizacion.ventana_abierta:
                VentanaBuscarClienteCotizacion.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarClienteCotizacion(self)
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
            from FrmBuscarArticuloCotizacion import VentanaBuscarArticuloCotizacion
            if not VentanaBuscarArticuloCotizacion.ventana_abierta:
                VentanaBuscarArticuloCotizacion.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarArticuloCotizacion(self)
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
    # Cargar los precion de ventas de los articulos en cmbPrecioVent
    def cargar_precios_venta(self):
        idarticulo = self.txtCodArticulo.text()
        
        query = QSqlQuery()
        query.prepare(f"SELECT top 1 precio_venta, precio_venta1, precio_venta2 from detalle_ingreso where idarticulo = {idarticulo} ORDER BY iddetalle_ingreso DESC")
        query.bindValue(":idarticulo", int(idarticulo))
        
        
        
        if query.exec_():
            self.cmbPrecioVent.clear()
            while query.next():
                precio = query.value(0)
                precio1 = query.value(1)
                precio2 = query.value(2)
                self.cmbPrecioVent.addItem(str(precio))
                self.cmbPrecioVent.addItem(str(precio1))
                self.cmbPrecioVent.addItem(str(precio2))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    # Actualiza el stock disponible del articulo
    def actualizar_existencia_producto(self):
        idarticulo = self.txtCodArticulo.text()
        model = QSqlTableModel()
        model.setTable('stock')
        model.setFilter(f"idarticulo='{idarticulo}'")
        model.select()

        stock_disponible = ""
        if model.rowCount() > 0:
            stock_disponible = model.data(model.index(0, 2))

            self.txtStock.setText(str(stock_disponible)) 
        else:
            self.txtStock.setText("0")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def closeEvent(self, event):
        VentanaCotizaciones.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
                
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCotizaciones()
    GUI.show()
    sys.exit(app.exec_())