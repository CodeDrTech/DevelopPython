# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrmCliente.ui'
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
    QTableView, QTextEdit, QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(909, 575)
        MainWindow.setStyleSheet(u"/* Estilos comunes para varios controles */\n"
"QWidget {\n"
"    background-color: #deede3;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 0, 71, 21))
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
        self.tabWidget.setGeometry(QRect(10, 30, 871, 501))
        self.tabWidget.setStyleSheet(u"/* Estilos para QTabWidget */\n"
"QTabWidget {\n"
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
        self.groupBox_2 = QGroupBox(self.tab)
        self.groupBox_2.setObjectName(u"groupBox_2")
        self.groupBox_2.setGeometry(QRect(10, 5, 831, 451))
        self.groupBox_2.setStyleSheet(u"QGroupBox {\n"
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
        self.comboBox = QComboBox(self.groupBox_2)
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.comboBox.setObjectName(u"comboBox")
        self.comboBox.setGeometry(QRect(20, 15, 120, 35))
        self.comboBox.setStyleSheet(u"QComboBox {\n"
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
        self.txtBuscar = QLineEdit(self.groupBox_2)
        self.txtBuscar.setObjectName(u"txtBuscar")
        self.txtBuscar.setGeometry(QRect(150, 15, 120, 35))
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
        self.btnBuscar = QPushButton(self.groupBox_2)
        self.btnBuscar.setObjectName(u"btnBuscar")
        self.btnBuscar.setGeometry(QRect(285, 15, 85, 37))
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
        self.btnEliminar = QPushButton(self.groupBox_2)
        self.btnEliminar.setObjectName(u"btnEliminar")
        self.btnEliminar.setGeometry(QRect(375, 15, 85, 37))
        self.btnEliminar.setStyleSheet(u"QPushButton {\n"
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
        self.btnImprimir = QPushButton(self.groupBox_2)
        self.btnImprimir.setObjectName(u"btnImprimir")
        self.btnImprimir.setGeometry(QRect(465, 15, 85, 37))
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
        self.tbDatos = QTableView(self.groupBox_2)
        self.tbDatos.setObjectName(u"tbDatos")
        self.tbDatos.setGeometry(QRect(20, 70, 771, 351))
        self.tbDatos.setStyleSheet(u"QTableView {\n"
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
        self.groupBox.setGeometry(QRect(10, 20, 831, 411))
        self.groupBox.setStyleSheet(u"QGroupBox {\n"
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
        self.label_3.setGeometry(QRect(15, 30, 55, 21))
        self.label_3.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_4 = QLabel(self.groupBox)
        self.label_4.setObjectName(u"label_4")
        self.label_4.setGeometry(QRect(15, 70, 63, 21))
        self.label_4.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName(u"label_5")
        self.label_5.setGeometry(QRect(15, 210, 81, 21))
        self.label_5.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.btnGuardar = QPushButton(self.groupBox)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setGeometry(QRect(150, 350, 86, 37))
        self.btnGuardar.setStyleSheet(u"QPushButton {\n"
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
        self.btnEditar = QPushButton(self.groupBox)
        self.btnEditar.setObjectName(u"btnEditar")
        self.btnEditar.setGeometry(QRect(260, 350, 86, 37))
        self.btnEditar.setStyleSheet(u"QPushButton {\n"
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
        self.btnSalir = QPushButton(self.groupBox)
        self.btnSalir.setObjectName(u"btnSalir")
        self.btnSalir.setGeometry(QRect(370, 350, 86, 37))
        self.btnSalir.setStyleSheet(u"QPushButton {\n"
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
        self.txtCodigo.setGeometry(QRect(150, 20, 105, 35))
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
        self.txtNombre = QLineEdit(self.groupBox)
        self.txtNombre.setObjectName(u"txtNombre")
        self.txtNombre.setGeometry(QRect(150, 60, 105, 35))
        self.txtNombre.setStyleSheet(u"QLineEdit {\n"
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
        self.txtDireccion = QTextEdit(self.groupBox)
        self.txtDireccion.setObjectName(u"txtDireccion")
        self.txtDireccion.setGeometry(QRect(150, 200, 221, 41))
        self.txtDireccion.setStyleSheet(u"QTextEdit {\n"
"    background-color: #deede3;\n"
"    border: 1px solid #cccccc;\n"
"    padding: 6px;\n"
"    border-radius: 4px;\n"
"    font-size: 14px;\n"
"}\n"
"\n"
"QTextEdit:hover {\n"
"    border: 1px solid #689f84;\n"
"}\n"
"\n"
"QTextEdit:focus {\n"
"    border: 1px solid #689f84;\n"
"    outline: none;\n"
"}")
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName(u"label_6")
        self.label_6.setGeometry(QRect(280, 70, 81, 21))
        self.label_6.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.cmbTipoDocumento = QComboBox(self.groupBox)
        self.cmbTipoDocumento.addItem("")
        self.cmbTipoDocumento.addItem("")
        self.cmbTipoDocumento.addItem("")
        self.cmbTipoDocumento.setObjectName(u"cmbTipoDocumento")
        self.cmbTipoDocumento.setGeometry(QRect(150, 100, 105, 35))
        self.cmbTipoDocumento.setStyleSheet(u"QComboBox {\n"
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
"}\n"
"")
        self.label_7 = QLabel(self.groupBox)
        self.label_7.setObjectName(u"label_7")
        self.label_7.setGeometry(QRect(15, 110, 131, 21))
        self.label_7.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtNumDocumento = QLineEdit(self.groupBox)
        self.txtNumDocumento.setObjectName(u"txtNumDocumento")
        self.txtNumDocumento.setGeometry(QRect(270, 100, 181, 35))
        self.txtNumDocumento.setStyleSheet(u"QLineEdit {\n"
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
        self.label_8 = QLabel(self.groupBox)
        self.label_8.setObjectName(u"label_8")
        self.label_8.setGeometry(QRect(15, 260, 71, 21))
        self.label_8.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtTelefono = QLineEdit(self.groupBox)
        self.txtTelefono.setObjectName(u"txtTelefono")
        self.txtTelefono.setGeometry(QRect(150, 250, 120, 35))
        self.txtTelefono.setStyleSheet(u"QLineEdit {\n"
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
        self.label_10 = QLabel(self.groupBox)
        self.label_10.setObjectName(u"label_10")
        self.label_10.setGeometry(QRect(15, 310, 51, 21))
        self.label_10.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtEmail = QLineEdit(self.groupBox)
        self.txtEmail.setObjectName(u"txtEmail")
        self.txtEmail.setGeometry(QRect(150, 300, 181, 35))
        self.txtEmail.setStyleSheet(u"QLineEdit {\n"
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
        self.txtApellidos = QLineEdit(self.groupBox)
        self.txtApellidos.setObjectName(u"txtApellidos")
        self.txtApellidos.setGeometry(QRect(370, 60, 161, 35))
        self.txtApellidos.setStyleSheet(u"QLineEdit {\n"
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
        self.label_9 = QLabel(self.groupBox)
        self.label_9.setObjectName(u"label_9")
        self.label_9.setGeometry(QRect(20, 160, 41, 21))
        self.label_9.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.cmbSexo = QComboBox(self.groupBox)
        self.cmbSexo.addItem("")
        self.cmbSexo.addItem("")
        self.cmbSexo.setObjectName(u"cmbSexo")
        self.cmbSexo.setGeometry(QRect(150, 150, 105, 35))
        self.cmbSexo.setStyleSheet(u"QComboBox {\n"
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
        self.label_11 = QLabel(self.groupBox)
        self.label_11.setObjectName(u"label_11")
        self.label_11.setGeometry(QRect(270, 160, 158, 21))
        self.label_11.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.txtFechaNac = QDateEdit(self.groupBox)
        self.txtFechaNac.setObjectName(u"txtFechaNac")
        self.txtFechaNac.setGeometry(QRect(440, 150, 105, 35))
        self.txtFechaNac.setAcceptDrops(False)
        self.txtFechaNac.setStyleSheet(u"/* Estilos para QDateEdit */\n"
"QDateEdit {\n"
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
"}\n"
"\n"
"\n"
"\n"
"")
        self.txtFechaNac.setCalendarPopup(True)
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
        self.label.setText(QCoreApplication.translate("MainWindow", u"Clientes", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Ver, agregar o editar un cliente</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox_2.setTitle("")
        self.comboBox.setItemText(0, QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.comboBox.setItemText(1, QCoreApplication.translate("MainWindow", u"Documento", None))

#if QT_CONFIG(tooltip)
        self.txtBuscar.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p>Inserte el dato para buscar</p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnBuscar.setText(QCoreApplication.translate("MainWindow", u"Buscar", None))
        self.btnEliminar.setText(QCoreApplication.translate("MainWindow", u"Eliminar", None))
        self.btnImprimir.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Listado", None))
        self.groupBox.setTitle("")
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Codigo", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Direccion", None))
        self.btnGuardar.setText(QCoreApplication.translate("MainWindow", u"Guardar", None))
        self.btnEditar.setText(QCoreApplication.translate("MainWindow", u"Editar", None))
        self.btnSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", u"Apeliddos", None))
        self.cmbTipoDocumento.setItemText(0, QCoreApplication.translate("MainWindow", u"RNC", None))
        self.cmbTipoDocumento.setItemText(1, QCoreApplication.translate("MainWindow", u"CEDULA", None))
        self.cmbTipoDocumento.setItemText(2, QCoreApplication.translate("MainWindow", u"PASAPORTE", None))

        self.label_7.setText(QCoreApplication.translate("MainWindow", u"Tipo Documento", None))
        self.label_8.setText(QCoreApplication.translate("MainWindow", u"Telefono", None))
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"Email", None))
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"Sexo", None))
        self.cmbSexo.setItemText(0, QCoreApplication.translate("MainWindow", u"M", None))
        self.cmbSexo.setItemText(1, QCoreApplication.translate("MainWindow", u"F", None))

        self.label_11.setText(QCoreApplication.translate("MainWindow", u"Fecha de nacimiento", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Mantenimiento", None))
    # retranslateUi

