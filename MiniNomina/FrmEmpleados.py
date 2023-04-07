import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from Conexion_db import conectar_db

class VentanaEmpleados(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Empleados.ui',self)
        self.setWindowTitle('AGREGAR EMPLEADOS')
        self.setFixedSize(self.size())
        
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnAgregar.clicked.connect(self.guardar)
        
    #Funcion para colocar el foco en el objeto indicado    
    def showEvent(self, event):
        # Llamar al método showEvent() de la superclase
        super().showEvent(event)

        # Establecer el foco en el cuadro de texto txtNombre
        self.txtNombre.setFocus()
        
        
    def guardar(self):
        # Obtener los valores de los cuadros de texto
        Nombre = self.txtNombre.text()
        Num_banca = self.txtNumbanca.text()
        Salario = self.txtSalario.text()
        

        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO empleados (nombre, num_banca, salario) VALUES (?, ?, ?)", (Nombre, Num_banca, Salario))
        conn.commit()

        # Cerrar la conexión
        conn.close()

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