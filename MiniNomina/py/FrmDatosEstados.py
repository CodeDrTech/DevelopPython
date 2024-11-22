import sys
import locale
import os
import textwrap
from datetime import datetime

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QDialog, QMessageBox, QStyledItemDelegate, QAbstractItemView
from PyQt5 import QtGui
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextDocument
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter, QPrintPreviewDialog
from PyQt5.QtCore import Qt, QDate
from Consultas_db import mostrar_datos_de_empleados
from PyQt5.QtSql import QSqlTableModel, QSqlQuery

import win32api

from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus import Table, TableStyle
from reportlab.lib import colors






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
        uic.loadUi('MiniNomina/ui/DatosEstados.ui',self)
        
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('ESTADOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/png/folder.png'))
        
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        self.BtnImprimir.clicked.connect(self.imprimir_pdf)
        
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
            column_data.append(model.data(model.index(i, 1)))
        
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
            query.exec_(f"SELECT '', NOMBRE, BANCA, SUM(ABONO) AS ABONO, SUM(FALTANTE) AS FALTANTE\
            FROM faltantes\
            WHERE FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'\
            GROUP BY NOMBRE\
            UNION ALL\
            SELECT NULL AS FECHA, NULL AS NOMBRE, NULL AS BANCA, NULL AS ABONO, NULL AS FALTANTE\
            UNION ALL\
            SELECT NULL AS FECHA, NULL AS NOMBRE, NULL AS BANCA, NULL AS ABONO, NULL AS FALTANTE\
            UNION ALL\
            SELECT NULL AS FECHA, '*faltante DE TRANSACCIONES*' AS NOMBRE, NULL AS BANCA, NULL AS ABONO, NULL AS FALTANTE\
            UNION ALL\
            SELECT 'FECHA' AS FECHA, 'NOMBRE' AS NOMBRE, 'BANCA' AS BANCA, 'ABONO' AS ABONO, 'FALTANTE' AS FALTANTE\
            UNION ALL\
            SELECT FECHA, NOMBRE, BANCA, ABONO, FALTANTE\
            FROM faltantes\
            WHERE FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'\
            UNION ALL\
            SELECT '', '', 'TOTAL', SUM(ABONO), SUM(FALTANTE)\
            FROM faltantes\
            WHERE FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}';")
            
   
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
                    SELECT '', '', 'TOTAL', SUM(ABONO), SUM(FALTANTE) \
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
    def imprimir_pdf(self):
        
            
            # Obtiene la fecha actual para usar en el pdf
            fecha = QDate.currentDate()
            fecha_formato = fecha.toString("dd-MMMM-yyyy")

            FechaInicio = self.txtFechaInicio.date().toString("d-MMMM-yyyy")
            FechaFinal = self.txtFechaFinal.date().toString("d-MMMM-yyyy")
            Empleado = self.cmbEmpleado.currentText()
            
            if Empleado:
                try:
                    
                    # Con el parametro row como int se obtienen todos los datos de la fila seleccionada, datos 
                    # que seran usados para la creacion del pdf.
                    #self.obtener_id_fila_cotizacion(row) 
                    
                    
                    # Preguntar si el usuario está seguro de convertir la cotizacion seleccionada
                    confirmacion = QMessageBox.question(self, "MENSAJE", "¿ESTA SEGURO QUE QUIERE CONTINUAR?",
                                                        QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                        
                        
                    # Si el usuario hace clic en el botón "Sí", convierte la cotizacion en pdf
                    if confirmacion == QMessageBox.Yes:
                        
                        c = canvas.Canvas(f"MiniNomina/pdf/reporte {fecha_formato}.pdf", pagesize=letter)

                        # Agregar el logo de la empresa
                        c.drawImage("MiniNomina/png/Logo.png", 400, 700, width=150, height=75)

                        # Datos de la empresa
                        data = [
                            ["Banca Elix la Fortuna."],
                            ["Ave. Ind. km 12 1/2 # 23."],
                            ["809-534-2323"]
                        ]

                        table = Table(data)

                        # Establecer el estilo de la tabla para datos de la empresa
                        style = TableStyle([
                            ('BACKGROUND', (0,0), (-1,-1), colors.lightgrey),
                            ('TEXTCOLOR', (0,0), (-1,-1), colors.black),

                            ('ALIGN', (0,0), (-1,-1), 'CENTER'),
                            ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
                            ('FONTSIZE', (0,0), (-1,-1), 12),

                            ('BOTTOMPADDING', (0,0), (-1,-1), 10),
                            ('BACKGROUND', (0,0), (-1,0), colors.lightgrey),
                            ('GRID', (0,0), (-1,-1), 1, colors.black)
                        ])
                        table.setStyle(style)

                        # Agregar la tabla de datos de la empresa al canvas.
                        table.wrapOn(c, 50, 750)
                        table.drawOn(c, 50, 700)
                        
                        # Totales, subtotales, impuestos, etc.
                        suma_faltantes = self.obtener_suma_faltantes_por_fehca()
                        suma_abono = self.obtener_suma_abonos_por_fehca()

                        # No. Cotización y fecha
                        c.setFont("Helvetica", 15)
                        c.drawString(390,680,"Abonos: " + "$ " + str(suma_abono))
                        c.setFont("Helvetica", 15)
                        c.drawString(390,660,"Faltantes: " + "$ " + str(suma_faltantes))

                        # Datos del cliente
                        c.setFont("Helvetica-Bold", 15)
                        c.drawString(50,680,"Empleada: " + f"{Empleado}")
                        c.setFont("Helvetica", 10)
                        c.drawString(50,660,"Desde el " + f"{FechaInicio}" + " Hasta el " + f"{FechaFinal}")
                        
                        # Dibujar una línea debajo de los datos de la empresa y logo.
                        c.line(50, 695, 550, 695)

                        # Dibujar una línea debajo de los datos del cliente
                        c.line(50, 650, 550, 650)
                        
                        # Cabecera de los datos de los artículos
                        c.setFont("Helvetica-Bold", 12)
                        c.drawString(50, 630, "FECHA.") 
                        c.drawString(150, 630, "BANCA")                 
                        c.drawString(220, 630, "NOMBRE")
                        c.drawString(400, 630, "ABONO")
                        c.drawString(485, 630, "FALTANTE")

                        # Datos de los artículos.
                        faltantes = self.obtener_faltantes()
                        
                        
                        
                        y = 610
                        for faltante in faltantes:
                            c.setFont("Helvetica", 10)
                            
                            # Establecer la configuración regional a español
                            locale.setlocale(locale.LC_TIME, 'es_ES.UTF-8')
                            
                            # Convertir la cadena a un objeto datetime
                            fecha_objeto = datetime.strptime(faltante['FECHA'], "%Y-%m-%d")

                            # Formatear el objeto datetime como cadena en el nuevo formato
                            fecha_faltante = fecha_objeto.strftime("%d-%B-%Y")
                            
                            c.drawString(50, y, fecha_faltante)
                            c.drawString(150, y, str(faltante['BANCA']))

                            # Guardar la posición "y" (up/down) antes de dibujar el nombre del artículo
                            # esta posicion la uso para que si el nombre del articulo tiene varias lineas
                            # las demas columnas queden alineadas con la primera linea del nombre de articulo.
                            alinear_columnas = y

                            # Obtener el nombre del artículo y dividirlo en varias líneas si es demasiado largo
                            nombre_empleado = str(faltante['NOMBRE']) # obtengo el nombre del articulo en la variable nombre_empleado
                            lineas_nombre_empleado = textwrap.wrap(nombre_empleado, width=30)  # Ajusta el ancho a un espacio de 30 caracteres.

                            # Revisa cada nombre de articulo si alguno pasa de 30 caracteres crea un salto de linea.
                            for linea in lineas_nombre_empleado:
                                c.drawString(220, y, linea)
                                y -= 15
                                
                                
                            
                            c.drawString(400, alinear_columnas, "$ " + str(faltante['ABONO']) if str(faltante['ABONO']) else "$ 0.00")
                            c.drawString(485, alinear_columnas, "$ " + str(faltante['FALTANTE']) if str(faltante['FALTANTE']) else "$ 0.00")
                            y -= 15

                            # Si los articulos llegan a la línea 40, se crea una nueva página
                            # para seguir imprimiendo en ella
                            if y <= 30:
                                c.showPage()
                                y = 750  # Posición inicial en "y" (up/down) de la nueva pagina creada.
                        c.save()

                        # Ruta completa del archivo PDF para ser usada para imprimir el pdf creado.
                        pdf_file_name = os.path.abspath(f"MiniNomina/pdf/reporte {fecha_formato}.pdf")

                        # Abrir el cuadro de diálogo de impresión de Windows, open crea y abre el pdf, print
                        # imprime el archivo por la impresora predeterminada.
                        
                        win32api.ShellExecute(0, "open", pdf_file_name, None, ".", 0) # type: ignore
                        
                        #win32api.ShellExecute(0, "print", pdf_file_name, None, ".", 0) # type: ignore

                        QMessageBox.warning(self, "MENSAJE", "HECHO SATISCAFTORIAMENTE")
                except Exception as e:
                    # Manejar otros errores, mostrar un mensaje de error o realizar otra acción necesaria
                    mensaje_error = QMessageBox()
                    mensaje_error.setIcon(QMessageBox.Critical)
                    mensaje_error.setWindowTitle("Llamar al administrador")
                    mensaje_error.setText(f"Error al intentar imprimir: {str(e)}")
                    mensaje_error.exec_()
                    
            else:
                QMessageBox.warning(self, "ERROR", "SELECCIONA LA COTIZACION PARA CONTINUAR.")

    
    def obtener_faltantes(self):
        Empleado = self.cmbEmpleado.currentText()
        FechaInicio = self.txtFechaInicio.date().toString("yyyy-MM-dd")
        FechaFinal = self.txtFechaFinal.date().toString("yyyy-MM-dd")
        query = QSqlQuery()
        query.exec_(f"SELECT * FROM faltantes WHERE NOMBRE LIKE '%{Empleado}%' AND FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'")

        faltante = []
        while query.next():
            faltante.append({
                    'FECHA': query.value('FECHA'),
                    'BANCA': query.value('BANCA'),
                    'NOMBRE': query.value('NOMBRE'),
                    'ABONO': query.value('ABONO'),
                    'FALTANTE': query.value('FALTANTE')
                })

        return faltante
    
    def obtener_suma_faltantes_por_fehca(self):
        Empleado = self.cmbEmpleado.currentText()
        FechaInicio = self.txtFechaInicio.date().toString("yyyy-MM-dd")
        FechaFinal = self.txtFechaFinal.date().toString("yyyy-MM-dd")
        query = QSqlQuery()
        query.exec_(f"SELECT sum(FALTANTE) FROM faltantes WHERE NOMBRE LIKE '%{Empleado}%' AND FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'")

        # Verificar si la consulta se ejecutó correctamente
        if query.next():
            # Obtener el valor de la suma (si es nulo, devolver 0)
            suma_faltantes = query.value(0) or 0.0
            return suma_faltantes
        else:
            # En caso de error o si no hay resultados, devolver 0
            return 0.0

    def obtener_suma_abonos_por_fehca(self):
        Empleado = self.cmbEmpleado.currentText()
        FechaInicio = self.txtFechaInicio.date().toString("yyyy-MM-dd")
        FechaFinal = self.txtFechaFinal.date().toString("yyyy-MM-dd")
        query = QSqlQuery()
        query.exec_(f"SELECT sum(ABONO) FROM faltantes WHERE NOMBRE LIKE '%{Empleado}%' AND FECHA BETWEEN '{FechaInicio}' AND '{FechaFinal}'")

        # Verificar si la consulta se ejecutó correctamente
        if query.next():
            # Obtener el valor de la suma (si es nulo, devolver 0)
            suma_abono = query.value(0) or 0.0
            return suma_abono
        else:
            # En caso de error o si no hay resultados, devolver 0
            return 0.0
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
        padding: 05px;\
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
            
            table_html += f"<th>REPORTE DE ESTADOS</th>" 
            table_html += "<table>"
            table_html += "<tr>"
            table_html += "<th>FECHA</th>"
            table_html += "<th>NOMBRE</th>"
            table_html += "<th>BANCA</th>"
            table_html += "<th>ABONO</th>"
            table_html += "<th>FALTANTE</th>"
            table_html += "</tr>"
            
            table_model = self.tbtabla.model()
            row_count = table_model.rowCount()
            column_count = table_model.columnCount()
            
            for row in range(row_count):
                
                table_html += "<tr>"
            
                for column in range(column_count):
                
                    cell_value = table_model.data(table_model.index(row, column), Qt.DisplayRole) # type: ignore
                    if column == 0:  # Si es la primera columna (la de la fecha)
                        date_str = table_model.data(table_model.index(row, column), Qt.DisplayRole)  # type: ignore # Obtener el valor de la celda
                        date_obj = QDate.fromString(date_str, "yyyy-MM-dd")  # Convertir en objeto QDate
                        cell_value = date_obj.toString("d-MMMM-yyyy")  # Convertir en string en el formato deseado
                             
                    if isinstance(cell_value, (float)):
                        cell_value = locale.currency(cell_value, symbol=True, grouping=True)
                    table_html += f"<td>{cell_value}</td>"
                                       
                table_html += "</tr>"
                
            table_html += f"<th>REPORTE DESDE EL {FechaInicio}  HASTA EL {FechaFinal} </th>"    
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