import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5.QtCore import QDate, Qt, QDateTime, QLocale
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db
from Consultas_db import insertar_nuevo_faltante


class VentanaFaltantes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Faltantes.ui',self)
        
        # Configuraiones de la ventana Faltantes.
        self.setWindowTitle('REGISTRAR FALTANTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        # Esrtabece los focos a los texbox en orden hacia abajo.
        self.setTabOrder(self.cmbEmpleado, self.txtNumbanca)
        self.setTabOrder(self.txtNumbanca, self.txtAbono)
        self.setTabOrder(self.txtAbono, self.txtFaltante)
        self.setTabOrder(self.txtFaltante, self.BtnRegistrar)
        self.setTabOrder(self.BtnRegistrar, self.BtnSalir)
        
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
         # Llama a la funcion guardar        
        self.BtnRegistrar.clicked.connect(self.guardar)
     
     
    # Funcion para dotar de eventos a la ventana al cargar.    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase.
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto cmbEmpleado.
        self.cmbEmpleado.setFocus()    
        
        #Establecer la feha actual.
        self.txtFecha.setDisplayFormat("dd/MMMM/yyyy")  # Formato de fecha.
        self.txtFecha.setDate(QDate.currentDate())    # Establecer fecha actual en txtFecha.
        
        
    # Funcion para guardar los datos de los textboxts en la base de los datos    
    def guardar(self):
        # Obtener los valores de los cuadros de texto
        Fecha = self.txtFecha.date().toString("dd/MMMM/yyyy")        
        Nombre = self.cmbEmpleado.currentText()
        Num_banca = self.txtNumbanca.text()
        Abono = self.txtAbono.text()
        Faltante = self.txtFaltante.text()
        
        insertar_nuevo_faltante(Fecha, Nombre, Num_banca, Abono, Faltante)
        
        

        # Limpiar los cuadros de texto        
        self.cmbEmpleado.setCurrentText("")
        self.txtNumbanca.setText("")
        self.txtAbono.setText("")
        self.txtFaltante.setText("")
        self.cmbEmpleado.setFocus()

    # Funion para cerar la ventana llamado desde el boton Salir.    
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaFaltantes()
    GUI.show()
    sys.exit(app.exec_())