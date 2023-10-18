import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsDropShadowEffect, QMdiSubWindow
from PyQt5.QtCore import Qt
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from Consultas_db import insertar_nuevo_cliente, obtener_ultimo_codigo, generar_nuevo_codigo


class VentanaBuscarproveedor(QMainWindow):
    ventana_abierta = False    
    def __init__(self,ventana_ingreso):
        super().__init__()
        self.ventana_ingreso = ventana_ingreso        
        uic.loadUi('Sistema de ventas/ui/FrmBuscarProveedor.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Buscar Proveedores .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        # Botones del formulario y sus funciones
        self.btnBuscar.clicked.connect(self.buscar_proveedores)
        #self.btnBuscar.clicked.connect(self.insertar_cliente_en_cotizacion)
        
        self.tbDatos.doubleClicked.connect(self.insertar_proveedor_en_ingreso)
        
        
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
    def buscar_proveedores(self):
        # Variables con datos de los inputs para usar como criterios / filtros de busquedas.
        criterio_de_busqueda = self.comboBox.currentText()
        nombre_a_buscar = self.txtBuscar.text()

        if criterio_de_busqueda == "Razon social":
            
            
            query = QSqlQuery()
            query.exec_(f"SELECT idproveedor as 'CODIGO', razon_social AS 'NOMBRE' FROM proveedor WHERE razon_social LIKE '%{nombre_a_buscar}%';")
                
                
            # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
            model = QSqlTableModel()    
            model.setQuery(query)        
            self.tbDatos.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()
            self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
        elif criterio_de_busqueda == "Codigo":
            query = QSqlQuery()
            query.exec_(f"SELECT idproveedor as 'CODIGO', razon_social AS 'NOMBRE' FROM proveedor WHERE idproveedor LIKE '%{nombre_a_buscar}%';")
                
                
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

    # Funciones conectadas a los botones
    def insertar_proveedor_en_ingreso(self, index):
        from FrmIngreso import VentanaIngresoAlmacen
        
        if not VentanaIngresoAlmacen.ventana_abierta:
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Ventana cerrada")
            mensaje.setText("La ventana Ingreso está cerrada.")
            mensaje.exec_()
        else:
            # Obtener la fila seleccionada
            row = index.row()

            # Obtener los datos de la fila seleccionada
            id_proveedor = self.tbDatos.model().index(row, 0).data()
            nombre_proveedor = self.tbDatos.model().index(row, 1).data()
            

            # Llamar a la función traer_proveedor en la instancia de VentanaCotizaciones y mandarle el id y nombre de proveedor.
            self.ventana_ingreso.traer_proveedor(id_proveedor, nombre_proveedor)
            self.close()

        
        
    def visualiza_datos(self):
        # Consulta SELECT * FROM proveedor
        query = QSqlQuery()
        query.exec_(f"SELECT idproveedor as 'CODIGO', razon_social AS 'NOMBRE' FROM proveedor")
        
        
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
        VentanaBuscarproveedor.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        self.visualiza_datos()   
                
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaBuscarproveedor()
    GUI.show()
    sys.exit(app.exec_())