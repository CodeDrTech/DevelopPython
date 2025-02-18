import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from Consultas_db import insertar_nueva_presentacion, obtener_ultimo_codigo, generar_nuevo_codigo



class VentanaPresentacion(QMainWindow):
    ventana_abierta = False    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema_de_ventas/ui/FrmPresentacion.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Presentaciones .:.')
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
        self.btnGuardar.clicked.connect(self.insertar_datos)
        self.btnEditar.clicked.connect(self.editar_datos)
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnBuscar.clicked.connect(self.buscar_articulo)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        
        query = QSqlQuery()
        query.exec_(f"SELECT idpresentacion as 'CODIGO', nombre AS 'NOMBRE', descripcion AS 'DESCRIPCION' FROM presentacion")
        
           
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
        model.setTable("presentacion")
        model.select()        
        self.tbDatos.setModel(model)

        
        # Ocultar columnas para que no sean editadas
        self.tbDatos.setColumnHidden(0, True)
        
        # Renombra las cabeceras y organiza las columnas para mejorar la vista a la información.
        model.setHeaderData(1, Qt.Horizontal, "NOMBRE") # type: ignore
        model.setHeaderData(2, Qt.Horizontal, "DESCRIPCION") # type: ignore
        
        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    
        self.tbDatos.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
        
    def listado(self):
        self.tabWidget.setCurrentIndex(0)
        
    def actualizar_codigo_categoria(self):
        ultimo_codigo = obtener_ultimo_codigo("presentacion","idpresentacion")
        nuevo_codigo = generar_nuevo_codigo(ultimo_codigo)
        self.txtCodigo.setText(nuevo_codigo)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

    def buscar_articulo(self):
        # Variables con datos de los inputs para usar como criterios/filtros de busquedas.
        buscar_nombre = self.txtBuscar.text()

        if not buscar_nombre:
            self.visualiza_datos()
        else:    
            query = QSqlQuery()
            query.exec_(f"SELECT idpresentacion as 'CODIGO', nombre AS 'NOMBRE', descripcion AS 'DESCRIPCION' FROM presentacion\
                                WHERE descripcion LIKE '%{buscar_nombre}%';")
                
                
            # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
            model = QSqlTableModel()    
            model.setQuery(query)        
            self.tbDatos.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()
            self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

        
    def insertar_datos(self):
        
        try:
            #codigo = self.txtCodigo.text().upper()
            nombre = self.txtNombre.text().upper()
            descripcion = self.txtDescripcion.toPlainText().upper()
        
        
            if  not nombre:
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            
            else:
                insertar_nueva_presentacion(nombre, descripcion)
        
                self.visualiza_datos()
        

                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar presentacion")
                mensaje.setText("presentacion registrada.")
                mensaje.exec_()
                
                
                #Limpia los TexBox
                self.txtNombre.setText("")
                self.txtDescripcion.setPlainText("")
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
    def closeEvent(self, event):
        VentanaPresentacion.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
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
        
        
        #Limpia los TexBox
        self.txtNombre.setText("")
        self.txtDescripcion.setPlainText("")
        self.txtNombre.setFocus()
        
    def fn_Salir(self):
        # Preguntar si el usuario está seguro de cerrar la ventana
        confirmacion = QMessageBox.question(self, "", "¿ESTAS SEGURO QUE QUIERE CERRAR LA VENTANA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
        # Si el usuario hace clic en el botón "Sí", se cierra la ventana
        if confirmacion == QMessageBox.Yes:
            self.close()
            
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaPresentacion()
    GUI.show()
    sys.exit(app.exec_())