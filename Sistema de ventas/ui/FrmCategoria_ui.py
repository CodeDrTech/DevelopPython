# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrmCategoria.ui'
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
from PySide6.QtWidgets import (QApplication, QGroupBox, QHeaderView, QLabel,
    QLineEdit, QMainWindow, QPushButton, QSizePolicy,
    QStatusBar, QTabWidget, QTableView, QTextEdit,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setWindowModality(Qt.NonModal)
        MainWindow.resize(757, 557)
        MainWindow.setStyleSheet(u"/* Estilos comunes para varios controles */\n"
"QWidget {\n"
"    background-color: #deede3;\n"
"}")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.label = QLabel(self.centralwidget)
        self.label.setObjectName(u"label")
        self.label.setGeometry(QRect(20, 0, 111, 21))
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
        self.tabWidget.setGeometry(QRect(10, 30, 721, 481))
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
        self.label_2 = QLabel(self.tab)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setGeometry(QRect(10, 5, 101, 21))
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
        self.txtBuscar = QLineEdit(self.tab)
        self.txtBuscar.setObjectName(u"txtBuscar")
        self.txtBuscar.setGeometry(QRect(120, 5, 120, 35))
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
        self.btnBuscar = QPushButton(self.tab)
        self.btnBuscar.setObjectName(u"btnBuscar")
        self.btnBuscar.setGeometry(QRect(250, 5, 85, 37))
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
"}\n"
"")
        self.btnEliminar = QPushButton(self.tab)
        self.btnEliminar.setObjectName(u"btnEliminar")
        self.btnEliminar.setGeometry(QRect(340, 5, 85, 37))
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
"}\n"
"")
        self.btnImprimir = QPushButton(self.tab)
        self.btnImprimir.setObjectName(u"btnImprimir")
        self.btnImprimir.setGeometry(QRect(430, 5, 85, 37))
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
"}\n"
"")
        self.tbDatos = QTableView(self.tab)
        self.tbDatos.setObjectName(u"tbDatos")
        self.tbDatos.setGeometry(QRect(10, 70, 681, 351))
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
        self.groupBox.setGeometry(QRect(10, 20, 531, 231))
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
        self.label_3.setGeometry(QRect(10, 30, 55, 21))
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
        self.label_4.setGeometry(QRect(10, 60, 63, 21))
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
        self.label_5.setGeometry(QRect(10, 100, 101, 21))
        self.label_5.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.btnEditar = QPushButton(self.groupBox)
        self.btnEditar.setObjectName(u"btnEditar")
        self.btnEditar.setGeometry(QRect(200, 160, 85, 37))
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
"}\n"
"")
        self.btnGuardar = QPushButton(self.groupBox)
        self.btnGuardar.setObjectName(u"btnGuardar")
        self.btnGuardar.setGeometry(QRect(110, 160, 85, 37))
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
"}\n"
"")
        self.btnSalir = QPushButton(self.groupBox)
        self.btnSalir.setObjectName(u"btnSalir")
        self.btnSalir.setGeometry(QRect(290, 160, 85, 37))
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
"}\n"
"")
        self.txtCodigo = QLineEdit(self.groupBox)
        self.txtCodigo.setObjectName(u"txtCodigo")
        self.txtCodigo.setGeometry(QRect(110, 20, 120, 35))
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
        self.txtNombre.setGeometry(QRect(110, 60, 120, 35))
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
        self.txtDescripcion = QTextEdit(self.groupBox)
        self.txtDescripcion.setObjectName(u"txtDescripcion")
        self.txtDescripcion.setGeometry(QRect(110, 100, 221, 41))
        self.txtDescripcion.setStyleSheet(u"QTextEdit {\n"
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
        self.label.setText(QCoreApplication.translate("MainWindow", u"CATEGORIAS", None))
#if QT_CONFIG(tooltip)
        self.tabWidget.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt;\">ver, agregar o editar categorias</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.tab.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Listado de categorias registradas</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.label_2.setText(QCoreApplication.translate("MainWindow", u"Descripcion", None))
#if QT_CONFIG(tooltip)
        self.txtBuscar.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Ingresa un nombre para buscar</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.btnBuscar.setText(QCoreApplication.translate("MainWindow", u"Buscar", None))
        self.btnEliminar.setText(QCoreApplication.translate("MainWindow", u"Eliminar", None))
        self.btnImprimir.setText(QCoreApplication.translate("MainWindow", u"Imprimir", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"Listado", None))
#if QT_CONFIG(tooltip)
        self.tab_2.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-size:11pt; font-weight:700;\">Agregar o editar una catedoriga</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", u"Categorias", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"Codigo", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"Nombre", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", u"Descripcion", None))
        self.btnEditar.setText(QCoreApplication.translate("MainWindow", u"Editar", None))
        self.btnGuardar.setText(QCoreApplication.translate("MainWindow", u"Guardar", None))
        self.btnSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
#if QT_CONFIG(shortcut)
        self.btnSalir.setShortcut(QCoreApplication.translate("MainWindow", u"Ctrl+S", None))
#endif // QT_CONFIG(shortcut)
#if QT_CONFIG(tooltip)
        self.txtNombre.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Ingresa el nombre de la categoria</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
#if QT_CONFIG(tooltip)
        self.txtDescripcion.setToolTip(QCoreApplication.translate("MainWindow", u"<html><head/><body><p><span style=\" font-weight:700;\">Una descripcion de la categoria</span></p></body></html>", None))
#endif // QT_CONFIG(tooltip)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"Mantenimiento", None))
    # retranslateUi

