import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from Consultas_db import insertar_nuevo_proveedor, generar_nuevo_codigo, obtener_ultimo_codigo

class Ventanaproveedores(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Inventario de almacen/ui/FrmProveedores.ui',self)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('PROVEEDORES')
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
        
        ultimo_codigo = obtener_ultimo_codigo("Proveedores")
        nuevo_codigo = generar_nuevo_codigo("PROV",ultimo_codigo)
        
        #Limpia los TexBox
        self.txtCodigo.setText(nuevo_codigo)        
        self.txtNombre.setText("")        
        self.txtNombre.setFocus()
        

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("Proveedores")
        model.select()        
        self.dataView.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.dataView.resizeColumnsToContents()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def insertar_datos(self):
        
        
        codigo = self.txtCodigo.text()        
        nombre = self.txtNombre.text().upper()
        
        if not codigo or not nombre:
            
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Faltan datos")
            mensaje.setText("Por favor, complete todos los campos.")
            mensaje.exec_()
        
        else:
            
        
            insertar_nuevo_proveedor(nombre)
        
            ultimo_codigo = obtener_ultimo_codigo("Proveedores")
            nuevo_codigo = generar_nuevo_codigo("PROV",ultimo_codigo)
        
            self.visualiza_datos()
        
        
            #Limpia los TexBox
            self.txtCodigo.setText(nuevo_codigo)        
            self.txtNombre.setText("")        
            self.txtNombre.setFocus()
        
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
            confirmacion = QMessageBox.question(self, "¿ELIMINAR?", "¿ESTA SEGURO QUE QUIERE ELIMINAR ESTE PROVEEDOR?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", eliminar la fila
            if confirmacion == QMessageBox.Yes:
                # Eliminar la fila seleccionada del modelo de datos
                model = self.dataView.model()
                model.removeRow(row)
                QMessageBox.warning(self, "ELIMINADO", "PROVEEDOR ELIMINADO.")
                
                ultimo_codigo = obtener_ultimo_codigo("Proveedores")
                nuevo_codigo = generar_nuevo_codigo("PROV",ultimo_codigo)          
                self.visualiza_datos()
                self.txtCodigo.setText(nuevo_codigo)
        
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA EL PROVEEDOR QUE VAS A ELIMINAR.")    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def showEvent(self, event):
        super().showEvent(event) 
        ultimo_codigo = obtener_ultimo_codigo("Proveedores")
        nuevo_codigo = generar_nuevo_codigo("PROV",ultimo_codigo)
          
        self.visualiza_datos()
        self.txtCodigo.setText(nuevo_codigo)
        self.txtNombre.setFocus()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = Ventanaproveedores()
    GUI.show()
    sys.exit(app.exec_())