import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QAbstractItemView, QMessageBox
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QTextDocument, QTextCursor
from PyQt5.QtPrintSupport import QPrinter
from PyQt5.QtSql import QSqlTableModel, QSqlQuery, QSqlDatabase
from Conexion_db import ruta_database
from reportlab.lib.pagesizes import letter, landscape
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from io import BytesIO


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
        #self.btnImprimir.clicked.connect(self.generate_invoice)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualiza_datos(self):
        
        query = QSqlQuery()
        query.exec_(f"SELECT DS.Fecha, DS.Cliente, S.Codigo, S.Categoria, S.Producto, S.CantidadTotal as Cantidad, DS.Comentario, DS.ID\
                        FROM DetalleSalidas AS DS JOIN Salidas AS S ON DS.ID = S.ID_Salida\
                        UNION ALL\
                        SELECT NULL as Fecha, NULL as Proveedor, NULL as Codigo, NULL as Categoria, NULL as Producto, NULL as Cantidad, NULL as Comentario, NULL as Und\
                        UNION ALL\
                        SELECT NULL as Fecha, '*DETALLE DE COMPRAS*', NULL as Codigo, NULL as Categoria, NULL as Producto, NULL as Cantidad, NULL as Comentario, NULL as Und\
                        UNION ALL\
                        SELECT 'Fecha', 'Proveedor', 'Codigo', 'Categoria', 'Producto', 'Cantidad', 'Comentario', 'Medida'\
                        UNION ALL\
                        SELECT Fecha, Proveedor, Codigo, Categoria, Producto, Cantidad, Comentario, Und FROM Compras")
        
           
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)
        self.dataView.setModel(model)        

        # Ajustar el tamaño de las columnas para que se ajusten al contenido y bloquea el editar
        self.dataView.resizeColumnsToContents()
        self.dataView.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    #aqui va el codigo para la opcion de imprimir    
    
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