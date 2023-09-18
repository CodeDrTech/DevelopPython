import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QAbstractItemView, QMessageBox
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
        
        
        self.setTabOrder(self.txtUsuario, self.txtPassword)
        
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
        #model.setFilter(f"usuario='{usuario.strip()}'")

        model.select()
        
            
        # Encuentra el índice de la columna "usuario"
        usuario_column_index = model.fieldIndex("usuario")
    
        # Itera a través de las filas para encontrar el usuario
        for row in range(model.rowCount()):
            index = model.index(row, usuario_column_index)
            if model.data(index) == usuario:
                # Si se encuentra el usuario, devuelve el número de fila
                return row
    
        # Si no se encuentra el usuario, devuelve None
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

        if modelo is not None and 0 <= fila_id < modelo.rowCount():
            
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
        password = self.txtPassword.text()
        usuario = self.txtUsuario.text()
        
        try:
            fila = self.obtener_codigo_empleado(usuario)
            self.obtener_datos_de_fila(fila)
            bd_acceso = self.valor_columna_9
            bd_usuario = self.valor_columna_10
            bd_password = self.valor_columna_11
        
        
            if not usuario or not password:
            
            
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            else:    
                if usuario == bd_usuario and password == bd_password:
                    print("Usuario correcto")
                else:
                    print("Usuario incorrecto")
        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
        
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