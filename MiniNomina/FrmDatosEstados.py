import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QMessageBox, QStyledItemDelegate, QAbstractItemView
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QPageLayout, QPageSize, QFont, QTransform, QStandardItemModel, QStandardItem
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrinterInfo
from PyQt5.QtCore import QMarginsF, Qt, QRectF, QDate
from Conexion_db import conectar_db
from Consultas_db import mostrar_datos_de_empleados
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery






class CurrencyDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        try:
            # Convierte el valor a un formato de moneda
            return locale.toCurrencyString(float(value))
        except ValueError:
            # Si no se puede convertir a un formato de moneda, devuelve el valor original
            return value 

class VentanaDatosEstados(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/DatosEstados.ui',self)
        
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('ESTADOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/folder.png'))
        
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        self.BtnImprimir.clicked.connect(self.imprimir_datos_tbtabla)
        
        self.BtnEliminar.clicked.connect(self.borrar_fila)
        
        self.BtnBuscar.clicked.connect(self.Filtro_por_fecha)
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
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
    # Muestra los datos de la consulta contenida en mostrar_datos_de_faltantes del modulo Consultas_db    
    #def datos_en_tabla_faltantes(self):
    #   mostrar_datos_de_faltantes(self.tbtabla)
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # Muestra los datos de la consulta contenida en mostrar_datos_de_empleados del modulo Consultas_db    
    def datos_en_tabla_empleados(self):    
        mostrar_datos_de_empleados(self.tbtabla)
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # TableView_de_FrmDatos almacena a tbtabla para visualizr los datos requeridos.    
    def TableView_de_FrmDatos(self):
        return self.tbtabla      
    
    def DeshabilitaBtnEliminar(self):
         self.BtnEliminar.setEnabled(False)
    
    def obtener_fecha_inicio(self):
        self.txtFechaInicio.date().toString("yyyy-MM-dd")
             
    def obtener_fecha_final(self):
        self.txtFechaFinal.date().toString("yyyy-MM-dd")
    
    def DeshabilitaBtnBuscar(self):
         self.BtnBuscar.setEnabled(False)
         
    def Filtro_por_fecha(self):
        Empleado = self.cmbEmpleado.currentText()
        FechaInicio = self.txtFechaInicio.date().toString("yyyy-MM-dd")
        FechaFinal = self.txtFechaFinal.date().toString("yyyy-MM-dd")
        currency_delegate = CurrencyDelegate()
    
        if not Empleado:
            query = QSqlQuery()
            query.exec_(f"SELECT FECHA, NOMBRE, BANCA, ABONO, FALTANTE \
                    FROM faltantes WHERE FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}' \
                    UNION ALL \
                    SELECT 'TOTAL', '', '', SUM(ABONO), SUM(FALTANTE) \
                    FROM faltantes WHERE FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}' \
                    GROUP BY 'TOTAL'")

   
            # Crear un modelo de tabla SQL
            model = QSqlTableModel()
    
            model.setQuery(query)   
    
            # Establecer el modelo en la tabla
            self.tbtabla.setModel(model)

        
        
            self.tbtabla.setItemDelegateForColumn(4, currency_delegate)
            self.tbtabla.setItemDelegateForColumn(3, currency_delegate)
        
            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbtabla.resizeColumnsToContents()
            self.tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
        else:
            query = QSqlQuery()
            query.exec_(f"SELECT FECHA, NOMBRE, BANCA, ABONO, FALTANTE \
                    FROM faltantes WHERE NOMBRE = '{Empleado}' AND FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'\
                    UNION ALL \
                    SELECT 'TOTAL', '', '', SUM(ABONO), SUM(FALTANTE) \
                    FROM faltantes WHERE NOMBRE = '{Empleado}' AND FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'\
                    GROUP BY 'TOTAL'")

   
            # Crear un modelo de tabla SQL
            model = QSqlTableModel()
    
            model.setQuery(query)   
    
            # Establecer el modelo en la tabla
            self.tbtabla.setModel(model)

        
        
            self.tbtabla.setItemDelegateForColumn(4, currency_delegate)
            self.tbtabla.setItemDelegateForColumn(3, currency_delegate)
        
            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbtabla.resizeColumnsToContents() 
            self.tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------        
    def estados_por_fechas(self):
        FechaInicio = self.txtFechaInicio.date().toString("yyyy-MM-dd")
        FechaFinal = self.txtFechaFinal.date().toString("yyyy-MM-dd")
        currency_delegate = CurrencyDelegate()
    
        
        query = QSqlQuery()
        query.exec_(f"SELECT FECHA, NOMBRE, BANCA, ABONO, FALTANTE \
                    FROM faltantes WHERE FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}' \
                    UNION ALL \
                    SELECT 'TOTAL', '', '', SUM(ABONO), SUM(FALTANTE) \
                    FROM faltantes WHERE FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}' \
                    GROUP BY 'TOTAL'")

   
        # Crear un modelo de tabla SQL
        model = QSqlTableModel()
    
        model.setQuery(query)   
    
        # Establecer el modelo en la tabla
        self.tbtabla.setModel(model)

        
        
        self.tbtabla.setItemDelegateForColumn(4, currency_delegate)
        self.tbtabla.setItemDelegateForColumn(3, currency_delegate)
        
        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbtabla.resizeColumnsToContents()
        self.tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def imprimir_datos_tbtabla(self):
        # Crear una instancia de QPrinter
        printer = QPrinter(QPrinter.HighResolution)

        # Crear un objeto QPrintDialog y mostrarlo al usuario
        print_dialog = QPrintDialog(printer)
        if print_dialog.exec_() == QPrintDialog.Accepted:
            # Escalar el tamaño del QTableView para que quepa en una página
            scale_factor = 1.0
            while (self.tbtabla.width() * scale_factor > printer.pageRect().width() or
                self.tbtabla.height() * scale_factor > printer.pageRect().height()):
                scale_factor *= 0.9

            # Configurar la página para que se ajuste al tamaño del QTableView
            layout = QPageLayout(printer.pageLayout())
            layout.setPaintRect(QRectF(0, 0, printer.pageRect().width(), printer.pageRect().height()))
            printer.setPageLayout(layout)

            # Establecer la escala del QTableView
            self.tbtabla.setTransform(QTransform().scale(scale_factor, scale_factor))

            # Ajustar el tamaño de las columnas
            self.tbtabla.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

            # Crear un objeto QPainter y dibujar el contenido del QTableView en el objeto QPrinter
            painter = QPainter()
            painter.begin(printer)
            self.tbtabla.render(painter)
            painter.end()

            # Restaurar la escala y el tamaño de las columnas del QTableView
            self.tbtabla.setTransform(QTransform())
            self.tbtabla.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        
        
    def borrar_fila(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.tbtabla.selectedIndexes()
        
        if indexes:
            
            # Obtener la fila al seleccionar una celda de la tabla
            index = indexes[0]
            row = index.row()
            
            # Eliminar la fila seleccionada del modelo de datos
            model = self.tbtabla.model()
            model.removeRow(row)
            QMessageBox.warning(self, "ELIMINADO", "REGISTRO ELIMINADO CIERRE PARA ACTUALIZAR LOS DATOS.")
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA EL REGISTRO QUE VAS A ELIMINAR.")
            
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # Funion para cerar la ventana llamado desde el boton Salir.    
    def fn_Salir(self):
        self.close()
          
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        # Este se ejecutra cuendo la ventana se abre
        super().showEvent(event)  
                
        self.tbtabla.clearSelection()
        self.DiaPrimero()
        self.DiaDeHoy()
        self.BtnEliminar.setEnabled(False)
        self.cmbEmpleado.setCurrentText("")
    
    
    def DiaPrimero(self):
        
        fecha_actual = QDate.currentDate()
        mes_actual = fecha_actual.month()
        fecha_inicio = QDate(fecha_actual.year(), mes_actual, 1)
        self.txtFechaInicio.setDate(fecha_inicio)
        return fecha_inicio
            
    def DiaDeHoy(self):    
        
        fecha_actual = QDate.currentDate()
        mes_actual = fecha_actual.month()
        #fecha_inicio = QDate(fecha_actual.year(), mes_actual, 1)        
        self.txtFechaFinal.setDate(QDate.currentDate())# Establecer fecha actual en txtFecha. 
        return fecha_actual
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    def closeEvent(self, event):        
        super().closeEvent(event)    
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaDatosEstados()
    GUI.show()
    sys.exit(app.exec_())