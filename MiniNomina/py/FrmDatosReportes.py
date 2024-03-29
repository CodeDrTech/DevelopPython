import sys
import locale
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QStyledItemDelegate, QAbstractItemView, QDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextDocument
from PyQt5.QtPrintSupport import QPrintDialog, QPrintPreviewDialog, QPrinter
from PyQt5.QtCore import Qt, QDate
from Consultas_db import mostrar_datos_de_empleados
from PyQt5.QtSql import QSqlTableModel, QSqlQuery


class CurrencyDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        try:
            # Convierte el valor a un formato de moneda
            return locale.toCurrencyString(float(value))
        except ValueError:
            # Si no se puede convertir a un formato de moneda, devuelve el valor original
            return value 

class VentanaDatosReportes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/ui/DatosFiltrar.ui',self)
        
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('REPORTES DE PAGOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/png/folder.png'))
        
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        self.BtnImprimir.clicked.connect(self.imprimir_datos_tbtabla)
        
        self.BtnEliminar.clicked.connect(self.borrar_fila)
        
        self.BtnBuscar.clicked.connect(self.Filtro_por_fecha)
        
        self.txtFechaInicio.dateChanged.connect(self.Filtro_por_fecha)
        self.txtFechaFinal.dateChanged.connect(self.Filtro_por_fecha)
        
        self.cmbEmpleado.currentIndexChanged.connect(self.Filtro_por_fecha)
        
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
            
            if FechaInicio > FechaFinal:
                QMessageBox.warning(self, "ERROR ENTRE FECHAS", "LA PRIMERA FECHA NO PUEDE SER MAYOR A LA SEGUNDA.")
                return
            
            query = QSqlQuery()
            query.exec_(f"SELECT e.NOMBRE,\
            COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0) AS FALTANTES,\
            COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0) AS ABONOS,\
            e.SALARIO - COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0)\
            + COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0) AS SALARIO_NETO\
            FROM empleados e GROUP BY NOMBRE")

   
            # Crear un modelo de tabla SQL
            model = QSqlTableModel()
    
            model.setQuery(query)   
    
            # Establecer el modelo en la tabla
            self.tbtabla.setModel(model)

        
            self.tbtabla.setItemDelegateForColumn(3, currency_delegate)
            self.tbtabla.setItemDelegateForColumn(2, currency_delegate)
            self.tbtabla.setItemDelegateForColumn(1, currency_delegate)
        
            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbtabla.resizeColumnsToContents()
            self.tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
            
        else:
            
            query = QSqlQuery()
            query.exec_(f"SELECT e.NOMBRE,\
            COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0) AS FALTANTES,\
            COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0) AS ABONOS,\
            e.SALARIO - COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0)\
            + COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0) AS SALARIO_NETO\
            FROM empleados e WHERE e.NOMBRE = '{Empleado}'")

   
            # Crear un modelo de tabla SQL
            model = QSqlTableModel()
    
            model.setQuery(query)   
    
            # Establecer el modelo en la tabla
            self.tbtabla.setModel(model)

        
            self.tbtabla.setItemDelegateForColumn(3, currency_delegate)
            self.tbtabla.setItemDelegateForColumn(2, currency_delegate)
            self.tbtabla.setItemDelegateForColumn(1, currency_delegate)
        
            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbtabla.resizeColumnsToContents() 
            self.tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def imprimir_datos_tbtabla(self):
        
        FechaInicio = self.txtFechaInicio.date().toString("d-MMMM-yyyy")
        FechaFinal = self.txtFechaFinal.date().toString("d-MMMM-yyyy") 
        
        
        # Configurar la localización para que use la convención de separación de miles adecuada
        locale.setlocale(locale.LC_ALL, '')
        conv = locale.localeconv()
        # Crear objeto QPrinter y configurar opciones de impresión
        printer = QPrinter(QPrinter.HighResolution)
        printer.setPageSize(QPrinter.A4)
        printer.setOutputFormat(QPrinter.NativeFormat)
        

        # Mostrar diálogo de impresión y obtener configuraciones de usuario
        dialog = QPrintDialog(printer, self.tbtabla)
        if dialog.exec_() == QDialog.Accepted:
            # Crear objeto QTextDocument y establecer contenido HTML
            
            table_html = "<style type='text/css'>\
    table {\
        border-collapse: collapse;\
        border-spacing: 0;\
        width: 100%;\
    }\
    th, td {\
        border: 0.5px solid black;\
        padding: 10px;\
        text-align: left;\
        font-size: 10pt;\
    }\
    th {\
        background-color: gray;\
        color: white;\
    }\
    tr:nth-child(even) {\
        background-color: #f2f2f2;\
    }\
</style>"


            table_html += "<th>REPORTE DE PAGOS </th>"
            table_html += "<table>"
            table_html += "<tr>"
            table_html += "<th>NOMBRE</th>"
            table_html += "<th>FALTANTES</th>"
            table_html += "<th>ABONOS</th>"
            table_html += "<th>SALARIO NETO</th>"
            table_html += "</tr>"
            table_model = self.tbtabla.model()
            row_count = table_model.rowCount()
            column_count = table_model.columnCount()
            
            for row in range(row_count):
                
                table_html += "<tr>"
            
                for column in range(column_count):
                
                    cell_value = table_model.data(table_model.index(row, column), Qt.DisplayRole) # type: ignore
                    if isinstance(cell_value, (float)):
                        cell_value = locale.currency(cell_value, symbol=True, grouping=True)
                    table_html += f"<td>{cell_value}</td>"
                                    
                table_html += "</tr>"
            
            table_html += f"<th>REPORTE DESDE EL {FechaInicio} HASTA EL {FechaFinal} </th>"    
            document = QTextDocument()
            
            document.setHtml(table_html)

            # Imprimir contenido del QTextDocument
            preview_dialog = QPrintPreviewDialog(printer, self.tbtabla)
            preview_dialog.paintRequested.connect(document.print_)
            preview_dialog.exec_()
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
        
    def borrar_fila(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.tbtabla.selectedIndexes()
        
        if indexes:
            
            # Obtener la fila al seleccionar una celda de la tabla
            index = indexes[0]
            row = index.row()
            
            
            # Preguntar si el usuario está seguro de eliminar la fila
            confirmacion = QMessageBox.question(self, "¿ELIMINAR?", "¿ESTAS SEGURO QUE QUIERE ELIMINAR ESTA FILA?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", eliminar la fila
            if confirmacion == QMessageBox.Yes:            
            
                # Eliminar la fila seleccionada del modelo de datos
                model = self.tbtabla.model()
                model.removeRow(row)
                QMessageBox.warning(self, "ELIMINADO", "REGISTRO ELIMINADO.")
            
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
        self.cmbEmpleado.setFocus()
    
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
    GUI = VentanaDatosReportes()
    GUI.show()
    sys.exit(app.exec_())