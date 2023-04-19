import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QPageLayout, QPageSize, QFont, QTransform
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrinterInfo
from PyQt5.QtCore import QMarginsF, Qt, QRectF
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
            # Escalar el tamaño del QTableView para que quepa en una página
            scale_factor = 1.0
            while (self.tbtabla.width() * scale_factor > printer.pageRect().width() or
                self.tbtabla.height() * scale_factor > printer.pageRect().height()):
                scale_factor *= 0.9

            # Configurar la página para que se ajuste al tamaño del QTableView
            layout = QPageLayout(printer.pageLayout())
            layout.setPaintRect(QRectF(0, 0, printer.pageRect().width(), printer.pageRect().height()))
            printer.setPageLayout(layout)

            # Establecer la escala del QTableView
            self.tbtabla.setTransform(QTransform().scale(scale_factor, scale_factor))

            # Ajustar el tamaño de las columnas
            self.tbtabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Crear un objeto QPainter y dibujar el contenido del QTableView en el objeto QPrinter
            painter = QPainter()
            painter.begin(printer)
            self.tbtabla.render(painter)
            painter.end()

            # Restaurar la escala y el tamaño de las columnas del QTableView
            self.tbtabla.setTransform(QTransform())
            self.tbtabla.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        
        
        
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