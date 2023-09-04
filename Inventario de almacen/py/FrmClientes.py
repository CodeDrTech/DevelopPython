import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from Consultas_db import insertar_nuevo_cliente

class Ventanaclientes(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Inventario de almacen/ui/FrmClientes.ui',self)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('CLIENTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Inventario de almacen/png/folder.png'))
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
 
        #Llamar a los diferentes formularios desde los botones
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnGuardar.clicked.connect(self.insertar_datos)
        self.btnLimpiar.clicked.connect(self.limpiar_textbox)
        self.btnBorrar.clicked.connect(self.borrar_fila)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def fn_Salir(self):
        self.close()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    def limpiar_textbox(self):
        #Limpia los TexBox
        self.txtCodigo.setText("CLI")        
        self.txtNombre.setText("")        
        self.txtCodigo.setFocus()
        

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("Clientes")
        model.select()        
        self.dataView.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.dataView.resizeColumnsToContents()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def insertar_datos(self):
        
        codigo = self.txtCodigo.text()        
        nombre = self.txtNombre.text().upper()
        
        insertar_nuevo_cliente(codigo, nombre)
        self.visualiza_datos()
        
        
        #Limpia los TexBox
        self.txtCodigo.setText("CLI")        
        self.txtNombre.setText("")        
        self.txtCodigo.setFocus()
        
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
            confirmacion = QMessageBox.question(self, "¿ELIMINAR?", "¿ESTA SEGURO QUE QUIERE ELIMINAR ESTE CLIENTE?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", eliminar la fila
            if confirmacion == QMessageBox.Yes:
                # Eliminar la fila seleccionada del modelo de datos
                model = self.dataView.model()
                model.removeRow(row)
                QMessageBox.warning(self, "ELIMINADO", "CLIENTE ELIMINADO.")
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA EL CLIENTE QUE VAS A ELIMINAR.")    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def showEvent(self, event):
        super().showEvent(event) 
          
        self.visualiza_datos()
        self.txtCodigo.setText("CLI")
        self.txtCodigo.setFocus()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = Ventanaclientes()
    GUI.show()
    sys.exit(app.exec_())