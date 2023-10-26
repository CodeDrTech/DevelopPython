import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QMessageBox, QWidget, QAbstractItemView
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QDoubleValidator
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QDate
from Consultas_db import obtener_ultimo_codigo, generar_nuevo_codigo,\
    insertar_nueva_cotizacion, insertar_nuevo_detalle_cotizacion,\
    quitar_detalle_cotizacion, obtener_codigo_cotizacion, generar_nuevo_codigo_cotizacion, convertir_cot_a_factura, insertar_cotizacion, insertar_detalle_cotizacion

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
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------   
        # Establece las fechas en los txtFechas que estan en el formulario
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------           
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
        self.btnAgregar.clicked.connect(self.insertar_detalle_cotizacion) 

        self.btnQuitar.clicked.connect(self.quitar_datos_detalle_cotizacion)

        self.btnBuscar.clicked.connect(self.visualizar_datos_cotizacion)
        
        self.btnConvertir.clicked.connect(self.convertir_cotizacion)

        # Controles de fecha conectados a la funcion visualizar_datos_cotizacion para buscar datos entre fechas seleccionadas.
        self.txtFechaInicio.dateChanged.connect(self.visualizar_datos_cotizacion)
        self.txtFechaFin.dateChanged.connect(self.visualizar_datos_cotizacion)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Evita que se inserte letras en los campos donde solo lleva numeros 0.0
        double_validator = QDoubleValidator()
        self.txtDescuento.setValidator(double_validator)
        self.cmbPrecioVent.setValidator(double_validator)
        self.txtCantidad.setValidator(double_validator)        
        self.txtItbis.setValidator(double_validator)

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
        
    # Coloca el id de cotizacion en su txt actulizado para el proximo registro
    def actualizar_num_cotizacion(self):
        ultimo_codigo = obtener_codigo_cotizacion("cotizacion")
        nuevo_codigo = generar_nuevo_codigo_cotizacion("COT", ultimo_codigo)
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
        self.txtComentario.setEnabled(False)

    def activar_botones_cotizacion(self):
        self.txtCodigo.setEnabled(True)
        self.cmbComprobante.setEnabled(True)
        self.txtIdCliente.setEnabled(True)
        self.cmbCliente.setEnabled(True)
        self.txtSerie.setEnabled(True)
        self.txtFecha.setEnabled(True)
        self.txtItbis.setEnabled(True)
        self.btnRegistrar.setEnabled(True)
        self.txtComentario.setEnabled(True)

        self.cmbCliente.clear()
        self.txtIdCliente.setText("")
        self.txtSerie.setText("")
        self.txtItbis.setText("")
        self.txtComentario.setPlainText("")
        self.txtFecha.setDate(QDate.currentDate())

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def convertir_cotizacion(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.tbDatos.selectedIndexes()
        
        if indexes:
            
            # Obtener el numero (int) de la fila al seleccionar una celda de la tabla detalle_cotizacion
            index = indexes[0]
            row = index.row()
            
            self.obtener_id_fila_cotizacion(row)
            id_cotizacion = self.bd_id_cotizacion
            
            
            
            # Preguntar si el usuario está seguro de convertir la cotizacion seleccionada
            confirmacion = QMessageBox.question(self, "CONVERITR?", "¿QUIERE CONVERTIR ESTA COTIZACION A FACTURA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", elimina el detalle
            if confirmacion == QMessageBox.Yes:
                convertir_cot_a_factura(id_cotizacion)
                QMessageBox.warning(self, "FACTURADO", "COTIZACION CONVERTIDA A FACTURA.")
                
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA LA COTIZACION A CONVERTIR.")
            
        # Pasando como parametro el numero de fila, obtengo el id de la cotizacion.
    def obtener_id_fila_cotizacion(self, num_fila):
        FechaInicio = self.txtFechaInicio.date().toString("yyyy-MM-dd")
        FechaFinal = self.txtFechaFin.date().toString("yyyy-MM-dd")
        Buscar = self.txtBuscar.text()

        if not Buscar:
            if FechaInicio > FechaFinal:
                QMessageBox.warning(self, "ERROR ENTRE FECHAS", "LA PRIMERA FECHA NO PUEDE SER MAYOR A LA SEGUNDA.")
                                        
                return
            else:
                query = QSqlQuery()
                query.exec_(f"SELECT\
                                        co.idcotizacion as 'ID',\
                                        UPPER(FORMAT(co.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                        CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                                        dc.descuento as 'DESCUENTO %',\
                                        co.itbis as 'IMPUESTOS %',\
                                        co.serie as 'NO. COTIZACION',\
                                        em.nombre as 'VENDEDOR',\
                                        FORMAT(SUM(dc.precio_venta), 'C', 'en-US') as 'TOTAL',\
                                        co.comentario as 'COMENTARIO'\
                                    FROM cotizacion co\
                                    INNER JOIN cliente cl ON co.idcliente = cl.idcliente\
                                    INNER JOIN detalle_cotizacion dc ON co.idcotizacion = dc.idcotizacion\
                                    INNER JOIN empleado em ON co.idempleado = em.idempleado\
                                    WHERE co.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}'\
                                    GROUP BY co.idcotizacion, co.fecha, CONCAT(cl.nombre, ' ', cl.apellidos),\
                                    dc.descuento, co.itbis, co.serie, em.nombre, co.comentario;")
                model = QSqlTableModel()    
                model.setQuery(query)
                self.tbDatos.setModel(model)
                
                # Obtener el modelo de datos del QTableView
                modelo = self.tbDatos.model()
                if modelo is not None and 0 <= num_fila < modelo.rowCount():
                    
                    # Obtener los datos de la fila seleccionada
                    columna_id = modelo.index(num_fila, 0).data()
                    
                    self.bd_id_cotizacion = columna_id
        else:
            if FechaInicio > FechaFinal:
                QMessageBox.warning(self, "ERROR ENTRE FECHAS", "LA PRIMERA FECHA NO PUEDE SER MAYOR A LA SEGUNDA.")
                return
            else:
                query = QSqlQuery()
                query.exec_(f"SELECT\
                                        co.idcotizacion as 'ID',\
                                        UPPER(FORMAT(co.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                        CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                                        dc.descuento as 'DESCUENTO %',\
                                        co.itbis as 'IMPUESTOS %',\
                                        co.serie as 'NO. COTIZACION',\
                                        em.nombre as 'VENDEDOR',\
                                        FORMAT(SUM(dc.precio_venta), 'C', 'en-US') as 'TOTAL',\
                                        co.comentario as 'COMENTARIO'\
                                    FROM cotizacion co\
                                    INNER JOIN cliente cl ON co.idcliente = cl.idcliente\
                                    INNER JOIN detalle_cotizacion dc ON co.idcotizacion = dc.idcotizacion\
                                    INNER JOIN empleado em ON co.idempleado = em.idempleado\
                                    WHERE co.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}' AND CONCAT(cl.nombre, ' ', cl.apellidos) LIKE '%{Buscar}%'\
                                    GROUP BY co.idcotizacion, co.fecha, CONCAT(cl.nombre, ' ', cl.apellidos),\
                                    dc.descuento, co.itbis, co.serie, em.nombre, co.comentario;")
                model = QSqlTableModel()    
                model.setQuery(query)
                self.tbDatos.setModel(model)
                
                # Obtener el modelo de datos del QTableView
                modelo = self.tbDatos.model()
                if modelo is not None and 0 <= num_fila < modelo.rowCount():
                    
                    # Obtener los datos de la fila seleccionada
                    columna_id = modelo.index(num_fila, 0).data()
                    
                    self.bd_id_cotizacion = columna_id
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualizar_datos_cotizacion(self):
        FechaInicio = self.txtFechaInicio.date().toString("yyyy-MM-dd")
        FechaFinal = self.txtFechaFin.date().toString("yyyy-MM-dd")
        Buscar = self.txtBuscar.text()

        if not Buscar:
            if FechaInicio > FechaFinal:
                        
                        QMessageBox.warning(self, "ERROR ENTRE FECHAS", "LA PRIMERA FECHA NO PUEDE SER MAYOR A LA SEGUNDA.")
                                        
                        return
            else:
                query = QSqlQuery()
                query.exec_(f"SELECT\
                                co.idcotizacion as 'ID',\
                                UPPER(FORMAT(co.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                                dc.descuento as 'DESCUENTO %',\
                                co.itbis as 'IMPUESTOS %',\
                                co.serie as 'NO. COTIZACION',\
                                em.nombre as 'VENDEDOR',\
                                FORMAT(SUM(dc.precio_venta), 'C', 'en-US') as 'TOTAL',\
                                co.comentario as 'COMENTARIO'\
                            FROM cotizacion co\
                            INNER JOIN cliente cl ON co.idcliente = cl.idcliente\
                            INNER JOIN detalle_cotizacion dc ON co.idcotizacion = dc.idcotizacion\
                            INNER JOIN empleado em ON co.idempleado = em.idempleado\
                            WHERE co.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}'\
                            GROUP BY co.idcotizacion, co.fecha, CONCAT(cl.nombre, ' ', cl.apellidos),\
                            dc.descuento, co.itbis, co.serie, em.nombre, co.comentario;")
                
                # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
                model = QSqlTableModel()    
                model.setQuery(query)        
                self.tbDatos.setModel(model)

                # Ajustar el tamaño de las columnas para que se ajusten al contenido
                self.tbDatos.resizeColumnsToContents()
                self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            if FechaInicio > FechaFinal:
                        
                        QMessageBox.warning(self, "ERROR ENTRE FECHAS", "LA PRIMERA FECHA NO PUEDE SER MAYOR A LA SEGUNDA.")
                                        
                        return
            else:
                query = QSqlQuery()
                query.exec_(f"SELECT\
                                co.idcotizacion as 'ID',\
                                UPPER(FORMAT(co.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                                dc.descuento as 'DESCUENTO %',\
                                co.itbis as 'IMPUESTOS %',\
                                co.serie as 'NO. COTIZACION',\
                                em.nombre as 'VENDEDOR',\
                                FORMAT(SUM(dc.precio_venta), 'C', 'en-US') as 'TOTAL',\
                                co.comentario as 'COMENTARIO'\
                            FROM cotizacion co\
                            INNER JOIN cliente cl ON co.idcliente = cl.idcliente\
                            INNER JOIN detalle_cotizacion dc ON co.idcotizacion = dc.idcotizacion\
                            INNER JOIN empleado em ON co.idempleado = em.idempleado\
                            WHERE co.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}' AND CONCAT(cl.nombre, ' ', cl.apellidos) LIKE '%{Buscar}%'\
                            GROUP BY co.idcotizacion, co.fecha, CONCAT(cl.nombre, ' ', cl.apellidos),\
                            dc.descuento, co.itbis, co.serie, em.nombre, co.comentario;")
                
                # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
                model = QSqlTableModel()    
                model.setQuery(query)        
                self.tbDatos.setModel(model)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualizar_datos_detalle_cotizacion(self):
        idcotizacion = self.txtCodigo.text()
        query = QSqlQuery()
        query.exec_(f"SELECT dc.iddetalle_cotizacion as 'ID DETALLE',\
                        dc.idcotizacion as 'ID COTIZACION',\
                        CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                        ar.nombre as 'ARTICULO',\
                        FORMAT(dc.precio_venta, 'C', 'en-US') as 'PRECIO',\
                        dc.cantidad as 'CANTIDAD',\
                        dc.descuento as 'DESCUENTO %',\
                        co.itbis as 'IMPUESTOS %',\
                        co.serie as 'NO. COTIZACION',\
                        em.nombre as 'VENDEDOR'\
                    FROM cotizacion co\
                    INNER JOIN cliente cl ON co.idcliente = cl.idcliente\
                    INNER JOIN detalle_cotizacion dc ON co.idcotizacion = dc.idcotizacion\
                    INNER JOIN articulo ar ON dc.idarticulo = ar.idarticulo\
                    INNER JOIN empleado em ON co.idempleado = em.idempleado\
                    WHERE dc.idcotizacion = {idcotizacion};")
        
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbDatos2.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos2.resizeColumnsToContents()
        self.tbDatos2.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
            comentario = self.txtComentario.toPlainText().upper()

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
                    insertar_nueva_cotizacion(idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis, comentario)
                    #insertar_cotizacion(idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis, comentario)
                    self.activar_botones_detalle()
                    self.desactivar_botones_cotizacion()


                    # Limpiar componentes antes de empesar a insertar detalles
                    self.cmbArticulo.clear()
                    self.txtCodArticulo.setText("")
                    self.txtCantidad.setText("")
                    self.cmbPrecioVent.clear()
                    self.txtDescuento.setText("")
                    self.txtCantidad.setFocus()

        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error en cotizacion: {str(e)}")
            mensaje.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def insertar_detalle_cotizacion(self):
        try:
            idoctizacion = self.txtCodigo.text()
            idarticulo = self.txtCodArticulo.text()
            catidad = self.txtCantidad.text()
            precio_venta = self.cmbPrecioVent.currentText()
            descuento = self.txtDescuento.text()

            if not descuento:                
                descuento = 0

            if not all([idoctizacion, idarticulo, catidad, precio_venta]):
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Hay un error en los datos")
                mensaje.setText("Por favor, complete todos los campos correctamente.")
                mensaje.exec_()
            
            
            else:
                insertar_nuevo_detalle_cotizacion(idoctizacion, idarticulo, catidad, precio_venta, descuento)
                #insertar_detalle_cotizacion(idoctizacion, idarticulo, catidad, precio_venta, descuento)      

                self.visualizar_datos_cotizacion()
                self.visualizar_datos_detalle_cotizacion()

                
                # mensaje = QMessageBox()
                # mensaje.setIcon(QMessageBox.Critical)
                # mensaje.setWindowTitle("Agregar detalles de cotizaion")
                # mensaje.setText("Detalles de cotizacion registrado.")
                # mensaje.exec_()
                
                
                
                # Limpia los TexBox
                self.txtCantidad.setText("")
                self.txtCantidad.setFocus()
        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error en detalle: {str(e)}")
            mensaje.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def quitar_datos_detalle_cotizacion(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.tbDatos2.selectedIndexes()
        
        if indexes:
            
            # Obtener el numero (int) de la fila al seleccionar una celda de la tabla detalle_cotizacion
            index = indexes[0]
            row = index.row()
            
            self.obtener_datos_de_fila_detalle_cotizacion(row)
            id_detalle_cotizacion = self.bd_id_detalle_cotizacion
            
            
            
            # Preguntar si el usuario está seguro de inhabilitar el ingreso de la fila seleccionada
            confirmacion = QMessageBox.question(self, "ELIMINAR?", "¿QUIERE ELIMINAR ESTE ARTICULO DE LA LISTA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", elimina el detalle
            if confirmacion == QMessageBox.Yes:
                quitar_detalle_cotizacion(id_detalle_cotizacion)
                QMessageBox.warning(self, "ELIMINADO", "ARTICULO ELIMINADO.")
                self.visualizar_datos_detalle_cotizacion()
                self.visualizar_datos_cotizacion()
                self.verificar_y_ocultar_botones()
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA EL ARTICULO QUE VAS A ELIMINAR.")
            
        # Pasando como parametro el numero de fila, obtengo el id de la cotizacion.
    def obtener_datos_de_fila_detalle_cotizacion(self, num_fila):
        idcotizacion = self.txtCodigo.text()
        query = QSqlQuery()
        query.exec_(f"SELECT dc.iddetalle_cotizacion as 'ID DETALLE',\
                        dc.idcotizacion as 'ID COTIZACION',\
                        CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                        ar.nombre as 'ARTICULO',\
                        FORMAT(dc.precio_venta, 'C', 'en-US') as 'PRECIO',\
                        dc.cantidad as 'CANTIDAD',\
                        dc.descuento as 'DESCUENTO %',\
                        co.itbis as 'IMPUESTOS %',\
                        co.serie as 'NO. COTIZACION',\
                        em.nombre as 'VENDEDOR'\
                    FROM cotizacion co\
                    INNER JOIN cliente cl ON co.idcliente = cl.idcliente\
                    INNER JOIN detalle_cotizacion dc ON co.idcotizacion = dc.idcotizacion\
                    INNER JOIN articulo ar ON dc.idarticulo = ar.idarticulo\
                    INNER JOIN empleado em ON co.idempleado = em.idempleado\
                    WHERE dc.idcotizacion = {idcotizacion};")
        model = QSqlTableModel()    
        model.setQuery(query)
        self.tbDatos2.setModel(model)
        
        # Obtener el modelo de datos del QTableView
        modelo = self.tbDatos2.model()
        if modelo is not None and 0 <= num_fila < modelo.rowCount():
            
            # Obtener los datos de la fila seleccionada
            columna_id = modelo.index(num_fila, 0).data()
            
            self.bd_id_detalle_cotizacion = columna_id
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # si se elimina el ultimo detalle_cotizacion se inhabilitan los botones de insertar detalles
    def verificar_y_ocultar_botones(self):
        idcotizacion = self.txtCodigo.text()
        
        query = QSqlQuery()
        query.prepare(f"SELECT COUNT(*) FROM detalle_cotizacion WHERE idcotizacion = :idcotizacion")
        query.bindValue(":idcotizacion", idcotizacion)
        
        if query.exec_() and query.next():
            num_detalles = query.value(0)
        
            if num_detalles == 1:
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("SE ELIMINARON TODOS LOS ARTICULOS")
                mensaje.setText("INGRESO DE ARTICULOS FINALIZADO, SE BLOQUEARAN LAS FUNICONES.")
                mensaje.exec_()
                self.ocultar_botones_detalle()  # Llama a la función para ocultar botones.
                self.actualizar_ID_cotizacion() # Actualiza el idcotizacion por si el usuario quiere volver a insertar detalles
                self.activar_botones_cotizacion() # Activo los botones para insertar cotizacion nueva.
                self.actualizar_num_cotizacion() # Actualiza el codigo de cotizacion por si el usuario quiere volver a insertar detalles
                
                # Refrescar los datos de las cotizaciones y los de detalle_cotizacion.
                self.visualizar_datos_cotizacion()
                self.visualizar_datos_detalle_cotizacion()
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
        self.visualizar_datos_cotizacion()
        self.actualizar_ID_cotizacion()
        self.actualizar_num_cotizacion()
        self.ocultar_botones_detalle()

        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCotizaciones()
    GUI.show()
    sys.exit(app.exec_())