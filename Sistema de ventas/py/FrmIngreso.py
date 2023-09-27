import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QDate
from Consultas_db import obtener_ultimo_codigo, generar_nuevo_codigo

class VentanaIngresoAlmacen(QMainWindow):
    ventana_abierta = False     
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmIngreso.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de ingresos almacén .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    def cargar_proveedores(self):    
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('proveedor')
        model.select()
        column_data = []
        codigo_data = []  # Agregamos una lista para almacenar los códigos de los artículos.
        for i in range(model.rowCount()):
            column_data.append(model.data(model.index(i, 1)))
            codigo_data.append(model.data(model.index(i, 0)))  # Obtenemos los códigos y los almacenamos.
        
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox cmbProveedor.
        combo_model = QStandardItemModel()
        for item in column_data:
            combo_model.appendRow(QStandardItem(str(item)))
        self.cmbProveedor.setModel(combo_model)
        
        # Guardar los códigos de los artículos para su uso posterior.
        self.codigo_data = codigo_data  

        # Conectar la señal currentIndexChanged del QComboBox a la función actualizar_codigo_proveedor.
        self.cmbProveedor.currentIndexChanged.connect(self.actualizar_codigo_proveedor)

        # Mostrar el código del cliente en el QLineEdit si hay al menos un cliente.
        if model.rowCount() > 0:
            codigo_proveedor = model.data(model.index(0, 0))
            self.txtIdProveedor.setText(str(codigo_proveedor))
    
    def actualizar_codigo_proveedor(self, index):
        # Obtener el código del proveedor seleccionado en el QComboBox y mostrarlo en el txtIdProveedor.
        if index >= 0 and index < len(self.codigo_data):
            codigo_proveedor = self.codigo_data[index]
            self.txtIdProveedor.setText(str(codigo_proveedor))
        else:
            self.txtIdProveedor.setText("")  # Limpiar el txtIdProveedor si no hay selección válida.
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    # Esta función carga los artículos en el QComboBox cmbArticulo.
    def cargar_articulos(self):    
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('articulo')
        model.select()
        column_name = []
        for i in range(model.rowCount()):
            column_name.append(model.data(model.index(i, 2)))
        
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox.
        combo_model_articulo = QStandardItemModel()
        for item in column_name:
            combo_model_articulo.appendRow(QStandardItem(str(item)))
        self.cmbArticulo.setModel(combo_model_articulo)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def actualizar_ID_articulo(self):
        ultimo_codigo = obtener_ultimo_codigo("ingreso","idingreso")
        nuevo_codigo = generar_nuevo_codigo(ultimo_codigo)
        self.txtCodigo.setText(nuevo_codigo)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------                
    def closeEvent(self, event):
        VentanaIngresoAlmacen.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def showEvent(self, event):
        super().showEvent(event)
        
        
        self.actualizar_ID_articulo()
        self.cargar_proveedores()
        self.cargar_articulos()
                
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaIngresoAlmacen()
    GUI.show()
    sys.exit(app.exec_())