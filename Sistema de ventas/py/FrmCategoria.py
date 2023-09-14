import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5 import QtGui
from Consultas_db import insertar_nueva_categoria

class VentanaCategoria(QMainWindow):
    ventana_abierta = False     
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmCategoria.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Categorias .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        self.btnGuardar.clicked.connect(self.insertar_datos)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        
        query = QSqlQuery()
        query.exec_(f"SELECT idcategoria as 'CODIGO', nombre AS 'NOMBRE', descripcion AS 'DESCRIPCION' FROM categoria")
        
           
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

        
    def insertar_datos(self):
        
        
        #codigo = self.txtCodigo.text().upper()
        nombre = self.txtNombre.text().upper()
        descripcion = self.txtDescripcion.toPlainText().upper()
        
        
        if  not nombre:
    
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Faltan datos importantes")
            mensaje.setText("Por favor, complete todos los campos.")
            mensaje.exec_()
            
            
        else:
            insertar_nueva_categoria(nombre, descripcion)
        
            self.visualiza_datos()
        
        
            #Limpia los TexBox
            self.txtNombre.setText("")
            self.txtDescripcion.setPlainText("")
            self.txtNombre.setFocus()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        
    def closeEvent(self, event):
        VentanaCategoria.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
                
    def showEvent(self, event):
        super().showEvent(event)
        
        model = QSqlTableModel()    
        self.visualiza_datos()
        
        
            
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCategoria()
    GUI.show()
    sys.exit(app.exec_())