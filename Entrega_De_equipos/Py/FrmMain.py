import sys
import io

from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication, QMessageBox, QAbstractItemView,\
                        QGraphicsScene, QGraphicsPixmapItem, QGraphicsDropShadowEffect
from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtSql import QSqlTableModel, QSqlQuery
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QPixmap

from PIL import Image


from Py.Conexion_db import connect_to_db


# Correccion de error de ejecucion <enum>Qt::NonModal</enum>
#---------------------------------------------Este modulo esta comentado---------------------------------------------------------
class VentanaArticulo(QMainWindow):
    # Con esta variable se le informa al formulario principal (MDI) 
    # que este formulario esta abierto y si es llamado no se abra otra vez..
    ventana_abierta = False
    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Entrega_De_equipos/Ui/FrmMain.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Registro de enga de equipos .:.')
        self.setFixedSize(self.size())
        
        self.setWindowIcon(QtGui.QIcon('Entrega_De_equipos/Png/configuracion.png'))
        
        #self.imagen_cargada = None
        
        # Botones del formulario y sus funciones.
        #self.btnGuardar.clicked.connect(self.insertar_datos)
        #self.btnEditar.clicked.connect(self.editar_datos)
        self.btnBuscar.clicked.connect(self.obtener_datos_usuarios)
        self.btnLimpiar.clicked.connect(self.limpiar_imagen)
        self.btnCargar.clicked.connect(self.cargar_imagen)
        
        
        # Crear un efecto de sombra en el tabpage y los groupBox.       
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tabContrato.setGraphicsEffect(tabWidget_shadow)
        
        groupBox_shadow = QGraphicsDropShadowEffect()
        groupBox_shadow.setBlurRadius(20)
        groupBox_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(groupBox_shadow)

        groupBox_2shadow = QGraphicsDropShadowEffect()
        groupBox_2shadow.setBlurRadius(20)
        groupBox_2shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_2.setGraphicsEffect(groupBox_2shadow)
        
        groupBox_2shadow = QGraphicsDropShadowEffect()
        groupBox_2shadow.setBlurRadius(20)
        groupBox_2shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_3.setGraphicsEffect(groupBox_2shadow)
        
        groupBox_2shadow = QGraphicsDropShadowEffect()
        groupBox_2shadow.setBlurRadius(20)
        groupBox_2shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_4.setGraphicsEffect(groupBox_2shadow)
        
        groupBox_2shadow = QGraphicsDropShadowEffect()
        groupBox_2shadow.setBlurRadius(20)
        groupBox_2shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_5.setGraphicsEffect(groupBox_2shadow)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
# Obtener todos los usuarios ordenados del más reciente al más antiguo
    def obtener_datos_usuarios(self):
        db = connect_to_db()  # Llama a la función para abrir la conexión
        
        if db is None:
            QMessageBox.critical(self, "Error", "No se pudo conectar a la base de datos.")
            return
        
        
        query.exec_(f"SELECT * FROM Usuario")
        
        # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
        model = QSqlTableModel()    
        model.setQuery(query)        
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()
        self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Al presionar el boton editar desde el tab mantenimiento se cambia al tab
    # de listado para y se activa a edidcion.
    #def listado(self):
        #self.tabWidget.setCurrentIndex(0)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def cargar_imagen(self):
        # Abre un cuadro de diálogo para seleccionar un archivo de imagen
        opciones = QFileDialog.Options()
        opciones |= QFileDialog.ReadOnly  # Asegura que el archivo seleccionado sea solo de lectura
        archivo_imagen, _ = QFileDialog.getOpenFileName(None, "Seleccionar imagen", "", "Imágenes (*.png *.jpg *.jpeg *.bmp *.gif);;Todos los archivos (*)", options=opciones)

        if archivo_imagen:
            # Carga la imagen seleccionada usando Pillow (PIL)
            try:
                imagen = Image.open(archivo_imagen)
                # Convierte la imagen en datos binarios
                imagen_bytes = io.BytesIO()
                imagen.save(imagen_bytes, format='PNG')  # Puedes ajustar 'PNG' a 'JPEG' u otro formato si es necesario
                imagen_data = imagen_bytes.getvalue()
                # Aquí puedes usar "imagen_data" para almacenar o mostrar la imagen según tus necesidades
                # Por ejemplo, puedes asignarla a un widget de imagen en tu interfaz gráfica
                
                # Crea una escena y un elemento gráfico de mapa de bits
                scene = QGraphicsScene()
                pixmap = QPixmap()
                pixmap.loadFromData(imagen_data)
                pixmap_item = QGraphicsPixmapItem(pixmap)
            
                # Agrega el elemento gráfico a la escena
                scene.addItem(pixmap_item)
            
                # Establece la escena en el QGraphicsView
                self.gFoto.setScene(scene)
                self.scene = scene
                # Ajusta la vista para que la imagen ocupe todo el espacio disponible en el QGraphicsView
                self.gFoto.fitInView(scene.sceneRect(), Qt.KeepAspectRatio)   # type: ignore
                self.imagen_cargada = imagen_data
                return imagen_data
            except Exception as e:
                # Muestra un mensaje de error utilizando QMessageBox
                mensaje_error = QMessageBox()
                mensaje_error.setIcon(QMessageBox.Critical)
                mensaje_error.setWindowTitle("Error al cargar la imagen")
                mensaje_error.setText(f"Se produjo un error al cargar la imagen: {str(e)}")
                mensaje_error.exec_()
    
        return None
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    

#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    #Limpiar la seccion de imaen en casod e que haya alguna.
    def limpiar_imagen(self):
        try:
            self.scene.clear()
        except Exception as e:
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("No hay imagen en la caja")
            mensaje.setText(f"Falta la imagen en: {str(e)}")
            mensaje.exec_()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
    def showEvent(self, event):
        super().showEvent(event)
        self.obtener_datos_usuarios()
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------     
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaArticulo()
    GUI.show()
    sys.exit(app.exec_())