from PyQt5.uic import loadUi
from PyQt5.QtWidgets import QMainWindow

class Ventana(QMainWindow):
    def __init__(self):
    super(Ventana,self).__init__()
    loadUi('FORMULARIO.ui',self)