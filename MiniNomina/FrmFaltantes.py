import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget, QAbstractItemView, QStyledItemDelegate
from PyQt5.QtCore import QDate, Qt, QDateTime, QLocale
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db
from FrmDatos import VentanaDatos
import locale, datetime
from Consultas_db import insertar_nuevo_faltante, mostrar_datos_totales_por_empleados


class VentanaFaltantes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Faltantes.ui',self)
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Faltantes.
        self.setWindowTitle('REGISTRAR FALTANTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/folder.png'))
        
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Esrtabece los focos a los texbox en orden hacia abajo.
        self.setTabOrder(self.cmbEmpleado, self.txtNumbanca)
        self.setTabOrder(self.txtNumbanca, self.txtAbono)
        self.setTabOrder(self.txtAbono, self.txtFaltante)
        self.setTabOrder(self.txtFaltante, self.BtnRegistrar)
        self.setTabOrder(self.BtnRegistrar, self.BtnSalir)
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
         # Llama a la funcion guardar        
        self.BtnRegistrar.clicked.connect(self.guardar)
        
        self.BtnEditar.clicked.connect(self.abrirFrmDatos)
        
        self.BtnEstado.clicked.connect(self.reporte_parcial)

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
    # Funcion para llamar la ventana secundaria (Ventana de datos) y editar las informaciones.
    def abrirFrmDatos(self):
        
        Empleado = self.cmbEmpleado.currentText()
        currency_delegate = CurrencyDelegate()
        # Validar que cmbEmpleado no esté vacío
        if not Empleado:
            
            self.llamar_venana_datos = VentanaDatos()
            self.llamar_venana_datos.show()
            self.llamar_venana_datos.datos_en_tabla_faltantes()
            
            
        else:
               
            self.llamar_tbtabla = VentanaDatos()
            self.llamar_tbtabla.show()
            tbtabla = self.llamar_tbtabla.TableView_de_FrmDatos() 
        
        
            # Crear un modelo de tabla SQL
            model = QSqlTableModel()
            model.setTable("faltantes")
    
            # Establecer el filtro por nombre
            model.setFilter(f"nombre = '{Empleado}'")
            model.setSort(0, Qt.DescendingOrder) # type: ignore
            
            # Seleccionar los datos filtrados
            model.select()           
    
            # Establecer el modelo en la tabla
            tbtabla.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            tbtabla.resizeColumnsToContents()  
            
            # Convierte a formato moneda los datos que se muesrtan en el tbtabla en la columna abonoy faltante
            tbtabla.setItemDelegateForColumn(4, currency_delegate)
            tbtabla.setItemDelegateForColumn(3, currency_delegate)  
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------ 
    # Funcion para dotar de eventos a la ventana al cargar.    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase.
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto cmbEmpleado.
        self.cmbEmpleado.setFocus()    
        self.cmbEmpleado.setCurrentText("")
        #Establecer la feha actual.
        #self.txtFecha.setDisplayFormat("d-MMMM-yyyy")  # Formato de fecha.
        self.txtFecha.setDate(QDate.currentDate())   # Establecer fecha actual en txtFecha.
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # Funcion para guardar los datos de los textboxts en la base de los datos    
    def guardar(self):
        # Obtener los valores de los cuadros de texto
        Fecha = self.txtFecha.date().toString("yyyy-MM-dd")        
        Nombre = self.cmbEmpleado.currentText()
        Num_banca = self.txtNumbanca.text()
        Abono = self.txtAbono.text()
        Faltante = self.txtFaltante.text()
        
        if not Fecha:
            QMessageBox.warning(None, "ERROR", "REVISA EL CAMPO FECHA.") # type: ignore
            return
        
        if not Nombre or Nombre.isdigit():
            QMessageBox.warning(None, "ERROR", "REVISA EL CAMPO NOMBRE.") # type: ignore
            return 
        
        if not Num_banca or not Num_banca.isdigit():
            QMessageBox.warning(None, "ERROR", "REVISA EL CAMPO BANCA #.") # type: ignore
            return
        
        if not Faltante and not Abono.isdigit():
            QMessageBox.warning(None, "ERROR", "REVISA EL CAMPO ABONO O FALTANTE.") # type: ignore
            return
        
        if not Abono and not Faltante.isdigit():
            QMessageBox.warning(None, "ERROR", "REVISA EL CAMPO ABONO O FALTANTE.") # type: ignore
            return
        
        insertar_nuevo_faltante(Fecha, Nombre, Num_banca, Abono, Faltante)
        
        

        # Limpiar los cuadros de texto        
        self.cmbEmpleado.setCurrentText("")
        self.txtNumbanca.setText("")
        self.txtAbono.setText("")
        self.txtFaltante.setText("")
        self.cmbEmpleado.setFocus()
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------
    def datos_totales_por_empleados(self):
        self.llamar_tbtabla = VentanaDatos()
        self.llamar_tbtabla.show()
        tbtabla = self.llamar_tbtabla.TableView_de_FrmDatos()
        mostrar_datos_totales_por_empleados(tbtabla)
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    def reporte_parcial(self):
        Empleado = self.cmbEmpleado.currentText()
        currency_delegate = CurrencyDelegate()
        self.llamar_tbtabla = VentanaDatos()
        self.llamar_tbtabla.show()
        tbtabla = self.llamar_tbtabla.TableView_de_FrmDatos()
        self.llamar_tbtabla.DeshabilitaBtnEliminar()
           
        if not Empleado:
            query = QSqlQuery()
            query.exec_("SELECT FECHA, NOMBRE, BANCA, ABONO, FALTANTE \
                    FROM faltantes \
                    UNION ALL \
                    SELECT 'TOTAL', '', '', SUM(ABONO), SUM(FALTANTE) \
                    FROM faltantes \
                    GROUP BY 'TOTAL'")

   
            # Crear un modelo de tabla SQL
            model = QSqlTableModel()
    
            model.setQuery(query)   
    
            # Establecer el modelo en la tabla
            tbtabla.setModel(model)

        
            
            tbtabla.setItemDelegateForColumn(4, currency_delegate)
            tbtabla.setItemDelegateForColumn(3, currency_delegate)
        
            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            tbtabla.resizeColumnsToContents()
            tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers) 
        else:
            query = QSqlQuery()
            query.exec_(f"SELECT FECHA, NOMBRE, BANCA, ABONO, FALTANTE \
                    FROM faltantes WHERE NOMBRE = '{Empleado}' \
                    UNION ALL \
                    SELECT 'TOTAL', '', '', SUM(ABONO), SUM(FALTANTE) \
                    FROM faltantes WHERE NOMBRE = '{Empleado}' \
                    GROUP BY 'TOTAL'")

   
            # Crear un modelo de tabla SQL
            model = QSqlTableModel()
    
            model.setQuery(query)   
    
            # Establecer el modelo en la tabla
            tbtabla.setModel(model)

        
        
            tbtabla.setItemDelegateForColumn(4, currency_delegate)
            tbtabla.setItemDelegateForColumn(3, currency_delegate)
        
            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            tbtabla.resizeColumnsToContents() 
            tbtabla.setEditTriggers(QAbstractItemView.NoEditTriggers)
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------       
    # Funion para cerar la ventana llamado desde el boton Salir.    
    def fn_Salir(self):
        self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
class CurrencyDelegate(QStyledItemDelegate):
    def displayText(self, value, locale):
        try:
            # Convierte el valor a un formato de moneda
            return locale.toCurrencyString(float(value))
        except ValueError:
            # Si no se puede convertir a un formato de moneda, devuelve el valor original
            return value
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaFaltantes()
    GUI.show()
    sys.exit(app.exec_())