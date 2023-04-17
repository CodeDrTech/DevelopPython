import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QPageLayout, QPageSize
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrinterInfo
from PyQt5.QtCore import QMarginsF
from Conexion_db import conectar_db
from Consultas_db import mostrar_datos_de_faltantes, mostrar_datos_de_empleados
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery




class VentanaDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Datos.ui',self)
        
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('PANEL DE DATOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/folder.png'))
        
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnImprimir.clicked.connect(self.imprimir_datos_tbtabla)
        
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    # Muestra los datos de la consulta contenida en mostrar_datos_de_faltantes del modulo Consultas_db    
    def datos_en_tabla_faltantes(self):
        mostrar_datos_de_faltantes(self.tbtabla)
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # Muestra los datos de la consulta contenida en mostrar_datos_de_empleados del modulo Consultas_db    
    def datos_en_tabla_empleados(self):    
        mostrar_datos_de_empleados(self.tbtabla)
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # TableView_de_FrmDatos almacena a tbtabla para visualizr los datos requeridos.    
    def TableView_de_FrmDatos(self):
        return self.tbtabla      
    
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def imprimir_datos_tbtabla(self):
        # Crear una instancia de QPrinter
        printer = QPrinter(QPrinter.HighResolution)

        # Crear un objeto QPrintDialog y mostrarlo al usuario
        print_dialog = QPrintDialog(printer)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            # Configurar el tamaño del QTableView para que quepa en una página
            self.tbtabla.resizeColumnsToContents()
            self.tbtabla.setFixedHeight(self.tbtabla.rowHeight(0) * self.tbtabla.model().rowCount() + 20)

            # Configurar la página para que se ajuste al tamaño del QTableView
            page_size = printer.pageLayout().pageSize()
            if page_size == QPageSize.Custom:
                page_size = printer.pageRect().size()
            layout = QPageLayout(QPageSize(page_size), printer.pageLayout().orientation(), QMarginsF(15,15,15,15), printer.pageLayout().units())
            printer.setPageLayout(layout)

            # Crear un objeto QPainter y dibujar el contenido del QTableView en el objeto QPrinter
            painter = QPainter()
            painter.begin(printer)
            self.tbtabla.render(painter)
            painter.end()

            # Llamar a la función newPage() para comenzar a imprimir en una nueva página si es necesario
            if printer.pageOrder() == QPrinter.LastPageFirst:
                printer.setPageOrder(QPrinter.FirstPageFirst)
            if len(QPrinter.supportedPageSizes(QPrinter.PageSize)) > 1:
                printer.newPage()
        
        
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # Funion para cerar la ventana llamado desde el boton Salir.    
    def fn_Salir(self):
        self.close()
          
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        # Este se ejecutra cuendo la ventana se abre
        super().showEvent(event)          
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    def closeEvent(self, event):
        
        super().closeEvent(event)    
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaDatos()
    GUI.show()
    sys.exit(app.exec_())