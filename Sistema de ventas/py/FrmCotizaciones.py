import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QMessageBox
from PyQt5 import QtGui
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
            from FrmBuscarCliente import VentanaBuscarCliente
            if not VentanaBuscarCliente.ventana_abierta:
                VentanaBuscarCliente.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarCliente(self)
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
            from FrmBuscarArticulo import VentanaBuscarArticulo
            if not VentanaBuscarArticulo.ventana_abierta:
                VentanaBuscarArticulo.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarArticulo()
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
        nombre_apellidos = nombre + apellido
        
        id_cliente = str(id)
        
        self.txtIdCliente.setText(id_cliente)
        #self.cmbCliente.setCurretText("")
        self.cmbCliente.addItem(str(nombre_apellidos))
        
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Esta función carga los clientes en un QComboBox.
    # No es necesario para esta solicitud, por lo que se comenta.
    # def cargar_cientes(self):    
    #     # Obtiene los datos de las columnas Nombre y Apellido de la tabla cliente.
    #     model = QSqlTableModel()
    #     model.setTable('cliente')
    #     model.select()
    #     client_data = []
    #
    #     for i in range(model.rowCount()):
    #         codigo = model.data(model.index(i, 0))
    #         nombre = model.data(model.index(i, 1))
    #         apellido = model.data(model.index(i, 2))
    #         nombre_completo = f"{nombre} {apellido}"
    #         client_data.append((nombre_completo, codigo))
    #         
    #     # Cargar los datos en el QComboBox.
    #     combo_model = QStandardItemModel()
    #     for item, _ in client_data:
    #         combo_model.appendRow(QStandardItem(item))
    # 
    #     self.client_data = client_data  # Guardar los datos del cliente para su uso posterior.
    #     self.cmbCliente.setModel(combo_model)
    #
    #     # Conectar la señal currentIndexChanged del QComboBox a la función actualizar_codigo_cliente.
    #     self.cmbCliente.currentIndexChanged.connect(self.actualizar_codigo_cliente)
    #
    #     # Mostrar el código del cliente en el QLineEdit si hay al menos un cliente.
    #     if model.rowCount() > 0:
    #         codigo_cliente = model.data(model.index(0, 0))
    #         self.txtIdCliente.setText(str(codigo_cliente))
    
    #def actualizar_codigo_cliente(self, index):
    #    # Obtener el código del cliente seleccionado en el QComboBox y mostrarlo en el QLineEdit.
    #    selected_client_data = self.client_data[index]
    #    codigo_cliente = selected_client_data[1]
    #    self.txtIdCliente.setText(str(codigo_cliente))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def cargar_articulos(self):    
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('articulo')
        model.select()
        articulo_data = []
        codigo_data = []  # Agregamos una lista para almacenar los códigos de los artículos.
        
        for i in range(model.rowCount()):
            articulo_data.append(model.data(model.index(i, 2)))
            codigo_data.append(model.data(model.index(i, 0)))  # Obtenemos los códigos y los almacenamos.
            
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox.
        combo_model_articulo = QStandardItemModel()
        for item2 in articulo_data:
            combo_model_articulo.appendRow(QStandardItem(str(item2)))
        self.cmbArticulo.setModel(combo_model_articulo)
        
        self.articulo_data = articulo_data  # Guardar los datos del cliente para su uso posterior.
        self.codigo_data = codigo_data  # Guardar los códigos de los artículos para su uso posterior.
        
        # Conectar la señal currentIndexChanged del QComboBox a la función actualizar_codigo_cliente.
        self.cmbArticulo.currentIndexChanged.connect(self.actualizar_codigo_articulo)

        # Mostrar el código del cliente en el QLineEdit si hay al menos un cliente.
        if model.rowCount() > 0:
            codigo_articulo = codigo_data[0]
            self.txtCodArticulo.setText(str(codigo_articulo))
    
    def actualizar_codigo_articulo(self,index):
        # Obtener el código del artículo seleccionado en el QComboBox y mostrarlo en el QLineEdit.
        if index >= 0 and index < len(self.codigo_data):
            codigo_articulo = self.codigo_data[index]
            self.txtCodArticulo.setText(str(codigo_articulo))
        else:
            self.txtCodArticulo.setText("")  # Limpiar el QLineEdit si no hay selección válida.
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def closeEvent(self, event):
        VentanaCotizaciones.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        #self.cargar_cientes()
        #self.cargar_articulos()
                
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCotizaciones()
    GUI.show()
    sys.exit(app.exec_())