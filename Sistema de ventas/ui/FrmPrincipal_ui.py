# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'FrmPrincipal.ui'
##
## Created by: Qt User Interface Compiler version 6.5.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QAction, QBrush, QColor, QConicalGradient,
    QCursor, QFont, QFontDatabase, QGradient,
    QIcon, QImage, QKeySequence, QLinearGradient,
    QPainter, QPalette, QPixmap, QRadialGradient,
    QTransform)
from PySide6.QtWidgets import (QApplication, QLabel, QMainWindow, QMdiArea,
    QMenu, QMenuBar, QSizePolicy, QStatusBar,
    QWidget)

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1236, 874)
        sizePolicy = QSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        MainWindow.setStyleSheet(u"")
        self.actionIndice = QAction(MainWindow)
        self.actionIndice.setObjectName(u"actionIndice")
        self.actionAcerca_de = QAction(MainWindow)
        self.actionAcerca_de.setObjectName(u"actionAcerca_de")
        self.actionSalir = QAction(MainWindow)
        self.actionSalir.setObjectName(u"actionSalir")
        self.actionArticulos = QAction(MainWindow)
        self.actionArticulos.setObjectName(u"actionArticulos")
        self.actionCategorias = QAction(MainWindow)
        self.actionCategorias.setObjectName(u"actionCategorias")
        self.actionPresentaciones = QAction(MainWindow)
        self.actionPresentaciones.setObjectName(u"actionPresentaciones")
        self.actionIngresos = QAction(MainWindow)
        self.actionIngresos.setObjectName(u"actionIngresos")
        self.actionProveedores = QAction(MainWindow)
        self.actionProveedores.setObjectName(u"actionProveedores")
        self.actionVentas = QAction(MainWindow)
        self.actionVentas.setObjectName(u"actionVentas")
        self.actionClientes = QAction(MainWindow)
        self.actionClientes.setObjectName(u"actionClientes")
        self.actionEmpleados = QAction(MainWindow)
        self.actionEmpleados.setObjectName(u"actionEmpleados")
        self.actionVentas_2 = QAction(MainWindow)
        self.actionVentas_2.setObjectName(u"actionVentas_2")
        self.actionCompras_por_fechas = QAction(MainWindow)
        self.actionCompras_por_fechas.setObjectName(u"actionCompras_por_fechas")
        self.actionStock_de_articulos = QAction(MainWindow)
        self.actionStock_de_articulos.setObjectName(u"actionStock_de_articulos")
        self.actionBack_up = QAction(MainWindow)
        self.actionBack_up.setObjectName(u"actionBack_up")
        self.actionCambiar_de_usuario = QAction(MainWindow)
        self.actionCambiar_de_usuario.setObjectName(u"actionCambiar_de_usuario")
        self.actionCotizacion = QAction(MainWindow)
        self.actionCotizacion.setObjectName(u"actionCotizacion")
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.centralwidget.setStyleSheet(u"/* Estilos comunes para varios controles */\n"
"QWidget {\n"
"    background-color: #deede3;\n"
"}")
        self.mdiArea = QMdiArea(self.centralwidget)
        self.mdiArea.setObjectName(u"mdiArea")
        self.mdiArea.setGeometry(QRect(9, 20, 1900, 900))
        sizePolicy1 = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy1.setHorizontalStretch(0)
        sizePolicy1.setVerticalStretch(0)
        sizePolicy1.setHeightForWidth(self.mdiArea.sizePolicy().hasHeightForWidth())
        self.mdiArea.setSizePolicy(sizePolicy1)
        self.mdiArea.setStyleSheet(u"")
        self.lblUsuario = QLabel(self.centralwidget)
        self.lblUsuario.setObjectName(u"lblUsuario")
        self.lblUsuario.setGeometry(QRect(10, 0, 121, 21))
        font = QFont()
        font.setBold(True)
        self.lblUsuario.setFont(font)
        self.lblUsuario.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        self.lblEmpleado = QLabel(self.centralwidget)
        self.lblEmpleado.setObjectName(u"lblEmpleado")
        self.lblEmpleado.setGeometry(QRect(140, 0, 121, 21))
        self.lblEmpleado.setFont(font)
        self.lblEmpleado.setStyleSheet(u"QWidget {\n"
"    background-color: var(--jade-50);\n"
"}\n"
"\n"
"QLabel {\n"
"    color: var(--jade-500);\n"
"    font-size: 16px;\n"
"    font-weight: bold;\n"
"}")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1236, 21))
        self.menubar.setStyleSheet(u"")
        self.menuSistema = QMenu(self.menubar)
        self.menuSistema.setObjectName(u"menuSistema")
        self.menuSistema.setStyleSheet(u"")
        self.menuHerramientas = QMenu(self.menubar)
        self.menuHerramientas.setObjectName(u"menuHerramientas")
        self.menuHerramientas.setStyleSheet(u"")
        self.menuBase_de_datos = QMenu(self.menuHerramientas)
        self.menuBase_de_datos.setObjectName(u"menuBase_de_datos")
        self.menuBase_de_datos.setStyleSheet(u"")
        self.menuAlmacen = QMenu(self.menubar)
        self.menuAlmacen.setObjectName(u"menuAlmacen")
        self.menuAlmacen.setStyleSheet(u"")
        self.menuCompras = QMenu(self.menubar)
        self.menuCompras.setObjectName(u"menuCompras")
        self.menuCompras.setStyleSheet(u"")
        self.menuVentas = QMenu(self.menubar)
        self.menuVentas.setObjectName(u"menuVentas")
        self.menuVentas.setStyleSheet(u"")
        self.menuMantenimiento = QMenu(self.menubar)
        self.menuMantenimiento.setObjectName(u"menuMantenimiento")
        self.menuMantenimiento.setStyleSheet(u"")
        self.menuConsultas = QMenu(self.menubar)
        self.menuConsultas.setObjectName(u"menuConsultas")
        self.menuConsultas.setStyleSheet(u"")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.menubar.addAction(self.menuSistema.menuAction())
        self.menubar.addAction(self.menuAlmacen.menuAction())
        self.menubar.addAction(self.menuCompras.menuAction())
        self.menubar.addAction(self.menuVentas.menuAction())
        self.menubar.addAction(self.menuMantenimiento.menuAction())
        self.menubar.addAction(self.menuConsultas.menuAction())
        self.menubar.addAction(self.menuHerramientas.menuAction())
        self.menuSistema.addAction(self.actionCambiar_de_usuario)
        self.menuSistema.addAction(self.actionSalir)
        self.menuHerramientas.addAction(self.menuBase_de_datos.menuAction())
        self.menuBase_de_datos.addAction(self.actionBack_up)
        self.menuAlmacen.addAction(self.actionArticulos)
        self.menuAlmacen.addAction(self.actionCategorias)
        self.menuAlmacen.addAction(self.actionPresentaciones)
        self.menuCompras.addAction(self.actionIngresos)
        self.menuCompras.addAction(self.actionProveedores)
        self.menuVentas.addAction(self.actionVentas)
        self.menuVentas.addAction(self.actionCotizacion)
        self.menuVentas.addAction(self.actionClientes)
        self.menuVentas.addSeparator()
        self.menuMantenimiento.addAction(self.actionEmpleados)
        self.menuConsultas.addAction(self.actionVentas_2)
        self.menuConsultas.addAction(self.actionCompras_por_fechas)
        self.menuConsultas.addAction(self.actionStock_de_articulos)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.actionIndice.setText(QCoreApplication.translate("MainWindow", u"Indice", None))
        self.actionAcerca_de.setText(QCoreApplication.translate("MainWindow", u"Acerca de", None))
        self.actionSalir.setText(QCoreApplication.translate("MainWindow", u"Salir", None))
        self.actionArticulos.setText(QCoreApplication.translate("MainWindow", u"Articulos", None))
        self.actionCategorias.setText(QCoreApplication.translate("MainWindow", u"Categorias", None))
        self.actionPresentaciones.setText(QCoreApplication.translate("MainWindow", u"Presentaciones", None))
        self.actionIngresos.setText(QCoreApplication.translate("MainWindow", u"Ingresos", None))
        self.actionProveedores.setText(QCoreApplication.translate("MainWindow", u"Proveedores", None))
        self.actionVentas.setText(QCoreApplication.translate("MainWindow", u"Ventas", None))
        self.actionClientes.setText(QCoreApplication.translate("MainWindow", u"Clientes", None))
        self.actionEmpleados.setText(QCoreApplication.translate("MainWindow", u"Empleados", None))
        self.actionVentas_2.setText(QCoreApplication.translate("MainWindow", u"Ventas por fecha", None))
        self.actionCompras_por_fechas.setText(QCoreApplication.translate("MainWindow", u"Compras por fecha", None))
        self.actionStock_de_articulos.setText(QCoreApplication.translate("MainWindow", u"Stock de articulos", None))
        self.actionBack_up.setText(QCoreApplication.translate("MainWindow", u"Back up", None))
        self.actionCambiar_de_usuario.setText(QCoreApplication.translate("MainWindow", u"Cerrar sesion", None))
        self.actionCotizacion.setText(QCoreApplication.translate("MainWindow", u"Cotizacion", None))
        self.lblUsuario.setText(QCoreApplication.translate("MainWindow", u"Usuario:", None))
        self.lblEmpleado.setText(QCoreApplication.translate("MainWindow", u"Empleado", None))
        self.menuSistema.setTitle(QCoreApplication.translate("MainWindow", u"SisVentas", None))
        self.menuHerramientas.setTitle(QCoreApplication.translate("MainWindow", u"Herramientas", None))
        self.menuBase_de_datos.setTitle(QCoreApplication.translate("MainWindow", u"Base de datos", None))
        self.menuAlmacen.setTitle(QCoreApplication.translate("MainWindow", u"Almacen", None))
        self.menuCompras.setTitle(QCoreApplication.translate("MainWindow", u"Compras", None))
        self.menuVentas.setTitle(QCoreApplication.translate("MainWindow", u"Ventas", None))
        self.menuMantenimiento.setTitle(QCoreApplication.translate("MainWindow", u"Mantenimiento", None))
        self.menuConsultas.setTitle(QCoreApplication.translate("MainWindow", u"Consultas", None))
    # retranslateUi

