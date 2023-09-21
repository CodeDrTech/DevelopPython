import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView
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
        self.btnGuardar.clicked.connect(self.evaluar_usuario)
        self.btnEditar.clicked.connect(self.editar_datos)
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnEliminar.clicked.connect(self.borrar_fila)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    # Funciones conectadas a los botones
    
    def insertar_datos(self, nombre, apellidos, sexo, fechanac, numdocumento, direccion, telefono, email, acceso, usuario, password):
        try:
                                            
            insertar_nuevo_empleados(nombre, apellidos, sexo, fechanac, numdocumento, direccion, telefono, email, acceso, usuario, password)
        
            self.visualiza_datos()
        

            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Agregar empleado")
            mensaje.setText("Empleado registrado.")
            mensaje.exec_()
                
            #Limpia los TexBox
            self.txtNombre.setText("")
            self.txtApellidos.setText("")
            self.cmbSexo.setCurrentText("")
            self.txtNumDocumento.setText("")
            self.txtDireccion.setPlainText("")
            self.txtTelefono.setText("")
            self.txtEmail.setText("")
            self.cmbAcceso.setCurrentText("") 
            self.txtUsuario.setText("")
            self.txtPassword.setText("")
            self.txtNombre.setFocus()
        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def borrar_fila(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.tbDatos.selectedIndexes()
        
        if indexes:
            
            # Obtener la fila al seleccionar una celda de la tabla
            index = indexes[0]
            row = index.row()
            
            # Preguntar si el usuario está seguro de eliminar la fila
            confirmacion = QMessageBox.question(self, "¿ELIMINAR?", "¿ESTA SEGURO QUE QUIERE ELIMINAR ESTA FILA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", eliminar la fila
            if confirmacion == QMessageBox.Yes:
                # Eliminar la fila seleccionada del modelo de datos
                model = self.tbDatos.model()
                model.removeRow(row)
                QMessageBox.warning(self, "ELIMINADA", "FILA ELIMINADA.")
                self.visualiza_datos()
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA LA FILA QUE VAS A ELIMINAR.")
            
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------             
    def obtener_fila_empleado(self, usuario_del_formulario):
        model = QSqlTableModel()
        model.setTable('empleado')
        model.select()
        
            
        # Encuentra el índice de la columna "usuario"
        usuario_column_index = model.fieldIndex("usuario")
    
        # Itera a través de las filas para encontrar el usuario
        for row in range(model.rowCount()):
            index = model.index(row, usuario_column_index)
            if model.data(index) == usuario_del_formulario:
                # Si se encuentra el usuario, devuelve el número de fila
                return row
    
        # Si no se encuentra el usuario, devuelve None
        return -1
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
    def obtener_datos_de_fila(self, fila_del_usuario):
        
        # Obtener el modelo de datos del QTableView
        modelo = self.tbDatos.model()
        if modelo is not None and 0 <= fila_del_usuario < modelo.rowCount():
            
            # Obtener los datos de la fila seleccionada
            columna_9 = modelo.index(fila_del_usuario, 9).data()
            columna_10 = modelo.index(fila_del_usuario, 10).data()
            columna_11 = modelo.index(fila_del_usuario, 11).data()
            

            self.valor_columna_9 = columna_9
            self.valor_columna_10 = columna_10
            self.valor_columna_11 = columna_11
            

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------     
    def evaluar_usuario(self):
        
        nombre = self.txtNombre.text().upper()
        apellidos = self.txtApellidos.text().upper()
        sexo = self.cmbSexo.currentText()
        fechanac = self.txtFechaNac.date().toString("yyyy-MM-dd")
        numdocumento = self.txtNumDocumento.text()
        direccion = self.txtDireccion.toPlainText().upper()
        telefono = self.txtTelefono.text()
        email = self.txtEmail.text()
        acceso = self.cmbAcceso.currentText()            
        password = self.txtPassword.text()
        usuario = self.txtUsuario.text()
        
        try:            
            fila = self.obtener_fila_empleado(usuario)
            self.obtener_datos_de_fila(fila)
            bd_usuario = self.valor_columna_10
            
            if fila == -1:
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Error inesperado")
                mensaje.setText("Por favor, revisar bien todos los campos.")
                mensaje.exec_()
                
            else:
                if  not nombre or not apellidos or not sexo or not fechanac or not numdocumento or not acceso or not usuario or not password:
                
                    mensaje = QMessageBox()
                    mensaje.setIcon(QMessageBox.Critical)
                    mensaje.setWindowTitle("Faltan datos importantes")
                    mensaje.setText("Por favor, complete todos los campos.")
                    mensaje.exec_()
                elif bd_usuario == usuario:                    
                        mensaje = QMessageBox()
                        mensaje.setIcon(QMessageBox.Critical)
                        mensaje.setWindowTitle("Usuario ya existe")
                        mensaje.setText(f"El usuario {usuario} pertenece a otra persona.")
                        mensaje.exec_()
                        self.txtUsuario.setText("")
                        self.txtUsuario.setFocus()
                
                else:
                    self.insertar_datos(nombre, apellidos, sexo, fechanac, numdocumento, direccion, telefono, email, acceso, usuario, password)
        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------             
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
        self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def editar_datos(self):
        self.listado()
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("empleado")
        model.select()        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    
        self.tbDatos.setEditTriggers(QAbstractItemView.AllEditTriggers)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def listado(self):
        self.tabWidget.setCurrentIndex(0)
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
    def fn_Salir(self):
        # Preguntar si el usuario está seguro de cerrar la ventana
        confirmacion = QMessageBox.question(self, "", "¿ESTAS SEGURO QUE QUIERE CERRAR LA VENTANA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
        # Si el usuario hace clic en el botón "Sí", se cierra la ventana
        if confirmacion == QMessageBox.Yes:
            self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaEmpleado()
    GUI.show()
    sys.exit(app.exec_())