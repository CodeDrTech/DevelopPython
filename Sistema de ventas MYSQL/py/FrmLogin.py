import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QGraphicsDropShadowEffect, QGraphicsScene, QTableWidgetItem
from PyQt5 import QtGui
from PyQt5.QtGui import QPixmap
from PyQt5.QtSql import QSqlDatabase, QSqlQuery, QSqlTableModel
from PyQt5.QtCore import QDateTime, Qt
from FrmPrincipal import VentanaPrincipal
import pymysql
import json
from Conexion_db import connect_to_db
from Consultas_db import insertar_datos_sesion

#---------------------------------------------Este modulo esta comentado---------------------------------------------------------
class VentanaLogin(QMainWindow):
    ventana_abierta = False
    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmLogin.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        # Configuracion de la ventana
        self.setWindowTitle('.:. Acceso al sistema de ventas .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/imagenes/login.jpg'))
        
        # crea efecto de sombra en la fecha hora, groupBox y graphicsView.
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
        
        # Establece el orden en las cajas de textos al usar la tecla tab para pasar de una caja a otra.
        self.setTabOrder(self.txtUsuario, self.txtPassword)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
        # Botones del formulario conectados a funciones.
        self.btnSalir.clicked.connect(self.fn_Salir)
        self.btnIngresar.clicked.connect(self.validar_usuario)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Funcion para cargar una imgen en el graphicsView de la ventana de login.
    def cargar_imagen(self):
        # Crea una instancia de QGraphicsScene
        scene = QGraphicsScene()

        # Carga una imagen en la escena
        pixmap = QPixmap('Sistema de ventas/imagenes/login.jpg')  # Ruta de la imagen
        scene.addPixmap(pixmap)

        # Establece la escala de la vista para que se ajuste automáticamente al tamaño de la ventana
        self.graphicsView.setScene(scene)
        self.graphicsView.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)  # type: ignore # El valor 1 es para ajustar la vista

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------  

    def visualizar_datos(self):
        # Conectar a la base de datos usando la función definida en Conexion_db.py
        conn = connect_to_db()
        if conn is not None:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM empleado")
            results = cursor.fetchall()

            # Configurar QTableWidget
            self.tbDatos.setRowCount(len(results))
            self.tbDatos.setColumnCount(len(results[0]))
            self.tbDatos.setHorizontalHeaderLabels([i[0] for i in cursor.description])

            # Rellenar datos en QTableWidget
            for row_index, row_data in enumerate(results):
                for column_index, data in enumerate(row_data):
                    self.tbDatos.setItem(row_index, column_index, QTableWidgetItem(str(data)))

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()

            # Cerrar la conexión
            conn.close()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    # Obtiene el codigo de idempleado de la tabla empleado al pasarle como parametro el nombre
    # de usuario que viene de la caja de texto de la ventana de login. Este codigo de usuario
    # se usa para obtener datos como contrasena entre otras cosas.
    def obtener_codigo_empleado(self, usuario):
        conn = connect_to_db()
        if conn is not None:
            try:
                cursor = conn.cursor()
                query = "SELECT idempleado FROM empleado WHERE usuario = %s"
                cursor.execute(query, (usuario,))
                result = cursor.fetchone()
                if result:
                    return result[0]  # Devuelve el código de empleado si se encontró el usuario
                else:
                    return None  # Devuelve None si no se encontró el usuario
            except Exception as e:
                print("Error al ejecutar la consulta:", str(e))
                return None  # Devuelve None en caso de error
            finally:
                conn.close()
        else:
            return None  # Devuelve None si no se pudo conectar a la base de datos


        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------     
    # Abre el formulario principal habilitando o no las funciones correspondiente al rol de usuario
    # que ha iniciado sesion, sea admin, vendedor o almacenista.
    def abrir_FrmPrincipal_admin(self, rol, nombre_usuario):
        
        self.llamar_venana_principal = VentanaPrincipal()
        self.llamar_venana_principal.administrador()
        self.llamar_venana_principal.showMaximized()
        self.llamar_venana_principal.etiqueta_usuario(rol, nombre_usuario)        
        self.hide() # Oculto el formulario de login al iniciar la ventana principal.
        
    def abrir_FrmPrincipal_almacen(self, rol,  nombre_usuario):
        
        self.llamar_venana_principal = VentanaPrincipal()
        self.llamar_venana_principal.almacen()
        self.llamar_venana_principal.showMaximized()
        self.llamar_venana_principal.etiqueta_usuario(rol, nombre_usuario)
        self.hide() # Oculto el formulario de login al iniciar la ventana principal.
        
    def abrir_FrmPrincipal_vendedor(self, rol, nombre_usuario):
        
        self.llamar_venana_principal = VentanaPrincipal()
        self.llamar_venana_principal.vendedor()
        self.llamar_venana_principal.showMaximized()
        self.llamar_venana_principal.etiqueta_usuario(rol, nombre_usuario)
        self.hide() # Oculto el formulario de login al iniciar la ventana principal.
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------      
    # Al pasar el numero de fila de la tabla como parametro se obtienen los datos de los indices
    # de esa fila.
    def obtener_datos_de_fila(self, fila_id):
        # Verificar que el índice de fila sea válido
        if 0 <= fila_id < self.tbDatos.rowCount():
            # Almacenar los datos de la fila en variables
            self.columna_0 = self.tbDatos.item(fila_id, 0).text() if self.tbDatos.item(fila_id, 0) else None
            self.columna_1 = self.tbDatos.item(fila_id, 1).text() if self.tbDatos.item(fila_id, 1) else None
            self.columna_2 = self.tbDatos.item(fila_id, 2).text() if self.tbDatos.item(fila_id, 2) else None
            self.columna_9 = self.tbDatos.item(fila_id, 9).text() if self.tbDatos.item(fila_id, 9) else None
            self.columna_10 = self.tbDatos.item(fila_id, 10).text() if self.tbDatos.item(fila_id, 10) else None
            self.columna_11 = self.tbDatos.item(fila_id, 11).text() if self.tbDatos.item(fila_id, 11) else None
            
            return True
        else:
            return False
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------             
    # Evalua el usuario y la contrasena que se ingreso en la ventana login para buscarlo en la base de
    # datos y evaluar si es correcto el usuario insertado, si el usuario es correcto se verifica si es 
    # un usuario administrador, vendedor o de almacen.
    def validar_usuario(self):
        # usuario y contrasena se obtienen de las cajas de texto de la ventana login.
        password = self.txtPassword.text()
        usuario = self.txtUsuario.text()
        
        # Se obtiene la fecha y hora actual del control para insertar en la base de datos
        # la fehca y hora que el usuario ingreso al sistema.
        fecha_y_hora = QDateTime.currentDateTime()
        fechaHora_formateada = fecha_y_hora.toString('yyyy-MM-dd HH:mm:ss')
        
        try:
            # Obtengo el idempleado que tambien es el numero de fila del mismo
            # para sacar los datos de la tabla y ser usado para el ingreso del usuario
            fila = self.obtener_codigo_empleado(usuario)
            self.obtener_datos_de_fila(fila)
            
            # Datos recibidos de las funciones anteriores para evaluar el usuario y su rol
            bd_usuadrio_id = self.columna_0
            bd_nombre = self.columna_1
            bd_apellidos = self.columna_2
            bd_rol = self.columna_9
            bd_usuario = self.columna_10
            bd_password = self.columna_11
            
            print(bd_usuadrio_id, bd_nombre, bd_apellidos, bd_rol, bd_usuario, bd_password)
            
            
            # Nombre y apellidos para ser enviados al femprincipal para identificar el
            # usuario que inicio sesion con su nombre en la pantalla arriba a la izquierda.
            nombre_apellido = (bd_nombre + " " + bd_apellidos).title() # Obliga a que el nombre salga con la primera letra mayuscula.
        
            # Si no se insertan los datos a los controles y la funcion obtener_codigo_empleado
            # no devolvio informacion se envia un mensaje al usuario.
            if not usuario or not password and fila == -1:            
            
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
                
                self.txtPassword.setText("")
                self.txtUsuario.setText("")
                self.txtUsuario.setFocus()
            
            else:
                # Evaluamos si el usuario que inicia sesion es un administrador , Vendedor o de almacen
                # se le da el acceso al formulario correspondiente, el usuario de cada empleado es 
                # unico e irepetible en la base de datos.
                if bd_rol == "Administrador":
                    
                    # Si el usuario que se inserta en el login coincide con la contrasena que esta
                    # en el campo password correspodiente a ese usuario se le da acceso.     
                    if usuario == bd_usuario and password == bd_password:
                        
                        self.abrir_FrmPrincipal_admin(bd_rol, nombre_apellido)
                        
                        # Se inserta un registro en la tabla sesiones con los datos del usuario que inicio sesion.
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
                        self.abrir_FrmPrincipal_vendedor(bd_rol, nombre_apellido)
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
                        self.abrir_FrmPrincipal_almacen(bd_rol, nombre_apellido)
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
            
            # Mensaje de error al usuario en caso que surja uno.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
            
            # Limpia las cajas de textos.
            self.txtPassword.setText("")
            self.txtUsuario.setText("")
            self.txtUsuario.setFocus()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # insertar un registro en la base de datos del usuario que inicia sesion.
    def insertar_sesion(self, empleadoId, nombre, apellidos, usuario, rol, fechaHora):
        try:
            conn = connect_to_db()
            if conn is not None:
                cursor = conn.cursor()
                query = "INSERT INTO sesiones (idempleado, nombre, apellidos, usuario, rol, fecha) VALUES (%s, %s, %s, %s, %s, %s)"
                cursor.execute(query, (empleadoId, nombre, apellidos, usuario, rol, fechaHora))
                conn.commit()
                cursor.close()
                conn.close()
        except Exception as e:
            # Mensaje de error al usuario en caso que surja uno.
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
        
        # Carga la imagen en el cuadro de imgen en la ventana del login.
        self.cargar_imagen()
        
        # Oculta el tableView que carga los datos del empleado que
        # van a ser usado para el inicio de sesion.
        self.tbDatos.hide() 
        
        # Carga los datos de los empleados al tableView tbDatos que esta oculto. 
        self.visualizar_datos()
        
        # Carga la fecha actual al control de fechas que esta en el formulario.        
        fecha_hora = QDateTime.currentDateTime()
        self.txtFecha.setDateTime(fecha_hora)
        
        # Establece el foco en la caja de texto usuario.
        self.txtUsuario.setFocus()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------                     
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaLogin()
    GUI.show()
    sys.exit(app.exec_())