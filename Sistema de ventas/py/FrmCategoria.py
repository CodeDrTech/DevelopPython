import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView
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
        self.btnEditar.clicked.connect(self.editar_datos) 
        self.btnSalir.clicked.connect(self.fn_Salir)
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
        self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        
    def editar_datos(self):
        self.listado()
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("categoria")
        model.select()        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    
        self.tbDatos.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
    def listado(self):
        self.tabWidget.setCurrentIndex(0)
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
        
    def fn_Salir(self):
        
        # Preguntar si el usuario está seguro de cerrar la ventana
        confirmacion = QMessageBox.question(self, "", "¿ESTAS SEGURO QUE QUIERE CERRAR LA VENTANA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
        # Si el usuario hace clic en el botón "Sí", se cierra la ventana
        if confirmacion == QMessageBox.Yes:
            self.close()   
        
            
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCategoria()
    GUI.show()
    sys.exit(app.exec_())