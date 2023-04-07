import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QPushButton, QDialog, QWidget
from Conexion_db import conectar_db

class VentanaFaltantes(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('MiniNomina/FrmDesign/Faltantes.ui',self)
        self.setWindowTitle('REGISTRAR FALTANTES')
        self.setFixedSize(self.size())
        
        
        self.BtnSalir.clicked.connect(self.fn_Salir)
        
        
    def guardar(self):
        # Obtener los valores de los cuadros de texto
        nombre = self.txtNombre.text()
        num_banca = self.txtNumbanca.text()
        salario = self.txtSalario.text()

        # Conectar a la base de datos
        conn = conectar_db()

        # Realizar la inserción en la base de datos
        conn.execute("INSERT INTO empleados (nombre, num_banca, salario) VALUES (?, ?, ?)", (nombre, num_banca, salario))
        conn.commit()

        # Cerrar la conexión
        conn.close()

        # Limpiar los cuadros de texto
        self.text_nombre.setText("")
        self.text_num_banca.setText("")
        self.text_salario.setText("")

        
    def fn_Salir(self):
        self.close()
        
if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = VentanaFaltantes()
    GUI.show()
    sys.exit(app.exec_())