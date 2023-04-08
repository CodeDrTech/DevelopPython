import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QTableView
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from Conexion_db import conectar_db

class VentanaReportes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Filtrar.ui',self)
        
        # Configuraiones de la ventana Filtrar.
        self.setWindowTitle('FILTRAR REPORTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        # Conectar el botón con la función mostrar_datos
        self.BtnReporte.clicked.connect(self.mostrar_datos)
        
        
    def mostrar_datos(self):
        # Establecer la conexión a la base de datos
        db = conectar_db()
        db = QSqlDatabase.addDatabase('QSQLITE')
        db.setDatabaseName('MiniNomina.db')
        if not db.open():
            QMessageBox.critical(None, 'Error', 'No se pudo establecer la conexión a la base de datos.', QMessageBox.Cancel)
            return
        
        # Crear una instancia de QSqlTableModel
        model = QSqlTableModel()
        model.setTable('faltantes')
        model.select()
        
        # Crear una instancia de QTableView y establecer el modelo
        view = QTableView()
        view.setModel(model)
        
        # Mostrar la vista de tabla en un diálogo modal
        dialog = QDialog(self)
        dialog.setWindowTitle('Datos de la tabla')
        layout = QtWidgets.QVBoxLayout(dialog)
        layout.addWidget(view)
        dialog.exec_()
        
        db.close()
        
        
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