import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect, QMdiSubWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Consultas_db import insertar_nuevo_cliente, obtener_ultimo_codigo, generar_nuevo_codigo

class VentanaBuscarArticuloVentas(QMainWindow):
    ventana_abierta = False    
    def __init__(self, ventana_Ventas):
        super().__init__()
        self.ventana_Ventas = ventana_Ventas        
        uic.loadUi('Sistema de ventas/ui/FrmBuscarArticuloVentas.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Buscar Articulos .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('SSistema de ventas/imagenes/login.jpg'))
        
        # Botones del formulario y sus funciones
        self.btnBuscar.clicked.connect(self.buscar_articulo)
        
        self.tbDatos.doubleClicked.connect(self.insertar_articulo_en_ventas)
        
        # Crear un efecto de sombra y aplicarlo a los QTableView
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))
        self.tbDatos.setGraphicsEffect(shadow)
        
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(tabWidget_shadow)
        
        # Establecer el texto de referencia a la caja de texto buscar
        # Conectar el evento de clic para borrar el texto
        self.txtBuscar.setPlaceholderText('Buscar')        
        self.txtBuscar.mousePressEvent = self.borrarTexto
        
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def insertar_articulo_en_ventas(self, index):
        from FrmVentas import VentanaVentas
        
        if not VentanaVentas.ventana_abierta:
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana cerrada")
            mensaje.setText("La ventana Ventas está cerrada.")
            mensaje.exec_()
        else:
            # Obtener la fila seleccionada
            row = index.row()

            # Obtener los datos de la fila seleccionada
            id_articulo = self.tbDatos.model().index(row, 0).data()
            nombre_articulo = self.tbDatos.model().index(row, 1).data()
            

            # Llamar a la función traer_cliente en la instancia de VentanaCotizaciones
            self.ventana_Ventas.traer_articulo(id_articulo, nombre_articulo)
            self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    # Funciones conectadas a los botones
            
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT a.idarticulo as 'ID', a.nombre as 'NOMBRE', s.disponible as 'CANTIDAD DISPONIBLE', a.descripcion as 'DESCRIPCION'\
                            FROM articulo a\
                            LEFT JOIN stock s ON a.idarticulo = s.idarticulo\
                            WHERE s.disponible IS NOT NULL\
                            UNION\
                            SELECT a.idarticulo as 'ID', a.nombre as 'NOMBRE', '0' as 'CANTIDAD DISPONIBLE', a.descripcion as 'DESCRIPCION'\
                            FROM articulo a\
                            LEFT JOIN stock s ON a.idarticulo = s.idarticulo\
                            WHERE s.disponible IS NULL;")
        
        
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

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    
        self.tbDatos.setEditTriggers(QAbstractItemView.AllEditTriggers)
        
    def listado(self):
        self.tabWidget.setCurrentIndex(0)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def buscar_articulo(self):
        # Variables con datos de los inputs para usar como criterios/filtros de busquedas
        criterio_de_busqueda = self.comboBox.currentText()
        buscar_nombre = self.txtBuscar.text()

        if criterio_de_busqueda == "Nombre":
                
            query = QSqlQuery()
            query.exec_(f"SELECT idarticulo as 'ID', nombre as 'NOMBRE', descripcion as 'DESCRIPCION' from articulo WHERE nombre LIKE '%{buscar_nombre}%';")
                
                
            # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
            model = QSqlTableModel()    
            model.setQuery(query)        
            self.tbDatos.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()
            self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        elif criterio_de_busqueda == "Codigo":
                
            query = QSqlQuery()
            query.exec_(f"SELECT idarticulo as 'ID', nombre as 'NOMBRE', descripcion as 'DESCRIPCION' from articulo WHERE idarticulo LIKE '%{buscar_nombre}%';")
                
                
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
        VentanaBuscarArticuloVentas.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
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
        #self.actualizar_codigo_categoria()
        self.visualiza_datos()   
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaBuscarArticuloVentas()
    GUI.show()
    sys.exit(app.exec_())