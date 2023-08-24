import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery

class VentanaProductos(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Inventario de almacen/ui/FrmProductos.ui',self)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('PRODUCTOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Inventario de almacen/png/folder.png'))
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
        #Llamar a los diferentes formularios desde los botones
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnGuardar.clicked.connect(self.insertar_datos)
        #self.btnLimpiar.clicked.connect(self.abrirFrmFaltanes)
        #self.btnBorrar.clicked.connect(self.abrirFrmDatosReportes)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def insertar_datos(self):
        codigo = self.txtCodigo.text()
        categoria = self.txtCategoria.text()
        nombre = self.txtNombre.text()
        medida = self.txtMedida.text()
    
        if codigo and categoria and nombre and medida:
            db = QSqlDatabase.addDatabase("QSQLITE")
            db.setDatabaseName("Almacen.db")  # Reemplaza con el nombre de tu base de datos SQLite
            if not db.open():
                QMessageBox.critical(self, "Error", "No se pudo abrir la base de datos.")
                return
    
            query = QSqlQuery()
            query.prepare("INSERT INTO Productos (Codigo, Categoria, Nombre, Medida) VALUES (:codigo, :categoria, :nombre, :medida)")
            query.bindValue(":Codigo", codigo)  # Usa ":codigo" en lugar de ":Codigo"
            query.bindValue(":Categoria", categoria)  # Usa ":categoria" en lugar de ":Categoria"
            query.bindValue(":Nombre", nombre)  # Usa ":nombre" en lugar de ":Nombre"
            query.bindValue(":Medida", medida)  # Usa ":medida" en lugar de ":Medida"
    
            if query.exec():
                QMessageBox.information(self, "Éxito", "Datos insertados correctamente.")
            else:
                QMessageBox.critical(self, "Error", "Error al insertar datos: " + query.lastError().text())
    
            db.close()
        else:
            QMessageBox.warning(self, "Advertencia", "Por favor, complete todos los campos.")


        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def fn_Salir(self):
        self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
        
        
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaProductos()
    GUI.show()
    sys.exit(app.exec_())