import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Consultas_db import insertar_nuevo_cliente

class VentanaCliente(QMainWindow):
    ventana_abierta = False    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmCliente.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Clientes .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        # Botones del formulario y sus funciones
        self.btnGuardar.clicked.connect(self.insertar_datos)
        self.btnEditar.clicked.connect(self.editar_datos)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    # Funciones conectadas a los botones
        
    def insertar_datos(self):
        
        
        
        nombre = self.txtNombre.text().upper()
        apellidos = self.txtApellidos.text().upper()
        sexo = self.cmbSexo.currentText()
        fechanac = self.txtFechaNac.date().toString("yyyy-MM-dd")
        tipo_doc = self.cmbTipoDocumento.currentText().upper()
        numdocumento = self.txtNumDocumento.text().upper()
        direccion = self.txtDireccion.toPlainText().upper()
        telefono = int(self.txtTelefono.text())
        email = self.txtEmail.text()
                
        if  not nombre or not tipo_doc or not numdocumento :
    
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Faltan datos importantes")
            mensaje.setText("Por favor, complete todos los campos.")
            mensaje.exec_()
            
            
        else:
            insertar_nuevo_cliente(nombre, apellidos, sexo, fechanac, tipo_doc, numdocumento, direccion, telefono, email)
        
            self.visualiza_datos()
        
        
            #Limpia los TexBox
            nombre = self.txtNombre.setText("")
            apellidos = self.txtApellidos.setText("")
            sexo = self.cmbSexo.setCurrentText("") 
            tipo_doc = self.cmbTipoDocumento.setCurrentText("")
            numdocumento = self.txtNumDocumento.setText("")
            direccion = self.txtDireccion.setPlainText("")
            telefono = self.txtTelefono.setText("")
            email = self.txtEmail.setText("")
            self.txtNombre.setFocus()
            
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT idcliente as 'CODIGO', nombre AS 'NOMBRE', apellidos AS 'APELLIDOS', sexo AS 'SEXO',\
                    fecha_nacimiento AS 'FECHA DE NACIMIENTO', tipo_documento AS 'TIPO DOCUMENTO', num_documento AS 'NUM DOCUMENTO',\
                    direccion AS 'DIRECCION', telefono AS 'TELEFONO',\
                    email AS 'CORREO' FROM cliente ORDER BY idcliente DESC")
        
           
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
        model.setTable("cliente")
        model.select()        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    
        self.tbDatos.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
    def listado(self):
        self.tabWidget.setCurrentIndex(0)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------       
    def closeEvent(self, event):
        VentanaCliente.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCliente()
    GUI.show()
    sys.exit(app.exec_())