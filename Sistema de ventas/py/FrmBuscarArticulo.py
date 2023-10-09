import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect, QMdiSubWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Consultas_db import insertar_nuevo_cliente, obtener_ultimo_codigo, generar_nuevo_codigo

class VentanaBuscarArticulo(QMainWindow):
    ventana_abierta = False    
    def __init__(self, ventana_cotizaciones):
        super().__init__()
        self.ventana_cotizaciones = ventana_cotizaciones        
        uic.loadUi('Sistema de ventas/ui/FrmBuscarArticulo.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Buscar Articulos .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        # Botones del formulario y sus funciones
        #self.btnGuardar.clicked.connect(self.insertar_datos)
        #self.btnEditar.clicked.connect(self.editar_datos)
        #self.btnSalir.clicked.connect(self.fn_Salir)
        
        self.tbDatos.doubleClicked.connect(self.insertar_articulo_en_cotizacion)
        
        # Crear un efecto de sombra y aplicarlo a los QTableView
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(20)
        shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))
        self.tbDatos.setGraphicsEffect(shadow)
        
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(tabWidget_shadow)
        
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def insertar_articulo_en_cotizacion(self, index):
        from FrmCotizaciones import VentanaCotizaciones
        
        if not VentanaCotizaciones.ventana_abierta:
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana cerrada")
            mensaje.setText("La ventana Cotizaciones está cerrada.")
            mensaje.exec_()
        else:
            # Obtener la fila seleccionada
            row = index.row()

            # Obtener los datos de la fila seleccionada
            id_articulo = self.tbDatos.model().index(row, 0).data()
            nombre_articulo = self.tbDatos.model().index(row, 1).data()
            

            # Llamar a la función traer_cliente en la instancia de VentanaCotizaciones
            self.ventana_cotizaciones.traer_articulo(id_articulo, nombre_articulo)
            self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    # Funciones conectadas a los botones
            
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT idarticulo as 'ID', nombre as 'NOMBRE', descripcion as 'DESCRIPCION' from articulo")
        
        
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
    def closeEvent(self, event):
        VentanaBuscarArticulo.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
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
        #self.actualizar_codigo_categoria()
        self.visualiza_datos()   
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaBuscarArticulo()
    GUI.show()
    sys.exit(app.exec_())