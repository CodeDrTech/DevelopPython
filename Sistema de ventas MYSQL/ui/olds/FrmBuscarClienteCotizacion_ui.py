# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrmBuscarClienteCotizacion.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QApplication, QComboBox, QGroupBox, QHeaderView,
    QLabel, QLineEdit, QMainWindow, QPushButton,
    QSizePolicy, QStatusBar, QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.ApplicationModal)
        MainWindow.resize(437, 556)
        MainWindow.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 0, 71, 21))
        font = QFont()
        font.setPointSize(1)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(20, 35, 391, 481))
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
"    border: 2px solid #2980b9;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QGroupBox:title {\n"
"    color: #2980b9;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    border: none;\n"
"}\n"
"\n"
"")
        self.comboBox = QComboBox(self.groupBox)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 35, 120, 35))
        self.comboBox.setStyleSheet(u"QComboBox {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    color: #2980b9;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #3498db;\n"
"}\n"
"\n"
"QComboBox QAbstractItemView {\n"
"    border: 1px solid #cccccc;\n"
"    background-color: white;\n"
"    selection-background-color: #3498db;\n"
"}\n"
"")
        self.btnBuscar = QPushButton(self.groupBox)
        self.btnBuscar.setObjectName(u"btnBuscar")
        self.btnBuscar.setGeometry(QRect(280, 35, 85, 37))
        self.btnBuscar.setStyleSheet(u"QPushButton {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #5DADE2, stop: 1 #2980b9);\n"
"    color: #ffffff;\n"
"    border: 1px solid #2980b9;\n"
"    padding: 8px 16px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #4DA8DB, stop: 1 #2471a3);\n"
"    border: 1px solid #2471a3;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #3C89B4, stop: 1 #1f618d);\n"
"    border: 1px solid #1f618d;\n"
"}\n"
"")
        self.txtBuscar = QLineEdit(self.groupBox)
        self.txtBuscar.setObjectName(u"txtBuscar")
        self.txtBuscar.setGeometry(QRect(150, 35, 120, 35))
        self.txtBuscar.setStyleSheet(u"QWidget {\n"
"    background-color: #f2f2f2;\n"
"}\n"
"\n"
"QPushButton {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #5DADE2, stop: 1 #2980b9);\n"
"    color: #ffffff;\n"
"    border: 1px solid #2980b9;\n"
"    padding: 8px 16px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #4DA8DB, stop: 1 #2471a3);\n"
"    border: 1px solid #2471a3;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #3C89B4, stop: 1 #1f618d);\n"
"    border: 1px solid #1f618d;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #3498db;\n"
"}\n"
"\n"
"QLineEd"
                        "it:focus {\n"
"    border: 1px solid #3498db;\n"
"    outline: none;\n"
"}\n"
"\n"
"QWidget {\n"
"    background-color: #f2f2f2;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"QLineEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    color: #2980b9;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #2980b9;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"")
        self.tbDatos = QTableView(self.groupBox)
        self.tbDatos.setObjectName(u"tbDatos")
        self.tbDatos.setGeometry(QRect(10, 100, 361, 351))
        self.tbDatos.setStyleSheet(u"QTableView {\n"
"    background-color: #9a9a9a;\n"
"    border: 1px solid #cccccc;\n"
"    selection-background-color: #3498db;\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"QTableView QHeaderView {\n"
"    background-color: #d3d3d3;\n"
"    color: #333333;\n"
"    border: none;\n"
"}\n"
"\n"
"QTableView QHeaderView::section {\n"
"    background-color: #bbbbbb;\n"
"    color: #333333;\n"
"    padding: 6px;\n"
"    border: 1px solid #cccccc;\n"
"}\n"
"\n"
"QTableView QHeaderView::section:checked {\n"
"    background-color: #3498db;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QTableView::item {\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background-color: #3498db;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QTableView::item:focus {\n"
"    background-color: #3498db;\n"
"    color: #ffffff;\n"
"    outline: none;\n"
"}\n"
"\n"
"QTableView::item:hover {\n"
"    background-color: #d3d3d3;\n"
"    color: #333333;\n"
"}\n"
"")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Clientes", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Seleccionar Cliente", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Codigo", None))

        self.btnBuscar.setText(QCoreApplication.translate("MainWindow", u"Buscar", None))
#if QT_CONFIG(tooltip)
        self.txtBuscar.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Inserte el dato para buscar</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
    # retranslateUi

