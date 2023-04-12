import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QTableView, QTableWidget, QHeaderView, QVBoxLayout
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db
import Consultas_db
from Consultas_db import mostrar_datos_de_faltantes, mostrar_datos_de_empleados
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery



class VentanaDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Datos.ui',self)
        
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('PANEL DE DATOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        
        
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        
        
    
    # Muestra los datos de la consulta contenida en mostrar_datos_de_faltantes del modulo Consultas_db    
    def datos_en_tabla_faltantes(self):    
        mostrar_datos_de_faltantes(self.tbtabla)
        
        
    # Muestra los datos de la consulta contenida en mostrar_datos_de_empleados del modulo Consultas_db    
    def datos_en_tabla_empleados(self):    
        mostrar_datos_de_empleados(self.tbtabla)
        
        
    
    
    
    # Funion para cerar la ventana llamado desde el boton Salir.    
    def fn_Salir(self):
        self.close()
          
        
        
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        # Este se ejecutra cuendo la ventana se abre
        super().showEvent(event)          
        
        
    def closeEvent(self, event):
        
        super().closeEvent(event)    
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaDatos()
    GUI.show()
    sys.exit(app.exec_())