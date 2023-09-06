import sys
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
        self.btnBorrar.clicked.connect(self.borrar_fila)
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
        self.cmbProducto.currentIndexChanged.connect(
            lambda i: self.actualizar_existencia_producto(self.cmbProducto.currentText()))
        
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
        
        
    def actualizar_existencia_producto(self, producto):
        model = QSqlTableModel()
        model.setTable('Stock')
        model.setFilter(f"Producto='{producto}'")
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
    #aqui va el codigo para la impresion de la factura
    def generate_invoice(self):
        
        items_from_table = []
        indexes = self.dataView.selectedIndexes()
        
        index = indexes[0]
        rows = index.row()
        
        

        now = datetime.now()        
        fecha_hora = now.strftime("%Y%m%d%H%M%S")
        fecha = now.strftime("%Y-%m-%d")
        # Datos de la factura (personaliza estos datos)
        invoice_data = {
            'invoice_number': f'# {fecha_hora}',
            'invoice_date': f'{fecha}',
            'due_date': f'{fecha}',
            'customer_name': 'JOSE LUIS PEREZ',
            'customer_address': 'C/ 1ra la cartonera, piedra blanca, Haina.',
            'items': [
                {'description': 'CODIGO', 'quantity': "DESCRIPCION", 'unit_price': "UND", 'total': "CANT."},
            ],
            'total': 190,
        }

        # Crear un documento PDF
        pdf_filename = f'Documento de salida {fecha_hora}.pdf'
        doc = SimpleDocTemplate(pdf_filename, pagesize=landscape(letter))

        # Crear una lista de elementos (contenido) para la factura
        elements = []

        # Agregar el encabezado de la factura
        styles = getSampleStyleSheet()
        header_text = Paragraph(f'<b>Documento de salida {invoice_data["invoice_number"]}</b>', styles['Heading2'])
        elements.append(header_text)

        # Agregar información de la factura y el cliente
        elements.append(Paragraph(f'Fecha de Factura: {invoice_data["invoice_date"]}', styles['Normal']))
        elements.append(Paragraph(f'Fecha de Vencimiento: {invoice_data["due_date"]}', styles['Normal']))
        elements.append(Paragraph(f'Entregado a: {invoice_data["customer_name"]}', styles['Normal']))
        elements.append(Paragraph(f'Dirección: {invoice_data["customer_address"]}', styles['Normal']))

        #item_data = []
        #for row in invoice_data[rows]:
            #codigo = self.dataView.columnAt(2)  # Columna 0
            #descripcion = self.dataView.columnAt(6) # Columna 1
            #und = self.dataView.columnAt(4)  # Columna 2
            #cant = self.dataView.columnAt(8)  # Columna 3

            # Agregar los datos de la fila a la lista de ítems
            #item_data.append({'description': codigo, 'quantity': descripcion, 'unit_price': und, 'total': cant})
        
        # Agregar la tabla de ítems
        item_data = []
        for item in invoice_data['items']:
            item_data.append([item['description'], item['quantity'], item['unit_price'], item['total']])

        item_table = Table(item_data, colWidths=[65, 300, 60, 60])
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
        elements.append(Paragraph(f'Total: ${invoice_data["total"]}', styles['Heading3']))

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
            mensaje.setText(f"Error de cantidad: {str(e)}")
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