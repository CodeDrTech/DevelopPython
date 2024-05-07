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

from Consultas_db import insertar_nuevo_articulo, obtener_codigo_articulo, generar_nuevo_codigo_articulo,\
                            obtener_ultimo_codigo, generar_nuevo_codigo


#---------------------------------------------Este modulo esta comentado---------------------------------------------------------
class VentanaArticulo(QMainWindow):
    # Con esta variable se le informa al formulario principal (MDI) 
    # que este formulario esta abierto y si es llamado no se abra otra vez..
    ventana_abierta = False
    
    def __init__(self):
        super().__init__()        
        uic.loadUi('Sistema de ventas/ui/FrmArticulo.ui',self)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------        
                
        # Configuraiones de la ventana principal.
        self.setWindowTitle('.:. Mantenimiento de Articulos .:.')
        self.setFixedSize(self.size())
        self.setWindowIcon(QtGui.QIcon('Sistema de ventas/imagenes/login.jpg'))
        
        self.imagen_cargada = None
        
        # Botones del formulario y sus funciones.
        self.btnGuardar.clicked.connect(self.insertar_datos)
        self.btnEditar.clicked.connect(self.editar_datos)
        self.btnBuscar.clicked.connect(self.buscar_articulo)
        self.btnLimpiar.clicked.connect(self.limpiar_imagen)
        self.btnCargar.clicked.connect(self.cargar_imagen)
        
        self.cmbCategoria.currentTextChanged.connect(self.actualizar_label_categoria)
        
        
        # Crear un efecto de sombra en el tabpage y los groupBox.       
        tabWidget_shadow = QGraphicsDropShadowEffect()
        tabWidget_shadow.setBlurRadius(20)
        tabWidget_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.tabWidget.setGraphicsEffect(tabWidget_shadow)
        
        groupBox_shadow = QGraphicsDropShadowEffect()
        groupBox_shadow.setBlurRadius(20)
        groupBox_shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox.setGraphicsEffect(groupBox_shadow)

        groupBox_2shadow = QGraphicsDropShadowEffect()
        groupBox_2shadow.setBlurRadius(20)
        groupBox_2shadow.setColor(Qt.black)# type: ignore #QColor(200, 200, 200))        
        self.groupBox_2.setGraphicsEffect(groupBox_2shadow)

        # Establecer el texto de referencia a la caja de texto buscar
        # Conectar el evento de clic para borrar el texto
        self.txtBuscar.setPlaceholderText('Buscar')        
        self.txtBuscar.mousePressEvent = self.borrarTexto
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------

    def actualizar_label_categoria(self):
        cmbText = self.cmbCategoria.currentText()
        self.label_Categoria.setText(cmbText)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def visualiza_datos(self):
        # Consulta SELECT * FROM Productos
        query = QSqlQuery()
        query.exec_(f"SELECT\
                        articulo.codigo as 'CODIGO',\
                        articulo.nombre AS 'NOMBRE',\
                        presentacion.descripcion AS 'PRESENTACION',\
                        articulo.descripcion AS 'DESCRIPCION',\
                        categoria.descripcion AS 'CATEGORIA'\
                    FROM\
                        articulo\
                    INNER JOIN\
                        categoria ON articulo.idcategoria = categoria.idcategoria\
                    INNER JOIN\
                        presentacion ON articulo.idpresentacion = presentacion.idpresentacion;")

        # Crear un modelo de tabla SQL, ejecutar el query y establecer el modelo en la tabla
        model = QSqlTableModel()
        model.setQuery(query)

        # Configura el modelo para permitir la edición
        #model.setEditStrategy(QSqlTableModel.OnFieldChange) # type: ignore

        # Establece el modelo en la tabla
        self.tbDatos.setModel(model)

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()
        # Permitir la edición en las celdas
        self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    def editar_datos(self):
        self.listado()
        # Consulta SELECT * FROM Productos
        model = QSqlTableModel()
        model.setTable("articulo")
        model.select()      
        self.tbDatos.setModel(model)
        
        # Ocultar columnas para que no sean editadas
        self.tbDatos.setColumnHidden(0, True)
        self.tbDatos.setColumnHidden(1, True)
        self.tbDatos.setColumnHidden(4, True)
        
        # Renombra las cabeceras y organiza las columnas para mojorar la vista a la informacion
        model.setHeaderData(2, Qt.Horizontal, "NOMBRE") # type: ignore
        model.setHeaderData(6, Qt.Horizontal, "PRESENTACION") # type: ignore
        model.setHeaderData(3, Qt.Horizontal, "DESCRIPCION") # type: ignore
        model.setHeaderData(5, Qt.Horizontal, "CATEGORIA") # type: ignore        

        # Ajustar el tamaño de las columnas para que se ajusten al contenido
        self.tbDatos.resizeColumnsToContents()    
        self.tbDatos.setEditTriggers(QAbstractItemView.AllEditTriggers)
    
    # Al presionar el boton editar desde el tab mantenimiento se cambia al tab
    # de listado para y se activa a edidcion.
    def listado(self):
        self.tabWidget.setCurrentIndex(0)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------    
    def insertar_datos(self):
        
        
        try:
            # Almacena en las variables los datos insertados en los controles
            # del formulario.
            codigoventa = self.txtCodArt.text().upper()
            nombre = self.txtNombre.text().upper()
            descripcion = self.txtDescripcion.toPlainText().upper()
            categoria = self.cmbCategoria.currentText()
            presentacion = self.cmbPresentacion.currentText()
            
            # Evalua si alguna de las variables que almacena datos de los controles
            # esta vacia, ya que algunas son NOT NULL para la base datos.
            if  not all([codigoventa, nombre, categoria, presentacion]):
    
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Faltan datos importantes")
                mensaje.setText("Por favor, complete todos los campos.")
                mensaje.exec_()
            
            
            else:
                # Si todo es correcto se envian los datos a la funcion que inserta los datos.                
                insertar_nuevo_articulo(codigoventa, nombre, descripcion, self.imagen_cargada, categoria, presentacion)
                
                
                # Se obtiene el nuevo codigo del articulo basado en el anterior +1
                # para ser insertado en el proximo registro de articulo.
                ultimo_codigo = obtener_codigo_articulo("articulo")
                nuevo_codigo = generar_nuevo_codigo_articulo("ART",ultimo_codigo)
                self.visualiza_datos()
        
                # Mensaje al usuario.
                mensaje = QMessageBox()
                mensaje.setIcon(QMessageBox.Critical)
                mensaje.setWindowTitle("Agregar articulo")
                mensaje.setText("Articulo registrado.")
                mensaje.exec_()
                
                
                #Limpia los TexBox, la imagen si hay y coloca el nuevo codigo en codigoVEnta.
                self.actualizar_ID_articulo()
                self.txtCodArt.setText(nuevo_codigo)
                self.txtNombre.setText("")
                self.txtDescripcion.setPlainText("")
                self.limpiar_imagen()
                self.cmbCategoria.setCurrentText("")
                self.cmbPresentacion.setCurrentText("")
                self.txtNombre.setFocus()
        except Exception as e:
            # Mensaje de error al usuario en caso que surja.
            mensaje = QMessageBox()
            mensaje.setIcon(QMessageBox.Critical)
            mensaje.setWindowTitle("Error")
            mensaje.setText(f"Se produjo un error: {str(e)}")
            mensaje.exec_()
            
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
    def buscar_articulo(self):
        # Variables con datos de los inputs para usar como criterios/filtros de busquedas
        buscar_nombre = self.txtBuscar.text()

        if not buscar_nombre:
            self.visualiza_datos()
        else:    
            query = QSqlQuery()
            query.exec_(f"SELECT\
                        articulo.codigo as 'CODIGO',\
                        articulo.nombre AS 'NOMBRE',\
                        presentacion.descripcion AS 'PRESENTACION',\
                        articulo.descripcion AS 'DESCRIPCION',\
                        categoria.descripcion AS 'CATEGORIA'\
                    FROM\
                        articulo\
                    INNER JOIN\
                        categoria ON articulo.idcategoria = categoria.idcategoria\
                    INNER JOIN\
                        presentacion ON articulo.idpresentacion = presentacion.idpresentacion\
                    WHERE articulo.nombre LIKE '%{buscar_nombre}%';")
                
                
            # Crear un modelo de tabla SQL ejecuta el query y establecer el modelo en la tabla
            model = QSqlTableModel()    
            model.setQuery(query)        
            self.tbDatos.setModel(model)

            # Ajustar el tamaño de las columnas para que se ajusten al contenido
            self.tbDatos.resizeColumnsToContents()
            self.tbDatos.setEditTriggers(QAbstractItemView.NoEditTriggers)
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
    def cargar_categoria(self):    
        # Obtiene los datos de la columna Nombre abreviados de la tabla categoria
        # y los inserta en el ComboBox categoria del formulario.
        model = QSqlTableModel()
        model.setTable('categoria')
        model.select()
        column_name = []
        for i in range(model.rowCount()):
            column_name.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Nombre de la tabla articulos en el QComboBox categoria del formulario.
        combo_model_categoria = QStandardItemModel()
        for item in column_name:
            combo_model_categoria.appendRow(QStandardItem(str(item)))
        self.cmbCategoria.setModel(combo_model_categoria)
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------          
    def cargar_presentacion(self):    
        # Obtiene los datos de la columna Nombre abreviados de la tabla presentacion
        # y los inserta en el ComboBox presentacion del formulario.
        model = QSqlTableModel()
        model.setTable('presentacion')
        model.select()
        column_name = []
        for i in range(model.rowCount()):
            column_name.append(model.data(model.index(i, 1)))
        
        # Cargar los datos de la columna Nombre de la tabla articulos en el QComboBox presentacion del formulario.
        combo_model_presentacion = QStandardItemModel()
        for item in column_name:
            combo_model_presentacion.appendRow(QStandardItem(str(item)))
        self.cmbPresentacion.setModel(combo_model_presentacion)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------         
    def actualizar_ID_articulo(self):
        # Al cargar el formulario se insertan en el control codigo idarticulo
        # este proviene de la tabla
        ultimo_codigo = obtener_ultimo_codigo("articulo","idarticulo")
        nuevo_codigo = generar_nuevo_codigo(ultimo_codigo)
        self.txtCodigo.setText(nuevo_codigo)
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------              
    def closeEvent(self, event):
        # Se le informa al formulario principal (MDI) que este formulario esta cerrado
        # y si es llamado se abra.
        VentanaArticulo.ventana_abierta = False  # Cuando se cierra la ventana, se establece en False
        event.accept()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------          
    def showEvent(self, event):
        super().showEvent(event)
        self.actualizar_ID_articulo()
        self.cargar_presentacion()
        self.cargar_categoria() 
        self.visualiza_datos()
        self.actualizar_label_categoria()

        # Al cargar el formulario se insertan en el control codigo. Barr 
        # el codigo siguiente siguiendo una secuencia de uso para los nuevos articulos.
        ultimo_codigo = obtener_codigo_articulo("articulo")
        nuevo_codigo = generar_nuevo_codigo_articulo("ART",ultimo_codigo)
        self.txtCodArt.setText(nuevo_codigo)
        
        
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------
    # Elimina el texto de referencia que tiene la casilla buscar
    def borrarTexto(self, event):
        # Borrar el texto cuando se hace clic
        self.txtBuscar.clear()
#------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------     
        
if __name__ == '__main__':
    app = QApplication(sys.argv)       
    GUI = VentanaArticulo()
    GUI.show()
    sys.exit(app.exec_())