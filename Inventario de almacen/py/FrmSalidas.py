import sys, os, subprocess
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView
from PyQt5 import QtGui
from datetime import datetime
from PyQt5.QtCore import QDate, QPoint
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from FrmProductos import VentanaProductos
from FrmClientes import Ventanaclientes
from Consultas_db import insertar_detalle_salida, insertar_producto_en_salida
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle

class VentanaSalidas(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Inventario de almacen/ui/FrmSalidas.ui',self)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('REQUISICION DE MATERIALES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Inventario de almacen/png/folder.png'))  
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Esrtabece los focos a los texbox en orden de arriba hacia abajo.
        
        self.setTabOrder(self.cmbDocumento, self.cmbClientes)
        self.setTabOrder(self.cmbClientes, self.txtComentario)
        self.setTabOrder(self.txtComentario, self.cmbCodigo)
        self.setTabOrder(self.cmbCodigo, self.cmbProducto)
        self.setTabOrder(self.cmbProducto, self.txtExistencia)
        self.setTabOrder(self.txtExistencia, self.txtCantidad)
        self.setTabOrder(self.txtCantidad, self.btnSalir)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

        #Llamar a los diferentes formularios desde los botones
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnGuardar.clicked.connect(self.insertar_datos)
        self.btnLimpiar.clicked.connect(self.limpiar_textbox)
        #self.btnBorrar.clicked.connect(self.borrar_fila)
        self.btnFrmProductos.clicked.connect(self.abrirFrmProductos)
        self.btnFrmClientes.clicked.connect(self.abrirFrmClientes)
        self.btnImprimir.clicked.connect(self.generate_invoice)
        
        # Evento que inserta el codigo de producto cuando seleccionas un nombre del cmbProducto.
        self.cmbProducto.currentIndexChanged.connect(
            lambda i: self.actualizar_codigo_producto(self.cmbProducto.currentText()))
        
        # Evento que inserta la unidad del producto cuando seleccionas un nombre del cmbProducto
        self.cmbProducto.currentIndexChanged.connect(
            lambda i: self.actualizar_categoria_producto(self.cmbProducto.currentText()))
        
        # Evento que inserta la categoria del producto cuando seleccionas un nombre del cmbProducto.
        self.cmbCodigo.currentIndexChanged.connect(
            lambda i: self.actualizar_existencia_producto(self.cmbCodigo.currentText()))
        
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
        model.setTable('Clientes')
        model.select()
        columna_proveedor = []
        for i in range(model.rowCount()):
            columna_proveedor.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Nombre de la tabla Proveedores en el QComboBox asignado.
        combo_model = QStandardItemModel()
        for item in columna_proveedor:
             combo_model.appendRow(QStandardItem(str(item)))
        self.cmbClientes.setModel(combo_model)
        
        
        
        # Obtiene el último dato de la columna N_Doc de la tabla Salidas y le suma uno.
        model = QSqlTableModel()
        model.setTable('Salidas')
        model.select()
        last_row_index = model.rowCount() - 1  # Índice del último registro

        if last_row_index > 0:  # Verificar si hay datos en la tabla
            last_Ndoc = int(model.data(model.index(last_row_index, 0)))       
            next_Ndoc = last_Ndoc + 1

            combo_model = QStandardItemModel()
            combo_model.appendRow(QStandardItem(str(next_Ndoc)))
    
            if next_Ndoc > 0: #combo_model.rowCount() > 0:
                self.cmbDocumento.setModel(combo_model)
            else:
                self.cmbDocumento.setCurrentText("")
        else:
            #self.cmbDocumento.setModel(None)  # No hay datos, configurar el combo box sin modelo
            self.cmbDocumento.setPlaceholderText("")

            


        
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
        
    # szxczxcxcvxcvxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcvzxcv. 
    def actualizar_categoria_producto(self, categoria):
        model = QSqlTableModel()
        model.setTable('Productos')
        model.setFilter(f"Nombre='{categoria}'")
        model.select()
        columna_medida = []
        for i in range(model.rowCount()):
            columna_medida.append(model.data(model.index(i, 1)))

        combo_und = QStandardItemModel()
        for item in columna_medida:
            combo_und.appendRow(QStandardItem(str(item)))
        self.cmbCategoria.setModel(combo_und)
        
        
    def actualizar_existencia_producto(self, codigo):
        model = QSqlTableModel()
        model.setTable('Stock')
        model.setFilter(f"Codigo='{codigo}'")
        model.select()

        medida = ""
        if model.rowCount() > 0:
            medida = model.data(model.index(0, 2))

            self.txtExistencia.setText(str(medida)) 
        else:
            self.txtExistencia.setText("Sin existencia") 
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------          
    
    #Funciones para llamar las ventanas secundarias y mostrarlas    
    def abrirFrmProductos(self):
        self.llamar_venana_productos = VentanaProductos()
        self.llamar_venana_productos.show()

    def abrirFrmClientes(self):
        self.llamar_venana_clientes = Ventanaclientes()
        self.llamar_venana_clientes.show()
    
    def fn_Salir(self):
        self.close()
        
        
    def limpiar_textbox(self):
        #Limpia los TexBox
        self.txtFecha.setDate(QDate.currentDate())        
        self.cmbDocumento.setCurrentText("")
        self.txtComentario.setText("") 
        self.cmbCodigo.setCurrentText("")
        self.cmbCategoria.setCurrentText("")  
        self.txtExistencia.setText("") 
        self.txtCantidad.setText("") 
        self.cmbClientes.setCurrentText("") 
        self.cmbProducto.setCurrentText("")         
        self.txtComentario.setFocus()
        
        
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT DS.Fecha, DS.Cliente, S.Codigo, S.Categoria, S.Producto, S.CantidadTotal as 'Cantidad', DS.Comentario\
                            FROM DetalleSalidas AS DS\
                            JOIN Salidas AS S ON DS.ID = S.ID_Salida")
        
           
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)
        self.dataView.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.dataView.resizeColumnsToContents()
        self.dataView.setEditTriggers(QAbstractItemView.NoEditTriggers)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    def obtener_datos_de_fila(self, fila_seleccionada):
        # Obtener el modelo de datos del QTableView
        modelo = self.dataView.model()

        if modelo is not None and 0 <= fila_seleccionada < modelo.rowCount():
            # Obtener los datos de la fila seleccionada
            columna_0 = modelo.index(fila_seleccionada, 0).data()
            columna_1 = modelo.index(fila_seleccionada, 1).data()
            columna_2 = modelo.index(fila_seleccionada, 2).data()
            columna_4 = modelo.index(fila_seleccionada, 4).data()
            columna_5 = modelo.index(fila_seleccionada, 5).data()
            columna_6 = modelo.index(fila_seleccionada, 6).data()

            self.valor_columna_0 = columna_0
            self.valor_columna_1 = columna_1
            self.valor_columna_2 = columna_2
            self.valor_columna_4 = columna_4
            self.valor_columna_5 = columna_5
            self.valor_columna_6 = columna_6
            

    #aqui va el codigo para la impresion de la factura
    def generate_invoice(self):
        
        # Obtener el índice de la fila seleccionada
        indexes = self.dataView.selectedIndexes()
        
        if indexes:
            
            # Obtener la fila al seleccionar una celda de la tabla
            index = indexes[0]
            row = index.row()

            self.obtener_datos_de_fila(row)
            
            now = datetime.now()        
            fecha_hora = now.strftime("%Y%m%d%H%M%S")
            fecha = now.strftime("%Y-%m-%d")
            # Datos de la factura 
            invoice_data = {
                'invoice_number': f'',
                'invoice_date': f'{self.valor_columna_0}',
                'due_date': f'{fecha_hora}',
                'customer_name': f'{self.valor_columna_1}',
                'customer_address': 'C/ 1ra la cartonera, piedra blanca, Haina.',
                'items': [
                    {'codigo': 'CODIGO', 'producto': "DESCRIPCION", 'comentario': "COMENTARIO", 'cantidad': "CANTIDAD"},
                    {'codigo': self.valor_columna_2, 'producto': self.valor_columna_4, 'comentario': self.valor_columna_6, 'cantidad': self.valor_columna_5},
                    
                ],
                'Firma': "__________________",
            }

            
            # Obtener el directorio actual del proyecto
            directorio_proyecto = os.getcwd()
            # Crear la ruta completa al archivo PDF en el directorio del proyecto
            pdf_filename = os.path.join(f'{directorio_proyecto}/Inventario de almacen/pdf', f'Documento de salida {fecha_hora}.pdf')
            # Crear un documento PDF
            doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))

            # Crear una lista de elementos (contenido) para la factura
            elements = []

            # Agregar el encabezado de la factura
            styles = getSampleStyleSheet()
            header_text = Paragraph(f'<b>SALIDA DE ALMACEN {invoice_data["invoice_number"]}</b>', styles['Heading2'])
            elements.append(header_text)

            # Agregar información de la factura y el cliente
            elements.append(Paragraph(f'Fecha de Factura: {invoice_data["invoice_date"]}', styles['Normal']))
            elements.append(Paragraph(f'Codigo de fecha: {invoice_data["due_date"]}', styles['Normal']))
            elements.append(Paragraph(f'Entregado a: {invoice_data["customer_name"]}', styles['Normal']))
            elements.append(Paragraph(f'Dirección: {invoice_data["customer_address"]}', styles['Normal']))
        
        
        
        
            # Agregar la tabla de ítems
            item_data = []
            for item in invoice_data['items']:
                item_data.append([item['codigo'], item['producto'], item['comentario'], item['cantidad']])

            item_table = Table(item_data, colWidths=[65, 250, 300, 60])
            item_table.setStyle(TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
            ]))

            elements.append(item_table)

            # Agregar el total
            elements.append(Paragraph(f'Recibido por: {invoice_data["Firma"]}', styles['Heading3']))

            # Construir el documento PDF
            doc.build(elements)
            
            #mensaje al usuario de pdf guardado
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Creacion de PDF")
            mensaje.setText("Documento guardado con exito.")
            mensaje.exec_()

            
            # Abrir la carpeta con el archivo pdf creado
            ruta = f'{directorio_proyecto}\Inventario de almacen\pdf'
            if os.path.exists(ruta):
                # Utiliza el comando adecuado según tu sistema operativo
                if os.name == 'posix':  # Para sistemas basados en Unix (Linux, macOS)
                    subprocess.Popen(['xdg-open', ruta])
                elif os.name == 'nt':   # Para Windows
                    subprocess.Popen(['explorer', ruta])
            
        else:
            codigo = self.cmbCodigo.currentText()
            producto_nombre = self.cmbProducto.currentText()
            comentario = self.txtComentario.text().upper()
            cantidad = self.txtCantidad.text()
            cliente = self.cmbClientes.currentText()
            
            if not codigo or not producto_nombre or not comentario or not cantidad or not cliente:
                
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
                
            else:
                now = datetime.now()        
                fecha_hora = now.strftime("%Y%m%d%H%M%S")
                fecha = now.strftime("%Y-%m-%d")
                # Datos de la factura 
                invoice_data = {
                    'invoice_number': f'',
                    'invoice_date': f'{fecha}',
                    'due_date': f'{fecha_hora}',
                    'customer_name': cliente,
                    'customer_address': 'C/ 1ra la cartonera, piedra blanca, Haina.',
                    'items': [
                        {'codigo': 'CODIGO', 'producto': "DESCRIPCION", 'comentario': "UNIDAD", 'cantidad': "CANT."},
                        {'codigo': codigo, 'producto': producto_nombre, 'comentario': comentario, 'cantidad': cantidad},
                
                    ],
                    'Firma': "__________________",
                }

                # Obtener el directorio actual del proyecto
                directorio_proyecto = os.getcwd()
                # Crear la ruta completa al archivo PDF en el directorio del proyecto
                pdf_filename = os.path.join(f'{directorio_proyecto}/Inventario de almacen/pdf', f'Documento de salida {fecha_hora}.pdf')
                # Crear un documento PDF
                doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))

                # Crear una lista de elementos (contenido) para la factura
                elements = []

                # Agregar el encabezado de la factura
                styles = getSampleStyleSheet()
                header_text = Paragraph(f'<b>SALIDA DE ALMACEN {invoice_data["invoice_number"]}</b>', styles['Heading2'])
                elements.append(header_text)

                # Agregar información de la factura y el cliente
                elements.append(Paragraph(f'Fecha de Factura: {invoice_data["invoice_date"]}', styles['Normal']))
                elements.append(Paragraph(f'Codigo de fecha: {invoice_data["due_date"]}', styles['Normal']))
                elements.append(Paragraph(f'Entregado a: {invoice_data["customer_name"]}', styles['Normal']))
                elements.append(Paragraph(f'Dirección: {invoice_data["customer_address"]}', styles['Normal']))
        
        
        
        
                # Agregar la tabla de ítems
                item_data = []
                for item in invoice_data['items']:
                    item_data.append([item['codigo'], item['producto'], item['comentario'], item['cantidad']])

                item_table = Table(item_data, colWidths=[65, 300, 200, 60])
                item_table.setStyle(TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
                    ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ]))

                elements.append(item_table)

                # Agregar el total
                elements.append(Paragraph(f'Recibido por: {invoice_data["Firma"]}', styles['Heading3']))

                # Construir el documento PDF
                doc.build(elements)



#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
        
    def insertar_datos(self):
        try:
            documento = self.cmbDocumento.currentText()
            fecha = self.txtFecha.date().toString("yyyy-MM-dd")
            cliente = self.cmbClientes.currentText()
            comentario = self.txtComentario.text().upper() 
            codigo = self.cmbCodigo.currentText()
            categoria = self.cmbCategoria.currentText()
            producto_nombre = self.cmbProducto.currentText()
            cantidad = float(self.txtCantidad.text())
        
            if not cantidad or not fecha or not cliente or not comentario or not codigo or not categoria or not producto_nombre or not documento:
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
        
            else:
                id_salida = insertar_detalle_salida(fecha, cliente, comentario)
                insertar_producto_en_salida(id_salida, codigo, categoria, producto_nombre, cantidad)
                self.visualiza_datos()
                self.generate_invoice()
        
                #Limpia los TexBox
                self.txtFecha.setDate(QDate.currentDate())        
                self.cmbDocumento.setCurrentText("")
                self.txtComentario.setText("")
                self.cmbCodigo.setCurrentText("") 
                self.cmbCategoria.setCurrentText("")
                self.txtExistencia.setText("") 
                self.txtCantidad.setText("") 
                self.cmbClientes.setCurrentText("") 
                self.cmbProducto.setCurrentText("")         
                self.txtComentario.setFocus()
                
        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def borrar_fila(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.dataView.selectedIndexes()
        
        if indexes:
            
            # Obtener la fila al seleccionar una celda de la tabla
            index = indexes[0]
            row = index.row()
            
            # Preguntar si el usuario está seguro de eliminar la fila
            confirmacion = QMessageBox.question(self, "¿ELIMINAR?", "¿ESTA SEGURO QUE QUIERE ELIMINAR ESTA FILA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", eliminar la fila
            if confirmacion == QMessageBox.Yes:
                # Eliminar la fila seleccionada del modelo de datos
                model = self.dataView.model()
                model.removeRow(row)
                QMessageBox.warning(self, "ELIMINADO", "FILA ELIMINADA.")
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA LA FILA QUE VAS A ELIMINAR.")

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def showEvent(self, event):
        super().showEvent(event) 
          
        self.visualiza_datos()
        self.txtComentario.setFocus()
        self.txtFecha.setDate(QDate.currentDate()) 
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaSalidas()
    GUI.show()
    sys.exit(app.exec_())