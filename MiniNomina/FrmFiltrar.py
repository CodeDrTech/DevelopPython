import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QTableView, QAbstractItemView
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from Conexion_db import conectar_db
from FrmDatos import VentanaDatos


class VentanaReportes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Filtrar.ui',self)
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Filtrar.
        self.setWindowTitle('FILTRAR REPORTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/folder.png'))
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnReporteTotal.clicked.connect(self.abrirFrmDatos)
        self.BtnReporte.clicked.connect(self.reporte_por_cmbEmpleado)
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('empleados')
        model.select()
        column_data = []
        for i in range(model.rowCount()):
            column_data.append(model.data(model.index(i, 0)))
        
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox.
        combo_model = QStandardItemModel()
        for item in column_data:
            combo_model.appendRow(QStandardItem(str(item)))
        self.cmbEmpleado.setModel(combo_model)
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # Funcion para llamar la ventana secundaria (Ventana de datos)
    def abrirFrmDatos(self):
        self.llamar_tbtabla = VentanaDatos()
        self.llamar_tbtabla.show()
        tbtabla = self.llamar_tbtabla.TableView_de_FrmDatos() 
        
        
        query = QSqlQuery()
        query.exec_("SELECT e.NOMBRE,\
       COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS TOTAL_FALTANTES,\
       COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS TOTAL_ABONOS,\
       e.SALARIO - COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0)\
       + COALESCE ((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS SALARIO_NETO FROM empleados e")

   
        # Crear un modelo de tabla SQL
        model = QSqlTableModel()
    
        model.setQuery(query)   
    
        # Establecer el modelo en la tabla
        tbtabla.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        tbtabla.resizeColumnsToContents()
        tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------    
    def reporte_por_cmbEmpleado(self):
        Empleado = self.cmbEmpleado.currentText()
        
        # Validar que cmbEmpleado no esté vacío
        if not Empleado:
            QMessageBox.warning(None, "ERROR", "DEBE ELEJIR UN NOMBRE.") # type: ignore
            return   
        self.llamar_tbtabla = VentanaDatos()
        self.llamar_tbtabla.show()
        tbtabla = self.llamar_tbtabla.TableView_de_FrmDatos() 
        
        
        query = QSqlQuery()
        query.exec_(f"SELECT e.NOMBRE,\
       COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS TOTAL_FALTANTES,\
       COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS TOTAL_ABONOS,\
       e.SALARIO - COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0)\
       + COALESCE ((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE), 0) AS SALARIO_NETO FROM empleados e WHERE e.NOMBRE = '{Empleado}'")

   
        # Crear un modelo de tabla SQL
        model = QSqlTableModel()
    
        model.setQuery(query)
        
        # Establecer el modelo en la tabla
        tbtabla.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        tbtabla.resizeColumnsToContents()
        tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)        
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # Funcion para colocar el foco en el objeto indicado    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto txtNombre
        self.cmbEmpleado.setFocus()
        # Limpiar los cuadros de texto Empleados.
        self.cmbEmpleado.setCurrentText("")
        
        
        
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaReportes()
    GUI.show()
    sys.exit(app.exec_())