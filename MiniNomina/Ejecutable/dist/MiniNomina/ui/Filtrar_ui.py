# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\josep\Documents\DevelopPython\MiniNomina\Ejecutable\dist\MiniNomina\ui\Filtrar.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FrmFiltrar(object):
    def setupUi(self, FrmFiltrar):
        FrmFiltrar.setObjectName("FrmFiltrar")
        FrmFiltrar.setWindowModality(QtCore.Qt.ApplicationModal)
        FrmFiltrar.resize(273, 246)
        self.centralwidget = QtWidgets.QWidget(FrmFiltrar)
        self.centralwidget.setObjectName("centralwidget")
        self.BtnSalir = QtWidgets.QPushButton(self.centralwidget)
        self.BtnSalir.setGeometry(QtCore.QRect(160, 190, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.BtnSalir.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("c:\\Users\\josep\\Documents\\DevelopPython\\MiniNomina\\Ejecutable\\dist\\MiniNomina\\ui\\../png/salir2.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnSalir.setIcon(icon)
        self.BtnSalir.setIconSize(QtCore.QSize(25, 25))
        self.BtnSalir.setObjectName("BtnSalir")
        self.BtnReporte = QtWidgets.QPushButton(self.centralwidget)
        self.BtnReporte.setGeometry(QtCore.QRect(10, 190, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.BtnReporte.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("c:\\Users\\josep\\Documents\\DevelopPython\\MiniNomina\\Ejecutable\\dist\\MiniNomina\\ui\\../png/agregar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnReporte.setIcon(icon1)
        self.BtnReporte.setIconSize(QtCore.QSize(25, 25))
        self.BtnReporte.setObjectName("BtnReporte")
        self.BtnReporteTotal = QtWidgets.QPushButton(self.centralwidget)
        self.BtnReporteTotal.setGeometry(QtCore.QRect(75, 20, 125, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.BtnReporteTotal.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("c:\\Users\\josep\\Documents\\DevelopPython\\MiniNomina\\Ejecutable\\dist\\MiniNomina\\ui\\../png/Reporte.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnReporteTotal.setIcon(icon2)
        self.BtnReporteTotal.setIconSize(QtCore.QSize(25, 25))
        self.BtnReporteTotal.setObjectName("BtnReporteTotal")
        self.label_5 = QtWidgets.QLabel(self.centralwidget)
        self.label_5.setGeometry(QtCore.QRect(90, 100, 91, 16))
        self.label_5.setObjectName("label_5")
        self.cmbEmpleado = QtWidgets.QComboBox(self.centralwidget)
        self.cmbEmpleado.setGeometry(QtCore.QRect(50, 120, 170, 20))
        self.cmbEmpleado.setEditable(True)
        self.cmbEmpleado.setObjectName("cmbEmpleado")
        FrmFiltrar.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FrmFiltrar)
        self.statusbar.setObjectName("statusbar")
        FrmFiltrar.setStatusBar(self.statusbar)

        self.retranslateUi(FrmFiltrar)
        QtCore.QMetaObject.connectSlotsByName(FrmFiltrar)

    def retranslateUi(self, FrmFiltrar):
        _translate = QtCore.QCoreApplication.translate
        FrmFiltrar.setWindowTitle(_translate("FrmFiltrar", "MainWindow"))
        self.BtnSalir.setText(_translate("FrmFiltrar", "Salir"))
        self.BtnSalir.setShortcut(_translate("FrmFiltrar", "Esc"))
        self.BtnReporte.setText(_translate("FrmFiltrar", "Reporte"))
        self.BtnReporteTotal.setText(_translate("FrmFiltrar", "Reporte total"))
        self.label_5.setText(_translate("FrmFiltrar", "ELIJA UN NOMBRE"))