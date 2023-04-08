import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from PyQt5 import QtWidgets, QtGui
from Conexion_db import conectar_db
from Consultas_db import insertar_nuevo_empleados

class VentanaEmpleados(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Empleados.ui',self)
        
        # Configuraiones de la ventana Empleados.
        self.setWindowTitle('AGREGAR EMPLEADOS')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('MiniNomina/ICO/lottery.ico'))
        self.setTabOrder(self.txtNombre, self.txtNumbanca)
        self.setTabOrder(self.txtNumbanca, self.txtSalario)
        self.setTabOrder(self.txtSalario, self.BtnAgregar)
        self.setTabOrder(self.BtnAgregar, self.BtnSalir)
        
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        self.BtnAgregar.clicked.connect(self.guardar)
        
    #Funcion para colocar el foco en el objeto indicado    
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
        
        
        # Conectar a la base de datos
        #conn = conectar_db()

        # Realizar la inserción en la base de datos
        #conn.execute("INSERT INTO empleados (nombre, num_banca, salario) VALUES (?, ?, ?)", (Nombre, Num_banca, Salario))
        #conn.commit()

        # Cerrar la conexión
        #conn.close()

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