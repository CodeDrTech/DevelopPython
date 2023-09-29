import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QDate
from Consultas_db import obtener_ultimo_codigo, generar_nuevo_codigo, insertar_nuevo_ingreso, insertar_nuevo_detalle_ingreso

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
        
        # Botones del formulario y sus funciones
        self.btnGuardar.clicked.connect(self.insertar_datos_ingreso)
        self.btnAgregar.clicked.connect(self.insertar_datos_detalle)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def insertar_datos_ingreso(self):
        impuesto = float(self.txtItbis.text())

        try:
            idempleado = int(self.txtIdProveedor.text()) #Falta ver como resolver este
            idproveedor = int(self.txtIdProveedor.text())
            fecha = self.txtFecha.date().toString("yyyy-MM-dd")
            tipo_comprobante = self.cmbComprobante.currentText()            
            num_comprobante = self.txtNumComprobante.text()
            itbis = impuesto/100
            estado = "Activo"
            
            idingreso = int(self.txtCodigo.text())
            idarticulo = int(self.txtCodArticulo.text())
            precio_compra = float(self.txtPrecioCom.text())
            precio_venta = float(self.txtPrecioVen.text())
            stock_inicial = int(self.txtStockInicial.text())
            stock_actual = self.txtFechaNac.date().toString("yyyy-MM-dd") #Falta ver como resolver este
            fecha_produccion = self.txtFechaProd.date().toString("yyyy-MM-dd")
            fecha_vencimiento = self.txtFechaVenc.date().toString("yyyy-MM-dd")
                
            if  not idempleado or not idproveedor or not fecha or not tipo_comprobante or not num_comprobante or not itbis or not estado or not idingreso or not idarticulo or not precio_compra or not precio_venta or not stock_inicial or not stock_actual or not fecha_produccion or not fecha_vencimiento:
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            
            else:
                insertar_nuevo_ingreso(idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado)
                insertar_nuevo_detalle_ingreso(idingreso, idarticulo, precio_compra, precio_venta, stock_inicial, stock_actual, fecha_produccion, fecha_vencimiento)
                #self.visualiza_datos_ingreso()
                #self.visualiza_datos_detalle()
        

                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar ingreso")
                mensaje.setText("ingreso registrado.")
                mensaje.exec_()
                
                
                # Limpia los TexBox 
                self.txtNumComprobante.setText("")
                self.txtApellidos.setText(self.txtApellidos.text().upper())
                self.txtFecha.setDate(QDate.currentDate())                
                self.txtPrecioCom.setText("")
                self.txtPrecioVen.setText("")
                self.txtStockInicial.setText("")
                self.txtFechaProd.setDate(QDate.currentDate())
                self.txtFechaVenc.setDate(QDate.currentDate())

        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def insertar_datos_detalle(self):
        impuesto = float(self.txtItbis.text())

        try:
            idempleado = int(self.txtIdProveedor.text()) #Falta ver como resolver este
            idproveedor = int(self.txtIdProveedor.text())
            fecha = self.txtFecha.date().toString("yyyy-MM-dd")
            tipo_comprobante = self.cmbComprobante.currentText()            
            num_comprobante = self.txtNumComprobante.text()
            itbis = impuesto/100
            estado = "Activo"
            
            idingreso = int(self.txtCodigo.text())
            idarticulo = int(self.txtCodArticulo.text())
            precio_compra = float(self.txtPrecioCom.text())
            precio_venta = float(self.txtPrecioVen.text())
            stock_inicial = int(self.txtStockInicial.text())
            stock_actual = self.txtFechaNac.date().toString("yyyy-MM-dd") #Falta ver como resolver este
            fecha_produccion = self.txtFechaProd.date().toString("yyyy-MM-dd")
            fecha_vencimiento = self.txtFechaVenc.date().toString("yyyy-MM-dd")
                
            if  not idempleado or not idproveedor or not fecha or not tipo_comprobante or not num_comprobante or not itbis or not estado or not idingreso or not idarticulo or not precio_compra or not precio_venta or not stock_inicial or not stock_actual or not fecha_produccion or not fecha_vencimiento:
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            
            else:
                insertar_nuevo_ingreso(idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado)
                insertar_nuevo_detalle_ingreso(idingreso, idarticulo, precio_compra, precio_venta, stock_inicial, stock_actual, fecha_produccion, fecha_vencimiento)
                #self.visualiza_datos_ingreso()
                #self.visualiza_datos_detalle()
        

                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar detalles de ingreso")
                mensaje.setText("detalles de ingreso registrado.")
                mensaje.exec_()
                
                
                # Limpia los TexBox 
                self.txtNumComprobante.setText("")
                self.txtApellidos.setText(self.txtApellidos.text().upper())
                self.txtFecha.setDate(QDate.currentDate())                
                self.txtPrecioCom.setText("")
                self.txtPrecioVen.setText("")
                self.txtStockInicial.setText("")
                self.txtFechaProd.setDate(QDate.currentDate())
                self.txtFechaVenc.setDate(QDate.currentDate())

        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
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
        articulo_data = []
        codigo_data = []  # Agregamos una lista para almacenar los códigos de los artículos.
        
        for i in range(model.rowCount()):
            articulo_data.append(model.data(model.index(i, 2)))
            codigo_data.append(model.data(model.index(i, 0)))  # Obtenemos los códigos y los almacenamos.
            
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox.
        combo_model_articulo = QStandardItemModel()
        for item in articulo_data:
            combo_model_articulo.appendRow(QStandardItem(str(item)))
        self.cmbArticulo.setModel(combo_model_articulo)
        
        self.articulo_data = articulo_data  # Guardar los datos del cliente para su uso posterior.
        self.codigo_data = codigo_data  # Guardar los códigos de los artículos para su uso posterior.
        
        # Conectar la señal currentIndexChanged del QComboBox a la función actualizar_codigo_articulo.
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
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaIngresoAlmacen()
    GUI.show()
    sys.exit(app.exec_())