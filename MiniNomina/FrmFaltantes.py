import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5.QtCore import QDate, Qt, QDateTime, QLocale
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db


class VentanaFaltantes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Faltantes.ui',self)
        
        # propiedades de la ventana
        self.setWindowTitle('REGISTRAR FALTANTES')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        
        
        # Llama a la funcion que cierra la ventana
        self.BtnSalir.clicked.connect(self.fn_Salir)        
        
     
     
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
        Fecha = self.txtFecha.text()
        Nombre = self.cmbEmpleado.text()
        Num_banca = self.txtNumbanca.text()
        Abono = self.txtAbono.text()
        Faltante = self.txtFaltante.text()
        
        

        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO empleados (fecha ,nombre, banca, abono, faltante) VALUES (?, ?, ?)", (Fecha, Nombre, Num_banca, Abono, Faltante))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Limpiar los cuadros de texto        
        self.cmbEmpleado.setText("")
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