import sys
import os
import time
import textwrap

import win32api
import win32print

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.colors import black

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QGraphicsDropShadowEffect, QMessageBox, QAbstractItemView, QWidget
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QDoubleValidator
from PyQt5.QtSql import QSqlQuery
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QDate
from Consultas_db import obtener_ultimo_codigo, generar_nuevo_codigo, obtener_codigo_venta,\
                            generar_nuevo_codigo_venta, insertar_nueva_venta, insertar_nuevo_detalle_venta, revertir_detalle_venta, revertir_venta

class VentanaVentas(QMainWindow):
    ventana_abierta = False     
    def __init__(self):
        self.se_llamo_activar_botones = False
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmVentas.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Ventas .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/imagenes/login.jpg'))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
        # Crear un efecto de sombra en los contenedores de controles        
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

        groupBox3_shadow = QGraphicsDropShadowEffect()
        groupBox3_shadow.setBlurRadius(20)
        groupBox3_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_3.setGraphicsEffect(groupBox3_shadow)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Botones del formulario y sus funciones
        self.btnRegistrar.clicked.connect(self.insertar_datos_venta)
        
        self.btnAgregar.clicked.connect(self.insertar_detalle_venta)        
        self.btnQuitar.clicked.connect(self.quitar_datos_detalle_venta)
        
        self.txtIdCliente.mouseDoubleClickEvent = self.abrirFrmBuscarCliente
        self.txtCodArticulo.mouseDoubleClickEvent = self.abrirFrmBuscarArticulo
        
        self.cmbCliente.mouseDoubleClickEvent = self.abrirFrmBuscarCliente
        self.cmbArticulo.mouseDoubleClickEvent = self.abrirFrmBuscarArticulo
        
        self.btnBuscar.clicked.connect(self.visualizar_datos_venta)

        self.btnAnular.clicked.connect(self.devolucion_de_venta)

        self.btnImprimir.clicked.connect(self.imprime_hoja)
        self.btnPdf.clicked.connect(self.imprime_pdf)

        # Controles de fecha conectados a la funcion visualizar_datos_venta para buscar datos entre fechas seleccionadas.
        self.txtFechaInicio.dateChanged.connect(self.visualizar_datos_venta)
        self.txtFechaFin.dateChanged.connect(self.visualizar_datos_venta)
        
        self.cmbArticulo.currentIndexChanged.connect(self.cargar_precios_venta)
        self.cmbArticulo.currentIndexChanged.connect(self.actualizar_existencia_producto)
        
        # Establecer el texto de referencia a la caja de texto buscar
        # Conectar el evento de clic para borrar el texto
        self.txtBuscar.setPlaceholderText('Buscar')        
        self.txtBuscar.mousePressEvent = self.borrarTexto 
        
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
    # Oculta los bototnes de los detalles para obligar al usuario a que coloque la venta antes que los detalles
    
    # Oculta los botones cuando la ventana de venta carga
    def ocultar_botones_detalle(self):
        if not self.se_llamo_activar_botones:
            for widget in self.groupBox_2.findChildren(QWidget):
                widget.setVisible(False)
            self.se_llamo_activar_botones = False
        return self.se_llamo_activar_botones

    # Activa los botones cuando se inserta la cotizacion en el boton 'Registrar'.
    def activar_botones_detalle(self):
        if not self.se_llamo_activar_botones:
            for widget in self.groupBox_2.findChildren(QWidget):
                widget.setVisible(True)
            self.se_llamo_activar_botones = True
        return self.se_llamo_activar_botones
            
    # Oculta los botones cuando se eliminan todos los detalles de la venta y esta queda sin articulos.
    def ocultar_botones_detalle_al_revertir_venta(self):
        if self.se_llamo_activar_botones:
            for widget in self.groupBox_2.findChildren(QWidget):
                widget.setVisible(False)
            self.se_llamo_activar_botones = False
        return self.se_llamo_activar_botones 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    def abrirFrmBuscarCliente(self, event):
        if event.button() == Qt.LeftButton: # type: ignore
            from FrmBuscarClienteVentas import VentanaBuscarClienteVentas
            if not VentanaBuscarClienteVentas.ventana_abierta:
                VentanaBuscarClienteVentas.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarClienteVentas(self)
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
            from FrmBuscarArticuloVentas import VentanaBuscarArticuloVentas
            if not VentanaBuscarArticuloVentas.ventana_abierta:
                VentanaBuscarArticuloVentas.ventana_abierta = True
                self.llamar_ventana = VentanaBuscarArticuloVentas(self)
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
        
    def traer_articulo(self, id_venta, nombre_articulo):
        
        self.txtCodArticulo.setText(str(id_venta))
        self.cmbArticulo.clear()
        self.cmbArticulo.addItem(str(nombre_articulo))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    # Coloca el id de venta en su txt actulizado para el proximo registro
    def actualizar_ID_venta(self):
        ultimo_codigo = obtener_ultimo_codigo("venta","idventa")
        nuevo_codigo = generar_nuevo_codigo(ultimo_codigo)
        self.txtCodigo.setText(nuevo_codigo)
        
    # Coloca el id de venta en su txt actulizado para el proximo registro
    def actualizar_num_venta(self):
        ultimo_codigo = obtener_codigo_venta("venta")
        nuevo_codigo = generar_nuevo_codigo_venta("FACT", ultimo_codigo)
        self.txtSerie.setText(nuevo_codigo)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    # Cargar los precios de venta de los articulos en cmbPrecioVent
    def cargar_precios_venta(self):
        idarticulo = self.txtCodArticulo.text()
        
        query = QSqlQuery()
        query.prepare(f"SELECT top 1 precio_venta, precio_venta1, precio_venta2 from detalle_ingreso where idarticulo\
                      = {idarticulo} ORDER BY iddetalle_ingreso DESC")
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
    def desactivar_botones_venta(self):
        self.txtCodigo.setEnabled(False)
        self.cmbComprobante.setEnabled(False)
        self.txtIdCliente.setEnabled(False)
        self.cmbCliente.setEnabled(False)
        self.txtSerie.setEnabled(False)
        self.txtFecha.setEnabled(False)
        self.txtItbis.setEnabled(False)
        self.btnRegistrar.setEnabled(False)
        self.txtComentario.setEnabled(False)

    def activar_botones_venta(self):
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
    def visualizar_datos_venta(self):
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
                                ve.idventa as 'ID',\
                                UPPER(FORMAT(ve.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                                dv.descuento as 'DESCUENTO %',\
                                ve.itbis as 'IMPUESTOS %',\
                                ve.serie as 'NO. VENTA',\
                                em.nombre as 'VENDEDOR',\
                                FORMAT(SUM(dv.cantidad * dv.precio_venta), 'C', 'en-US') as 'SUB TOTAL',\
                                FORMAT(SUM((dv.cantidad * dv.precio_venta * (1 - (dv.descuento / 100))) * (1 + (ve.itbis / 100))), 'C', 'en-US') as 'TOTAL',\
                                ve.comentario as 'COMENTARIO'\
                            FROM venta ve\
                            INNER JOIN cliente cl ON ve.idcliente = cl.idcliente\
                            INNER JOIN detalle_venta dv ON ve.idventa = dv.idventa\
                            INNER JOIN empleado em ON ve.idempleado = em.idempleado\
                            WHERE ve.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}'\
                            GROUP BY ve.idventa, ve.fecha, CONCAT(cl.nombre, ' ', cl.apellidos),\
                            dv.descuento, ve.itbis, ve.serie, em.nombre, ve.comentario;")
                
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
                                ve.idventa as 'ID',\
                                UPPER(FORMAT(ve.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                                dv.descuento as 'DESCUENTO %',\
                                ve.itbis as 'IMPUESTOS %',\
                                ve.serie as 'NO. VENTA',\
                                em.nombre as 'VENDEDOR',\
                                FORMAT(SUM(dv.cantidad * dv.precio_venta), 'C', 'en-US') as 'SUB TOTAL',\
                                FORMAT(SUM((dv.cantidad * dv.precio_venta * (1 - (dv.descuento / 100))) * (1 + (ve.itbis / 100))), 'C', 'en-US') as 'TOTAL',\
                                ve.comentario as 'COMENTARIO'\
                            FROM venta ve\
                            INNER JOIN cliente cl ON ve.idcliente = cl.idcliente\
                            INNER JOIN detalle_venta dv ON ve.idventa = dv.idventa\
                            INNER JOIN empleado em ON ve.idempleado = em.idempleado\
                            WHERE ve.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}' AND CONCAT(cl.nombre, ' ', cl.apellidos) LIKE '%{Buscar}%'\
                            GROUP BY ve.idventa, ve.fecha, CONCAT(cl.nombre, ' ', cl.apellidos),\
                            dv.descuento, ve.itbis, ve.serie, em.nombre, ve.comentario;")
                
                # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
                model = QSqlTableModel()    
                model.setQuery(query)        
                self.tbDatos.setModel(model)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualizar_datos_detalle_venta(self):
        idventa = self.txtCodigo.text()
        query = QSqlQuery()
        query.exec_(f"SELECT dv.iddetalle_venta as 'ID DETALLE',\
                        dv.idventa as 'ID COTIZACION',\
                        CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                        ar.nombre as 'ARTICULO',\
                        FORMAT(dv.precio_venta, 'C', 'en-US') as 'PRECIO',\
                        dv.cantidad as 'CANTIDAD',\
                        dv.descuento as 'DESCUENTO %',\
                        ve.itbis as 'IMPUESTOS %',\
                        ve.serie as 'NO. VENTA',\
                        em.nombre as 'VENDEDOR'\
                    FROM venta ve\
                    INNER JOIN cliente cl ON ve.idcliente = cl.idcliente\
                    INNER JOIN detalle_venta dv ON ve.idventa = dv.idventa\
                    INNER JOIN articulo ar ON dv.idarticulo = ar.idarticulo\
                    INNER JOIN empleado em ON ve.idempleado = em.idempleado\
                    WHERE dv.idventa = {idventa};")
        
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbDatos2.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos2.resizeColumnsToContents()
        self.tbDatos2.setEditTriggers(QAbstractItemView.NoEditTriggers)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------               
    # Funciones llamadas por los botones imprimir y pdf, para asignar la opcion a cada boton
    # segun decida el usuario.
    def imprime_pdf(self):
        opcion = "open"
        self.imprimir_pdf(opcion)
    def imprime_hoja(self):
        opcion = "print"
        self.imprimir_pdf(opcion)
        
    def imprimir_pdf(self, opcion):
        # Verifica si se ha terminado de ingresar los articulos para proceder a crear el pdf
        if self.se_llamo_activar_botones:
            QMessageBox.warning(self, "ERROR", "TIENE UNA VENTA ABIERTA, FAVOR TERMINAR DE INGRESAR LOS ARTICULOS.")
            
        else:
            # Obtener el índice de la fila seleccionada
            indexes = self.tbDatos.selectedIndexes()
            
            # Obtiene la fecha actual para usar en el pdf
            fecha = QDate.currentDate()
            fecha_formato = fecha.toString("dd-MMMM-yyyy")

            if indexes:
                    
                # Obtener el numero (int) de la fila al seleccionar una celda de la tabla ventas
                index = indexes[0]
                row = index.row()
                
                # Con el parametro row como int se obtienen todos los datos de la fila seleccionada, datos 
                # que seran usados para la creacion del pdf.
                self.obtener_id_venta(row)               
                
                
                # Preguntar si el usuario está seguro de convertir la factura seleccionada
                confirmacion = QMessageBox.question(self, "MENSAJE", "¿ESTA SEGURO QUE QUIERE CONTINUAR?",
                                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                    
                    
                # Si el usuario hace clic en el botón "Sí", convierte la factura en pdf
                if confirmacion == QMessageBox.Yes:
                    
                    c = canvas.Canvas(f"Sistema de ventas/pdf/Facturas/Factura {self.bd_serie}.pdf", pagesize=letter)

                    # Agregar el logo de la empresa
                    c.drawImage("Sistema de ventas/imagenes/Logo.jpg", 400, 700, width=150, height=75)

                    # Datos de la empresa
                    data = [
                        ["Ferremar"],
                        ["Ave. Ind. km 12 1/2 # 23."],
                        ["809-534-2323"]
                    ]

                    table = Table(data)

                    # Establecer el estilo de la tabla para datos de la empresa
                    style = TableStyle([
                        ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
                        ('TEXTCOLOR', (0,0), (-1,-1), colors.black),

                        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                        ('FONTSIZE', (0,0), (-1,-1), 12),

                        ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                        ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                        ('GRID', (0,0), (-1,-1), 1, colors.black)
                    ])
                    table.setStyle(style)

                    # Agregar la tabla de datos de la empresa al canvas
                    table.wrapOn(c, 50, 750)
                    table.drawOn(c, 50, 700)

                    # No. Cotización y fecha
                    c.setFont("Helvetica-Bold", 15)
                    c.drawString(390,680,"Factura: " + str(self.bd_serie))
                    c.setFont("Helvetica", 10)
                    c.drawString(390,660,"Fecha Fac.: " + f"{self.bd_fecha}")

                    # Datos del cliente
                    c.setFont("Helvetica-Bold", 15)
                    c.drawString(50,680,"Cliente: " + str(self.bd_cliente))
                    c.setFont("Helvetica", 10)
                    c.drawString(50,660,"Fecha de impresion: " + str(fecha_formato))
                    
                    # Dibujar una línea debajo de los datos de la empresa y logo.
                    c.line(50, 695, 550, 695)

                    # Dibujar una línea debajo de los datos del cliente
                    c.line(50, 650, 550, 650)
                    
                    # Cabecera de los datos de los artículos
                    c.setFont("Helvetica-Bold", 12)
                    #c.drawString(50, 630, "ID")
                    c.drawString(50, 630, "CODIGO")
                    c.drawString(120, 630, "CANT.") 
                    c.drawString(170, 630, "ARTICULO")                 
                    c.drawString(340, 630, "PRECIO")
                    c.drawString(410, 630, "VENTA POR")
                    c.drawString(495, 630, "TOTAL")

                    # Datos de los artículos.
                    detalles = self.obtener_detalles_venta(self.bd_id_venta)
                    y = 610
                    for detalle in detalles:
                        c.setFont("Helvetica", 10)
                        #c.drawString(50, y, str(detalle['idarticulo']))
                        c.drawString(50, y, self.obtener_codigo_articulo(detalle['idarticulo']))
                        c.drawString(120, y, str(detalle['cantidad']))

                        # Guardar la posición "y" (up/down) antes de dibujar el nombre del artículo
                        # esta posicion la uso para que si el nombre del articulo tiene varias lineas
                        # las demas columnas queden alineadas con la primera linea del nombre de articulo.
                        alinear_columnas = y

                        # Obtener el nombre del artículo y dividirlo en varias líneas si es demasiado largo
                        nombre_articulo = self.obtener_nombre_articulo(detalle['idarticulo']) # obtengo el nombre del articulo en la variable nombre_articulo
                        lineas_nombre_articulo = textwrap.wrap(nombre_articulo, width=30)  # Ajusta el ancho a un espacio de 30 caracteres.

                        # Revisa cada nombre de articulo si alguno pasa de 30 caracteres crea un salto de linea.
                        for linea in lineas_nombre_articulo:
                            c.drawString(170, y, linea)
                            y -= 20
                            
                        c.drawString(340, alinear_columnas, "$" + "{:,.2f}".format(detalle['precio_venta']))
                        c.drawString(410, alinear_columnas, self.obtener_presentacion_articulo(self.obtener_codigo_articulo(detalle['idarticulo'])))
                        c.drawString(495, alinear_columnas, "$" + "{:,.2f}".format(detalle['cantidad'] * detalle['precio_venta']))
                        y -= 20

                        # Si los articulos llegan a la línea 40, se crea una nueva página
                        # para seguir imprimiendo en ella
                        if y <= 40:
                            c.showPage()
                            y = 700  # Posición inicial en "y" (up/down) de la nueva pagina creada.

                    # Totales, subtotales, impuestos, etc.
                    c.setFont("Helvetica-Bold", 16)
                    c.drawString(50,120,"Subtotal: " + str(self.bd_sub_total))
                    c.drawString(50,100,"Impuesto: " + str(int(self.bd_impuesto)) + "%")
                    c.drawString(50,80,"Descuento: " + str(int(self.bd_descuento)) + "%")
                    c.drawString(50,60,"Total: " + str(self.bd_total))

                    # Nombre del empleado que crea la cotizacion
                    c.setFont("Helvetica", 10)
                    c.drawString(50,40,"Le atendió: " + str(self.obtener_nombre_empleado(self.bd_id_venta)).lower())

                    # Comentario de la cotizacion al pie de la hoja
                    c.setFont("Helvetica", 10)
                    c.drawString(50, 20,"Comentario: " + "**" + str(self.bd_comentario).lower() + "**") 

                    c.save()

                    # Ruta completa del archivo PDF para ser usada para imprimir el pdf creado.
                    pdf_file_name = os.path.abspath(f"Sistema de ventas/pdf/Facturas/Factura {self.bd_serie}.pdf")

                    # Abrir el cuadro de diálogo de impresión de Windows, open abre el pdf pero print deberia
                    # poder imprimir por impresora el archivo
                    if opcion == "open":
                        win32api.ShellExecute(0, "open", pdf_file_name, None, ".", 0) # type: ignore
                    else:
                        win32api.ShellExecute(0, "print", pdf_file_name, None, ".", 0) # type: ignore
                        
                        # Esperar un poco para que el archivo PDF se cargue en la impresora
                        time.sleep(5)

                        # Intentar eliminar el archivo PDF
                        max_intentos = 60  # Número máximo de intentos
                        intentos = 0

                        while intentos < max_intentos:
                            try:
                                os.remove(pdf_file_name)
                                break  # Si el archivo se eliminó con éxito, salir del bucle
                            except PermissionError:
                                time.sleep(1)  # Si el archivo aún está en uso, esperar un poco y volver a intentarlo
                                intentos += 1

                        if intentos == max_intentos:
                            msg = QMessageBox()
                            msg.setIcon(QMessageBox.Critical)
                            msg.setText("Error")
                            msg.setInformativeText("No se pudo eliminar el archivo después de 3 intentos.")
                            msg.setWindowTitle("Error")
                            msg.exec_()

                    QMessageBox.warning(self, "MENSAJE", "HECHO SATISCAFTORIAMENTE")
                    
            else:
                QMessageBox.warning(self, "ERROR", "SELECCIONA LA FACTURA PARA CONTINUAR.")
            
            
    # Obtiene datos importante de la tabla detalle_venta para imprimirlos en el pdf de la venta    
    def obtener_detalles_venta(self, id_venta):
        query = QSqlQuery()
        query.prepare("SELECT * FROM detalle_venta WHERE idventa = :idventa")
        query.bindValue(":idventa", id_venta)
        query.exec_()

        detalles = []
        while query.next():
            detalles.append({
                    'idarticulo': query.value('idarticulo'),
                    #'comentario': query.value('comentario'),
                    'cantidad': query.value('cantidad'),
                    'precio_venta': query.value('precio_venta'),
                    'descuento': query.value('descuento')
                })

        return detalles
        
    # Obtiene el nombre del articulo mediante el idarticulo insertado en la tabla detalle_venta
    # para imprimirlo en el pdf de la factura.
    def obtener_nombre_articulo(self, id_articulo):
        query = QSqlQuery()
        query.prepare("SELECT nombre FROM articulo WHERE idarticulo = :idarticulo")
        query.bindValue(":idarticulo", id_articulo)
        query.exec_()

        if query.next():
            return query.value('nombre')

        return ""
        
    # Obtiene la descripcion de la tabla presentacion mediante el codigo del articulo (no idarticulo) que esta en la tabla venta
    # primero obtengo el codigo del articulo mediante la funcion obtener_codigo_articulo() para luego sacar la presentacion del mismo.
    def obtener_presentacion_articulo(self, codigo_articulo):
        query = QSqlQuery()
        query.prepare("DECLARE @idpresentacion INT "
                        "SELECT @idpresentacion = idpresentacion FROM articulo WHERE codigo = :codigo "
                        "SELECT descripcion FROM presentacion WHERE idpresentacion = @idpresentacion")
        query.bindValue(":codigo", codigo_articulo)
        query.exec_()

        if query.next():
            return query.value('descripcion')

        return ""

    # obtener el codigo del articulo (no idarticulo) para imprimirlo en los de talle del articulos del pdf
    # y tambien se usa este codigo para obtener la descripcion de la presentacion para imprimirla en el pdf. 
    def obtener_codigo_articulo(self, id_articulo):
        query = QSqlQuery()
        query.prepare("SELECT codigo FROM articulo WHERE idarticulo = :idarticulo")
        query.bindValue(":idarticulo", id_articulo)
        query.exec_()

        if query.next():
            return query.value('codigo')

        return ""
    
    # obtiene el nombre y apellido del empleado que creo la cotizacion mediante el
    # idventa sabemos el idempleado que luego utilizamos para tener el nombre completo
    def obtener_nombre_empleado(self, id_venta):
        query = QSqlQuery()
        query.prepare("SELECT CONCAT(e.nombre, ' ', e.apellidos) "
                      "FROM empleado e "
                      "INNER JOIN venta v ON e.idempleado = v.idempleado "
                      "WHERE v.idventa = :idventa")
        query.bindValue(":idventa", id_venta)
        query.exec_()

        if query.next():
            return query.value(0)

        return ""
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
    def insertar_datos_venta(self):
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
            if not num_comprobante:
                num_comprobante = 0
            
            if not all([idempleado, idcliente, idempleado, fecha, tipo_comprobante]):
        
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
                    
                    insertar_nueva_venta(idcliente, idempleado, fecha, tipo_comprobante, num_comprobante, itbis, comentario)
                    
                    self.activar_botones_detalle()
                    self.desactivar_botones_venta()


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
            mensaje.setText(f"Se produjo un error en venta: {str(e)}")
            mensaje.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def insertar_detalle_venta(self):
        try:
            idoctizacion = self.txtCodigo.text()
            idarticulo = self.txtCodArticulo.text()
            catidad = int(self.txtCantidad.text())
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
                
                insertar_nuevo_detalle_venta(idoctizacion, idarticulo, catidad, precio_venta, descuento)

                self.visualizar_datos_venta()
                self.visualizar_datos_detalle_venta()
                self.actualizar_existencia_producto()
                
                
                
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
    def devolucion_de_venta(self):
        if self.se_llamo_activar_botones:
            QMessageBox.warning(self, "ERROR", "TIENE UNA VENTA ABIERTA, FAVOR TERMINAR DE INGRESAR LOS ARTICULOS.")
        
        else:
            # Obtener el índice de la fila seleccionada
            indexes = self.tbDatos.selectedIndexes()
            
            if indexes:
                
                # Obtener el numero (int) de la fila al seleccionar una celda de la tabla detalle_venta
                index = indexes[0]
                row = index.row()
                
                self.obtener_id_venta(row)
                id_venta = self.bd_id_venta


                # Preguntar si el usuario está seguro de crear una devolucion de la venta seleccionada
                confirmacion = QMessageBox.question(self, "DEVOLUCION?", "¿QUIERE HACER UNA DEVOLUCION DE ESTA FACTURA?",
                                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                
                
                # Si el usuario hace clic en el botón "Sí", elimina el detalle
                if confirmacion == QMessageBox.Yes:
                    if revertir_venta(id_venta):
                        QMessageBox.warning(self, "DEVOLUCION SATISFACTORIA", "FACTURA ANULADA.")
                        self.visualizar_datos_venta()
            else:
                QMessageBox.warning(self, "ERROR", "SELECCIONA LA VENTA QUE LLEVA DEVOLUCION.")
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Pasando como parametro el numero de fila el cual obtengo al seleccionar un celda en el QTableView obtengo datos que necesito
    # estos datos son usado con varios propositos como la impresion de informacion al crear un pdf por ejemplo.
    # los SELECT usados aqui son los mismo que muestran informacion al crear las ventas, son los datos mas relevantes.            
    def obtener_id_venta(self, num_fila):
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
                                ve.idventa as 'ID',\
                                UPPER(FORMAT(ve.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                                dv.descuento as 'DESCUENTO %',\
                                ve.itbis as 'IMPUESTOS %',\
                                ve.serie as 'NO. VENTA',\
                                em.nombre as 'VENDEDOR',\
                                FORMAT(SUM(dv.cantidad * dv.precio_venta), 'C', 'en-US') as 'SUB TOTAL',\
                                FORMAT(SUM((dv.cantidad * dv.precio_venta * (1 - (dv.descuento / 100))) * (1 + (ve.itbis / 100))), 'C', 'en-US') as 'TOTAL',\
                                ve.comentario as 'COMENTARIO'\
                            FROM venta ve\
                            INNER JOIN cliente cl ON ve.idcliente = cl.idcliente\
                            INNER JOIN detalle_venta dv ON ve.idventa = dv.idventa\
                            INNER JOIN empleado em ON ve.idempleado = em.idempleado\
                            WHERE ve.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}'\
                            GROUP BY ve.idventa, ve.fecha, CONCAT(cl.nombre, ' ', cl.apellidos),\
                            dv.descuento, ve.itbis, ve.serie, em.nombre, ve.comentario;")
                
                # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
                model = QSqlTableModel()    
                model.setQuery(query)        
                self.tbDatos.setModel(model)

                # Obtener el modelo de datos del QTableView
                modelo = self.tbDatos.model()
                if modelo is not None and 0 <= num_fila < modelo.rowCount():
            
                    # Obtener los datos de las columnas de la fila seleccionada
                    columna_id = modelo.index(num_fila, 0).data()
                    columna_fehca = modelo.index(num_fila, 1).data()
                    columna_cliente = modelo.index(num_fila, 2).data()
                    columna_descuento = modelo.index(num_fila, 3).data()
                    columna_impuesto = modelo.index(num_fila, 4).data()
                    columna_serie = modelo.index(num_fila, 5).data()
                    columna_sub_total = modelo.index(num_fila, 7).data()
                    columna_total = modelo.index(num_fila, 8).data()
                    columna_comentario = modelo.index(num_fila, 9).data()
                    
                    
                    self.bd_id_venta = columna_id
                    self.bd_fecha = columna_fehca
                    self.bd_cliente = columna_cliente
                    self.bd_serie = columna_serie
                    self.bd_sub_total = columna_sub_total
                    self.bd_total = columna_total
                    self.bd_impuesto = columna_impuesto
                    self.bd_descuento = columna_descuento
                    self.bd_comentario = columna_comentario
        else:
            if FechaInicio > FechaFinal:                        
                        QMessageBox.warning(self, "ERROR ENTRE FECHAS", "LA PRIMERA FECHA NO PUEDE SER MAYOR A LA SEGUNDA.")
                        return
            else:
                query = QSqlQuery()
                query.exec_(f"SELECT\
                                ve.idventa as 'ID',\
                                UPPER(FORMAT(ve.fecha, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA',\
                                CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                                dv.descuento as 'DESCUENTO %',\
                                ve.itbis as 'IMPUESTOS %',\
                                ve.serie as 'NO. VENTA',\
                                em.nombre as 'VENDEDOR',\
                                FORMAT(SUM(dv.cantidad * dv.precio_venta), 'C', 'en-US') as 'SUB TOTAL',\
                                FORMAT(SUM((dv.cantidad * dv.precio_venta * (1 - (dv.descuento / 100))) * (1 + (ve.itbis / 100))), 'C', 'en-US') as 'TOTAL',\
                                ve.comentario as 'COMENTARIO'\
                            FROM venta ve\
                            INNER JOIN cliente cl ON ve.idcliente = cl.idcliente\
                            INNER JOIN detalle_venta dv ON ve.idventa = dv.idventa\
                            INNER JOIN empleado em ON ve.idempleado = em.idempleado\
                            WHERE ve.fecha BETWEEN '{FechaInicio}' AND '{FechaFinal}' AND CONCAT(cl.nombre, ' ', cl.apellidos) LIKE '%{Buscar}%'\
                            GROUP BY ve.idventa, ve.fecha, CONCAT(cl.nombre, ' ', cl.apellidos),\
                            dv.descuento, ve.itbis, ve.serie, em.nombre, ve.comentario;")
                
                # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
                model = QSqlTableModel()    
                model.setQuery(query)        
                self.tbDatos.setModel(model)

                # Obtener el modelo de datos del QTableView
                modelo = self.tbDatos.model()
                if modelo is not None and 0 <= num_fila < modelo.rowCount():
            
                    # Obtener los datos de las columnas de la fila seleccionada
                    columna_id = modelo.index(num_fila, 0).data()
                    columna_fehca = modelo.index(num_fila, 1).data()
                    columna_cliente = modelo.index(num_fila, 2).data()
                    columna_descuento = modelo.index(num_fila, 3).data()
                    columna_impuesto = modelo.index(num_fila, 4).data()
                    columna_serie = modelo.index(num_fila, 5).data()
                    columna_sub_total = modelo.index(num_fila, 7).data()
                    columna_total = modelo.index(num_fila, 8).data()
                    columna_comentario = modelo.index(num_fila, 9).data()
                    
                    
                    self.bd_id_venta = columna_id
                    self.bd_fecha = columna_fehca
                    self.bd_cliente = columna_cliente
                    self.bd_serie = columna_serie
                    self.bd_sub_total = columna_sub_total
                    self.bd_total = columna_total
                    self.bd_impuesto = columna_impuesto
                    self.bd_descuento = columna_descuento
                    self.bd_comentario = columna_comentario
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def quitar_datos_detalle_venta(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.tbDatos2.selectedIndexes()
        
        if indexes:
            
            # Obtener el numero (int) de la fila al seleccionar una celda de la tabla detalle_venta
            index = indexes[0]
            row = index.row()
            
            self.obtener_datos_de_fila_detalle_venta(row)
            id_detalle_venta = self.bd_id_detalle_venta
            
            
            
            # Preguntar si el usuario está seguro de eliminar el detalle de la venta seleccionada
            confirmacion = QMessageBox.question(self, "ELIMINAR?", "¿QUIERE ELIMINAR ESTE ARTICULO DE LA LISTA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", elimina el detalle
            if confirmacion == QMessageBox.Yes:
                revertir_detalle_venta(id_detalle_venta)
                QMessageBox.warning(self, "ELIMINADO", "ARTICULO ELIMINADO.")
                self.visualizar_datos_detalle_venta()
                self.visualizar_datos_venta()
                self.actualizar_existencia_producto()
                self.verificar_y_ocultar_botones()
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA EL ARTICULO QUE VAS A ELIMINAR.")
            
        # Pasando como parametro el numero de fila, obtengo el id de la venta.
    def obtener_datos_de_fila_detalle_venta(self, num_fila):
        idventa = self.txtCodigo.text()
        query = QSqlQuery()
        query.exec_(f"SELECT dv.iddetalle_venta as 'ID DETALLE',\
                        dv.idventa as 'ID VENTA',\
                        CONCAT(cl.nombre, ' ', cl.apellidos) as 'CLIENTE',\
                        ar.nombre as 'ARTICULO',\
                        FORMAT(dv.precio_venta, 'C', 'en-US') as 'PRECIO',\
                        dv.cantidad as 'CANTIDAD',\
                        dv.descuento as 'DESCUENTO %',\
                        ve.itbis as 'IMPUESTOS %',\
                        ve.serie as 'NO. VENTA',\
                        em.nombre as 'VENDEDOR'\
                    FROM venta ve\
                    INNER JOIN cliente cl ON ve.idcliente = cl.idcliente\
                    INNER JOIN detalle_venta dV ON ve.idventa = dv.idventa\
                    INNER JOIN articulo ar ON dv.idarticulo = ar.idarticulo\
                    INNER JOIN empleado em ON ve.idempleado = em.idempleado\
                    WHERE dv.idventa = {idventa};")
        model = QSqlTableModel()    
        model.setQuery(query)
        self.tbDatos2.setModel(model)
        
        # Obtener el modelo de datos del QTableView
        modelo = self.tbDatos2.model()
        if modelo is not None and 0 <= num_fila < modelo.rowCount():
            
            # Obtener los datos de la fila seleccionada
            columna_id = modelo.index(num_fila, 0).data()
            self.bd_id_detalle_venta = columna_id
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # si se elimina el ultimo detalle_venta se inhabilitan los botones de insertar detalles
    def verificar_y_ocultar_botones(self):
        idventa = self.txtCodigo.text()
        
        query = QSqlQuery()
        query.prepare(f"SELECT COUNT(*) FROM detalle_venta WHERE idventa = :idventa")
        query.bindValue(":idventa", idventa)
        
        if query.exec_() and query.next():
            num_detalles = query.value(0)
        
            if num_detalles == 0:
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("SE ELIMINARON TODOS LOS ARTICULOS")
                mensaje.setText("INGRESO DE ARTICULOS FINALIZADO, SE BLOQUEARAN LAS FUNICONES.")
                mensaje.exec_()
                self.ocultar_botones_detalle_al_revertir_venta()  # Llama a la función para ocultar botones.
                self.actualizar_ID_venta() # Actualiza el idventa por si el usuario quiere volver a insertar detalles
                self.activar_botones_venta() # Activo los botones para insertar nueva venta.
                self.actualizar_num_venta() # Actualiza el codigo de venta por si el usuario quiere volver a insertar detalles
                
                # Refrescar los datos de las ventas y los de detalle_venta.
                self.visualizar_datos_venta()
                self.visualizar_datos_detalle_venta()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def closeEvent(self, event):        
        # Preguntar si el usuario está seguro de cerrar la ventana
        confirmacion = QMessageBox.question(self, "¿ESTAS SEGURO QUE DESEA SALIR?", "Cotinue solo ha terminado de insertar todos los ariculos",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
                                                                
        # Si el usuario hace clic en el botón "Sí", cierra la ventana
        if confirmacion == QMessageBox.No:
            event.ignore()
        else:
            VentanaVentas.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
            event.accept()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Elimina el textp de referencia que tiene la casilla buscar
    def borrarTexto(self, event):
        # Borrar el texto cuando se hace clic
        self.txtBuscar.clear()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)
        
        self.tbSesiones.hide()
        self.ocultar_botones_detalle()
        self.visualizar_datos_venta()
        self.actualizar_num_venta()
        self.actualizar_ID_venta()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaVentas()
    GUI.show()
    sys.exit(app.exec_())