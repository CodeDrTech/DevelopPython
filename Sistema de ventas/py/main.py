import sys
from PyQt5.QtWidgets import QApplication
from FrmLogin import VentanaLogin

if __name__ == '__main__':
    app = QApplication(sys.argv)
    login_window = VentanaLogin()
    login_window.show()
    sys.exit(app.exec_())
