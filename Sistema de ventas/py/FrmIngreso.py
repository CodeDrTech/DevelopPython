import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QDate

class VentanaIngresoAlmacen(QMainWindow):
    ventana_abierta = False     
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmIngreso.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de ingresos almacén .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    def cargar_proveedores(self):    
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('proveedor')
        model.select()
        column_data = []
        for i in range(model.rowCount()):
            column_data.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox.
        combo_model = QStandardItemModel()
        for item in column_data:
            combo_model.appendRow(QStandardItem(str(item)))
        self.cmbProveedor.setModel(combo_model)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def closeEvent(self, event):
        VentanaIngresoAlmacen.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        self.cargar_proveedores()
                
        self.txtFecha.setDate(QDate.currentDate())
        self.txtFechaInicio.setDate(QDate.currentDate())
        self.txtFechaFin.setDate(QDate.currentDate())
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaIngresoAlmacen()
    GUI.show()
    sys.exit(app.exec_())