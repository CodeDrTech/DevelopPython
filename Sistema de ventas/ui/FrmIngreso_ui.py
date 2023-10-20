# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrmIngreso.ui'
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
        MainWindow.resize(999, 769)
        MainWindow.setStyleSheet(u"/* Estilos comunes para varios controles */\n"
"QWidget {\n"
"    background-color: #deede3;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 0, 151, 21))
        font = QFont()
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.tabWidget = QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName(u"tabWidget")
        self.tabWidget.setGeometry(QRect(10, 30, 961, 691))
        self.tabWidget.setStyleSheet(u"QTabWidget {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    border-radius: 4px;\n"
"}\n"
"\n"
"QTabWidget::tab-bar {\n"
"    left: 5px;\n"
"}\n"
"\n"
"QTabWidget::tab {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #1e362d;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"    padding: 6px 12px;\n"
"}\n"
"\n"
"QTabWidget::tab:selected {\n"
"    background-color: #c0dacb;\n"
"    border: 1px solid #1e362d;\n"
"    border-bottom: 1px solid #c0dacb;\n"
"}\n"
"\n"
"QTabWidget::pane {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #1e362d;\n"
"    border-top: none;\n"
"    border-bottom-left-radius: 4px;\n"
"    border-bottom-right-radius: 4px;\n"
"}")
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")
        self.groupBox_3 = QGroupBox(self.tab)
        self.groupBox_3.setObjectName(u"groupBox_3")
        self.groupBox_3.setGeometry(QRect(10, 10, 921, 631))
        self.groupBox_3.setStyleSheet(u"/* Estilos para QGroupBox */\n"
"QGroupBox {\n"
"    border: 2px solid #1e362d;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QGroupBox:title {\n"
"    color: #1e362d;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    border: none;\n"
"}")
        self.label_2 = QLabel(self.groupBox_3)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(25, 30, 73, 27))
        self.label_2.setFont(font)
        self.label_2.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtBuscar = QLineEdit(self.groupBox_3)
        self.txtBuscar.setObjectName(u"txtBuscar")
        self.txtBuscar.setGeometry(QRect(100, 20, 120, 35))
        self.txtBuscar.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.btnBuscar = QPushButton(self.groupBox_3)
        self.btnBuscar.setObjectName(u"btnBuscar")
        self.btnBuscar.setGeometry(QRect(235, 20, 85, 37))
        self.btnBuscar.setStyleSheet(u"QPushButton {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #c0dacb, stop: 1 #1e362d);\n"
"    color: #ffffff;\n"
"    border: 1px solid #1e362d;\n"
"    padding: 8px 16px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #689f84, stop: 1 #96bfaa);\n"
"    border: 1px solid #96bfaa;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #2a5242, stop: 1 #32624d);\n"
"    border: 1px solid #32624d;\n"
"}")
        self.btnAnular = QPushButton(self.groupBox_3)
        self.btnAnular.setObjectName(u"btnAnular")
        self.btnAnular.setGeometry(QRect(330, 20, 85, 37))
        self.btnAnular.setStyleSheet(u"QPushButton {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #c0dacb, stop: 1 #1e362d);\n"
"    color: #ffffff;\n"
"    border: 1px solid #1e362d;\n"
"    padding: 8px 16px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #689f84, stop: 1 #96bfaa);\n"
"    border: 1px solid #96bfaa;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #2a5242, stop: 1 #32624d);\n"
"    border: 1px solid #32624d;\n"
"}")
        self.btnImprimir = QPushButton(self.groupBox_3)
        self.btnImprimir.setObjectName(u"btnImprimir")
        self.btnImprimir.setGeometry(QRect(425, 20, 85, 37))
        self.btnImprimir.setStyleSheet(u"QPushButton {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #c0dacb, stop: 1 #1e362d);\n"
"    color: #ffffff;\n"
"    border: 1px solid #1e362d;\n"
"    padding: 8px 16px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #689f84, stop: 1 #96bfaa);\n"
"    border: 1px solid #96bfaa;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #2a5242, stop: 1 #32624d);\n"
"    border: 1px solid #32624d;\n"
"}")
        self.label_10 = QLabel(self.groupBox_3)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(25, 70, 101, 21))
        self.label_10.setFont(font)
        self.label_10.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_11 = QLabel(self.groupBox_3)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(160, 70, 81, 21))
        self.label_11.setFont(font)
        self.label_11.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_26 = QLabel(self.groupBox_3)
        self.label_26.setObjectName(u"label_26")
        self.label_26.setGeometry(QRect(295, 70, 61, 21))
        self.label_26.setFont(font)
        self.label_26.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtFechaInicio = QDateEdit(self.groupBox_3)
        self.txtFechaInicio.setObjectName(u"txtFechaInicio")
        self.txtFechaInicio.setGeometry(QRect(20, 100, 110, 30))
        self.txtFechaInicio.setAcceptDrops(False)
        self.txtFechaInicio.setStyleSheet(u"QDateEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QDateEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}")
        self.txtFechaInicio.setAlignment(Qt.AlignCenter)
        self.txtFechaInicio.setCalendarPopup(True)
        self.txtFechaFin = QDateEdit(self.groupBox_3)
        self.txtFechaFin.setObjectName(u"txtFechaFin")
        self.txtFechaFin.setGeometry(QRect(145, 100, 110, 30))
        self.txtFechaFin.setStyleSheet(u"QDateEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QDateEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}")
        self.txtFechaFin.setAlignment(Qt.AlignCenter)
        self.txtFechaFin.setCalendarPopup(True)
        self.cmbEstado = QComboBox(self.groupBox_3)
        self.cmbEstado.addItem("")
        self.cmbEstado.addItem("")
        self.cmbEstado.setObjectName(u"cmbEstado")
        self.cmbEstado.setGeometry(QRect(270, 100, 110, 30))
        self.cmbEstado.setStyleSheet(u"QComboBox {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QComboBox::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.tbIngreso = QTableView(self.groupBox_3)
        self.tbIngreso.setObjectName(u"tbIngreso")
        self.tbIngreso.setGeometry(QRect(20, 150, 871, 451))
        self.tbIngreso.setStyleSheet(u"QTableView {\n"
"    background-color: #f2f7f4;\n"
"    border: 1px solid #cccccc;\n"
"    selection-background-color: #96bfaa;\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"QTableView QHeaderView {\n"
"    background-color: #c0dacb;\n"
"    color: #333333;\n"
"    border: none;\n"
"}\n"
"\n"
"QTableView QHeaderView::section {\n"
"    background-color: #deede3;\n"
"    color: #333333;\n"
"    padding: 6px;\n"
"    border: 1px solid #1e362d;\n"
"}\n"
"\n"
"QTableView QHeaderView::section:checked {\n"
"    background-color: #96bfaa;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QTableView::item {\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background-color: #96bfaa;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QTableView::item:focus {\n"
"    background-color: #96bfaa;\n"
"    color: #ffffff;\n"
"    outline: none;\n"
"}")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.groupBox = QGroupBox(self.tab_2)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 10, 931, 631))
        self.groupBox.setStyleSheet(u"/* Estilos para QGroupBox */\n"
"QGroupBox {\n"
"    border: 2px solid #1e362d;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QGroupBox:title {\n"
"    color: #1e362d;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    border: none;\n"
"}")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(20, 70, 55, 21))
        self.label_3.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.btnRegistrar = QPushButton(self.groupBox)
        self.btnRegistrar.setObjectName(u"btnRegistrar")
        self.btnRegistrar.setGeometry(QRect(820, 110, 85, 37))
        self.btnRegistrar.setStyleSheet(u"QPushButton {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #c0dacb, stop: 1 #1e362d);\n"
"    color: #ffffff;\n"
"    border: 1px solid #1e362d;\n"
"    padding: 8px 16px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #689f84, stop: 1 #96bfaa);\n"
"    border: 1px solid #96bfaa;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #2a5242, stop: 1 #32624d);\n"
"    border: 1px solid #32624d;\n"
"}")
        self.txtCodigo = QLineEdit(self.groupBox)
        self.txtCodigo.setObjectName(u"txtCodigo")
        self.txtCodigo.setGeometry(QRect(135, 60, 120, 35))
        self.txtCodigo.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.txtCodigo.setReadOnly(True)
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(20, 120, 111, 21))
        self.label_6.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtFecha = QDateEdit(self.groupBox)
        self.txtFecha.setObjectName(u"txtFecha")
        self.txtFecha.setGeometry(QRect(670, 60, 120, 35))
        self.txtFecha.setAcceptDrops(False)
        self.txtFecha.setStyleSheet(u"QDateEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QDateEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}")
        self.txtFecha.setAlignment(Qt.AlignCenter)
        self.txtFecha.setCalendarPopup(True)
        self.label_12 = QLabel(self.groupBox)
        self.label_12.setObjectName(u"label_12")
        self.label_12.setGeometry(QRect(285, 70, 91, 21))
        self.label_12.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.cmbComprobante = QComboBox(self.groupBox)
        self.cmbComprobante.addItem("")
        self.cmbComprobante.addItem("")
        self.cmbComprobante.addItem("")
        self.cmbComprobante.setObjectName(u"cmbComprobante")
        self.cmbComprobante.setGeometry(QRect(135, 110, 120, 35))
        self.cmbComprobante.setStyleSheet(u"QComboBox {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QComboBox::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.cmbProveedor = QComboBox(self.groupBox)
        self.cmbProveedor.setObjectName(u"cmbProveedor")
        self.cmbProveedor.setGeometry(QRect(375, 60, 221, 35))
        self.cmbProveedor.setStyleSheet(u"QComboBox {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QComboBox::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.label_13 = QLabel(self.groupBox)
        self.label_13.setObjectName(u"label_13")
        self.label_13.setGeometry(QRect(285, 120, 67, 21))
        self.label_13.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtNumComprobante = QLineEdit(self.groupBox)
        self.txtNumComprobante.setObjectName(u"txtNumComprobante")
        self.txtNumComprobante.setGeometry(QRect(375, 110, 191, 35))
        self.txtNumComprobante.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.label_14 = QLabel(self.groupBox)
        self.label_14.setObjectName(u"label_14")
        self.label_14.setGeometry(QRect(610, 70, 51, 21))
        self.label_14.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.groupBox_2 = QGroupBox(self.groupBox)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(15, 160, 891, 201))
        self.groupBox_2.setStyleSheet(u"/* Estilos para QGroupBox */\n"
"QGroupBox {\n"
"    border: 2px solid #1e362d;\n"
"    border-radius: 8px;\n"
"    padding: 10px;\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QGroupBox:title {\n"
"    color: #1e362d;\n"
"    subcontrol-origin: margin;\n"
"    subcontrol-position: top left;\n"
"    left: 10px;\n"
"    padding-left: 5px;\n"
"    padding-right: 5px;\n"
"    border: none;\n"
"}")
        self.txtFechaProd = QDateEdit(self.groupBox_2)
        self.txtFechaProd.setObjectName(u"txtFechaProd")
        self.txtFechaProd.setGeometry(QRect(580, 80, 120, 35))
        self.txtFechaProd.setAcceptDrops(False)
        self.txtFechaProd.setStyleSheet(u"QDateEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QDateEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}")
        self.txtFechaProd.setAlignment(Qt.AlignCenter)
        self.txtFechaProd.setCalendarPopup(True)
        self.txtFechaVenc = QDateEdit(self.groupBox_2)
        self.txtFechaVenc.setObjectName(u"txtFechaVenc")
        self.txtFechaVenc.setGeometry(QRect(580, 140, 120, 35))
        self.txtFechaVenc.setAcceptDrops(False)
        self.txtFechaVenc.setStyleSheet(u"QDateEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QDateEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QDateEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}")
        self.txtFechaVenc.setAlignment(Qt.AlignCenter)
        self.txtFechaVenc.setCalendarPopup(True)
        self.label_16 = QLabel(self.groupBox_2)
        self.label_16.setObjectName(u"label_16")
        self.label_16.setGeometry(QRect(480, 90, 101, 21))
        self.label_16.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_17 = QLabel(self.groupBox_2)
        self.label_17.setObjectName(u"label_17")
        self.label_17.setGeometry(QRect(480, 150, 101, 21))
        self.label_17.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_18 = QLabel(self.groupBox_2)
        self.label_18.setObjectName(u"label_18")
        self.label_18.setGeometry(QRect(480, 30, 121, 21))
        self.label_18.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_19 = QLabel(self.groupBox_2)
        self.label_19.setObjectName(u"label_19")
        self.label_19.setGeometry(QRect(279, 90, 121, 21))
        self.label_19.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtPrecioCom = QLineEdit(self.groupBox_2)
        self.txtPrecioCom.setObjectName(u"txtPrecioCom")
        self.txtPrecioCom.setGeometry(QRect(606, 20, 61, 35))
        self.txtPrecioCom.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.txtPrecioVen1 = QLineEdit(self.groupBox_2)
        self.txtPrecioVen1.setObjectName(u"txtPrecioVen1")
        self.txtPrecioVen1.setGeometry(QRect(400, 80, 61, 35))
        self.txtPrecioVen1.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.cmbArticulo = QComboBox(self.groupBox_2)
        self.cmbArticulo.setObjectName(u"cmbArticulo")
        self.cmbArticulo.setGeometry(QRect(100, 80, 161, 35))
        self.cmbArticulo.setStyleSheet(u"QComboBox {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QComboBox:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QComboBox:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QComboBox::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.label_15 = QLabel(self.groupBox_2)
        self.label_15.setObjectName(u"label_15")
        self.label_15.setGeometry(QRect(10, 90, 71, 21))
        self.label_15.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtCantidad = QLineEdit(self.groupBox_2)
        self.txtCantidad.setObjectName(u"txtCantidad")
        self.txtCantidad.setGeometry(QRect(100, 140, 61, 35))
        self.txtCantidad.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.label_20 = QLabel(self.groupBox_2)
        self.label_20.setObjectName(u"label_20")
        self.label_20.setGeometry(QRect(10, 150, 81, 21))
        self.label_20.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtCodArticulo = QLineEdit(self.groupBox_2)
        self.txtCodArticulo.setObjectName(u"txtCodArticulo")
        self.txtCodArticulo.setGeometry(QRect(100, 20, 61, 30))
        self.txtCodArticulo.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.txtCodArticulo.setReadOnly(True)
        self.label_22 = QLabel(self.groupBox_2)
        self.label_22.setObjectName(u"label_22")
        self.label_22.setGeometry(QRect(279, 30, 111, 21))
        self.label_22.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtPrecioVen = QLineEdit(self.groupBox_2)
        self.txtPrecioVen.setObjectName(u"txtPrecioVen")
        self.txtPrecioVen.setGeometry(QRect(400, 20, 61, 35))
        self.txtPrecioVen.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.label_23 = QLabel(self.groupBox_2)
        self.label_23.setObjectName(u"label_23")
        self.label_23.setGeometry(QRect(279, 150, 121, 21))
        self.label_23.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtPrecioVen2 = QLineEdit(self.groupBox_2)
        self.txtPrecioVen2.setObjectName(u"txtPrecioVen2")
        self.txtPrecioVen2.setGeometry(QRect(400, 140, 61, 35))
        self.txtPrecioVen2.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.label_24 = QLabel(self.groupBox_2)
        self.label_24.setObjectName(u"label_24")
        self.label_24.setGeometry(QRect(760, 90, 71, 21))
        self.label_24.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_25 = QLabel(self.groupBox_2)
        self.label_25.setObjectName(u"label_25")
        self.label_25.setGeometry(QRect(770, 150, 51, 21))
        self.label_25.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.btnAgregar = QPushButton(self.groupBox_2)
        self.btnAgregar.setObjectName(u"btnAgregar")
        self.btnAgregar.setGeometry(QRect(840, 80, 21, 37))
        self.btnAgregar.setStyleSheet(u"QPushButton {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #c0dacb, stop: 1 #1e362d);\n"
"    color: #ffffff;\n"
"    border: 1px solid #1e362d;\n"
"    padding: 8px 16px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #689f84, stop: 1 #96bfaa);\n"
"    border: 1px solid #96bfaa;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #2a5242, stop: 1 #32624d);\n"
"    border: 1px solid #32624d;\n"
"}")
        icon = QIcon()
        iconThemeName = u"audio-card"
        if QIcon.hasThemeIcon(iconThemeName):
            icon = QIcon.fromTheme(iconThemeName)
        else:
            icon.addFile(u".", QSize(), QIcon.Normal, QIcon.Off)

        self.btnAgregar.setIcon(icon)
        self.btnQuitar = QPushButton(self.groupBox_2)
        self.btnQuitar.setObjectName(u"btnQuitar")
        self.btnQuitar.setGeometry(QRect(840, 140, 21, 37))
        self.btnQuitar.setStyleSheet(u"QPushButton {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #c0dacb, stop: 1 #1e362d);\n"
"    color: #ffffff;\n"
"    border: 1px solid #1e362d;\n"
"    padding: 8px 16px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QPushButton:hover {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #689f84, stop: 1 #96bfaa);\n"
"    border: 1px solid #96bfaa;\n"
"}\n"
"\n"
"QPushButton:pressed {\n"
"    background: qlineargradient(x1: 0, y1: 0, x2: 0, y2: 1,\n"
"                                 stop: 0 #2a5242, stop: 1 #32624d);\n"
"    border: 1px solid #32624d;\n"
"}")
        self.btnQuitar.setIcon(icon)
        self.label_27 = QLabel(self.groupBox_2)
        self.label_27.setObjectName(u"label_27")
        self.label_27.setGeometry(QRect(10, 30, 61, 21))
        self.label_27.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.tbDetalleIngreso = QTableView(self.groupBox)
        self.tbDetalleIngreso.setObjectName(u"tbDetalleIngreso")
        self.tbDetalleIngreso.setGeometry(QRect(15, 380, 891, 221))
        self.tbDetalleIngreso.setStyleSheet(u"QTableView {\n"
"    background-color: #f2f7f4;\n"
"    border: 1px solid #cccccc;\n"
"    selection-background-color: #96bfaa;\n"
"    selection-color: #ffffff;\n"
"}\n"
"\n"
"QTableView QHeaderView {\n"
"    background-color: #c0dacb;\n"
"    color: #333333;\n"
"    border: none;\n"
"}\n"
"\n"
"QTableView QHeaderView::section {\n"
"    background-color: #deede3;\n"
"    color: #333333;\n"
"    padding: 6px;\n"
"    border: 1px solid #1e362d;\n"
"}\n"
"\n"
"QTableView QHeaderView::section:checked {\n"
"    background-color: #96bfaa;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QTableView::item {\n"
"    padding: 6px;\n"
"}\n"
"\n"
"QTableView::item:selected {\n"
"    background-color: #96bfaa;\n"
"    color: #ffffff;\n"
"}\n"
"\n"
"QTableView::item:focus {\n"
"    background-color: #96bfaa;\n"
"    color: #ffffff;\n"
"    outline: none;\n"
"}")
        self.label_21 = QLabel(self.groupBox)
        self.label_21.setObjectName(u"label_21")
        self.label_21.setGeometry(QRect(620, 120, 41, 21))
        self.label_21.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtItbis = QLineEdit(self.groupBox)
        self.txtItbis.setObjectName(u"txtItbis")
        self.txtItbis.setGeometry(QRect(670, 110, 120, 35))
        self.txtItbis.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.txtIdProveedor = QLineEdit(self.groupBox)
        self.txtIdProveedor.setObjectName(u"txtIdProveedor")
        self.txtIdProveedor.setGeometry(QRect(375, 20, 75, 30))
        self.txtIdProveedor.setStyleSheet(u"QLineEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QLineEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QLineEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}\n"
"\n"
"QLineEdit::placeholder {\n"
"    color: #1e362d;\n"
"    font-weight: bold;\n"
"}")
        self.txtIdProveedor.setReadOnly(True)
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(285, 30, 55, 21))
        self.label_4.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.tabWidget.addTab(self.tab_2, "")
        self.tbSesiones = QTableView(self.centralwidget)
        self.tbSesiones.setObjectName(u"tbSesiones")
        self.tbSesiones.setGeometry(QRect(790, 10, 51, 31))
        self.tbSesiones.setStyleSheet(u"")
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
        self.label.setText(QCoreApplication.translate("MainWindow", u"Ingresos almacen", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Mantenimiento de los ingresos a almacen</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_3.setTitle("")
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.btnBuscar.setText(QCoreApplication.translate("MainWindow", u"Buscar", None))
#if QT_CONFIG(shortcut)
        self.btnBuscar.setShortcut(QCoreApplication.translate("MainWindow", u"Return", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.btnAnular.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Anula el ingreso para que no se pueda vender posteriormente.</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnAnular.setText(QCoreApplication.translate("MainWindow", u"Anular", None))
        self.btnImprimir.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Fecha Inicio", None))
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Fecha Fin", None))
        self.label_26.setText(QCoreApplication.translate("MainWindow", u"Estado", None))
        self.cmbEstado.setItemText(0, QCoreApplication.translate("MainWindow", u"Activo", None))
        self.cmbEstado.setItemText(1, QCoreApplication.translate("MainWindow", u"Inactivo", None))

#if QT_CONFIG(tooltip)
        self.cmbEstado.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Doble click para buscar articulos</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Listado", None))
        self.groupBox.setTitle("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Codigo", None))
        self.btnRegistrar.setText(QCoreApplication.translate("MainWindow", u"Agregar", None))
#if QT_CONFIG(tooltip)
        self.txtCodigo.setToolTip(QCoreApplication.translate("MainWindow", u"Insertar codigo de articulo", None))
#endif // QT_CONFIG(tooltip)
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Comprobante", None))
        self.label_12.setText(QCoreApplication.translate("MainWindow", u"Proveedor", None))
        self.cmbComprobante.setItemText(0, QCoreApplication.translate("MainWindow", u"FACTURA", None))
        self.cmbComprobante.setItemText(1, QCoreApplication.translate("MainWindow", u"RECIBO", None))
        self.cmbComprobante.setItemText(2, QCoreApplication.translate("MainWindow", u"CONDUCE", None))

#if QT_CONFIG(tooltip)
        self.cmbProveedor.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Doble click para buscar proveedores</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_13.setText(QCoreApplication.translate("MainWindow", u"Numero ", None))
        self.label_14.setText(QCoreApplication.translate("MainWindow", u"Fecha", None))
        self.groupBox_2.setTitle("")
        self.label_16.setText(QCoreApplication.translate("MainWindow", u"Fecha prod.", None))
        self.label_17.setText(QCoreApplication.translate("MainWindow", u"Fecha venc.", None))
        self.label_18.setText(QCoreApplication.translate("MainWindow", u"Precio compra", None))
        self.label_19.setText(QCoreApplication.translate("MainWindow", u"Precio venta 2", None))
#if QT_CONFIG(tooltip)
        self.cmbArticulo.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Doble click para buscar articulos</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_15.setText(QCoreApplication.translate("MainWindow", u"Articulo", None))
        self.label_20.setText(QCoreApplication.translate("MainWindow", u"Cantidad", None))
        self.label_22.setText(QCoreApplication.translate("MainWindow", u"Precio venta", None))
        self.label_23.setText(QCoreApplication.translate("MainWindow", u"Precio venta 3", None))
        self.label_24.setText(QCoreApplication.translate("MainWindow", u"Agregar ", None))
        self.label_25.setText(QCoreApplication.translate("MainWindow", u"Quitar", None))
        self.btnAgregar.setText(QCoreApplication.translate("MainWindow", u"+", None))
        self.btnQuitar.setText(QCoreApplication.translate("MainWindow", u"-", None))
        self.label_27.setText(QCoreApplication.translate("MainWindow", u"Codigo", None))
        self.label_21.setText(QCoreApplication.translate("MainWindow", u"Itbis", None))
        self.txtItbis.setText("")
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Codigo", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Mantenimiento", None))
    # retranslateUi

