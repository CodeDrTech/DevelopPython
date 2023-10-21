import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QMessageBox, QWidget
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QDate
from Consultas_db import obtener_ultimo_codigo, generar_nuevo_codigo, insertar_nueva_cotizacion

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

        self.btnRegistrar.clicked.connect(self.insertar_datos_cotiacion)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Abrir los form para buscar e insertar los clientes y y articulos a las cotizaciones.
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
    
    # Trae el resultado y los inserta en los txt y cmb correspondientes
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
    # Coloca el id de cotizacion en su txt actulizado para el proximo registro
    def actualizar_ID_cotizacion(self):
        ultimo_codigo = obtener_ultimo_codigo("cotizacion","idcotizacion")
        nuevo_codigo = generar_nuevo_codigo(ultimo_codigo)
        self.txtCodigo.setText(nuevo_codigo)
        self.txtSerie.setText(nuevo_codigo)   

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    # Oculta los bototnes de los detalles para obligar al usuario a que coloque la cotizacion antes que los detalles
    def ocultar_botones_detalle(self):
        for widget in self.groupBox_2.findChildren(QWidget):
            widget.setVisible(False)

    def activar_botones_detalle(self):
        for widget in self.groupBox_2.findChildren(QWidget):
            widget.setVisible(True)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def desactivar_botones_cotizacion(self):
        self.txtCodigo.setEnabled(False)
        self.cmbComprobante.setEnabled(False)
        self.txtIdCliente.setEnabled(False)
        self.cmbCliente.setEnabled(False)
        self.txtSerie.setEnabled(False)
        self.txtFecha.setEnabled(False)
        self.txtItbis.setEnabled(False)
        self.btnRegistrar.setEnabled(False)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def insertar_datos_cotiacion(self):
        try:
            # llamada de funciones que obtienen el id del ultimo usuario que inicio sesion.
            # Ese dato es usado para saber quien esta registrando datos de ingreso/ventas etc.
            id_ultima_sesion = self.ultima_sesion()
            fila = self.obtener_id_sesion(id_ultima_sesion)
            self.obtener_datos_de_fila(fila)
            id_empleado = self.valor_columna_1


            #Almacena en las variables los valores insertados en los controles inputs txt y cmb.
            idempleado = id_empleado
            idcliente = self.txtIdCliente.text()
            fecha = self.txtFecha.date().toString("yyyy-MM-dd")
            tipo_comprobante = self.cmbComprobante.currentText()            
            num_comprobante = self.txtSerie.text()
            itbis = self.txtItbis.text()

            if not itbis:                
                itbis = 0
            
            if not all([idempleado, idcliente, idempleado, fecha, tipo_comprobante, num_comprobante]):
        
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Hay un error en los datos")
                mensaje.setText("Por favor, complete todos los campos correctamente.")
                mensaje.exec_()
                
                
            else:           

                # Preguntar si el usuario está seguro de empezar a insertar los datos.
                confirmacion = QMessageBox.question(self, "INSERTAR LOS DETALLES", "¿ESTAS SEGURO QUE DESEA CONTINUAR?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
                # Si el usuario hace clic en el botón "Sí", se activa detalle_ingreso.
                if confirmacion == QMessageBox.Yes:
                    insertar_nueva_cotizacion(idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis)
                    self.activar_botones_detalle()
                    self.desactivar_botones_cotizacion()
                    self.txtCantidad.setFocus()

        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Estas 3 funciones obtienen el id de empleado que inicio sesion.
    # Este id de empleado se usa para saber quien ingreso dato a la base de datos
    
    # Obtengo el id del ultimo inicio de sesion, lo usao para buscar el id del usuario que inició.
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
        
    # Pasando como parametro el numero de fila, obtengo el id del empleado
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
            
    # obtengo el numero de fila correspondiente a la sesion, el numero de la fila es igual al idsesion        
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
    
        # Si no se encuentra el idsesion, devuelve -1.
        return -1
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    # Cargar los precios de venta de los articulos en cmbPrecioVent
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
    # Actualiza el stock disponible del articulo seleccionado
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

        self.tbSesiones.hide()
        self.actualizar_ID_cotizacion()
                
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCotizaciones()
    GUI.show()
    sys.exit(app.exec_())