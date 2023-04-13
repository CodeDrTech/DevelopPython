import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QTableView
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Conexion_db import conectar_db
from FrmDatos import VentanaDatos


class VentanaReportes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Filtrar.ui',self)
        
        # Configuraiones de la ventana Filtrar.
        self.setWindowTitle('FILTRAR REPORTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/folder.png'))
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        #self.BtnReporteTotal.clicked.connect(self.abrirFrmDatos)
        self.BtnReporte.clicked.connect(self.abrirFrmDatos_por_nombres)
        
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('faltantes')
        model.select()
        column_data = []
        for i in range(model.rowCount()):
            column_data.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox.
        combo_model = QStandardItemModel()
        for item in column_data:
            combo_model.appendRow(QStandardItem(str(item)))
        self.cmbEmpleado.setModel(combo_model)
        
    # Funcion para llamar la ventana secundaria (Ventana de datos)
    #def abrirFrmDatos(self):
        #self.llamar_venana_datos = VentanaDatos()
        #self.llamar_venana_datos.show()
        #self.llamar_venana_datos.datos_en_tabla_faltantes()
        
        
    # Funcion para llamar la ventana secundaria (Ventana de datos, datos filtrados)
    def abrirFrmDatos_por_nombres(self):
        self.llamar_venana_datos = VentanaDatos()
        self.llamar_venana_datos.show()
        self.llamar_venana_datos.datos_en_tabla_faltantes_por_nombre()
        
        
    def abrirSelectTotal(self):        
        self.llamar_select_total = VentanaDatos()
        self.llamar_select_total.show()
        self.llamar_select_total.datos_de_select()
        
        
        
        
        
        
    # Funcion para colocar el foco en el objeto indicado    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto txtNombre
        self.cmbEmpleado.setFocus()
        # Limpiar los cuadros de texto Empleados.
        self.cmbEmpleado.setCurrentText("")
        
        
        
    
        
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaReportes()
    GUI.show()
    sys.exit(app.exec_())