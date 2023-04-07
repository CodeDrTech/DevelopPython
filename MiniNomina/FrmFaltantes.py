import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5.QtCore import QDate, Qt, QDateTime, QLocale


class VentanaFaltantes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Faltantes.ui',self)
        self.setWindowTitle('REGISTRAR FALTANTES')
        self.setFixedSize(self.size())
        
        
        self.BtnSalir.clicked.connect(self.fn_Salir)        
        
     
     
    # Funcion para dotar de eventos a la ventana al cargar.    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase.
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto cmbEmpleado.
        self.cmbEmpleado.setFocus()
        
    
        
        self.txtFecha.setDisplayFormat("dd/MMMM/yyyy")  # Formato de fecha
        self.txtFecha.setDate(QDate.currentDate())    # Establecer fecha actual en txtFecha

        
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaFaltantes()
    GUI.show()
    sys.exit(app.exec_())