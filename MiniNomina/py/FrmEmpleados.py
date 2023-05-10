import sys
import re
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5 import QtWidgets, QtGui
from Consultas_db import insertar_nuevo_empleados
from FrmDatosEmpleados import VentanaDatosEmpleados

class VentanaEmpleados(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/ui/Empleados.ui',self)
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('AGREGAR EMPLEADOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/png/folder.png'))
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Esrtabece los focos a los texbox en orden hacia abajo.
        self.setTabOrder(self.txtNombre, self.txtNumbanca)
        self.setTabOrder(self.txtNumbanca, self.txtSalario)
        self.setTabOrder(self.txtSalario, self.BtnAgregar)
        self.setTabOrder(self.BtnAgregar, self.BtnSalir)
        
        #------------------------------------------------------------------------------------------------------
        #------------------------------------------------------------------------------------------------------
        # Funciones asignadas al evento click de los botones de este formulario.
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnAgregar.clicked.connect(self.guardar)
        self.BtnEditar.clicked.connect(self.abrirFrmDatos)
        
        
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # Funcione para llamar la ventana secundaria (Ventana de datos.)
    def abrirFrmDatos(self):
        self.llamar_venana_datos = VentanaDatosEmpleados()
        self.llamar_venana_datos.show()
        self.llamar_venana_datos.datos_en_tabla_empleados()
        
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------        
    # Funcion para colocar el foco en el objeto indicado    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto txtNombre
        self.txtNombre.setFocus()
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # Funcion para guardar los datos de los textboxts en la base de los datos    
    def guardar(self):   
        
        # Obtener los valores de los cuadros de texto
        Nombre = self.txtNombre.text().upper()
        Num_banca = self.txtNumbanca.text()
        Salario = self.txtSalario.text()
        
        # Validar que los campos no estén vacíos
        #if not Nombre or not Num_banca or not Salario:
            #QMessageBox.warning(None, "ERROR", "DEBE COMPLETAR LOS CAMPOS QUE SON OBLIGATORIOS.") # type: ignore
            #return
            
        if not Nombre or Nombre.isdigit():
            QMessageBox.warning(None, "ERROR", "REVISA EL CAMPO NOMBRE.") # type: ignore
            return
        
        if not Num_banca or not Num_banca.isdigit():
            QMessageBox.warning(None, "ERROR", "REVISA EL CAMPO BANCA #.") # type: ignore
            return
        
        if not Salario or not Salario.isdigit():
            QMessageBox.warning(None, "ERROR", "REVISA EL CAMPO SALARIO.") # type: ignore
            return
            
        insertar_nuevo_empleados(Nombre, Num_banca, Salario)        
        
        
        # Limpiar los cuadros de texto
        self.txtNombre.setText("")
        self.txtNumbanca.setText("")
        self.txtSalario.setText("")
        self.txtNombre.setFocus()
    
    #------------------------------------------------------------------------------------------------------
    #------------------------------------------------------------------------------------------------------    
    # funcion salir llamada desde el boton BtnSalir.    
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaEmpleados()
    GUI.show()
    sys.exit(app.exec_())