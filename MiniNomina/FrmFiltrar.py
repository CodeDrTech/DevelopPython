import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QTableView
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from Conexion_db import conectar_db
from FrmDatos import VentanaDatos


class VentanaReportes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Filtrar.ui',self)
        
        # Configuraiones de la ventana Filtrar.
        self.setWindowTitle('FILTRAR REPORTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnReporteTotal.clicked.connect(self.abrirFrmDatos)
        
        
        
    # Funcion para llamar la ventana secundaria (Ventana de datos)
    def abrirFrmDatos(self):
        self.llamar_venana_datos = VentanaDatos()
        self.llamar_venana_datos.show()
        self.llamar_venana_datos.datos_en_tabla_faltantes() 
    
    
        
    # Funcion para colocar el foco en el objeto indicado    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto txtNombre
        self.cmbEmpleado.setFocus()
        
        
        
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaReportes()
    GUI.show()
    sys.exit(app.exec_())