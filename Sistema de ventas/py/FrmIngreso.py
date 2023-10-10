import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtCore import QDate, Qt
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
        
        # Crear un efecto de sombra y aplicarlo a los QTableView
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))
        self.tbIngreso.setGraphicsEffect(shadow)      
        
        tbDetalleIngreso_shadow = QGraphicsDropShadowEffect()
        tbDetalleIngreso_shadow.setBlurRadius(20)
        tbDetalleIngreso_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tbDetalleIngreso.setGraphicsEffect(tbDetalleIngreso_shadow)
        
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tabWidget.setGraphicsEffect(tabWidget_shadow)
        
        
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
        self.txtIdProveedor.mouseDoubleClickEvent = self.abrirFrmBuscarProveedor
        self.txtCodArticulo.mouseDoubleClickEvent = self.abrirFrmBuscarArticulo
        
        self.cmbProveedor.mouseDoubleClickEvent = self.abrirFrmBuscarProveedor
        self.cmbArticulo.mouseDoubleClickEvent = self.abrirFrmBuscarArticulo

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def abrirFrmBuscarProveedor(self, event):
        if event.button() == Qt.LeftButton: # type: ignore
            from FrmBuscarProveedor import VentanaBuscarproveedor
            if not VentanaBuscarproveedor.ventana_abierta:
                VentanaBuscarproveedor.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarproveedor(self)
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
            from FrmBuscarArticuloIngreso import VentanaBuscarArticuloIngreso
            if not VentanaBuscarArticuloIngreso.ventana_abierta:
                VentanaBuscarArticuloIngreso.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarArticuloIngreso(self)
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
    

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def traer_proveedor(self, id, nombre):
        
        
        self.txtIdProveedor.setText(str(id))
        self.cmbProveedor.clear()
        self.cmbProveedor.addItem(str(nombre))
        
    def traer_articulo(self, id_articulo, nombre_articulo):
        
        self.txtCodArticulo.setText(str(id_articulo))
        self.cmbArticulo.clear()
        self.cmbArticulo.addItem(str(nombre_articulo))

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    def ultima_sesion(self):
        query = QSqlQuery()
        query.exec_(f"SELECT max(idsesion) FROM sesiones")
        
        # Almacena en una variable el resultado del select que es de tipo int
        resultado = 0
        if query.next():
            resultado = query.value(0)
        
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)
        self.tbSesiones.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbSesiones.resizeColumnsToContents()    
        
        return resultado
        
        
    def obtener_datos_de_fila(self, fila_id):
        query = QSqlQuery()
        query.exec_(f"SELECT * FROM sesiones")
        model = QSqlTableModel()    
        model.setQuery(query)
        self.tbSesiones.setModel(model)
        
        # Obtener el modelo de datos del QTableView
        modelo = self.tbSesiones.model()
        if modelo is not None and 0 <= fila_id < modelo.rowCount():
            
            # Obtener los datos de la fila seleccionada
            columna_1 = modelo.index(fila_id, 1).data()
            
            self.valor_columna_1 = columna_1
            
            
    def obtener_id_sesion(self, idsesion):
        model = QSqlTableModel()
        model.setTable('sesiones')
        model.select()
        
            
        # Encuentra el índice de la columna "idsesion"
        idsesion_column_index = model.fieldIndex("idsesion")
    
        # Itera a través de las filas para encontrar el idsesion
        for row in range(model.rowCount()):
            index = model.index(row, idsesion_column_index)
            if model.data(index) == idsesion:
                # Si se encuentra el idsesion, devuelve el número de fila
                return row
    
        # Si no se encuentra el idsesion, devuelve -1
        return -1
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def insertar_datos_ingreso(self):
        impuesto = float(self.txtItbis.text())
        
        
        try:
            id_ultima_sesion = self.ultima_sesion()
            fila = self.obtener_id_sesion(id_ultima_sesion)
            self.obtener_datos_de_fila(fila)
            id_empleado = self.valor_columna_1
            
            
            # Variables usadas para los ingresos
            idempleado = id_empleado
            idproveedor = self.txtIdProveedor.text()
            fecha = self.txtFecha.date().toString("yyyy-MM-dd")
            tipo_comprobante = self.cmbComprobante.currentText()            
            num_comprobante = self.txtNumComprobante.text()
            itbis = impuesto/100
            estado = "Activo"
            
            idingreso = int(self.txtCodigo.text())
            idarticulo = int(self.txtCodArticulo.text())
            precio_compra = float(self.txtPrecioCom.text())
            precio_venta = float(self.txtPrecioVen.text())
            cantidad = int(self.txtCantidad.text())
            fecha_produccion = self.txtFechaProd.date().toString("yyyy-MM-dd")
            fecha_vencimiento = self.txtFechaVenc.date().toString("yyyy-MM-dd")
                
            if  not idempleado or not idproveedor or not fecha or not tipo_comprobante or not num_comprobante or not itbis or not estado or not idingreso or not idarticulo or not precio_compra or not precio_venta or not cantidad or not fecha_produccion or not fecha_vencimiento:
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            
            else:
                insertar_nuevo_ingreso(idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado)
                
                self.visualiza_datos_ingreso()
                
        

                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar ingreso")
                mensaje.setText("ingreso registrado.")
                mensaje.exec_()
                
                
                # Limpia los TexBox 
                self.txtNumComprobante.setText("")
                self.txtFecha.setDate(QDate.currentDate())                
                self.txtPrecioCom.setText("")
                self.txtPrecioVen.setText("")
                self.txtCantidad.setText("")
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
            
            #Variables para detalles de ingreso
            idingreso = int(self.txtCodigo.text())
            idarticulo = int(self.txtCodArticulo.text())
            precio_compra = float(self.txtPrecioCom.text())
            precio_venta = float(self.txtPrecioVen.text())
            cantidad = int(self.txtCantidad.text())
            fecha_produccion = self.txtFechaProd.date().toString("yyyy-MM-dd")
            fecha_vencimiento = self.txtFechaVenc.date().toString("yyyy-MM-dd")
                
            if  not idempleado or not idproveedor or not fecha or not tipo_comprobante or not num_comprobante or not itbis or not estado or not idingreso or not idarticulo or not precio_compra or not precio_venta or not cantidad or not fecha_produccion or not fecha_vencimiento:
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            
            else:
                insertar_nuevo_detalle_ingreso(idingreso, idarticulo, precio_compra, precio_venta, cantidad, fecha_produccion, fecha_vencimiento)
                
                
                
                
                self.visualiza_datos_detalles()
        

                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar detalles de ingreso")
                mensaje.setText("detalles de ingreso registrado.")
                mensaje.exec_()
                
                
                # Limpia los TexBox 
                self.txtNumComprobante.setText("")
                self.txtFecha.setDate(QDate.currentDate())                
                self.txtPrecioCom.setText("")
                self.txtPrecioVen.setText("")
                self.txtCantidad.setText("")
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
    def visualiza_datos_detalles(self):
        # Consulta SELECT * FROM Productos visualiza_datos_ingreso
        query = QSqlQuery()
        query.exec_(f"SELECT * FROM detalle_ingreso")
        
        
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbDetalleIngreso.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDetalleIngreso.resizeColumnsToContents()
        self.tbDetalleIngreso.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def visualiza_datos_ingreso(self):
        # Consulta SELECT * FROM Productos 
        query = QSqlQuery()
        query.exec_(f"SELECT * FROM ingreso")
        
        
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbIngreso.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbIngreso.resizeColumnsToContents()
        self.tbIngreso.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    
        
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
        
        self.tbSesiones.hide()
        self.ultima_sesion()
        self.visualiza_datos_ingreso()
        self.visualiza_datos_detalles()
        self.actualizar_ID_articulo()
        
        
        
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
        self.txtFechaProd.setDate(QDate.currentDate())
        self.txtFechaVenc.setDate(QDate.currentDate())
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaIngresoAlmacen()
    GUI.show()
    sys.exit(app.exec_())