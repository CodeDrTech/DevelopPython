import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect, QMdiSubWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Consultas_db import insertar_nuevo_cliente, obtener_ultimo_codigo, generar_nuevo_codigo


class VentanaBuscarClienteVentas(QMainWindow):
    ventana_abierta = False    
    def __init__(self, ventana_ventas):
        super().__init__()
        self.ventana_ventas = ventana_ventas        
        uic.loadUi('Sistema de ventas/ui/FrmBuscarClienteVentas.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Buscar Clientes .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/imagenes/login.jpg'))
        
        # Botones del formulario y sus funciones
        self.btnBuscar.clicked.connect(self.buscar_clientes)
        
        self.tbDatos.doubleClicked.connect(self.insertar_cliente_en_ventas)
        
        
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
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    # Funciones conectadas a los botones
    def insertar_cliente_en_ventas(self, index):
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
            id_cliente = self.tbDatos.model().index(row, 0).data()
            nombre_cliente = self.tbDatos.model().index(row, 1).data()
            apellidos_cliente = self.tbDatos.model().index(row, 2).data()

            # Llamar a la función traer_cliente en la instancia de VentanaCotizaciones
            self.ventana_ventas.traer_cliente(id_cliente, nombre_cliente, apellidos_cliente)
            self.close()

        
        
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT idcliente as 'CODIGO', nombre AS 'NOMBRE', apellidos AS 'APELLIDOS' FROM cliente")
        
        
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()
        self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def buscar_clientes(self):
        # Variables con datos de los inputs para usar como criterios / filtros de busquedas.
        criterio_de_busqueda = self.comboBox.currentText()
        nombre_a_buscar = self.txtBuscar.text()

        if criterio_de_busqueda == "Nombre":
            
            
            query = QSqlQuery()
            query.exec_(f"SELECT idcliente as 'CODIGO', nombre AS 'NOMBRE', apellidos AS 'APELLIDOS' FROM cliente WHERE nombre LIKE '%{nombre_a_buscar}%';")
                
                
            # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
            model = QSqlTableModel()    
            model.setQuery(query)        
            self.tbDatos.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()
            self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
        elif criterio_de_busqueda == "Codigo":
            query = QSqlQuery()
            query.exec_(f"SELECT idcliente as 'CODIGO', nombre AS 'NOMBRE', apellidos AS 'APELLIDOS' FROM cliente WHERE idcliente LIKE '%{nombre_a_buscar}%';")
                
                
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
        VentanaBuscarClienteVentas.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        self.visualiza_datos()   
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaBuscarClienteVentas()
    GUI.show()
    sys.exit(app.exec_())