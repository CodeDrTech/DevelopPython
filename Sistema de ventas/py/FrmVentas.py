import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui
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
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    def cargar_cientes(self):    
        # Obtiene los datos de las columnas Nombre y Apellido de la tabla cliente.
        model = QSqlTableModel()
        model.setTable('cliente')
        model.select()
        client_data = []

        for i in range(model.rowCount()):
            codigo = model.data(model.index(i, 0))
            nombre = model.data(model.index(i, 1))
            apellido = model.data(model.index(i, 2))
            nombre_completo = f"{nombre} {apellido}"
            client_data.append((nombre_completo, codigo))
            
        # Cargar los datos en el QComboBox.
        combo_model = QStandardItemModel()
        for item, _ in client_data:
            combo_model.appendRow(QStandardItem(item))
    
        self.client_data = client_data  # Guardar los datos del cliente para su uso posterior.
        self.cmbCliente.setModel(combo_model)

        # Conectar la señal currentIndexChanged del QComboBox a la función actualizar_codigo_cliente.
        self.cmbCliente.currentIndexChanged.connect(self.actualizar_codigo_cliente)

        # Mostrar el código del cliente en el QLineEdit si hay al menos un cliente.
        if model.rowCount() > 0:
            codigo_cliente = model.data(model.index(0, 0))
            self.txtIdCliente.setText(str(codigo_cliente))
    
    def actualizar_codigo_cliente(self, index):
        # Obtener el código del cliente seleccionado en el QComboBox y mostrarlo en el QLineEdit.
        selected_client_data = self.client_data[index]
        codigo_cliente = selected_client_data[1]
        self.txtIdCliente.setText(str(codigo_cliente))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def cargar_articulos(self):    
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('articulo')
        model.select()
        articulo_data = []
        
        for i in range(model.rowCount()):
            articulo_data.append(model.data(model.index(i, 2)))
        
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox.
        combo_model_articulo = QStandardItemModel()
        for item in articulo_data:
            combo_model_articulo.appendRow(QStandardItem(str(item)))
        self.cmbArticulo.setModel(combo_model_articulo)
        
        self.articulo_data = articulo_data  # Guardar los datos del cliente para su uso posterior.
        self.cmbCliente.setModel(combo_model_articulo)
        
        # Conectar la señal currentIndexChanged del QComboBox a la función actualizar_codigo_cliente.
        self.cmbArticulo.currentIndexChanged.connect(self.actualizar_codigo_articulo)

        # Mostrar el código del cliente en el QLineEdit si hay al menos un cliente.
        if model.rowCount() > 0:
            codigo_articulo = model.data(model.index(0, 1))
            self.txtCodArticulo.setText(str(codigo_articulo))
    
    def actualizar_codigo_articulo(self, index):
        # Obtener el código del cliente seleccionado en el QComboBox y mostrarlo en el QLineEdit.
        selected_client_data = self.articulo_data[index]
        codigo_articulo = selected_client_data[1]
        self.txtCodArticulo.setText(str(codigo_articulo))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def closeEvent(self, event):
        VentanaVentas.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        self.cargar_cientes()
        self.cargar_articulos()
                
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaVentas()
    GUI.show()
    sys.exit(app.exec_())