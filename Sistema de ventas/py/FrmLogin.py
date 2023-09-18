import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QAbstractItemView
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtCore import QDateTime
from FrmPrincipal import VentanaPrincipal

class VentanaLogin(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmLogin.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Acceso al sistema de ventas .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnIngresar.clicked.connect(self.validar_usuario)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

    def visualizar_datos(self):
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("empleado")
        model.select()        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def obtener_codigo_empleado(self, usuario):
        model = QSqlTableModel()
        model.setTable('empleado')
        model.setFilter(f"usuario='{usuario}'")
        model.select()
        
            
        if model.rowCount() > 0:
            # Obtén la fila del primer registro que cumple con la condición
            fila = model.index(0, 9).row()
            return fila
        else:
            return None
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------     
    def abrirFrmPrincipal(self):
        self.llamar_venana_principal = VentanaPrincipal()
        self.llamar_venana_principal.show()
        self.fn_Salir()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------      
        
    def obtener_datos_de_fila(self, fila_id):
        # Obtener el modelo de datos del QTableView
        modelo = self.tbDatos.model()

        #if modelo is not None and 0 <= fila_seleccionada < modelo.rowCount():
        # Obtener los datos de la fila seleccionada
        columna_9 = modelo.index(fila_id, 9).data()
        columna_10 = modelo.index(fila_id, 10).data()
        columna_11 = modelo.index(fila_id, 11).data()
            

        self.valor_columna_9 = columna_9
        self.valor_columna_10 = columna_10
        self.valor_columna_11 = columna_11    

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def validar_usuario(self):
        usuario = self.txtUsuario.text()
        fila = self.obtener_codigo_empleado(usuario)
        usuario_comp = self.obtener_datos_de_fila(fila)
        print(fila)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def fn_Salir(self):
        self.close()
        
    def closeEvent(self, event):
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        self.tbDatos.hide()
        self.visualizar_datos()        
        fecha_hora = QDateTime.currentDateTime()
        self.txtFecha.setDateTime(fecha_hora)
        self.txtUsuario.setFocus()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------                     
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaLogin()
    GUI.show()
    sys.exit(app.exec_())