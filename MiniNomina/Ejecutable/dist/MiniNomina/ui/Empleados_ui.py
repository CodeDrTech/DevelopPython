# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\Users\josep\Documents\DevelopPython\MiniNomina\Ejecutable\dist\MiniNomina\ui\Empleados.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_FrmEmpleado(object):
    def setupUi(self, FrmEmpleado):
        FrmEmpleado.setObjectName("FrmEmpleado")
        FrmEmpleado.setWindowModality(QtCore.Qt.ApplicationModal)
        FrmEmpleado.resize(291, 324)
        self.centralwidget = QtWidgets.QWidget(FrmEmpleado)
        self.centralwidget.setObjectName("centralwidget")
        self.BtnSalir = QtWidgets.QPushButton(self.centralwidget)
        self.BtnSalir.setGeometry(QtCore.QRect(90, 270, 101, 31))
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
        self.BtnAgregar = QtWidgets.QPushButton(self.centralwidget)
        self.BtnAgregar.setGeometry(QtCore.QRect(10, 220, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.BtnAgregar.setFont(font)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("c:\\Users\\josep\\Documents\\DevelopPython\\MiniNomina\\Ejecutable\\dist\\MiniNomina\\ui\\../png/agregar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnAgregar.setIcon(icon1)
        self.BtnAgregar.setIconSize(QtCore.QSize(25, 25))
        self.BtnAgregar.setObjectName("BtnAgregar")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(10, 30, 47, 13))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(10, 90, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(10, 150, 111, 16))
        self.label_3.setObjectName("label_3")
        self.txtNombre = QtWidgets.QLineEdit(self.centralwidget)
        self.txtNombre.setGeometry(QtCore.QRect(120, 25, 150, 20))
        self.txtNombre.setText("")
        self.txtNombre.setObjectName("txtNombre")
        self.txtNumbanca = QtWidgets.QLineEdit(self.centralwidget)
        self.txtNumbanca.setGeometry(QtCore.QRect(120, 85, 150, 20))
        self.txtNumbanca.setObjectName("txtNumbanca")
        self.txtSalario = QtWidgets.QLineEdit(self.centralwidget)
        self.txtSalario.setGeometry(QtCore.QRect(120, 145, 150, 20))
        self.txtSalario.setObjectName("txtSalario")
        self.BtnEditar = QtWidgets.QPushButton(self.centralwidget)
        self.BtnEditar.setGeometry(QtCore.QRect(180, 220, 101, 31))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.BtnEditar.setFont(font)
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap("c:\\Users\\josep\\Documents\\DevelopPython\\MiniNomina\\Ejecutable\\dist\\MiniNomina\\ui\\../png/editar.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.BtnEditar.setIcon(icon2)
        self.BtnEditar.setIconSize(QtCore.QSize(25, 25))
        self.BtnEditar.setObjectName("BtnEditar")
        FrmEmpleado.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(FrmEmpleado)
        self.statusbar.setObjectName("statusbar")
        FrmEmpleado.setStatusBar(self.statusbar)

        self.retranslateUi(FrmEmpleado)
        QtCore.QMetaObject.connectSlotsByName(FrmEmpleado)

    def retranslateUi(self, FrmEmpleado):
        _translate = QtCore.QCoreApplication.translate
        FrmEmpleado.setWindowTitle(_translate("FrmEmpleado", "MainWindow"))
        self.BtnSalir.setText(_translate("FrmEmpleado", "Salir"))
        self.BtnSalir.setShortcut(_translate("FrmEmpleado", "Esc"))
        self.BtnAgregar.setText(_translate("FrmEmpleado", "Registrar"))
        self.BtnAgregar.setShortcut(_translate("FrmEmpleado", "Return"))
        self.label.setText(_translate("FrmEmpleado", "NOMBRE"))
        self.label_2.setText(_translate("FrmEmpleado", "BANCA #"))
        self.label_3.setText(_translate("FrmEmpleado", "SALARIO"))
        self.BtnEditar.setText(_translate("FrmEmpleado", "Editar"))