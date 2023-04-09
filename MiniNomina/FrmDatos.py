import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QTableView
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery


class VentanaDatos(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Datos.ui',self)
        
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('VISUALIZAR DATOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        # Conectar a la base de datos
        db = QSqlDatabase.addDatabase("QSQLITE")
        db.setDatabaseName("C:/Users/Jose/Documents/GitHub/DevelopPython/Base de datos/MiniNomina.db")
        if not db.open():
            QMessageBox.critical(None, "Error", "No se pudo conectar a la base de datos")

        # Crear el modelo de tabla y establecer la tabla
        self.tbTablas = QSqlTableModel()
        self.tbTablas.setTable("faltantes")

        # Establecer el modelo de tabla en el QTableView
        self.tbTablas.setModel(self.tbTablas)
        
        
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)  
        
        # Seleccionar los datos de la tabla
        self.tbTablas.select()
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaDatos()
    GUI.show()
    sys.exit(app.exec_())