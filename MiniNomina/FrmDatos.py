import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel


class VentanaDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Datos.ui',self)
        
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('VISUALIZAR DATOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaDatos()
    GUI.show()
    sys.exit(app.exec_())