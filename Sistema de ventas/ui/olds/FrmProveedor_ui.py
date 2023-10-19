# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrmProveedor.ui'
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
    QSizePolicy, QStatusBar, QTabWidget, QTableView,
    QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(848, 555)
        MainWindow.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 0, 101, 21))
        font = QFont()
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
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 30, 811, 481))
        self.tabWidget.setStyleSheet(u"QTabWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QTabWidget {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.txtBuscar = QLineEdit(self.tab)
        self.txtBuscar.setObjectName(u"txtBuscar")
        self.txtBuscar.setGeometry(QRect(150, 5, 120, 35))
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
        self.btnBuscar = QPushButton(self.tab)
        self.btnBuscar.setObjectName(u"btnBuscar")
        self.btnBuscar.setGeometry(QRect(280, 5, 85, 37))
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
        self.btnEliminar = QPushButton(self.tab)
        self.btnEliminar.setObjectName(u"btnEliminar")
        self.btnEliminar.setGeometry(QRect(370, 5, 85, 37))
        self.btnEliminar.setStyleSheet(u"QPushButton {\n"
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
"")
        self.btnImprimir = QPushButton(self.tab)
        self.btnImprimir.setObjectName(u"btnImprimir")
        self.btnImprimir.setGeometry(QRect(460, 5, 85, 37))
        self.btnImprimir.setStyleSheet(u"QPushButton {\n"
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
        self.tbDatos = QTableView(self.tab)
        self.tbDatos.setObjectName(u"tbDatos")
        self.tbDatos.setGeometry(QRect(10, 70, 771, 351))
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
        self.comboBox = QComboBox(self.tab)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(10, 5, 120, 35))
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
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 20, 771, 401))
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
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(5, 30, 55, 21))
        self.label_3.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(5, 70, 111, 21))
        self.label_4.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(5, 160, 81, 21))
        self.label_5.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.btnEditar = QPushButton(self.groupBox)
        self.btnEditar.setObjectName(u"btnEditar")
        self.btnEditar.setGeometry(QRect(250, 350, 86, 37))
        self.btnEditar.setStyleSheet(u"QPushButton {\n"
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
        self.btnGuardar = QPushButton(self.groupBox)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setGeometry(QRect(140, 350, 86, 37))
        self.btnGuardar.setStyleSheet(u"QPushButton {\n"
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
        self.btnSalir = QPushButton(self.groupBox)
        self.btnSalir.setObjectName(u"btnSalir")
        self.btnSalir.setGeometry(QRect(360, 350, 86, 37))
        self.btnSalir.setStyleSheet(u"QPushButton {\n"
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
        self.txtCodigo = QLineEdit(self.groupBox)
        self.txtCodigo.setObjectName(u"txtCodigo")
        self.txtCodigo.setGeometry(QRect(140, 20, 120, 35))
        self.txtCodigo.setStyleSheet(u"QWidget {\n"
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
        self.txtCodigo.setReadOnly(True)
        self.txtRazonSocial = QLineEdit(self.groupBox)
        self.txtRazonSocial.setObjectName(u"txtRazonSocial")
        self.txtRazonSocial.setGeometry(QRect(140, 60, 120, 35))
        self.txtRazonSocial.setStyleSheet(u"QWidget {\n"
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
        self.txtDireccion = QTextEdit(self.groupBox)
        self.txtDireccion.setObjectName(u"txtDireccion")
        self.txtDireccion.setGeometry(QRect(140, 150, 221, 41))
        self.txtDireccion.setStyleSheet(u"QWidget {\n"
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
"QTextEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QTextEdit:hover {\n"
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
"QTextEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    color: #2980b9;\n"
"}\n"
"\n"
"QTextEdit::placeholder {\n"
"    color: #2980b9;\n"
"    font-weight: bold;\n"
"}\n"
"\n"
"")
        self.cmbSectorComercial = QComboBox(self.groupBox)
        self.cmbSectorComercial.addItem("")
        self.cmbSectorComercial.addItem("")
        self.cmbSectorComercial.addItem("")
        self.cmbSectorComercial.addItem("")
        self.cmbSectorComercial.setObjectName(u"cmbSectorComercial")
        self.cmbSectorComercial.setGeometry(QRect(410, 50, 120, 35))
        self.cmbSectorComercial.setStyleSheet(u"QComboBox {\n"
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
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(270, 60, 131, 21))
        self.label_6.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.cmbTipoDocumento = QComboBox(self.groupBox)
        self.cmbTipoDocumento.addItem("")
        self.cmbTipoDocumento.addItem("")
        self.cmbTipoDocumento.addItem("")
        self.cmbTipoDocumento.setObjectName(u"cmbTipoDocumento")
        self.cmbTipoDocumento.setGeometry(QRect(140, 100, 103, 35))
        self.cmbTipoDocumento.setStyleSheet(u"QComboBox {\n"
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
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(5, 110, 131, 21))
        self.label_7.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtNumDocumento = QLineEdit(self.groupBox)
        self.txtNumDocumento.setObjectName(u"txtNumDocumento")
        self.txtNumDocumento.setGeometry(QRect(260, 100, 181, 35))
        self.txtNumDocumento.setStyleSheet(u"QWidget {\n"
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
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(5, 210, 71, 21))
        self.label_8.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtTelefono = QLineEdit(self.groupBox)
        self.txtTelefono.setObjectName(u"txtTelefono")
        self.txtTelefono.setGeometry(QRect(140, 200, 120, 35))
        self.txtTelefono.setStyleSheet(u"QWidget {\n"
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
        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(5, 260, 31, 21))
        self.label_9.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtUrl = QLineEdit(self.groupBox)
        self.txtUrl.setObjectName(u"txtUrl")
        self.txtUrl.setGeometry(QRect(140, 250, 120, 35))
        self.txtUrl.setStyleSheet(u"QWidget {\n"
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
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(270, 260, 51, 21))
        self.label_10.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtEmail = QLineEdit(self.groupBox)
        self.txtEmail.setObjectName(u"txtEmail")
        self.txtEmail.setGeometry(QRect(330, 250, 181, 35))
        self.txtEmail.setStyleSheet(u"QWidget {\n"
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
        self.tabWidget.addTab(self.tab_2, "")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        self.tabWidget.setCurrentIndex(0)


        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"Proveedores", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Ver, agregar o editar proveedores</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.txtBuscar.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Inserte el dato para buscar</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnBuscar.setText(QCoreApplication.translate("MainWindow", u"Buscar", None))
        self.btnEliminar.setText(QCoreApplication.translate("MainWindow", u"Eliminar", None))
        self.btnImprimir.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Documento", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Razon social", None))

        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Listado", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Proveedores", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Codigo", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Razon Social", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Direccion", None))
        self.btnEditar.setText(QCoreApplication.translate("MainWindow", u"Editar", None))
        self.btnGuardar.setText(QCoreApplication.translate("MainWindow", u"Guardar", None))
        self.btnSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.cmbSectorComercial.setItemText(0, QCoreApplication.translate("MainWindow", u"Alimentos", None))
        self.cmbSectorComercial.setItemText(1, QCoreApplication.translate("MainWindow", u"Salud", None))
        self.cmbSectorComercial.setItemText(2, QCoreApplication.translate("MainWindow", u"Tecnologia", None))
        self.cmbSectorComercial.setItemText(3, QCoreApplication.translate("MainWindow", u"Servicios", None))

        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Sector comercial", None))
        self.cmbTipoDocumento.setItemText(0, QCoreApplication.translate("MainWindow", u"RCN", None))
        self.cmbTipoDocumento.setItemText(1, QCoreApplication.translate("MainWindow", u"CEDULA", None))
        self.cmbTipoDocumento.setItemText(2, QCoreApplication.translate("MainWindow", u"PASAPORTE", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Tipo Documento", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Telefono", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Url", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Mantenimiento", None))
    # retranslateUi

