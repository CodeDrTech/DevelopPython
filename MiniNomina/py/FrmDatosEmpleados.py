import sys
import locale
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QStyledItemDelegate, QDialog
from PyQt5 import QtGui
from PyQt5.QtGui import QTextDocument
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtCore import Qt
from Consultas_db import mostrar_datos_de_empleados

class CurrencyDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        try:
            # Convierte el valor a un formato de moneda
            return locale.toCurrencyString(float(value))
        except ValueError:
            # Si no se puede convertir a un formato de moneda, devuelve el valor original
            return value 

class VentanaDatosEmpleados(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/ui/DatosEmpleados.ui',self)
        
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('EMPLEADOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/png/folder.png'))
        
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        self.BtnImprimir.clicked.connect(self.imprimir_datos_tbtabla)
        
        self.BtnEliminar.clicked.connect(self.borrar_fila)
        
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    
        
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
   
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def imprimir_datos_tbtabla(self):
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
    }\
    th, td {\
        border: 0.5px solid black;\
        padding: 10px;\
        text-align: left;\
    }\
    th {\
        background-color: gray;\
        color: white;\
    }\
    tr:nth-child(even) {\
        background-color: #f2f2f2;\
    }\
</style>"
            table_html += f"<th>REPORTE DE EMPLEADOS</th>"
            table_html += "<table>"
            table_html += "<tr>"
            table_html += "<th>NOMBRE</th>"
            table_html += "<th>BANCA</th>"
            table_html += "<th>SALARIO</th>"
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
            
                
            document = QTextDocument()
            
            document.setHtml(table_html)

            # Imprimir contenido del QTextDocument
            preview_dialog = QPrintPreviewDialog(printer, self.tbtabla)
            preview_dialog.paintRequested.connect(document.print_)
            preview_dialog.exec_()
        
        
    def borrar_fila(self):
        # Obtener el índice de la fila seleccionada
        indexes = self.tbtabla.selectedIndexes()
        
        if indexes:
            
            # Obtener la fila al seleccionar una celda de la tabla
            index = indexes[0]
            row = index.row()
            
            # Preguntar si el usuario está seguro de eliminar la fila
            confirmacion = QMessageBox.question(self, "¿ELIMINAR?", "¿ESTAS SEGURO QUE QUIERE ELIMINAR ESTE EMPLEADO?",
                                             QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            
            
            # Si el usuario hace clic en el botón "Sí", eliminar la fila
            if confirmacion == QMessageBox.Yes:
                # Eliminar la fila seleccionada del modelo de datos
                model = self.tbtabla.model()
                model.removeRow(row)
                QMessageBox.warning(self, "ELIMINADO", "EMPLEADO ELIMINADO.")
        else:
            QMessageBox.warning(self, "ERROR", "SELECCIONA EL EMPLEADO QUE VAS A ELIMINAR.")
            
        
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
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    def closeEvent(self, event):        
        super().closeEvent(event)    
        
        
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaDatosEmpleados()
    GUI.show()
    sys.exit(app.exec_())