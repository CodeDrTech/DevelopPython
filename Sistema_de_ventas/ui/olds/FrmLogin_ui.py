# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrmLogin.ui'
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
from PySide6.QtWidgets import (QApplication, QDateTimeEdit, QGraphicsView, QGroupBox,
    QHeaderView, QLabel, QLineEdit, QMainWindow,
    QPushButton, QSizePolicy, QStatusBar, QTableView,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(558, 266)
        MainWindow.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.txtFecha = QDateTimeEdit(self.centralwidget)
        self.txtFecha.setObjectName(u"txtFecha")
        self.txtFecha.setGeometry(QRect(410, 20, 121, 25))
        self.txtFecha.setReadOnly(True)
        self.txtFecha.setCalendarPopup(True)
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(180, 10, 191, 21))
        font = QFont()
        font.setPointSize(1)
        font.setBold(True)
        self.label.setFont(font)
        self.label.setStyleSheet(u"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 20px;\n"
"    font-weight: bold;\n"
"}")
        self.graphicsView = QGraphicsView(self.centralwidget)
        self.graphicsView.setObjectName(u"graphicsView")
        self.graphicsView.setGeometry(QRect(10, 60, 160, 160))
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(210, 60, 321, 161))
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
        self.btnIngresar = QPushButton(self.groupBox)
        self.btnIngresar.setObjectName(u"btnIngresar")
        self.btnIngresar.setGeometry(QRect(113, 110, 85, 37))
        self.btnIngresar.setStyleSheet(u"QPushButton {\n"
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
        self.btnSalir.setGeometry(QRect(210, 110, 85, 37))
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
        self.txtPassword = QLineEdit(self.groupBox)
        self.txtPassword.setObjectName(u"txtPassword")
        self.txtPassword.setGeometry(QRect(113, 70, 181, 35))
        self.txtPassword.setStyleSheet(u"QWidget {\n"
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
        self.txtPassword.setEchoMode(QLineEdit.Password)
        self.txtUsuario = QLineEdit(self.groupBox)
        self.txtUsuario.setObjectName(u"txtUsuario")
        self.txtUsuario.setGeometry(QRect(113, 30, 181, 35))
        self.txtUsuario.setStyleSheet(u"QWidget {\n"
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
        self.label_2 = QLabel(self.groupBox)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 80, 101, 21))
        self.label_2.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName(u"label_3")
        self.label_3.setGeometry(QRect(10, 40, 71, 21))
        self.label_3.setStyleSheet(u"QWidget {\n"
"    background-color: #9a9a9a;\n"
"}\n"
"\n"
"QLabel {\n"
"    color: #2980b9;\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.tbDatos = QTableView(self.centralwidget)
        self.tbDatos.setObjectName(u"tbDatos")
        self.tbDatos.setGeometry(QRect(10, 0, 51, 41))
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
        self.label.setText(QCoreApplication.translate("MainWindow", u"Sistema de Ventas", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Acceso al Sistema", None))
        self.btnIngresar.setText(QCoreApplication.translate("MainWindow", u"Ingresar", None))
#if QT_CONFIG(shortcut)
        self.btnIngresar.setShortcut(QCoreApplication.translate("MainWindow", u"Return", None))
#endif // QT_CONFIG(shortcut)
        self.btnSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
#if QT_CONFIG(shortcut)
        self.btnSalir.setShortcut(QCoreApplication.translate("MainWindow", u"Esc", None))
#endif // QT_CONFIG(shortcut)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Contrase\u00f1a:", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Usuario:", None))
    # retranslateUi

