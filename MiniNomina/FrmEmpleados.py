import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db
from Consultas_db import insertar_nuevo_empleados, mostrar_datos_de_empleados
from FrmDatos import VentanaDatos

class VentanaEmpleados(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Empleados.ui',self)
        
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('AGREGAR EMPLEADOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        # Esrtabece los focos a los texbox en orden hacia abajo.
        self.setTabOrder(self.txtNombre, self.txtNumbanca)
        self.setTabOrder(self.txtNumbanca, self.txtSalario)
        self.setTabOrder(self.txtSalario, self.BtnAgregar)
        self.setTabOrder(self.BtnAgregar, self.BtnSalir)
        
        # Funciones asignadas al evento click de los botones de este formulario.
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnAgregar.clicked.connect(self.guardar)
        self.BtnEditar.clicked.connect(self.abrirFrmDatos)
        
        
        
    # Funcione para llamar la ventana secundaria (Ventana de datos)
    def abrirFrmDatos(self):
        self.llamar_venana_datos = VentanaDatos()
        self.llamar_venana_datos.show()
        self.llamar_venana_datos.datos_en_tabla_empleados() 
        
    # Funcion para colocar el foco en el objeto indicado    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto txtNombre
        self.txtNombre.setFocus()
        
    # Funcion para guardar los datos de los textboxts en la base de los datos    
    def guardar(self):
        # Obtener los valores de los cuadros de texto
        Nombre = self.txtNombre.text()
        Num_banca = self.txtNumbanca.text()
        Salario = self.txtSalario.text()
        

        insertar_nuevo_empleados(Nombre, Num_banca, Salario)        
        
        
        # Limpiar los cuadros de texto
        self.txtNombre.setText("")
        self.txtNumbanca.setText("")
        self.txtSalario.setText("")
        self.txtNombre.setFocus()
        
        
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaEmpleados()
    GUI.show()
    sys.exit(app.exec_())