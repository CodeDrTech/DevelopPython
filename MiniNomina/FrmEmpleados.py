import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

class VentanaEmpleados(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Empleados.ui',self)
        self.setWindowTitle('AGREGAR EMPLEADOS')
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        
        
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaEmpleados()
    GUI.show()
    sys.exit(app.exec_())