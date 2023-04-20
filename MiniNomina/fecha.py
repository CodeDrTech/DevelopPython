from PyQt5.QtWidgets import QStyledItemDelegate
from PyQt5.QtSql import QSqlDatabase, QSqlTableModel, QSqlQuery
from PyQt5 import QtWidgets
from Conexion_db import conectar_db, db
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QTextDocument
from PyQt5.QtCore import Qt, QDate, QLocale, QTextStream




# Crear un modelo de tabla SQL
model = QSqlTableModel()
model.setTable("faltantes")
#model.setSort(0, Qt.DescendingOrder) # type: ignore    
# Seleccionar los datos filtrados
model.select()





fecha_actual = QDate.currentDate()
mes_actual = fecha_actual.month()
fecha_inicio = QDate(fecha_actual.year(), mes_actual, 1)
DiaDeHoy = fecha_actual.day()
for row in range(model.rowCount()):
    model.setData(model.index(row, 0), fecha_inicio.toString("yyyy-MM-dd"))
fecha_inicio = fecha_inicio.addDays(DiaDeHoy)