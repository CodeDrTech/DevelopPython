import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QGraphicsDropShadowEffect
from PyQt5 import QtGui
from PyQt5.QtSql import QSqlTableModel
from PyQt5.QtCore import QDateTime, Qt
from FrmPrincipal import VentanaPrincipal
from Consultas_db import insertar_datos_sesion


class VentanaLogin(QMainWindow):
    ventana_abierta = False
    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmLogin.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Acceso al sistema de ventas .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/png/folder.png'))
        
        txtFecha_shadow = QGraphicsDropShadowEffect()
        txtFecha_shadow.setBlurRadius(20)
        txtFecha_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.txtFecha.setGraphicsEffect(txtFecha_shadow)
        
        groupBox_shadow = QGraphicsDropShadowEffect()
        groupBox_shadow.setBlurRadius(20)
        groupBox_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(groupBox_shadow)
        
        graphicsView_shadow = QGraphicsDropShadowEffect()
        graphicsView_shadow.setBlurRadius(20)
        graphicsView_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.graphicsView.setGraphicsEffect(graphicsView_shadow)
        
        self.setTabOrder(self.txtUsuario, self.txtPassword)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnIngresar.clicked.connect(self.validar_usuario)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------ 

    def visualizar_datos(self):
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("empleado")
        model.select()        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def obtener_codigo_empleado(self, usuario):
        model = QSqlTableModel()
        model.setTable('empleado')
        model.select()
        
            
        # Encuentra el índice de la columna "usuario"
        usuario_column_index = model.fieldIndex("usuario")
    
        # Itera a través de las filas para encontrar el usuario
        for row in range(model.rowCount()):
            index = model.index(row, usuario_column_index)
            if model.data(index) == usuario:
                # Si se encuentra el usuario, devuelve el número de fila
                return row
    
        # Si no se encuentra el usuario, devuelve None
        return -1
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------     
    def abrir_FrmPrincipal_admin(self, rol, nombre_usuario):
        
        self.llamar_venana_principal = VentanaPrincipal()
        self.llamar_venana_principal.administrador()
        self.llamar_venana_principal.showMaximized()
        self.llamar_venana_principal.etiqueta_usuario(rol, nombre_usuario)        
        self.hide()
        
    def abrir_FrmPrincipal_almacen(self, rol,  nombre_usuario):
        
        self.llamar_venana_principal = VentanaPrincipal()
        self.llamar_venana_principal.almacen()
        self.llamar_venana_principal.showMaximized()
        self.llamar_venana_principal.etiqueta_usuario(rol, nombre_usuario)
        self.hide()
        
    def abrir_FrmPrincipal_vendedor(self, rol, nombre_usuario):
        
        self.llamar_venana_principal = VentanaPrincipal()
        self.llamar_venana_principal.vendedor()
        self.llamar_venana_principal.showMaximized()
        self.llamar_venana_principal.etiqueta_usuario(rol, nombre_usuario)
        self.hide()
        
        
    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------      
        
    def obtener_datos_de_fila(self, fila_id):
        # Obtener el modelo de datos del QTableView
        modelo = self.tbDatos.model()
        if modelo is not None and 0 <= fila_id < modelo.rowCount():
            
            # Obtener los datos de la fila seleccionada
            columna_0 = modelo.index(fila_id, 0).data()
            columna_1 = modelo.index(fila_id, 1).data()
            columna_2 = modelo.index(fila_id, 2).data()
            columna_9 = modelo.index(fila_id, 9).data()
            columna_10 = modelo.index(fila_id, 10).data()
            columna_11 = modelo.index(fila_id, 11).data()
            
            self.valor_columna_0 = columna_0
            self.valor_columna_1 = columna_1
            self.valor_columna_2 = columna_2
            self.valor_columna_9 = columna_9
            self.valor_columna_10 = columna_10
            self.valor_columna_11 = columna_11
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------             
    def validar_usuario(self):
        password = self.txtPassword.text()
        usuario = self.txtUsuario.text()
        fecha_y_hora = QDateTime.currentDateTime()
        fechaHora_formateada = fecha_y_hora.toString('yyyy-MM-dd HH:mm:ss')
        try:
            fila = self.obtener_codigo_empleado(usuario)
            self.obtener_datos_de_fila(fila)
            bd_usuadrio_id = self.valor_columna_0
            bd_nombre = self.valor_columna_1
            bd_apellidos = self.valor_columna_2
            bd_rol = self.valor_columna_9
            bd_usuario = self.valor_columna_10
            bd_password = self.valor_columna_11
        
        
            if not usuario or not password and fila == -1:
            
            
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            else:
                if bd_rol == "Administrador":    
                    if usuario == bd_usuario and password == bd_password:
                        
                        self.abrir_FrmPrincipal_admin(bd_rol, bd_nombre)
                        self.insertar_sesion(bd_usuadrio_id, bd_nombre, bd_apellidos, bd_usuario, bd_rol, fechaHora_formateada)
                    else:
                        mensaje = QMessageBox()
                        mensaje.setIcon(QMessageBox.Critical)
                        mensaje.setWindowTitle("Error de datos")
                        mensaje.setText("Usuario o contraseña incorrecto.")
                        mensaje.exec_()
                        self.txtPassword.setText("")
                        self.txtUsuario.setText("")
                        self.txtUsuario.setFocus()
                        
                elif bd_rol == "Vendedor":
                    if usuario == bd_usuario and password == bd_password:
                        self.abrir_FrmPrincipal_vendedor(bd_rol, bd_nombre)
                        self.insertar_sesion(bd_usuadrio_id, bd_nombre, bd_apellidos, bd_usuario, bd_rol, fechaHora_formateada)
                        
                    else:
                        mensaje = QMessageBox()
                        mensaje.setIcon(QMessageBox.Critical)
                        mensaje.setWindowTitle("Error de datos")
                        mensaje.setText("Usuario o contraseña incorrecto.")
                        mensaje.exec_()
                        self.txtPassword.setText("")
                        self.txtUsuario.setText("")
                        self.txtUsuario.setFocus()
                        
                else:
                    if usuario == bd_usuario and password == bd_password:
                        self.abrir_FrmPrincipal_almacen(bd_rol, bd_nombre)
                        self.insertar_sesion(bd_usuadrio_id, bd_nombre, bd_apellidos, bd_usuario, bd_rol, fechaHora_formateada)
                        
                    else:
                        mensaje = QMessageBox()
                        mensaje.setIcon(QMessageBox.Critical)
                        mensaje.setWindowTitle("Error de datos")
                        mensaje.setText("Usuario o contraseña incorrecto.")
                        mensaje.exec_()
                        self.txtPassword.setText("")
                        self.txtUsuario.setText("")
                        self.txtUsuario.setFocus()
        except Exception as e:
            # Maneja la excepción aquí.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
            self.txtPassword.setText("")
            self.txtUsuario.setText("")
            self.txtUsuario.setFocus()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def insertar_sesion(self, empleadoId, nombre, apellidos, usuario, rol, fechaHora):
        try:


            insertar_datos_sesion(empleadoId, nombre, apellidos, usuario, rol, fechaHora)


        except Exception as e:
            # Maneja la excepción aquí, puedes mostrar un mensaje de error o hacer lo que necesites.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()


#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def fn_Salir(self):
        self.close()
        
    def closeEvent(self, event):
        VentanaLogin.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
        
    def showEvent(self, event):
        super().showEvent(event)
        
        self.tbDatos.hide()
        self.visualizar_datos()        
        fecha_hora = QDateTime.currentDateTime()
        self.txtFecha.setDateTime(fecha_hora)
        self.txtUsuario.setFocus()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------                     
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaLogin()
    GUI.show()
    sys.exit(app.exec_())