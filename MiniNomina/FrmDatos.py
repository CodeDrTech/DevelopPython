import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QTableView, QTableWidget, QHeaderView, QVBoxLayout
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db
from Consultas_db import mostrar_datos_de_faltantes
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
import Consultas_db


class VentanaDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Datos.ui',self)
        
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('REPORTE TOTAL')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        # Muestra los datos de la consulta contenida en mostrar_datos_de_faltantes del modulo Consultas_db
        self.BtnGuardar.clicked.connect(self.datos_en_tabla)
    
        
    def datos_en_tabla(self):    
        mostrar_datos_de_faltantes(self.tbtabla)
        
        
    
    
    
    # Funion para cerar la ventana llamado desde el boton Salir.    
    def fn_Salir(self):
        self.close()
        conn = conectar_db()
        conn.close()
        
        
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)          
        
        #mostrar_datos_de_faltantes(self.tbtabla)
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaDatos()
    GUI.show()
    sys.exit(app.exec_())