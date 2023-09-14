import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5 import QtGui
from Consultas_db import insertar_nueva_presentacion

class VentanaPresentacion(QMainWindow):
    ventana_abierta = False    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmPresentacion.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Presentaciones .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        self.btnGuardar.clicked.connect(self.insertar_datos)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("presentacion")
        model.select()        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

        
    def insertar_datos(self):
        
        
        codigo = self.txtCodigo.text().upper()
        nombre = self.txtNombre.text().upper()
        descripcion = self.txtDescripcion.toPlainText().upper()
        
        
        if  not nombre:
    
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Faltan datos importantes")
            mensaje.setText("Por favor, complete todos los campos.")
            mensaje.exec_()
            
            
        else:
            insertar_nueva_presentacion(codigo, nombre, descripcion)
        
            self.visualiza_datos()
        
        
            #Limpia los TexBox
            self.txtCodigo.setText("")
            self.txtNombre.setText("")
            self.txtDescripcion.setPlainText("")
            self.txtCodigo.setFocus()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def closeEvent(self, event):
        VentanaPresentacion.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
            
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPresentacion()
    GUI.show()
    sys.exit(app.exec_())