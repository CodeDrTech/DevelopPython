import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Consultas_db import insertar_nuevo_articulo

class VentanaArticulo(QMainWindow):
    ventana_abierta = False     
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmArticulo.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Articulos .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        
        # Botones del formulario y sus funciones
        self.btnGuardar.clicked.connect(self.insertar_datos)
        #self.btnEditar.clicked.connect(self.editar_datos)
        self.btnSalir.clicked.connect(self.fn_Salir)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def insertar_datos(self):
        
        
        try:
            codigoventa = self.txtCodVenta.text().upper()
            nombre = self.txtNombre.text().upper()
            descripcion = self.txtDescripcion.toPlainText().upper()
            imagen = self.gFoto
            categoria = self.cmbCategoria.currentText()
            presentacion = self.cmbPresentacion.currentText()
            
                
            if  not codigoventa or not nombre or not categoria or not presentacion:
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            
            else:
                insertar_nuevo_articulo(codigoventa, nombre, descripcion, imagen, categoria, presentacion)
        
                #self.visualiza_datos()
        

                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar cliente")
                mensaje.setText("cliente registrado.")
                mensaje.exec_()
                
                
                #Limpia los TexBox
                self.txtCodVenta.setText("")
                self.txtNombre.setText("")
                self.txtDescripcion.setPlainText("")
                #self.gFoto
                self.cmbCategoria.setCurrentText("")
                self.cmbPresentacion.setCurrentText("")
                self.txtNombre.setFocus()
        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
            
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def cargar_categoria(self):    
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('categoria')
        model.select()
        column_name = []
        for i in range(model.rowCount()):
            column_name.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox.
        combo_model_categoria = QStandardItemModel()
        for item in column_name:
            combo_model_categoria.appendRow(QStandardItem(str(item)))
        self.cmbCategoria.setModel(combo_model_categoria)
        
        
    def cargar_presentacion(self):    
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('presentacion')
        model.select()
        column_name = []
        for i in range(model.rowCount()):
            column_name.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox.
        combo_model_presentacion = QStandardItemModel()
        for item in column_name:
            combo_model_presentacion.appendRow(QStandardItem(str(item)))
        self.cmbPresentacion.setModel(combo_model_presentacion)
        
    def closeEvent(self, event):
        VentanaArticulo.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)  
        
        self.cargar_presentacion()
        self.cargar_categoria()      
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaArticulo()
    GUI.show()
    sys.exit(app.exec_())