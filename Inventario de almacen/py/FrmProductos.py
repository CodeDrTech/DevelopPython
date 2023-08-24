import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery
from Consultas_db import insertar_nuevo_producto

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
        insertar_nuevo_producto(codigo, categoria, nombre, medida)
        



        
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