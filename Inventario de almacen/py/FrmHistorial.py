import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QAbstractItemView, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel, QSqlQuery, QSqlDatabase
from Conexion_db import ruta_database
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle


class VentanaHistorial(QMainWindow):    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Inventario de almacen/ui/FrmHistorial.ui',self)
        
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('MOVIMIENTOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Inventario de almacen/png/folder.png'))
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  
        #Llamar a los diferentes formularios desde los botones
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnImprimir.clicked.connect(self.imprimir_datos)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualiza_datos(self):
        
        query = QSqlQuery()
        query.exec_(f"SELECT * from Compras\
                        UNION ALL\
                        SELECT NULL as Fecha, NULL as N_doc, NULL as Proveedor, NULL as Codigo, NULL as Categoria, NULL as Producto, NULL as Und, NULL as Comentario, NULL as Cantidad\
                        UNION ALL\
                        SELECT NULL as Fecha, NULL as N_doc, '*HISTORIAL DE SALIDAS*', NULL as Codigo, NULL as Categoria, NULL as Producto, NULL as Und, NULL as Comentario, NULL as Cantidad\
                        UNION ALL\
                        SELECT 'Fecha', 'N_doc', 'Cliente', 'Codigo', 'Categoria', 'Producto', NULL as Und, 'Comentario', 'Cantidad'\
                        UNION ALL\
                        SELECT Fecha, N_doc, Cliente, Codigo, Categoria, Producto, NULL, Comentario, Cantidad\
                        FROM Salidas")

   
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)
        self.dataView.setModel(model)        

        # Ajustar el tamaño de las columnas para que se ajusten al contenido y bloquea el editar
        self.dataView.resizeColumnsToContents()
        self.dataView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
    def imprimir_datos(self):
        # Crear una QTableView con datos (reemplaza esto con tus propios datos)
        self.dataView = QTableView(self)
        # Carga los datos en la self.dataView

        # Crear un botón para imprimir
        self.print_button = QPushButton("Imprimir", self)
        self.print_button.clicked.connect(self.print_table)

    def print_table(self):
        # Crear un documento PDF
        doc = SimpleDocTemplate("tabla_qtableview.pdf", pagesize=letter)

        # Obtener los datos de la self.dataView
        data = []
        for row in range(self.dataView.model().rowCount()):
            row_data = []
            for col in range(self.dataView.model().columnCount()):
                item = self.dataView.model().index(row, col).data(Qt.DisplayRole)
                row_data.append(str(item))
            data.append(row_data)

        # Crear la tabla con los datos
        tabla_qtableview = Table(data)
        tabla_qtableview.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            # Agrega otros estilos según tus preferencias
        ]))

        # Crear el contenido del PDF
        contenido = [tabla_qtableview]

        # Agregar contenido al documento
        doc.build(contenido)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def fn_Salir(self):
        self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    def showEvent(self, event):
        super().showEvent(event) 
          
        
        model = QSqlTableModel()
        model.setTable("Compras")
        model.select()
        self.visualiza_datos()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaHistorial()
    GUI.show()
    sys.exit(app.exec_())