import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QHeaderView, QMessageBox, QStyledItemDelegate, QAbstractItemView, QDialog, QPushButton, QTreeWidget
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtGui import QPainter, QPageLayout, QPageSize, QFont, QTransform, QStandardItemModel, QStandardItem, QTextDocument
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

class VentanaDatosReportes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/DatosFiltrar.ui',self)
        
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('REPORTES')
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
            query.exec_(f"SELECT e.NOMBRE,\
            COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0) AS FALTANTES,\
            COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0) AS ABONOS,\
            e.SALARIO - COALESCE((SELECT SUM(f.FALTANTE) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0)\
            + COALESCE((SELECT SUM(f.ABONO) FROM faltantes f WHERE f.NOMBRE = e.NOMBRE AND f.FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'), 0) AS SALARIO_NETO\
            FROM empleados e")

   
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
        
        class visualizarImprimirExportar(QDialog):
            def __init__(self, parent=None):
                super(visualizarImprimirExportar, self).__init__()
        
            self.setWindowTitle("Visualizar, imprimir y exportar datos a PDF con PyQt5")
            self.setWindowIcon(QIcon("Qt.png"))
            self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.MSWindowsFixedSizeDialogHint)
            self.setFixedSize(612, 408)

            self.initUI()

            def initUI(self):
                self.documento = QTextDocument()

            # =================== WIDGETS QPUSHBUTTON ==================

                buttonBuscar = QPushButton("Buscar usuarios", self)
                buttonBuscar.setFixedSize(426, 26)
                buttonBuscar.move(20, 20)

                buttonLimpiar = QPushButton("Limpiar tabla", self)
                buttonLimpiar.setFixedSize(140, 26)
                buttonLimpiar.move(452, 20)

            # =================== WIDGET QTREEWIDGET ===================

                self.treeWidgetUsuarios = QTreeWidget(self)

                self.treeWidgetUsuarios.setFont(QFont(self.treeWidgetUsuarios.font().family(), 10, False))
                self.treeWidgetUsuarios.setRootIsDecorated(False)
                self.treeWidgetUsuarios.setHeaderLabels(("D.N.I", "NOMBRE", "APELLIDO", "FECHA DE NACIMIENTO"))

                self.model = self.treeWidgetUsuarios.model()

                for indice, ancho in enumerate((110, 150, 150, 160), start=0):
                    self.model.setHeaderData(indice, Qt.Horizontal, Qt.AlignCenter, Qt.TextAlignmentRole)
                    self.treeWidgetUsuarios.setColumnWidth(indice, ancho)
        
                self.treeWidgetUsuarios.setAlternatingRowColors(True)

                self.treeWidgetUsuarios.setFixedSize(572, 300)
                self.treeWidgetUsuarios.move(20, 56)

            # =================== WIDGETS QPUSHBUTTON ==================

                buttonVistaPrevia = QPushButton("Vista previa", self)
                buttonVistaPrevia.setFixedSize(140, 26)
                buttonVistaPrevia.move(156, 364)

                buttonImprimir = QPushButton("Imprimir", self)
                buttonImprimir.setFixedSize(140, 26)
                buttonImprimir.move(304, 364)

                buttonExportarPDF = QPushButton("Exportar a PDF", self)
                buttonExportarPDF.setFixedSize(140, 26)
                buttonExportarPDF.move(452, 364)

            # =================== EVENTOS QPUSHBUTTON ==================

                buttonBuscar.clicked.connect(self.Buscar)
                buttonLimpiar.clicked.connect(self.limpiarTabla)
        
                buttonVistaPrevia.clicked.connect(self.vistaPrevia)
                buttonImprimir.clicked.connect(self.Imprimir)
                buttonExportarPDF.clicked.connect(self.exportarPDF)

  # ======================= FUNCIONES ============================

            def Buscar(self):
                conexionDB = connect("DB_USUARIOS.db")
                cursor = conexionDB.cursor()

                cursor.execute("SELECT DNI, NOMBRE, APELLIDO, FECHA_NACIMIENTO FROM USUARIOS")
                datosDB = cursor.fetchall()

                conexionDB.close()

                if datosDB:
                    self.documento.clear()
                    self.treeWidgetUsuarios.clear()

                    datos = ""
                    item_widget = []
                    for dato in datosDB:
                        datos += "<tr><td>%s</td><td>%s</td><td>%s</td><td>%s</td></tr>" %dato
                        item_widget.append(QTreeWidgetItem((str(dato[0]), dato[1], dato[2], dato[3])))

                        reporteHtml = """
<!DOCTYPE html>
<html>
<head>
<meta charset="UTF-8">
<style>
h3 {
    font-family: Helvetica-Bold;
    text-align: center;
   }
table {
       font-family: arial, sans-serif;
       border-collapse: collapse;
       width: 100%;
      }
td {
    text-align: left;
    padding-top: 4px;
    padding-right: 6px;
    padding-bottom: 2px;
    padding-left: 6px;
   }
th {
    text-align: left;
    padding: 4px;
    background-color: black;
    color: white;
   }
tr:nth-child(even) {
                    background-color: #dddddd;
                   }
</style>
</head>
<body>
<h3>LISTADO DE USUARIOS<br/></h3>
<table align="left" width="100%" cellspacing="0">
  <tr>
    <th>D.N.I</th>
    <th>NOMBRE</th>
    <th>APELLIDO</th>
    <th>FECHA DE NACIMIENTO</th>
  </tr>
  [DATOS]
</table>
</body>
</html>
""".replace("[DATOS]", datos)

            datos = QByteArray()
            datos.append(str(reporteHtml))
            codec = QTextCodec.codecForHtml(datos)
            unistr = codec.toUnicode(datos)

            if Qt.mightBeRichText(unistr):
                self.documento.setHtml(unistr)
            else:
                self.documento.setPlainText(unistr)

            self.treeWidgetUsuarios.addTopLevelItems(item_widget)
            else:
                QMessageBox.information(self, "Buscar usuarios", "No se encontraron resultados.      ",
                                    QMessageBox.Ok)

            def limpiarTabla(self):
                self.documento.clear()
                self.treeWidgetUsuarios.clear()

            def vistaPrevia(self):
                if not self.documento.isEmpty():
                    impresion = QPrinter(QPrinter.HighResolution)
            
                    vista = QPrintPreviewDialog(impresion, self)
                    vista.setWindowTitle("Vista previa")
                    vista.setWindowFlags(Qt.Window)
                    vista.resize(800, 600)

                    exportarPDF = vista.findChildren(QToolBar)
                    exportarPDF[0].addAction(QIcon("exportarPDF.png"), "Exportar a PDF", self.exportarPDF)
            
                    vista.paintRequested.connect(self.vistaPreviaImpresion)
                    vista.exec_()
                else:
                    QMessageBox.critical(self, "Vista previa", "No hay datos para visualizar.   ",
                                 QMessageBox.Ok)

            def vistaPreviaImpresion(self, impresion):
                self.documento.print_(impresion)

            def Imprimir(self):
                if not self.documento.isEmpty():
                    impresion = QPrinter(QPrinter.HighResolution)
            
                    dlg = QPrintDialog(impresion, self)
                    dlg.setWindowTitle("Imprimir documento")

                    if dlg.exec_() == QPrintDialog.Accepted:
                        self.documento.print_(impresion)

                    del dlg
                else:
                    QMessageBox.critical(self, "Imprimir", "No hay datos para imprimir.   ",
                                 QMessageBox.Ok)

            def exportarPDF(self):
                if not self.documento.isEmpty():
                    nombreArchivo, _ = QFileDialog.getSaveFileName(self, "Exportar a PDF", "Listado de usuarios",
                                                           "Archivos PDF (*.pdf);;All Files (*)",
                                                           options=QFileDialog.Options())

                    if nombreArchivo:
                        # if QFileInfo(nombreArchivo).suffix():
                        #     nombreArchivo += ".pdf"

                        impresion = QPrinter(QPrinter.HighResolution)
                        impresion.setOutputFormat(QPrinter.PdfFormat)
                        impresion.setOutputFileName(nombreArchivo)
                        self.documento.print_(impresion)

                        QMessageBox.information(self, "Exportar a PDF", "Datos exportados con éxito.   ",
                                        QMessageBox.Ok)
                else:
                    QMessageBox.critical(self, "Exportar a PDF", "No hay datos para exportar.   ",
                                 QMessageBox.Ok)


# ================================================================   

        if __name__ == '__main__':

            import sys

            aplicacion = QApplication(sys.argv)

            qt_traductor = QTranslator()
            qt_traductor.load("qtbase_" + QLocale.system().name(),
                       QLibraryInfo.location(QLibraryInfo.TranslationsPath))
            aplicacion.installTranslator(qt_traductor)

            fuente = QFont()
            fuente.setPointSize(10)
            fuente.setFamily("Bahnschrift Light")

            aplicacion.setFont(fuente)

            ventana = visualizarImprimirExportar()
            ventana.show()

            sys.exit(aplicacion.exec_())
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
        
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