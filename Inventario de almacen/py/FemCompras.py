import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel


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



#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------          
    def fn_Salir(self):
        self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def showEvent(self, event):
        super().showEvent(event) 
          
        #self.visualiza_datos()
        #self.txtCodigo.setText("PROD")
        #self.txtCodigo.setFocus()
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCompras()
    GUI.show()
    sys.exit(app.exec_())