from PyQt5.QtWidgets import QApplication, QDateEdit
from PyQt5.QtCore import QDate

app = QApplication([])

date_edit = QDateEdit()
date_edit.setDate(QDate.currentDate())
date_edit.show()

# Obtener la fecha seleccionada y almacenarla en una variable
fecha_seleccionada = date_edit.date().toString("yyyy-MM-d")

print("Fecha seleccionada:", fecha_seleccionada)

app.exec_()
