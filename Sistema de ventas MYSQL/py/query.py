from PyQt5.QtWidgets import QApplication
from PyQt5.QtSql import QSqlDatabase

app = QApplication([])  # Asegrate de crear una instancia de QApplication antes de QSqlDatabase
print(QSqlDatabase.drivers())  # Esto imprimirá los drivers disponibles

