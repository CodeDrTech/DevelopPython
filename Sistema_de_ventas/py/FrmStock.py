import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView, QGraphicsScene, QGraphicsPixmapItem, QGraphicsDropShadowEffect
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap
from Consultas_db import insertar_nuevo_articulo

class VentanaStock(QMainWindow):
    ventana_abierta = False
    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema_de_ventas/ui/FrmStock.ui',self)

        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Stocks .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema_de_ventas/imagenes/login.jpg'))
        
        # Establecer el texto de referencia a la caja de texto buscar
        # Conectar el evento de clic para borrar el texto
        self.txtBuscar.setPlaceholderText('Buscar')        
        self.txtBuscar.mousePressEvent = self.borrarTexto
        
        self.btnBuscar.clicked.connect(self.buscar_datos)


        # Crear un efecto de sombra        
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tabWidget.setGraphicsEffect(tabWidget_shadow)

        groupBox_2shadow = QGraphicsDropShadowEffect()
        groupBox_2shadow.setBlurRadius(20)
        groupBox_2shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_2.setGraphicsEffect(groupBox_2shadow)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT ar.codigo AS 'CODIGO',\
                            ar.nombre AS 'NOMBRE',\
                            ISNULL(st.disponible, 0) AS 'CANTIDAD DISPONIBLE',\
                            ar.descripcion AS 'DESCRIPCION',\
                            ca.descripcion AS 'CATEGORIA',\
                            pe.descripcion AS 'UNIDAD DE MEDIDA'\
                        FROM articulo ar\
                        INNER JOIN Categoria ca ON ca.idcategoria = ar.idcategoria\
                        INNER JOIN presentacion pe ON pe.idpresentacion = ar.idpresentacion\
                        LEFT JOIN stock st ON st.idarticulo = ar.idarticulo;")

        # Crear un modelo de tabla SQL, ejecutar el query y establecer el modelo en la tabla
        model = QSqlTableModel()
        model.setQuery(query)

        # Configura el modelo para permitir la edición
        #model.setEditStrategy(QSqlTableModel.OnFieldChange) # type: ignore

        # Establece el modelo en la tabla
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()
        # Permitir la edición en las celdas
        self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
    def buscar_datos(self):
        buscar = self.txtBuscar.text()
        
        if self.cmbBuscar.currentText() == "Nombre":    
                query = QSqlQuery()
                query.exec_(f"SELECT ar.codigo AS 'CODIGO',\
                                    ar.nombre AS 'NOMBRE',\
                                    ISNULL(st.disponible, 0) AS 'CANTIDAD DISPONIBLE',\
                                    ar.descripcion AS 'DESCRIPCION',\
                                    ca.descripcion AS 'CATEGORIA',\
                                    pe.descripcion AS 'UNIDAD DE MEDIDA'\
                                FROM articulo ar\
                                INNER JOIN Categoria ca ON ca.idcategoria = ar.idcategoria\
                                INNER JOIN presentacion pe ON pe.idpresentacion = ar.idpresentacion\
                                LEFT JOIN stock st ON st.idarticulo = ar.idarticulo\
                                WHERE ar.nombre like '%{buscar}%';")

                # Crear un modelo de tabla SQL, ejecutar el query y establecer el modelo en la tabla
                model = QSqlTableModel()
                model.setQuery(query)

                # Establece el modelo en la tabla
                self.tbDatos.setModel(model)

                # Ajustar el tamaño de las columnas para que se ajusten al contenido
                self.tbDatos.resizeColumnsToContents()
                # Permitir la edición en las celdas
                self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        elif self.cmbBuscar.currentText() == "Codigo":    
                query = QSqlQuery()
                query.exec_(f"SELECT ar.codigo AS 'CODIGO',\
                                    ar.nombre AS 'NOMBRE',\
                                    ISNULL(st.disponible, 0) AS 'CANTIDAD DISPONIBLE',\
                                    ar.descripcion AS 'DESCRIPCION',\
                                    ca.descripcion AS 'CATEGORIA',\
                                    pe.descripcion AS 'UNIDAD DE MEDIDA'\
                                FROM articulo ar\
                                INNER JOIN Categoria ca ON ca.idcategoria = ar.idcategoria\
                                INNER JOIN presentacion pe ON pe.idpresentacion = ar.idpresentacion\
                                LEFT JOIN stock st ON st.idarticulo = ar.idarticulo\
                                WHERE ar.codigo like '%{buscar}%';")

                # Crear un modelo de tabla SQL, ejecutar el query y establecer el modelo en la tabla
                model = QSqlTableModel()
                model.setQuery(query)

                # Establece el modelo en la tabla
                self.tbDatos.setModel(model)

                # Ajustar el tamaño de las columnas para que se ajusten al contenido
                self.tbDatos.resizeColumnsToContents()
                # Permitir la edición en las celdas
                self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
        else:    
            query = QSqlQuery()
            query.exec_(f"SELECT ar.codigo AS 'CODIGO',\
                                    ar.nombre AS 'NOMBRE',\
                                    ISNULL(st.disponible, 0) AS 'CANTIDAD DISPONIBLE',\
                                    ar.descripcion AS 'DESCRIPCION',\
                                    ca.descripcion AS 'CATEGORIA',\
                                    pe.descripcion AS 'UNIDAD DE MEDIDA'\
                                FROM articulo ar\
                                INNER JOIN Categoria ca ON ca.idcategoria = ar.idcategoria\
                                INNER JOIN presentacion pe ON pe.idpresentacion = ar.idpresentacion\
                                LEFT JOIN stock st ON st.idarticulo = ar.idarticulo\
                                WHERE ca.descripcion like '%{buscar}%';")

            # Crear un modelo de tabla SQL, ejecutar el query y establecer el modelo en la tabla
            model = QSqlTableModel()
            model.setQuery(query)

            # Establece el modelo en la tabla
            self.tbDatos.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()
            # Permitir la edición en las celdas
            self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Elimina el textp de referencia que tiene la casilla buscar
    def borrarTexto(self, event):
        # Borrar el texto cuando se hace clic
        self.txtBuscar.clear()

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------              
    def closeEvent(self, event):
        VentanaStock.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------          
    def showEvent(self, event):
        super().showEvent(event)
        self.visualiza_datos()



if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaStock()
    GUI.show()
    sys.exit(app.exec_())