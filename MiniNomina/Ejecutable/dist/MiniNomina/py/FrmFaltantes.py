import sys
from PyQt5 import uic, QtCore
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QStyledItemDelegate
from PyQt5.QtCore import QDate
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5 import QtGui
from FrmDatosFaltantes import VentanaDatosFaltantes
from FrmDatosEstados import VentanaDatosEstados
from Consultas_db import insertar_nuevo_faltante, mostrar_datos_totales_por_empleados


class VentanaFaltantes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/ui/Faltantes.ui',self)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Faltantes.
        self.setWindowTitle('REGISTRAR FALTANTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/png/folder.png'))
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Esrtabece los focos a los texbox en orden de arriba hacia abajo.
        self.setTabOrder(self.cmbEmpleado, self.cmbBanca)
        self.setTabOrder(self.cmbBanca, self.txtAbono)
        self.setTabOrder(self.txtAbono, self.txtFaltante)
        self.setTabOrder(self.txtFaltante, self.BtnRegistrar)
        self.setTabOrder(self.BtnRegistrar, self.BtnSalir)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        # Botonoes del formulario y sus funciones.
        self.BtnSalir.clicked.connect(self.fn_Salir)      
        self.BtnRegistrar.clicked.connect(self.guardar)        
        self.BtnEditar.clicked.connect(self.abrirFrmDatos)        
        self.BtnEstado.clicked.connect(self.reporte_parcial)
        
        # Evento que inserta el # de banca cuando seleccionas un nombre del ComboBox.
        self.cmbEmpleado.currentIndexChanged.connect(
            lambda i: self.actualizar_cmbBanca(self.cmbEmpleado.currentText()))
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
        
        # Obtiene los datos de la columna Nombre de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('empleados')
        model.select()
        columna_empleados = []
        for i in range(model.rowCount()):
            columna_empleados.append(model.data(model.index(i, 0)))
        
        # Cargar los datos de la columna Nombre de la tabla empleados en el QComboBox asignado.
        combo_model = QStandardItemModel()
        for item in columna_empleados:
             combo_model.appendRow(QStandardItem(str(item)))
        self.cmbEmpleado.setModel(combo_model)
        
        
        # Obtiene los datos de la columna Banca de la tabla empleados.
        model = QSqlTableModel()
        model.setTable('empleados')
        model.select()
        columna_banca = []
        for i in range(model.rowCount()):
           columna_banca.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Banca de la tabla empleados en el QComboBox asignado.
        combo_model2 = QStandardItemModel()
        for item in columna_banca:
           combo_model2.appendRow(QStandardItem(str(item)))
        self.cmbBanca.setModel(combo_model2)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Obtiene el nombre de empleado correspondiente al numero de banca seleccionado en el ComboBox. 
    def actualizar_cmbEmpleados(self, banca):
        model = QSqlTableModel()
        model.setTable('empleados')
        model.setFilter(f"banca='{banca}'")
        model.select()
        columna_banca2 = []
        for i in range(model.rowCount()):
            columna_banca2.append(model.data(model.index(i, 0)))

        combo_model3 = QStandardItemModel()
        for item in columna_banca2:
            combo_model3.appendRow(QStandardItem(str(item)))
        self.cmbEmpleado.setModel(combo_model3)
        
    # Obtiene el numero de banca correspondiente al nombre de empleado seleccionado en el ComboBox.    
    def actualizar_cmbBanca(self, Empleado):
        model = QSqlTableModel()
        model.setTable('empleados')
        model.setFilter(f"Nombre='{Empleado}'")
        model.select()
        columna_empleados2 = []
        for i in range(model.rowCount()):
            columna_empleados2.append(model.data(model.index(i, 1)))

        combo_model4 = QStandardItemModel()
        for item in columna_empleados2:
            combo_model4.appendRow(QStandardItem(str(item)))
        self.cmbBanca.setModel(combo_model4)        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
    # Funcion para llamar la ventana secundaria (Ventana de datos) y editar las informaciones.
    def abrirFrmDatos(self):        
            
        self.llamar_venana_datos = VentanaDatosFaltantes()
        self.llamar_venana_datos.show()
        self.llamar_venana_datos.Filtro_por_fecha()
                
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 
    # Funcion para dotar de eventos a la ventana al cargar.    
    def showEvent(self, event):
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto cmbEmpleado y limpia los demas.
        self.cmbEmpleado.setFocus()    
        self.cmbEmpleado.setCurrentText("")
        self.cmbBanca.setCurrentText("")
        
        #Establecer la feha actual.
        self.txtFecha.setDisplayFormat("d-MMMM-yyyy")# Formato de fecha.
        self.txtFecha.setDate(QDate.currentDate())# Establecer fecha actual en txtFecha.
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
    # Funcion para guardar los datos de los textboxts en la base de los datos    
    def guardar(self):
        # Obtener los valores de los cuadros de texto
        Fecha = self.txtFecha.date().toString("yyyy-MM-dd")     
        Nombre = self.cmbEmpleado.currentText()
        Num_banca = self.cmbBanca.currentText()
        Abono = self.txtAbono.text()
        Faltante = self.txtFaltante.text()
        
        # Almacena la fecha actual en la variable Hoy
        Hoy = QDate.currentDate()
        
        # Condiciones que deben cumplirse antes de ingresar los datos a la base de datos.
        if Fecha > Hoy.toString("yyyy-MM-dd"):
            QMessageBox.warning(None, "ERROR", "ESTAS INGRESANDO UNA FECHA FUTURA.") # type: ignore
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
        # Pase de parametros a la funcion insertar_nuevo_faltante del modulo Consultas_db
        insertar_nuevo_faltante(Fecha, Nombre, Num_banca, Abono, Faltante)
        
        

        # Limpiar los cuadros de texto y mantiene la fecha del sistema en el txtFecha.        
        self.cmbEmpleado.setCurrentText("")
        self.cmbBanca.setCurrentText("")
        self.txtAbono.setText("")
        self.txtFaltante.setText("")
        self.txtFecha.setDate(QDate.currentDate()) 
        self.cmbEmpleado.setFocus()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Asignacion del QTableViw tbtabla a la funcion mostrar_datos_totales_por_empleados d Consulta_db.
    def datos_totales_por_empleados(self):
        self.llamar_tbtabla = VentanaDatosFaltantes()
        self.llamar_tbtabla.show()
        tbtabla = self.llamar_tbtabla.TableView_de_FrmDatos()
        mostrar_datos_totales_por_empleados(tbtabla)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Llamma al reporte "estados" configurados en la clase VentanaDatosEstados   
    def reporte_parcial(self):
        self.llamar_tbtabla = VentanaDatosEstados()
        self.llamar_tbtabla.show()           
        self.llamar_tbtabla.Filtro_por_fecha()
               
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------       
    # Funion para cerar la ventana llamado desde el boton Salir.    
    def fn_Salir(self):
        self.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Configura los numero float de tbtabla y les da formato de moneda al visualizarse.
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