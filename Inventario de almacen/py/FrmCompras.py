import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from FrmProductos import VentanaProductos
from FrmProveedores import Ventanaproveedores
from Consultas_db import insertar_compras


class VentanaCompras(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Inventario de almacen/ui/FrmCompras.ui',self)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('COMPRAS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Inventario de almacen/png/folder.png'))  
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Esrtabece los focos a los texbox en orden de arriba hacia abajo.
        
        self.setTabOrder(self.txtDocumento, self.cmbProveedor)
        self.setTabOrder(self.cmbProveedor, self.txtComentario)
        self.setTabOrder(self.txtComentario, self.cmbCodigo)
        self.setTabOrder(self.cmbCodigo, self.cmbProducto)
        self.setTabOrder(self.cmbProducto, self.txtMedida)
        self.setTabOrder(self.txtMedida, self.txtCantidad)
        self.setTabOrder(self.txtCantidad, self.btnSalir)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

        #Llamar a los diferentes formularios desde los botones
        self.btnSalir.clicked.connect(self.fn_Salir)
        #self.btnGuardar.clicked.connect(self.insertar_datos)
        self.btnLimpiar.clicked.connect(self.limpiar_textbox)
        #self.btnBorrar.clicked.connect(self.borrar_fila)
        self.btnFrmProductos.clicked.connect(self.abrirFrmProductos)
        self.btnFrmProveedores.clicked.connect(self.abrirFrmProveedores)
        
        # Evento que inserta el codigo de producto cuando seleccionas un nombre del cmbProducto.
        self.cmbProducto.currentIndexChanged.connect(
            lambda i: self.actualizar_codigo_producto(self.cmbProducto.currentText()))
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    # Obtiene el codigo del producto correspondiente al producto seleccionado en el cmbProducto. 
    def actualizar_codigo_producto(self, nombre):
        model = QSqlTableModel()
        model.setTable('Productos')
        model.setFilter(f"Nombre='{nombre}'")
        model.select()
        columna_codigo = []
        for i in range(model.rowCount()):
            columna_codigo.append(model.data(model.index(i, 0)))

        combo_producto = QStandardItemModel()
        for item in columna_codigo:
            combo_producto.appendRow(QStandardItem(str(item)))
        self.cmbCodigo.setModel(combo_producto) 

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------          
    
    #Funciones para llamar las ventanas secundarias y mostrarlas    
    def abrirFrmProductos(self):
        self.llamar_venana_productos = VentanaProductos()
        self.llamar_venana_productos.show()

    def abrirFrmProveedores(self):
        self.llamar_venana_proveedores = Ventanaproveedores()
        self.llamar_venana_proveedores.show()
    
    def fn_Salir(self):
        self.close()
        
        
    def limpiar_textbox(self):
        #Limpia los TexBox
        self.txtFecha.setDate(QDate.currentDate())        
        self.txtDocumento.setText("")
        self.txtComentario.setText("") 
        self.cmbCodigo.setCurrentText("")  
        self.txtMedida.setText("") 
        self.txtCantidad.setText("") 
        self.cmbProveedor.setCurrentText("") 
        self.cmbProducto.setCurrentText("")         
        self.txtDocumento.setFocus()
        
        
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("Compras")
        model.select()        
        self.dataView.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.dataView.resizeColumnsToContents()
        
        
    def insertar_datos(self):
        
        fecha = self.txtFecha.date().toString("yyyy-MM-dd") 
        proveedor = self.cmbProveedor.currentText()
        codigo = self.cmbCodigo.currentText()
        categoria = 5
        producto = self.cmbProducto.currentText()
        und = self.txtMedida.text()
        comentario = self.txtComentario.text()         
        cantidad = self.txtCantidad.text()       
        insertar_compras(fecha, proveedor, codigo, categoria, producto, und, comentario, cantidad)
        self.visualiza_datos()
        
        
        #Limpia los TexBox
        self.txtFecha.setDate(QDate.currentDate())        
        self.txtDocumento.setText("")
        self.txtComentario.setText("") 
        self.cmbCodigo.setCurrentText("")
        self.txtMedida.setText("") 
        self.txtCantidad.setText("") 
        self.cmbProveedor.setCurrentText("") 
        self.cmbProducto.setCurrentText("")         
        self.txtDocumento.setFocus()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    # Obtiene los datos de la columna Nombre de la tabla Productos.
        model = QSqlTableModel()
        model.setTable('Productos')
        model.select()
        columna_nombre = []
        for i in range(model.rowCount()):
            columna_nombre.append(model.data(model.index(i, 2)))
        
        # Cargar los datos de la columna Nombre de la tabla Productos en el QComboBox asignado.
        combo_model = QStandardItemModel()
        for item in columna_nombre:
             combo_model.appendRow(QStandardItem(str(item)))
        self.cmbProducto.setModel(combo_model)
        
        
    # Obtiene los datos de la columna Nombre de la tabla Proveedores.
        model = QSqlTableModel()
        model.setTable('Proveedores')
        model.select()
        columna_proveedor = []
        for i in range(model.rowCount()):
            columna_proveedor.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Nombre de la tabla Proveedores en el QComboBox asignado.
        combo_model = QStandardItemModel()
        for item in columna_proveedor:
             combo_model.appendRow(QStandardItem(str(item)))
        self.cmbProveedor.setModel(combo_model)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def showEvent(self, event):
        super().showEvent(event) 
          
        #self.visualiza_datos()
        self.txtDocumento.setFocus()
        self.txtFecha.setDate(QDate.currentDate()) 
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCompras()
    GUI.show()
    sys.exit(app.exec_())