import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QTableView
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from Conexion_db import conectar_db
from Consultas_db import mostrar_datos_de_faltantes

class VentanaReportes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Filtrar.ui',self)
        
        # Configuraiones de la ventana Filtrar.
        self.setWindowTitle('FILTRAR REPORTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnReporteTotal.clicked.connect(self.mostrar_faltantes)
        
        
    def mostrar_faltantes(self):
        mostrar_datos_de_faltantes()    
        
    #Funcion para colocar el foco en el objeto indicado    
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