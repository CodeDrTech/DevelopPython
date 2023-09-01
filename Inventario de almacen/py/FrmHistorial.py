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