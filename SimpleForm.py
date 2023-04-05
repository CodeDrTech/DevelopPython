import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox

class SimpleApp(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("appui.ui",self)
        self.BtnDesactivar.setEnabled(False)
        self.BtnActivar.clicked.connect(self.fn_activar)
        self.BtnDesactivar.clicked.connect(self.fn_desactivar)
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnMensaje.clicked.connect(self.fn_Mensaje)
        
    def fn_activar(self):
        self.BtnDesactivar.setEnabled(True)
        self.BtnActivar.setEnabled(False)
        self.Etiqueta.setText("ACTIVADO")
        
    def fn_desactivar(self):
        self.BtnDesactivar.setEnabled(False)
        self.BtnActivar.setEnabled(True)
        self.Etiqueta.setText("DESACTIVADO")
        
    def fn_Salir(self):
        self.close()
    
    def fn_Mensaje(self):
        mensaje="Solo mensaje de texto"
        QMessageBox.information(self,"Advertencia",mensaje, QMessageBox.Yes|QMessageBox.Ok)
    
    
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = SimpleApp()
    GUI.show()
    sys.exit(app.exec_())
