import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Consultas_db import insertar_nuevo_empleados

class VentanaEmpleado(QMainWindow):
    ventana_abierta = False    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmEmpleado.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Empleados .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Botones del formulario y sus funciones
        self.btnGuardar.clicked.connect(self.insertar_datos)
        self.btnNuevo.clicked.connect(self.visualiza_datos)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    # Funciones conectadas a los botones
        
    def insertar_datos(self):
        
        
        
        nombre = self.txtNombre.text().upper()
        apellidos = self.txtApellidos.text().upper()
        sexo = self.cmbSexo.currentText()
        fechanac = self.txtFechaNac.date().toString("yyyy-MM-dd")
        numdocumento = self.txtNumDocumento.text().upper()
        direccion = self.txtDireccion.toPlainText().upper()
        telefono = int(self.txtTelefono.text())
        email = self.txtEmail.text()
        acceso = self.cmbAcceso.currentText()
        usuario = self.txtUsuario.text()
        password = self.txtPassword.text()
                
        if  not nombre or not apellidos or not sexo or not fechanac or not numdocumento or not acceso or not usuario or not password:
    
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Faltan datos importantes")
            mensaje.setText("Por favor, complete todos los campos.")
            mensaje.exec_()
            
            
        else:
            insertar_nuevo_empleados(nombre, apellidos, sexo, fechanac, numdocumento, direccion, telefono, email, acceso, usuario, password)
        
            self.visualiza_datos()
        
        
            #Limpia los TexBox
            nombre = self.txtNombre.setText("")
            apellidos = self.txtApellidos.setText("")
            sexo = self.cmbSexo.setCurrentText("") 
            #fechanac = self.txtFechaNac.date().toString("yyyy-MM-dd")
            numdocumento = self.txtNumDocumento.setText("")
            direccion = self.txtDireccion.setPlainText("")
            telefono = self.txtTelefono.setText("")
            email = self.txtEmail.setText("")
            acceso = self.cmbAcceso.setCurrentText("") 
            usuario = self.txtUsuario.setText("")
            password = self.txtPassword.setText("")
            self.txtNombre.setFocus()
            
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT idempleado as 'CODIGO', nombre AS 'NOMBRE', apellidos AS 'APELLIDOS', sexo AS 'SEXO',\
                    fecha_nac AS 'FECHA DE NACIMIENTO', num_documento AS 'CEDULA', direccion AS 'DIRECCION', telefono AS 'TELEFONO',\
                    email AS 'CORREO', acceso AS 'ACCESO', usuario AS 'USUARIO', password AS 'CONTRASENA'  FROM empleado")
        
           
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def closeEvent(self, event):
        VentanaEmpleado.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        model = QSqlTableModel()   
        self.visualiza_datos()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaEmpleado()
    GUI.show()
    sys.exit(app.exec_())