# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrmVentas.ui'
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
from PySide6.QtWidgets import (QApplication, QComboBox, QDateEdit, QGroupBox,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTabWidget,
    QTableView, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(904, 672)
        MainWindow.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 0, 61, 21))
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
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 30, 871, 601))
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
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 10, 73, 27))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtBuscar = QLineEdit(self.tab)
        self.txtBuscar.setObjectName(u"txtBuscar")
        self.txtBuscar.setGeometry(QRect(90, 5, 120, 35))
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
        self.btnBuscar.setGeometry(QRect(220, 5, 85, 37))
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
        self.btnAnular = QPushButton(self.tab)
        self.btnAnular.setObjectName(u"btnAnular")
        self.btnAnular.setGeometry(QRect(310, 5, 85, 37))
        self.btnAnular.setStyleSheet(u"QPushButton {\n"
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
        self.btnImprimir.setGeometry(QRect(400, 5, 85, 37))
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
        self.tbDatos.setGeometry(QRect(10, 110, 811, 421))
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
        self.txtFechaInicio = QDateEdit(self.tab)
        self.txtFechaInicio.setObjectName(u"txtFechaInicio")
        self.txtFechaInicio.setGeometry(QRect(5, 70, 110, 30))
        self.txtFechaInicio.setAcceptDrops(False)
        self.txtFechaInicio.setStyleSheet(u"/* Estilos para QDateEdit */\n"
"QDateEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    color: #2980b9;\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 1px solid #3498db;\n"
"}\n"
"\n"
"QDateEdit QAbstractItemView {\n"
"    border: 1px solid #cccccc;\n"
"    background-color: white;\n"
"    selection-background-color: #3498db;\n"
"}\n"
"\n"
"\n"
"")
        self.txtFechaInicio.setAlignment(Qt.AlignCenter)
        self.txtFechaInicio.setCalendarPopup(True)
        self.txtFechaFin = QDateEdit(self.tab)
        self.txtFechaFin.setObjectName(u"txtFechaFin")
        self.txtFechaFin.setGeometry(QRect(125, 70, 110, 30))
        self.txtFechaFin.setStyleSheet(u"/* Estilos para QDateEdit */\n"
"QDateEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    color: #2980b9;\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 1px solid #3498db;\n"
"}\n"
"\n"
"QDateEdit QAbstractItemView {\n"
"    border: 1px solid #cccccc;\n"
"    background-color: white;\n"
"    selection-background-color: #3498db;\n"
"}\n"
"\n"
"\n"
"")
        self.txtFechaFin.setAlignment(Qt.AlignCenter)
        self.txtFechaFin.setCalendarPopup(True)
        self.label_10 = QLabel(self.tab)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(10, 50, 101, 21))
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_11 = QLabel(self.tab)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(140, 50, 81, 21))
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 831, 531))
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
        self.label_3.setGeometry(QRect(10, 30, 55, 21))
        self.label_3.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.btnNuevo = QPushButton(self.groupBox)
        self.btnNuevo.setObjectName(u"btnNuevo")
        self.btnNuevo.setGeometry(QRect(130, 490, 85, 37))
        self.btnNuevo.setStyleSheet(u"QPushButton {\n"
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
        self.btnEditar = QPushButton(self.groupBox)
        self.btnEditar.setObjectName(u"btnEditar")
        self.btnEditar.setGeometry(QRect(310, 490, 85, 37))
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
        self.btnGuardar.setGeometry(QRect(220, 490, 85, 37))
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
        self.btnCancelar = QPushButton(self.groupBox)
        self.btnCancelar.setObjectName(u"btnCancelar")
        self.btnCancelar.setGeometry(QRect(400, 490, 90, 37))
        self.btnCancelar.setStyleSheet(u"QPushButton {\n"
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
        self.txtCodigo.setGeometry(QRect(130, 30, 120, 35))
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
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(10, 70, 111, 21))
        self.label_6.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtFecha = QDateEdit(self.groupBox)
        self.txtFecha.setObjectName(u"txtFecha")
        self.txtFecha.setGeometry(QRect(645, 30, 120, 35))
        self.txtFecha.setAcceptDrops(False)
        self.txtFecha.setStyleSheet(u"/* Estilos para QDateEdit */\n"
"QDateEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    color: #2980b9;\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 1px solid #3498db;\n"
"}\n"
"\n"
"QDateEdit QAbstractItemView {\n"
"    border: 1px solid #cccccc;\n"
"    background-color: white;\n"
"    selection-background-color: #3498db;\n"
"}\n"
"\n"
"\n"
"")
        self.txtFecha.setAlignment(Qt.AlignCenter)
        self.txtFecha.setCalendarPopup(True)
        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(260, 30, 61, 21))
        self.label_12.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.cmbComprobante = QComboBox(self.groupBox)
        self.cmbComprobante.addItem("")
        self.cmbComprobante.addItem("")
        self.cmbComprobante.addItem("")
        self.cmbComprobante.addItem("")
        self.cmbComprobante.setObjectName(u"cmbComprobante")
        self.cmbComprobante.setGeometry(QRect(130, 70, 120, 35))
        self.cmbComprobante.setStyleSheet(u"QComboBox {\n"
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
        self.cmbCliente = QComboBox(self.groupBox)
        self.cmbCliente.setObjectName(u"cmbCliente")
        self.cmbCliente.setGeometry(QRect(330, 35, 241, 35))
        self.cmbCliente.setStyleSheet(u"QComboBox {\n"
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
        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(260, 70, 67, 21))
        self.label_13.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtSerie = QLineEdit(self.groupBox)
        self.txtSerie.setObjectName(u"txtSerie")
        self.txtSerie.setGeometry(QRect(330, 70, 120, 35))
        self.txtSerie.setStyleSheet(u"QWidget {\n"
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
        self.txtCorrelativo = QLineEdit(self.groupBox)
        self.txtCorrelativo.setObjectName(u"txtCorrelativo")
        self.txtCorrelativo.setGeometry(QRect(450, 70, 120, 35))
        self.txtCorrelativo.setStyleSheet(u"QWidget {\n"
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
        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(580, 30, 51, 21))
        self.label_14.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 109, 791, 121))
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
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
        self.txtFechaVenc = QDateEdit(self.groupBox_2)
        self.txtFechaVenc.setObjectName(u"txtFechaVenc")
        self.txtFechaVenc.setGeometry(QRect(639, 40, 91, 35))
        self.txtFechaVenc.setAcceptDrops(False)
        self.txtFechaVenc.setStyleSheet(u"/* Estilos para QDateEdit */\n"
"QDateEdit {\n"
"    background-color: #ffffff;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    color: #2980b9;\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 1px solid #3498db;\n"
"}\n"
"\n"
"QDateEdit QAbstractItemView {\n"
"    border: 1px solid #cccccc;\n"
"    background-color: white;\n"
"    selection-background-color: #3498db;\n"
"}\n"
"\n"
"\n"
"")
        self.txtFechaVenc.setAlignment(Qt.AlignCenter)
        self.txtFechaVenc.setCalendarPopup(True)
        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(540, 50, 91, 21))
        self.label_16.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(550, 90, 91, 21))
        self.label_17.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(310, 90, 111, 21))
        self.label_19.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.cmbArticulo = QComboBox(self.groupBox_2)
        self.cmbArticulo.setObjectName(u"cmbArticulo")
        self.cmbArticulo.setGeometry(QRect(90, 40, 201, 35))
        self.cmbArticulo.setStyleSheet(u"QComboBox {\n"
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
        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(10, 50, 71, 21))
        self.label_15.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtCantidad = QLineEdit(self.groupBox_2)
        self.txtCantidad.setObjectName(u"txtCantidad")
        self.txtCantidad.setGeometry(QRect(90, 80, 61, 35))
        self.txtCantidad.setStyleSheet(u"QWidget {\n"
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
        self.label_20 = QLabel(self.groupBox_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(10, 90, 81, 21))
        self.label_20.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtCodArticulo = QLineEdit(self.groupBox_2)
        self.txtCodArticulo.setObjectName(u"txtCodArticulo")
        self.txtCodArticulo.setGeometry(QRect(90, 5, 91, 30))
        self.txtCodArticulo.setStyleSheet(u"QWidget {\n"
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
        self.txtCodArticulo.setReadOnly(True)
        self.txtStock = QLineEdit(self.groupBox_2)
        self.txtStock.setObjectName(u"txtStock")
        self.txtStock.setGeometry(QRect(200, 80, 61, 35))
        self.txtStock.setStyleSheet(u"QWidget {\n"
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
        self.label_22 = QLabel(self.groupBox_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(155, 90, 41, 21))
        self.label_22.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtDescuento = QLineEdit(self.groupBox_2)
        self.txtDescuento.setObjectName(u"txtDescuento")
        self.txtDescuento.setGeometry(QRect(639, 80, 91, 35))
        self.txtDescuento.setStyleSheet(u"QWidget {\n"
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
        self.btnAgrgar = QPushButton(self.groupBox_2)
        self.btnAgrgar.setObjectName(u"btnAgrgar")
        self.btnAgrgar.setGeometry(QRect(750, 40, 21, 37))
        self.btnAgrgar.setStyleSheet(u"QPushButton {\n"
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
        icon = QIcon()
        iconThemeName = u"audio-card"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.btnAgrgar.setIcon(icon)
        self.btnQuitar = QPushButton(self.groupBox_2)
        self.btnQuitar.setObjectName(u"btnQuitar")
        self.btnQuitar.setGeometry(QRect(750, 80, 21, 37))
        self.btnQuitar.setStyleSheet(u"QPushButton {\n"
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
        self.btnQuitar.setIcon(icon)
        self.cmbPrecioVent = QComboBox(self.groupBox_2)
        self.cmbPrecioVent.setObjectName(u"cmbPrecioVent")
        self.cmbPrecioVent.setGeometry(QRect(429, 80, 91, 35))
        self.cmbPrecioVent.setStyleSheet(u"QComboBox {\n"
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
        self.tbDatos2 = QTableView(self.groupBox)
        self.tbDatos2.setObjectName(u"tbDatos2")
        self.tbDatos2.setGeometry(QRect(10, 250, 791, 221))
        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(590, 80, 41, 21))
        self.label_21.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtItbis = QLineEdit(self.groupBox)
        self.txtItbis.setObjectName(u"txtItbis")
        self.txtItbis.setGeometry(QRect(645, 70, 120, 35))
        self.txtItbis.setStyleSheet(u"QWidget {\n"
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
        self.txtIdCliente = QLineEdit(self.groupBox)
        self.txtIdCliente.setObjectName(u"txtIdCliente")
        self.txtIdCliente.setGeometry(QRect(330, 5, 75, 30))
        self.txtIdCliente.setStyleSheet(u"QWidget {\n"
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
        self.txtIdCliente.setReadOnly(True)
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
        self.label.setText(QCoreApplication.translate("MainWindow", u"Ventas", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Mantenimiento de los ingresos a almacen</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.btnBuscar.setText(QCoreApplication.translate("MainWindow", u"Buscar", None))
        self.btnAnular.setText(QCoreApplication.translate("MainWindow", u"Anular", None))
        self.btnImprimir.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Fecha Inicio", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Fecha Fin", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Listado", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Ventas", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Codigo", None))
        self.btnNuevo.setText(QCoreApplication.translate("MainWindow", u"Nuevo", None))
        self.btnEditar.setText(QCoreApplication.translate("MainWindow", u"Editar", None))
        self.btnGuardar.setText(QCoreApplication.translate("MainWindow", u" Guardar ", None))
        self.btnCancelar.setText(QCoreApplication.translate("MainWindow", u"Cancelar", None))
#if QT_CONFIG(tooltip)
        self.txtCodigo.setToolTip(QCoreApplication.translate("MainWindow", u"Insertar codigo de articulo", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Comprobante", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Cliente", None))
        self.cmbComprobante.setItemText(0, QCoreApplication.translate("MainWindow", u"TICKET", None))
        self.cmbComprobante.setItemText(1, QCoreApplication.translate("MainWindow", u"BOLETA", None))
        self.cmbComprobante.setItemText(2, QCoreApplication.translate("MainWindow", u"FACTURA", None))
        self.cmbComprobante.setItemText(3, QCoreApplication.translate("MainWindow", u"GUI REMISION", None))

#if QT_CONFIG(tooltip)
        self.cmbCliente.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Doble click para buscar clientes</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Numero ", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Fecha", None))
        self.groupBox_2.setTitle("")
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Fecha venc.", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Descuento", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Precion venta", None))
#if QT_CONFIG(tooltip)
        self.cmbArticulo.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Doble click para buscar articulos</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Articulo", None))
        self.txtCantidad.setText("")
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Cantidad", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Disp.", None))
        self.btnAgrgar.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.btnQuitar.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Itbis", None))
        self.txtItbis.setText("")
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Mantenimiento", None))
    # retranslateUi

