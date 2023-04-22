from PyQt5.QtWidgets import QApplication, QDateEdit
from PyQt5.QtCore import QDate
# # import sys
# # from PyQt5.QtWidgets import QApplication, QTableView, QStyledItemDelegate
# # import datetime
# # from PyQt5.QtGui import QStandardItemModel, QStandardItem

app = QApplication([])

date_edit = QDateEdit()
date_edit.setDate(QDate.currentDate())
date_edit.show()

#Obtener la fecha seleccionada y almacenarla en una variable
fecha_seleccionada = date_edit.date().toString("yyyy-MM-dd")

print("Fecha seleccionada:", fecha_seleccionada)

app.exec_()


# class DateDelegate(QStyledItemDelegate):
#     def displayText(self, value, locale):
#         try:
#             # Analiza el valor de la fecha y hora
#             datetime_obj = datetime.datetime.strptime(value, 'yyyy-MM-d')
#             # Obtiene solo la fecha
#             date_obj = datetime_obj.date()
#             # Formatea la fecha en un formato legible
#             return date_obj.strftime('d-MMMM-yyyy')
#         except ValueError:
#             # Si no se puede convertir a una fecha, devuelve el valor original
#             return value

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
    
#     # Crea una instancia de la clase QStandardItemModel
#     model = QStandardItemModel()
    
#     # Agrega las columnas necesarias al modelo
#     model.setHorizontalHeaderLabels(['Fecha'])
    
#     # Agrega los datos al modelo
#     date_str = '2022-05-10 12:30:00'
#     date_item = QStandardItem(date_str)
#     model.setItem(0, 0, date_item)
    
#     # Crea una instancia de la clase QTableView
#     table_view = QTableView()
    
#     # Asigna la instancia de la clase QStandardItemModel al QTableView
#     table_view.setModel(model)
    
#     # Asigna una instancia de la clase DateDelegate a la columna correspondiente del QTableView
#     date_delegate = DateDelegate()
#     table_view.setItemDelegateForColumn(0, date_delegate)
    
#     # Muestra la ventana
#     table_view.show()
    
#     sys.exit(app.exec_())

