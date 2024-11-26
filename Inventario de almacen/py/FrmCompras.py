import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView
from PyQt5 import QtGui
from PyQt5.QtCore import QDate
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from FrmProductos import VentanaProductos
from FrmProveedores import Ventanaproveedores
from Consultas_db import insertar_compras


class VentanaCompras(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Inventario de almacen/ui/FrmCompras.ui',self)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('COMPRAS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Inventario de almacen/png/folder.png'))  
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Esrtabece los focos a los texbox en orden de arriba hacia abajo.
        
        self.setTabOrder(self.cmbDocumento, self.cmbProveedor)
        self.setTabOrder(self.cmbProveedor, self.txtComentario)
        self.setTabOrder(self.txtComentario, self.cmbCodigo)
        self.setTabOrder(self.cmbCodigo, self.cmbProducto)
        self.setTabOrder(self.cmbProducto, self.cmbMedida)
        self.setTabOrder(self.cmbMedida, self.txtCantidad)
        self.setTabOrder(self.txtCantidad, self.btnSalir)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

        #Llamar a los diferentes formularios desde los botones
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnGuardar.clicked.connect(self.insertar_datos)
        self.btnLimpiar.clicked.connect(self.limpiar_textbox)
        self.btnBorrar.clicked.connect(self.borrar_fila)
        self.btnFrmProductos.clicked.connect(self.abrirFrmProductos)
        self.btnFrmProveedores.clicked.connect(self.abrirFrmProveedores)
        
        # Evento que inserta el codigo de producto cuando seleccionas un nombre del cmbProducto.
        self.cmbProducto.currentIndexChanged.connect(
            lambda i: self.actualizar_codigo_producto(self.cmbProducto.currentText()))
        
        # Evento que inserta la unidad del producto cuando seleccionas un nombre del cmbProducto
        self.cmbProducto.currentIndexChanged.connect(
            lambda i: self.actualizar_und_producto(self.cmbProducto.currentText()))
        
        # Evento que inserta la categoria del producto cuando seleccionas un nombre del cmbProducto.
        self.cmbProducto.currentIndexChanged.connect(
            lambda i: self.actualizar_categoria(self.cmbProducto.currentText()))
        
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
        model.setTable('Proveedores')
        model.select()
        columna_proveedor = []
        for i in range(model.rowCount()):
            columna_proveedor.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Nombre de la tabla Proveedores en el QComboBox asignado.
        combo_model = QStandardItemModel()
        for item in columna_proveedor:
             combo_model.appendRow(QStandardItem(str(item)))
        self.cmbProveedor.setModel(combo_model)
        
        
        
        # Obtiene el último dato de la columna N_Doc de la tabla Compras.
        model = QSqlTableModel()
        model.setTable('Compras')
        model.select()
        last_row_index = model.rowCount() - 1  # Índice del último registro
        
        if last_row_index > 0:  # Verificar si hay datos en la tabla            
            last_Ndoc = int(model.data(model.index(last_row_index, 1)))
            # Incrementar el último valor en 1 y cargarlo en el QComboBox asignado.
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
    def actualizar_und_producto(self, und):
        model = QSqlTableModel()
        model.setTable('Productos')
        model.setFilter(f"Nombre='{und}'")
        model.select()
        columna_medida = []
        for i in range(model.rowCount()):
            columna_medida.append(model.data(model.index(i, 3)))

        combo_und = QStandardItemModel()
        for item in columna_medida:
            combo_und.appendRow(QStandardItem(str(item)))
        self.cmbMedida.setModel(combo_und)
        
        
    def actualizar_categoria(self, categoria):
        model = QSqlTableModel()
        model.setTable('Productos')
        model.setFilter(f"Nombre='{categoria}'")
        model.select()
        columna_categoria = []
        for i in range(model.rowCount()):
            columna_categoria.append(model.data(model.index(i, 1)))

        combo_categoria = QStandardItemModel()
        for item in columna_categoria:
            combo_categoria.appendRow(QStandardItem(str(item)))
        self.cmbCategoria.setModel(combo_categoria)  

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------          
    
    #Funciones para llamar las ventanas secundarias y mostrarlas    
    def abrirFrmProductos(self):
        self.llamar_venana_productos = VentanaProductos()
        self.llamar_venana_productos.show()

    def abrirFrmProveedores(self):
        self.llamar_venana_proveedores = Ventanaproveedores()
        self.llamar_venana_proveedores.show()
    
    def fn_Salir(self):
        self.close()
        
        
    def limpiar_textbox(self):
        #Limpia los TexBox
        self.txtFecha.setDate(QDate.currentDate())        
        self.cmbDocumento.setCurrentText("")
        self.txtComentario.setText("") 
        self.cmbCodigo.setCurrentText("")
        self.cmbCategoria.setCurrentText("")  
        self.cmbMedida.setCurrentText("") 
        self.txtCantidad.setText("") 
        self.cmbProveedor.setCurrentText("") 
        self.cmbProducto.setCurrentText("")         
        self.txtComentario.setFocus()
        
        
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT Fecha, Proveedor, Codigo, Categoria, Producto, Und, Cantidad, Comentario FROM compras")
        
           
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)
        self.dataView.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.dataView.resizeColumnsToContents()
        self.dataView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        
    def insertar_datos(self):
        try:
            fecha = self.txtFecha.date().toString("yyyy-MM-dd") 
            proveedor = self.cmbProveedor.currentText()
            codigo = self.cmbCodigo.currentText()
            categoria = self.cmbCategoria.currentText()
            producto = self.cmbProducto.currentText()
            und = self.cmbMedida.currentText()
            comentario = self.txtComentario.text().upper()         
            cantidad = float(self.txtCantidad.text())
            
            if not fecha or not proveedor or not codigo or not categoria or not producto or not und or not comentario or not cantidad:
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            
            else:       
                insertar_compras(fecha, proveedor, codigo, categoria, producto, und, comentario, cantidad)
                self.visualiza_datos()
        
        
                #Limpia los TexBox
                self.txtFecha.setDate(QDate.currentDate())        
                self.cmbDocumento.setCurrentText("")
                self.txtComentario.setText("")
                self.cmbCodigo.setCurrentText("") 
                self.cmbCategoria.setCurrentText("")
                self.cmbMedida.setCurrentText("") 
                self.txtCantidad.setText("") 
                self.cmbProveedor.setCurrentText("") 
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
    GUI = VentanaCompras()
    GUI.show()
    sys.exit(app.exec_())