import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QTableView
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db
from Consultas_db import mostrar_datos_de_faltantes
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery



class VentanaDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Datos.ui',self)
        
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('REPORTE TOTAL')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        # Crear un objeto QSqlTableModel y establecer la tabla de destino para el modelo
        self.modelo = QSqlTableModel()
        self.modelo.setTable("faltantes")
        
        # Establecer el modelo en la tabla QTableView
        self.tbtabla.setModel(self.modelo)
        
        # Mostrar los datos en la tabla QTableView
        mostrar_datos_de_faltantes(self.tbtabla)   
        
        
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)  
        
                 
           
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaDatos()
    GUI.show()
    sys.exit(app.exec_())