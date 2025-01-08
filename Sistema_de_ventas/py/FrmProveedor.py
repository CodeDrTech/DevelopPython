import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Consultas_db import insertar_nuevo_proveedor, obtener_ultimo_codigo,generar_nuevo_codigo 


class VentanaProveedor(QMainWindow):
    ventana_abierta = False    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema_de_ventas/ui/FrmProveedor.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Proveedores .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema_de_ventas/imagenes/login.jpg'))
        
        
        # Crear un efecto de sombra        
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tabWidget.setGraphicsEffect(tabWidget_shadow)
        
        groupBox_shadow = QGraphicsDropShadowEffect()
        groupBox_shadow.setBlurRadius(20)
        groupBox_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(groupBox_shadow)
        
        groupBox_shadow = QGraphicsDropShadowEffect()
        groupBox_shadow.setBlurRadius(20)
        groupBox_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(groupBox_shadow)

        groupBox_2shadow = QGraphicsDropShadowEffect()
        groupBox_2shadow.setBlurRadius(20)
        groupBox_2shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_2.setGraphicsEffect(groupBox_2shadow)

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Establecer el texto de referencia a la caja de texto buscar
        # Conectar el evento de clic para borrar el texto
        self.txtBuscar.setPlaceholderText('Buscar')        
        self.txtBuscar.mousePressEvent = self.borrarTexto
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Botones del formulario y sus funciones
        self.btnGuardar.clicked.connect(self.insertar_datos)
        self.btnEditar.clicked.connect(self.editar_datos)
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnBuscar.clicked.connect(self.buscar_proveedores)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Funciones conectadas a los botones
        
    def insertar_datos(self):
        
        
        try:
            razon_soc = self.txtRazonSocial.text().upper()
            sector_com = self.cmbSectorComercial.currentText().upper()
            tipo_doc = self.cmbTipoDocumento.currentText()
            numdocumento = self.txtNumDocumento.text().upper()
            direccion = self.txtDireccion.toPlainText().upper()
            telefono = int(self.txtTelefono.text())
            email = self.txtEmail.text()
            url = self.txtUrl.text()
                
            if  not razon_soc or not sector_com or not tipo_doc or not numdocumento or not direccion:
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            
            else:
                insertar_nuevo_proveedor(razon_soc, sector_com, tipo_doc, numdocumento, direccion, telefono, email, url)
        
                self.visualiza_datos()
        

                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar proveedor")
                mensaje.setText("Proveedor registrado.")
                mensaje.exec_()
                
                
                #Limpia los TexBox
                razon_soc = self.txtRazonSocial.setText("")
                sector_com = self.cmbSectorComercial.setCurrentText("")
                tipo_doc = self.cmbTipoDocumento.setCurrentText("")
                numdocumento = self.txtNumDocumento.setText("")
                direccion = self.txtDireccion.setPlainText("")
                telefono = self.txtTelefono.setText("")
                email = self.txtEmail.setText("")
                url = self.txtUrl.text()
                self.txtRazonSocial.setFocus()
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
        query.exec_(f"SELECT idproveedor as 'CODIGO', razon_social AS 'RAZON SOCIAL', sector_comercial AS 'SECTOR COMERCIAL', tipo_documento AS 'TIPO DOCUMENTO',\
                    num_documento AS 'NUMERO DOCUMENTO', direccion AS 'DIRECCION', telefono AS 'TELEFONO', email AS 'CORREO',\
                    url AS 'URL' FROM proveedor ORDER by idproveedor DESC")
        
        
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
        model.setTable("proveedor")
        model.select()        
        self.tbDatos.setModel(model)
        
        # Ocultar columnas para que no sean editadas
        self.tbDatos.setColumnHidden(0, True)
        
        # Renombra las cabeceras y organiza las columnas para mejorar la vista a la información.
        model.setHeaderData(1, Qt.Horizontal, "RAZON SOCIAL") # type: ignore
        model.setHeaderData(2, Qt.Horizontal, "SECTOR COMERCIAL") # type: ignore
        model.setHeaderData(3, Qt.Horizontal, "TIPO DOCUMENTO") # type: ignore
        model.setHeaderData(4, Qt.Horizontal, "NUMERO DOCUMENTO") # type: ignore
        model.setHeaderData(5, Qt.Horizontal, "DIRECCION") # type: ignore
        model.setHeaderData(6, Qt.Horizontal, "TELEFONO") # type: ignore
        model.setHeaderData(7, Qt.Horizontal, "CORREO") # type: ignore
        model.setHeaderData(8, Qt.Horizontal, "URL") # type: ignore

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    
        self.tbDatos.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
    def listado(self):
        self.tabWidget.setCurrentIndex(0)

    def actualizar_codigo_categoria(self):
        ultimo_codigo = obtener_ultimo_codigo("proveedor","idproveedor")
        nuevo_codigo = generar_nuevo_codigo(ultimo_codigo)
        self.txtCodigo.setText(nuevo_codigo)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def buscar_proveedores(self):
        # Variables con datos de los inputs para usar como criterios / filtros de busquedas.
        criterio_de_busqueda = self.comboBox.currentText()
        nombre_a_buscar = self.txtBuscar.text()

        if criterio_de_busqueda == "Documento":
            
            
            query = QSqlQuery()
            query.exec_(f"SELECT idproveedor as 'CODIGO', razon_social AS 'RAZON SOCIAL', sector_comercial AS 'SECTOR COMERCIAL', tipo_documento AS 'TIPO DOCUMENTO',\
                        num_documento AS 'NUMERO DOCUMENTO', direccion AS 'DIRECCION', telefono AS 'TELEFONO', email AS 'CORREO',\
                        url AS 'URL' FROM proveedor WHERE num_documento LIKE '%{nombre_a_buscar}%';")
                
                
            # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
            model = QSqlTableModel()    
            model.setQuery(query)        
            self.tbDatos.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()
            self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
        elif criterio_de_busqueda == "Razon social":
            query = QSqlQuery()
            query.exec_(f"SELECT idproveedor as 'CODIGO', razon_social AS 'RAZON SOCIAL', sector_comercial AS 'SECTOR COMERCIAL', tipo_documento AS 'TIPO DOCUMENTO',\
                        num_documento AS 'NUMERO DOCUMENTO', direccion AS 'DIRECCION', telefono AS 'TELEFONO', email AS 'CORREO',\
                        url AS 'URL' FROM proveedor WHERE razon_social LIKE '%{nombre_a_buscar}%';")
                
                
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
    def closeEvent(self, event):
        VentanaProveedor.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Elimina el textp de referencia que tiene la casilla buscar
    def borrarTexto(self, event):
        # Borrar el texto cuando se hace clic
        self.txtBuscar.clear()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def showEvent(self, event):
        super().showEvent(event)
        self.actualizar_codigo_categoria()
        model = QSqlTableModel()   
        self.visualiza_datos()
        
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
    GUI = VentanaProveedor()
    GUI.show()
    sys.exit(app.exec_())