from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow
import sys

def window():
    app = QApplication(sys.argv)
    win = QMainWindow()
    win.setGeometry(200, 200, 300, 300)
    win.setWindowTitle("Titulo")
    
    win.show
    sys.exit(app.exec_())
    
window()


#Simple comentario luego de sincronisar github.
#Otro cambio realizado a las 2:50 PM