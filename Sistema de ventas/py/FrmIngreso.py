import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect, QWidget
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QColor, QDoubleValidator, QIntValidator
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtCore import QDate, Qt
from Consultas_db import obtener_ultimo_codigo, generar_nuevo_codigo, insertar_nuevo_ingreso, insertar_nuevo_detalle_ingreso, anular_ingreso, quitar_detalle_ingreso

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
        # Establece la echa actual en los inputs que contienen fechas
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
        self.txtFechaProd.setDate(QDate.currentDate())
        self.txtFechaVenc.setDate(QDate.currentDate())
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        # Botones del formulario y sus funciones
        self.btnRegistrar.clicked.connect(self.insertar_datos_ingreso)
        self.btnAgregar.clicked.connect(self.insertar_datos_detalle)
        self.btnQuitar.clicked.connect(self.quitar_datos_detalle)        
        self.btnBuscar.clicked.connect(self.buscar_ingresos)
        self.btnAnular.clicked.connect(self.inhabilita_ingreso)
        
        # Controles de fecha conectados a la funcion buscar_ingresos
        self.txtFechaInicio.dateChanged.connect(self.buscar_ingresos)
        self.txtFechaFin.dateChanged.connect(self.buscar_ingresos)
        
        # Control combobox conectado a la funcion buscar_ingresos
        self.cmbEstado.currentIndexChanged.connect(self.buscar_ingresos)        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
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
        # Abre formulario para buscar articulos y/o proveedores e insertarlos en el formulario ingreso.
        self.txtIdProveedor.mouseDoubleClickEvent = self.abrirFrmBuscarProveedor
        self.txtCodArticulo.mouseDoubleClickEvent = self.abrirFrmBuscarArticulo        
        self.cmbProveedor.mouseDoubleClickEvent = self.abrirFrmBuscarProveedor
        self.cmbArticulo.mouseDoubleClickEvent = self.abrirFrmBuscarArticulo

        
        # Evita que se inserte letras en los campos donde solo lleva numeros 0.0
        double_validator = QDoubleValidator()
        self.txtCodigo.setValidator(double_validator)
        self.txtCodArticulo.setValidator(double_validator)
        self.txtPrecioCom.setValidator(double_validator)
        self.txtPrecioVen.setValidator(double_validator)
        self.txtPrecioVen1.setValidator(double_validator)
        self.txtPrecioVen2.setValidator(double_validator)
        self.txtCantidad.setValidator(double_validator)        
        self.txtItbis.setValidator(double_validator)
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
    def inhabilita_ingreso(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.tbIngreso.selectedIndexes()
        
        if indexes:
            
            # Obtener el numero (int) de la fila al seleccionar una celda de la tabla
            index = indexes[0]
            row = index.row()
            
            self.obtener_datos_de_fila_ingresos(row)
            idingreso = self.valor_columna_id
            
            
            
            # Preguntar si el usuario está seguro de inhabilitar el ingreso de la fila seleccionada
            confirmacion = QMessageBox.question(self, "INHABILITAR?", "¿ESTAS SEGURO QUE QUIERE INHABILITAR ESTE INGRESO?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", inhabilita el ingreso
            if confirmacion == QMessageBox.Yes:
                anular_ingreso(idingreso)
                QMessageBox.warning(self, "INHABILITADO", "INGRESO INHABILITADO.")
                self.buscar_ingresos()
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA EL INGRESO QUE VAS A INHABILITAR.")
            
        # Pasando como parametro el numero de fila, obtengo el id del ingreso
    def obtener_datos_de_fila_ingresos(self, num_fila):
        FechaInicio = self.txtFechaInicio.date().toString("yyyy-MM-dd")
        FechaFinal = self.txtFechaFin.date().toString("yyyy-MM-dd")
        estado = self.cmbEstado.currentText()
        query = QSqlQuery()
        query.exec_(f"SELECT \
                                i.idingreso as 'CODIGO',\
                                a.nombre AS ARTICULO,\
                                di.precio_compra AS 'PRECIO DE COMPRA',\
                                di.precio_venta AS 'PRECIO DE VENTA',\
                                di.precio_venta1 AS 'PRECIO DE VENTA 2',\
                                di.precio_venta2 AS 'PRECIO DE VENTA 3',\
                                di.cantidad AS 'CANTIDAD',\
                                UPPER(FORMAT(i.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                i.tipo_comprobante AS 'COMPROBANTE',\
                                i.num_comprobante AS 'NUM COMPROBANTE',\
                                i.itbis AS 'IMPUESTO',\
                                i.estado AS 'ESTADO',\
                                UPPER(FORMAT(di.fecha_produccion, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE PRODUCCION',\
                                UPPER(FORMAT(di.fecha_vencimiento, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE VENCIMIENTO'\
                            FROM detalle_ingreso di\
                            INNER JOIN ingreso i ON di.idingreso = i.idingreso\
                            INNER JOIN articulo a ON di.idarticulo = a.idarticulo\
                            WHERE i.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}'AND i.estado = '{estado}';")
        model = QSqlTableModel()    
        model.setQuery(query)
        self.tbIngreso.setModel(model)
        
        # Obtener el modelo de datos del QTableView
        modelo = self.tbIngreso.model()
        if modelo is not None and 0 <= num_fila < modelo.rowCount():
            
            # Obtener los datos de la fila seleccionada
            columna_id = modelo.index(num_fila, 0).data()
            
            self.valor_columna_id = columna_id
            
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
    
        # Si no se encuentra el idsesion, devuelve -1
        return -1
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def insertar_datos_ingreso(self):   
        try:
            # llamada de funciones que obtienen el id del ultimo usuario que inicio sesion.
            # Ese dato es usado para saber quien esta registrando datos de ingreso/ventas etc.
            id_ultima_sesion = self.ultima_sesion()
            fila = self.obtener_id_sesion(id_ultima_sesion)
            self.obtener_datos_de_fila(fila)
            id_empleado = self.valor_columna_1
            
            

            #Almacena en las variables los valores insertados en los controles inputs txt y cmb.
            idempleado = id_empleado
            idproveedor = self.txtIdProveedor.text()
            fecha = self.txtFecha.date().toString("yyyy-MM-dd")
            tipo_comprobante = self.cmbComprobante.currentText()            
            num_comprobante = self.txtNumComprobante.text()
            itbis = self.txtItbis.text()
            estado = "Activo"
            
            if not itbis:                
                itbis = 0
            
            if not all([idempleado, idproveedor, idempleado, fecha, tipo_comprobante, num_comprobante]):
        
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Hay un error en los datos")
                mensaje.setText("Por favor, complete todos los campos correctamente.")
                mensaje.exec_()
                
                
            else:           

                # Preguntar si el usuario está seguro de empezar a insertar los detalle_ingreso
                confirmacion = QMessageBox.question(self, "INSERTAR LOS DETALLES", "¿ESTAS SEGURO QUE DESEA CONTINUAR?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
                # Si el usuario hace clic en el botón "Sí", se activa detalle_ingreso
                if confirmacion == QMessageBox.Yes:
                    insertar_nuevo_ingreso(idempleado, idproveedor, fecha, tipo_comprobante, num_comprobante, itbis, estado)
                    self.activar_botones_detalle()
                    self.desactivar_botones_ingreso()
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
    def quitar_datos_detalle(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.tbDetalleIngreso.selectedIndexes()
        
        if indexes:
            
            # Obtener el numero (int) de la fila al seleccionar una celda de la tabla tbDetalleIngreso
            index = indexes[0]
            row = index.row()
            
            self.obtener_datos_de_fila_detalle_ingresos(row)
            id_detalle = self.bd_id_detalle_ingreso
            
            
            
            # Preguntar si el usuario está seguro de inhabilitar el ingreso de la fila seleccionada
            confirmacion = QMessageBox.question(self, "ELIMINAR?", "¿QUIERE ELIMINAR ESTE ARTICULO DE LA LISTA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", inhabilita el ingreso
            if confirmacion == QMessageBox.Yes:
                quitar_detalle_ingreso(id_detalle)
                QMessageBox.warning(self, "ELIMINADO", "ARTICULO ELIMINADO.")
                self.visualiza_datos_detalles()
                self.buscar_ingresos()
                self.verificar_y_ocultar_botones()
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA EL ARTICULO QUE VAS A ELIMINAR.")
            
        # Pasando como parametro el numero de fila, obtengo el id del ingreso
    def obtener_datos_de_fila_detalle_ingresos(self, num_fila):
        idingreso = self.txtCodigo.text()
        query = QSqlQuery()
        query.exec_(f"SELECT \
                        di.iddetalle_ingreso as 'CODIGO', \
                        a.nombre AS ARTICULO, \
                        di.precio_compra AS 'PRECIO DE COMPRA', \
                        di.precio_venta AS 'PRECIO DE VENTA', \
                        di.precio_venta1 AS 'PRECIO DE VENTA 2', \
                        di.precio_venta2 AS 'PRECIO DE VENTA 3', \
                        di.cantidad AS 'CANTIDAD', \
                        UPPER(FORMAT(i.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA', \
                        i.tipo_comprobante AS 'COMPROBANTE', \
                        i.num_comprobante AS 'NUM COMPROBANTE', \
                        i.itbis AS 'IMPUESTO', \
                        i.estado AS 'ESTADO', \
                        UPPER(FORMAT(di.fecha_produccion, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE PRODUCCION',\
                        UPPER(FORMAT(di.fecha_vencimiento, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE VENCIMIENTO'\
                    FROM detalle_ingreso di \
                    INNER JOIN ingreso i ON di.idingreso = i.idingreso\
                    INNER JOIN articulo a ON di.idarticulo = a.idarticulo\
                    WHERE i.idingreso = {idingreso}")
        model = QSqlTableModel()    
        model.setQuery(query)
        self.tbDetalleIngreso.setModel(model)
        
        # Obtener el modelo de datos del QTableView
        modelo = self.tbDetalleIngreso.model()
        if modelo is not None and 0 <= num_fila < modelo.rowCount():
            
            # Obtener los datos de la fila seleccionada
            columna_id = modelo.index(num_fila, 0).data()
            
            self.bd_id_detalle_ingreso = columna_id

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def verificar_y_ocultar_botones(self):
        idingreso = self.txtCodigo.text()
        
        query = QSqlQuery()
        query.prepare("SELECT COUNT(*) FROM detalle_ingreso WHERE idingreso = :idingreso")
        query.bindValue(":idingreso", idingreso)
        
        if query.exec_() and query.next():
            num_detalles = query.value(0)
        
            if num_detalles == 0:
                self.ocultar_botones_detalle()  # Llama a la función para ocultar botones



#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    
    def insertar_datos_detalle(self):
        
        try:            
            #Almacena en las variables los valores insertados en los controles inputs txt y cmb.
            idingreso = self.txtCodigo.text()
            idarticulo = self.txtCodArticulo.text()
            precio_compra = self.txtPrecioCom.text()
            precio_venta = self.txtPrecioVen.text()
            precio_venta1 = self.txtPrecioVen1.text()
            precio_venta2 = self.txtPrecioVen2.text()
            cantidad = int(self.txtCantidad.text())
            fecha_produccion = self.txtFechaProd.date().toString("yyyy-MM-dd")
            fecha_vencimiento = self.txtFechaVenc.date().toString("yyyy-MM-dd")
            
            # controla que los precios de venta 1 y 2 tenga valor 0 a la base de dato si uno de ellos o ambos lo estan vacio.
            if not precio_venta1:
                precio_venta1 = 0
            if not precio_venta2:
                precio_venta2 = 0
            if not precio_venta1 and not precio_venta2:
                precio_venta1 = 0
                precio_venta2 = 0
            
            if not all([cantidad, idingreso, idarticulo, precio_compra, precio_venta, fecha_produccion, fecha_vencimiento]):
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Hay un error en los datos")
                mensaje.setText("Por favor, complete todos los campos correctamente.")
                mensaje.exec_()
            
            
            else:
                insertar_nuevo_detalle_ingreso(idingreso, idarticulo, precio_compra, precio_venta, cantidad, fecha_produccion, fecha_vencimiento, precio_venta1, precio_venta2)      

                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar detalles de ingreso")
                mensaje.setText("Detalles de ingreso registrado.")
                mensaje.exec_()
                
                self.visualiza_datos_detalles()
                self.buscar_ingresos()
                
                # Limpia los TexBox
                #self.txtFecha.setDate(QDate.currentDate())                
                self.txtPrecioCom.setText("")
                self.txtPrecioVen.setText("")
                self.txtPrecioVen1.setText("")
                self.txtPrecioVen2.setText("")
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
    def buscar_ingresos(self):
        # Variables con datos de los inputs para usar como criterios/filtros de busquedas
        FechaInicio = self.txtFechaInicio.date().toString("yyyy-MM-dd")
        FechaFinal = self.txtFechaFin.date().toString("yyyy-MM-dd")
        estado = self.cmbEstado.currentText()
        buscar_nombre = self.txtBuscar.text()

        if not buscar_nombre:
            if FechaInicio > FechaFinal:
                    QMessageBox.warning(self, "ERROR ENTRE FECHAS", "LA PRIMERA FECHA NO PUEDE SER MAYOR A LA SEGUNDA.")                
                    return
            else:
                query = QSqlQuery()
                query.exec_(f"SELECT \
                                    i.idingreso as 'CODIGO',\
                                    a.nombre AS ARTICULO,\
                                    di.precio_compra AS 'PRECIO DE COMPRA',\
                                    di.precio_venta AS 'PRECIO DE VENTA',\
                                    di.precio_venta1 AS 'PRECIO DE VENTA 2',\
                                    di.precio_venta2 AS 'PRECIO DE VENTA 3',\
                                    di.cantidad AS 'CANTIDAD',\
                                    UPPER(FORMAT(i.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                    i.tipo_comprobante AS 'COMPROBANTE',\
                                    i.num_comprobante AS 'NUM COMPROBANTE',\
                                    i.itbis AS 'IMPUESTO',\
                                    i.estado AS 'ESTADO',\
                                    UPPER(FORMAT(di.fecha_produccion, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE PRODUCCION',\
                                    UPPER(FORMAT(di.fecha_vencimiento, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE VENCIMIENTO'\
                                FROM detalle_ingreso di\
                                INNER JOIN ingreso i ON di.idingreso = i.idingreso\
                                INNER JOIN articulo a ON di.idarticulo = a.idarticulo\
                                WHERE i.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}' AND i.estado = '{estado}'\
                                UNION ALL\
                                SELECT \
                                    i.idingreso as 'CODIGO',\
                                    'ARTICULO ELIMINADO' AS ARTICULO,\
                                    '0' AS 'PRECIO DE COMPRA',\
                                    '0' AS 'PRECIO DE VENTA',\
                                    '0' AS 'PRECIO DE VENTA 2',\
                                    '0' AS 'PRECIO DE VENTA 3',\
                                    '0' AS 'CANTIDAD',\
                                    UPPER(FORMAT(i.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                    'ELIMINADO' AS 'COMPROBANTE',\
                                    '0' AS 'NUM COMPROBANTE',\
                                    '0' AS 'IMPUESTO',\
                                    'Inactivo' AS 'ESTADO',\
                                    NULL AS 'FECHA DE PRODUCCION',\
                                    NULL AS 'FECHA DE VENCIMIENTO'\
                                FROM ingreso i\
                                WHERE i.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}' AND i.estado = '{estado}'\
                                AND i.idingreso NOT IN (SELECT idingreso FROM detalle_ingreso);")
                
                
                # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
                model = QSqlTableModel()    
                model.setQuery(query)        
                self.tbIngreso.setModel(model)

                # Ajustar el tamaño de las columnas para que se ajusten al contenido
                self.tbIngreso.resizeColumnsToContents()
                self.tbIngreso.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            if FechaInicio > FechaFinal:
                    QMessageBox.warning(self, "ERROR ENTRE FECHAS", "LA PRIMERA FECHA NO PUEDE SER MAYOR A LA SEGUNDA.")                
                    return
            else:
                query = QSqlQuery()
                query.exec_(f"SELECT \
                                    i.idingreso as 'CODIGO',\
                                    a.nombre AS ARTICULO,\
                                    di.precio_compra AS 'PRECIO DE COMPRA',\
                                    di.precio_venta AS 'PRECIO DE VENTA',\
                                    di.precio_venta1 AS 'PRECIO DE VENTA 2',\
                                    di.precio_venta2 AS 'PRECIO DE VENTA 3',\
                                    di.cantidad AS 'CANTIDAD',\
                                    UPPER(FORMAT(i.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                    i.tipo_comprobante AS 'COMPROBANTE',\
                                    i.num_comprobante AS 'NUM COMPROBANTE',\
                                    i.itbis AS 'IMPUESTO',\
                                    i.estado AS 'ESTADO',\
                                    UPPER(FORMAT(di.fecha_produccion, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE PRODUCCION',\
                                    UPPER(FORMAT(di.fecha_vencimiento, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE VENCIMIENTO'\
                                FROM detalle_ingreso di\
                                INNER JOIN ingreso i ON di.idingreso = i.idingreso\
                                INNER JOIN articulo a ON di.idarticulo = a.idarticulo\
                                WHERE i.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}' AND i.estado = '{estado}' AND a.nombre LIKE '%{buscar_nombre}%'\
                                UNION ALL\
                                SELECT \
                                    i.idingreso as 'CODIGO',\
                                    'ARTICULO ELIMINADO' AS ARTICULO,\
                                    '0' AS 'PRECIO DE COMPRA',\
                                    '0' AS 'PRECIO DE VENTA',\
                                    '0' AS 'PRECIO DE VENTA 2',\
                                    '0' AS 'PRECIO DE VENTA 3',\
                                    '0' AS 'CANTIDAD',\
                                    UPPER(FORMAT(i.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                    'ELIMINADO' AS 'COMPROBANTE',\
                                    '0' AS 'NUM COMPROBANTE',\
                                    '0' AS 'IMPUESTO',\
                                    'Inactivo' AS 'ESTADO',\
                                    NULL AS 'FECHA DE PRODUCCION',\
                                    NULL AS 'FECHA DE VENCIMIENTO'\
                                FROM ingreso i\
                                WHERE i.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}' AND i.estado = '{estado}'\
                                AND i.idingreso NOT IN (SELECT idingreso FROM detalle_ingreso);")
                
                
                # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
                model = QSqlTableModel()    
                model.setQuery(query)        
                self.tbIngreso.setModel(model)

                # Ajustar el tamaño de las columnas para que se ajusten al contenido
                self.tbIngreso.resizeColumnsToContents()
                self.tbIngreso.setEditTriggers(QAbstractItemView.NoEditTriggers)
                
        if estado == "Inactivo":
            self.btnAnular.setEnabled(False)
        else:
            self.btnAnular.setEnabled(True)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualiza_datos_detalles(self):
        idingreso = self.txtCodigo.text()
        query = QSqlQuery()
        query.exec_(f"SELECT \
                        di.iddetalle_ingreso as 'CODIGO', \
                        a.nombre AS ARTICULO, \
                        di.precio_compra AS 'PRECIO DE COMPRA', \
                        di.precio_venta AS 'PRECIO DE VENTA', \
                        di.precio_venta1 AS 'PRECIO DE VENTA 2', \
                        di.precio_venta2 AS 'PRECIO DE VENTA 3', \
                        di.cantidad AS 'CANTIDAD', \
                        UPPER(FORMAT(i.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA', \
                        i.tipo_comprobante AS 'COMPROBANTE', \
                        i.num_comprobante AS 'NUM COMPROBANTE', \
                        i.itbis AS 'IMPUESTO', \
                        i.estado AS 'ESTADO', \
                        UPPER(FORMAT(di.fecha_produccion, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE PRODUCCION',\
                        UPPER(FORMAT(di.fecha_vencimiento, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE VENCIMIENTO'\
                    FROM detalle_ingreso di \
                    INNER JOIN ingreso i ON di.idingreso = i.idingreso\
                    INNER JOIN articulo a ON di.idarticulo = a.idarticulo\
                    WHERE i.idingreso = {idingreso}")
        
        
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
        query.exec_(f"SELECT \
                        di.iddetalle_ingreso as 'CODIGO', \
                        a.nombre AS ARTICULO, \
                        di.precio_compra AS 'PRECIO DE COMPRA', \
                        di.precio_venta AS 'PRECIO DE VENTA', \
                        di.precio_venta1 AS 'PRECIO DE VENTA 2', \
                        di.precio_venta2 AS 'PRECIO DE VENTA 3', \
                        di.cantidad AS 'CANTIDAD',\
                        UPPER(FORMAT(i.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA', \
                        i.tipo_comprobante AS 'COMPROBANTE', \
                        i.num_comprobante AS 'NUM COMPROBANTE', \
                        i.itbis AS 'IMPUESTO', \
                        i.estado AS 'ESTADO', \
                        UPPER(FORMAT(di.fecha_produccion, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE PRODUCCION',\
                        UPPER(FORMAT(di.fecha_vencimiento, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE VENCIMIENTO'\
                    FROM detalle_ingreso di \
                    INNER JOIN ingreso i ON di.idingreso = i.idingreso \
                    INNER JOIN articulo a ON di.idarticulo = a.idarticulo;")
        
        
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbIngreso.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbIngreso.resizeColumnsToContents()
        self.tbIngreso.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def desactivar_botones_ingreso(self):
        self.txtCodigo.setEnabled(False)
        self.cmbComprobante.setEnabled(False)
        self.txtIdProveedor.setEnabled(False)
        self.cmbProveedor.setEnabled(False)
        self.txtNumComprobante.setEnabled(False)
        self.txtFecha.setEnabled(False)
        self.txtItbis.setEnabled(False)
        self.btnRegistrar.setEnabled(False)
        
        
    def activar_botones_ingreso(self):
        self.txtCodigo.setEnabled(True)
        self.cmbComprobante.setEnabled(True)
        self.txtIdProveedor.setEnabled(True)
        self.cmbProveedor.setEnabled(True)
        self.txtNumComprobante.setEnabled(True)
        self.txtFecha.setEnabled(True)
        self.txtItbis.setEnabled(True)
        self.btnRegistrar.setEnabled(True)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def ocultar_botones_detalle(self):
        for widget in self.groupBox_2.findChildren(QWidget):
            widget.setVisible(False)

    def activar_botones_detalle(self):
        for widget in self.groupBox_2.findChildren(QWidget):
            widget.setVisible(True)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def actualizar_ID_ingreso(self):
        ultimo_codigo = obtener_ultimo_codigo("ingreso","idingreso")
        nuevo_codigo = generar_nuevo_codigo(ultimo_codigo)
        self.txtCodigo.setText(nuevo_codigo)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------                
    def closeEvent(self, event):        
        # Preguntar si el usuario está seguro de insertar los detalle_ingreso
        confirmacion = QMessageBox.question(self, "¿ESTAS SEGURO QUE DESEA SALIR?", "Cotinue solo ha terminado de insertar todos los ariculos",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
                                                                
        # Si el usuario hace clic en el botón "Sí", inserta los detalle_ingreso
        if confirmacion == QMessageBox.No:
            event.ignore()
        else:
            VentanaIngresoAlmacen.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
            event.accept()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def showEvent(self, event):
        super().showEvent(event)
        
        
        
        self.tbSesiones.hide()
        self.ultima_sesion()
        #self.visualiza_datos_ingreso()
        #self.visualiza_datos_detalles()
        self.actualizar_ID_ingreso()
        self.ocultar_botones_detalle()       
        
        self.buscar_ingresos()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaIngresoAlmacen()
    GUI.show()
    sys.exit(app.exec_())