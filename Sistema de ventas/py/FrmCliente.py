import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Consultas_db import insertar_nuevo_cliente, obtener_ultimo_codigo, generar_nuevo_codigo

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
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnBuscar.clicked.connect(self.buscar_clientes)
        
        
        # Crear un efecto de sombra y aplicarlo a los QTableView
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))
        self.tbDatos.setGraphicsEffect(shadow)
        
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tabWidget.setGraphicsEffect(tabWidget_shadow)
        
        groupBox_shadow = QGraphicsDropShadowEffect()
        groupBox_shadow.setBlurRadius(20)
        groupBox_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(groupBox_shadow)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def buscar_clientes(self):
        # Variables con datos de los inputs para usar como criterios / filtros de busquedas.
        criterio_de_busqueda = self.comboBox.currentText()
        nombre_a_buscar = self.txtBuscar.text()

        if criterio_de_busqueda == "Nombre":
            
            
            query = QSqlQuery()
            query.exec_(f"SELECT idcliente as 'CODIGO', nombre AS 'NOMBRE', apellidos AS 'APELLIDOS', sexo AS 'SEXO',\
                    UPPER(FORMAT(fecha_nacimiento, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE NACIMIENTO', tipo_documento AS 'TIPO DOCUMENTO', num_documento AS 'NUM DOCUMENTO',\
                    direccion AS 'DIRECCION', telefono AS 'TELEFONO',\
                    email AS 'CORREO' FROM cliente WHERE nombre LIKE '%{nombre_a_buscar}%';")
                
                
            # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
            model = QSqlTableModel()    
            model.setQuery(query)        
            self.tbDatos.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()
            self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
        elif criterio_de_busqueda == "Documento":
            query = QSqlQuery()
            query.exec_(f"SELECT idcliente as 'CODIGO', nombre AS 'NOMBRE', apellidos AS 'APELLIDOS', sexo AS 'SEXO',\
                    UPPER(FORMAT(fecha_nacimiento, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE NACIMIENTO', tipo_documento AS 'TIPO DOCUMENTO', num_documento AS 'NUM DOCUMENTO',\
                    direccion AS 'DIRECCION', telefono AS 'TELEFONO',\
                    email AS 'CORREO' FROM cliente WHERE num_documento LIKE '%{nombre_a_buscar}%';")
                
                
            # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
            model = QSqlTableModel()    
            model.setQuery(query)        
            self.tbDatos.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()
            self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:
            self.visualiza_datos()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def insertar_datos(self):
        
        
        try:
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
        

                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar cliente")
                mensaje.setText("cliente registrado.")
                mensaje.exec_()
                
                
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
        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
            
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT idcliente as 'CODIGO', nombre AS 'NOMBRE', apellidos AS 'APELLIDOS', sexo AS 'SEXO',\
                    UPPER(FORMAT(fecha_nacimiento, 'dd MMMM yyyy', 'es-ES')) AS 'FECHA DE NACIMIENTO', tipo_documento AS 'TIPO DOCUMENTO', num_documento AS 'NUM DOCUMENTO',\
                    direccion AS 'DIRECCION', telefono AS 'TELEFONO',\
                    email AS 'CORREO' FROM cliente ORDER BY idcliente DESC")
        
        
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()
        self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def actualizar_codigo_categoria(self):
        ultimo_codigo = obtener_ultimo_codigo("cliente","idcliente")
        nuevo_codigo = generar_nuevo_codigo(ultimo_codigo)
        self.txtCodigo.setText(nuevo_codigo)
            
    def editar_datos(self):
        self.listado()
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("cliente")
        model.select()        
        self.tbDatos.setModel(model)

        
        # Ocultar columnas para que no sean editadas
        self.tbDatos.setColumnHidden(0, True)
        
        # Renombra las cabeceras y organiza las columnas para mejorar la vista a la información.
        model.setHeaderData(1, Qt.Horizontal, "NOMBRE") # type: ignore
        model.setHeaderData(2, Qt.Horizontal, "APELLIDOS") # type: ignore
        model.setHeaderData(3, Qt.Horizontal, "SEXO") # type: ignore
        model.setHeaderData(4, Qt.Horizontal, "FECHA DE NACIMIENTO") # type: ignore
        model.setHeaderData(5, Qt.Horizontal, "TIPO DOCUMENTO") # type: ignore
        model.setHeaderData(6, Qt.Horizontal, "NUM DOCUMENTO") # type: ignore
        model.setHeaderData(7, Qt.Horizontal, "DIRECCION") # type: ignore
        model.setHeaderData(8, Qt.Horizontal, "TELEFONO") # type: ignore
        model.setHeaderData(9, Qt.Horizontal, "CORREO") # type: ignore
        
        
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
        
    def fn_Salir(self):
        # Preguntar si el usuario está seguro de cerrar la ventana
        confirmacion = QMessageBox.question(self, "", "¿ESTAS SEGURO QUE QUIERE CERRAR LA VENTANA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
        # Si el usuario hace clic en el botón "Sí", se cierra la ventana
        if confirmacion == QMessageBox.Yes:
            self.close()
    def showEvent(self, event):
        super().showEvent(event)
        self.actualizar_codigo_categoria()
        self.visualiza_datos()   
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaCliente()
    GUI.show()
    sys.exit(app.exec_())