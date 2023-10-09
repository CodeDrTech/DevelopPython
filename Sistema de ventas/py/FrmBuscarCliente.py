import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect, QMdiSubWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Consultas_db import insertar_nuevo_cliente, obtener_ultimo_codigo, generar_nuevo_codigo

class VentanaBuscarCliente(QMainWindow):
    ventana_abierta = False    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmBuscarCliente.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Buscar Clientes .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        # Botones del formulario y sus funciones
        #self.btnBuscar.clicked.connect(self.insertar_cliente_en_cotizacion)
        
        self.tbDatos.doubleClicked.connect(self.insertar_cliente_en_cotizacion)
        
        
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
    def insertar_cliente_en_cotizacion(self, index):
        from FrmCotizaciones import VentanaCotizaciones
        ventana = VentanaCotizaciones()
        
        
        # Obtener la fila seleccionada
        row = index.row()

        # Obtener los datos de la fila seleccionada
        id_cliente = self.tbDatos.model().index(row, 0).data()
        nombre_cliente = self.tbDatos.model().index(row, 1).data()
        apellidos_cliente = self.tbDatos.model().index(row, 2).data()
        
        
        
        ventana.traer_cliente(id_cliente, nombre_cliente, apellidos_cliente)
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
    def closeEvent(self, event):
        VentanaBuscarCliente.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        self.visualiza_datos()   
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaBuscarCliente()
    GUI.show()
    sys.exit(app.exec_())