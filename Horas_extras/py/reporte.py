import flet as ft
from flet import ScrollMode
from consultas import get_horas_por_fecha_pdf, get_horas_por_fecha_tabla
import os, datetime, calendar
from database import get_base_dir

from datetime import timedelta
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib.enums import TA_CENTER
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Spacer, PageTemplate, Frame, Paragraph
from reportlab.lib.units import inch
from itertools import groupby
from operator import itemgetter


#Funcion principal para iniciar la ventana con los controles.
def reporte(page: ft.Page):
    page.title = "Horas Extras"
    page.window.alignment = ft.alignment.center
    page.window.width = 1200
    page.window.height = 700
    page.window.resizable = False
    page.padding = 20
    page.scroll = False
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def tab_registro(e):
            """
            Maneja el evento de cambio de tab a "Registro".

            Limpia la página actual y llama a la función registro desde el módulo registro.py, la
            cual imprime los controles y la tabla de registro en la página actual.
            """
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from registro import registro
            registro(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------    
    
    def open_dlg_modal(e):
        """
        Opens a modal dialog by appending it to the page overlay and setting its open attribute to True.

        Args:
            e: The event object that contains the control and page information.
        """
        e.control.page.overlay.append(dlg_modal)
        dlg_modal.open = True
        e.control.page.update()
        
    def close_dlg(e):
        """
        Cierra el diálogo modal.

        :param e: Instancia de la clase Principal.
        """
        dlg_modal.open = False
        e.control.page.update()

    dlg_modal = ft.AlertDialog(
        modal=True,
        title=ft.Text("Falta información"),
        content=ft.Text("Ha dejado algun campo vacío"),
        actions=[
                    ft.TextButton("Ok", on_click=close_dlg),
                ],
        actions_alignment=ft.MainAxisAlignment.END,
        #on_dismiss=lambda e: print("Modal dialog dismissed!"),
    )
    
    # Initialize SnackBar at start
    page.snack_bar = ft.SnackBar(
        content=ft.Text(""),
        action="OK"
    )
    
    # Make nombre_seleccionado accessible
    nombre_seleccionado = None
    
    def show_snackbar(mensaje):
        """
        Muestra un mensaje en una SnackBar en la parte inferior de la pantalla.

        :param mensaje: El mensaje a mostrar en la SnackBar.
        """
        if not page.snack_bar:
            page.snack_bar = ft.SnackBar(content=ft.Text(mensaje))
        else:
            page.snack_bar.content.value = mensaje
        page.snack_bar.open = True
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    # Inicializa las fechas actuales para ambos TextField
    fecha_actual1 = datetime.date.today()
    fecha_actual2 = datetime.date.today()

    # Referencias para los campos de texto
    txt_fecha1 = ft.Ref[ft.TextField]()
    txt_fecha2 = ft.Ref[ft.TextField]()

    # Traer el número del día actual como un entero
    hoy = datetime.date.today()
    num_dia_actual = int(hoy.strftime("%d"))

    # Configuración de `fecha_actual1`
    if num_dia_actual <= 15:
        fecha_actual1 = fecha_actual1.replace(day=1)
    else:
        fecha_actual1 = fecha_actual1.replace(day=15)

    # Configuración de `fecha_actual2`
    if num_dia_actual <= 15:
        fecha_actual2 = fecha_actual2.replace(day=15)
    else:
        fecha_actual2 = fecha_actual2.replace(day=30)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    def mostrar_datepicker(e):
        """
        Abre el diálogo del DatePicker para que el usuario seleccione una fecha.
        """
        page.overlay.append(date_picker_dialog1)
        date_picker_dialog1.open = True
        page.update()

    
    def mostrar_datepicker2(e):
        """
        Abre el diálogo del DatePicker para que el usuario seleccione una fecha.

        Es llamada cuando se hace clic en el icono de calendario del segundo
        TextField.
        """
        page.overlay.append(date_picker_dialog2)
        date_picker_dialog2.open = True
        page.update()

    
    def seleccionar_fecha1(e):
        """
        Selecciona una fecha desde el DatePicker y actualiza el texto en el primer
        campo de texto con la fecha seleccionada en formato "YYYY-MM-DD".
        Luego cierra el diálogo del DatePicker.

        Args:
            e: El evento que contiene la información del control asociado.
        """
        fecha_seleccionada = date_picker_dialog1.value
        if fecha_seleccionada:
            fecha_solo = formato_fecha_usuario(str(fecha_seleccionada.date()))
            txt_fecha1.current.value = fecha_solo #.strftime("%Y-%m-%d")
            date_picker_dialog1.open = False
            
            # Actualizar tabla al cambiar de fechas
            actualizar_tabla(e=None)
            
            page.update()

    
    def seleccionar_fecha2(e):
        """
        Selecciona una fecha desde el DatePicker y actualiza el texto en el segundo
        campo de texto con la fecha seleccionada en formato "YYYY-MM-DD".
        Luego cierra el diálogo del DatePicker.

        Args:
            e: El evento que contiene la información del control asociado.
        """
        fecha_seleccionada = date_picker_dialog2.value
        if fecha_seleccionada:
            fecha_solo = formato_fecha_usuario(str(fecha_seleccionada.date()))
            txt_fecha2.current.value = fecha_solo #.strftime("%Y-%m-%d")
            date_picker_dialog2.open = False
            
            # Actualizar tabla al cambiar de fechas
            actualizar_tabla(e=None)
            
            page.update()

    # Crea el DatePicker y establece que `seleccionar_fecha` se ejecutará cuando cambie la fecha seleccionada.
    def get_rango_fechas():
        """
        Calcula rango de fechas desde primer día mes anterior hasta último día mes actual.
        
        Returns:
            tuple: (fecha_inicio, fecha_fin)
        """
        fecha_actual = datetime.datetime.now()
        
        # Primer día del mes anterior
        if fecha_actual.month == 1:
            primer_dia = datetime.datetime(fecha_actual.year - 1, 12, 1)
        else:
            primer_dia = datetime.datetime(fecha_actual.year, fecha_actual.month - 1, 1)
        
        # Último día del mes actual
        ultimo_dia = fecha_actual.replace(
            day=calendar.monthrange(fecha_actual.year, fecha_actual.month)[1]
        )
        
        return primer_dia, ultimo_dia

    # En la creación del DatePicker
    fecha_inicio, fecha_fin = get_rango_fechas()

    date_picker_dialog1 = ft.DatePicker(
        first_date=fecha_inicio,
        last_date=fecha_fin,
        current_date=datetime.datetime.now(),
        on_change=seleccionar_fecha1
    )
    
    date_picker_dialog2 = ft.DatePicker(
        first_date=fecha_inicio,
        last_date=fecha_fin,
        current_date=datetime.datetime.now(),
        on_change=seleccionar_fecha2
    )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_tabla_horas(registros):
        """
        Crea una tabla de datos con registros de horas extras.
        Args:
            registros (list of tuple): Una lista de tuplas, donde cada tupla contiene los siguientes elementos:
                - Fecha (str): La fecha del registro.
                - Código (int): El código del empleado.
                - Nombre (str): El nombre del empleado.
                - Horas 35% (str): Las horas trabajadas al 35%.
                - Horas 100% (str): Las horas trabajadas al 100%.
                - Comentario (str): Comentarios adicionales.
        Returns:
            ft.DataTable: Un objeto DataTable que contiene los registros de horas extras.
        """
        """Crea DataTable con registros de horas"""
        columns = [
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Horas 35%")),
            ft.DataColumn(ft.Text("Horas 100%")),
            ft.DataColumn(ft.Text("Comentario")),
        ]
        
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(reg[0])),  # Fecha
                    ft.DataCell(ft.Text(str(reg[1]))),  # Código
                    ft.DataCell(ft.Text(reg[2])),  # Nombre
                    ft.DataCell(ft.Text(reg[3])),  # Horas 35
                    ft.DataCell(ft.Text(reg[4])),  # Horas 100
                    ft.DataCell(ft.Text(reg[5])),  # Comentario
                ],
            ) for reg in registros
        ]
        
        return ft.DataTable(
            columns=columns,
            rows=rows,
            border=ft.border.all(1, ft.colors.GREY_400),
            border_radius=10,
            vertical_lines=ft.border.BorderSide(1, ft.colors.GREY_400, 1.0),
            horizontal_lines=ft.border.BorderSide(1, ft.colors.GREY_400),            
        )
    
    
    tabla_container = ft.Container(content=crear_tabla_horas([]))
    def actualizar_tabla(e):
        """
        Actualiza la tabla de registros de horas extras según el rango de fechas seleccionado.

        Args:
            e: El evento que desencadena la actualización.

        La función obtiene las fechas de inicio y fin seleccionadas por el usuario. 
        Si la fecha de inicio es mayor que la fecha de fin, muestra un mensaje de error 
        y sale de la función. Si las fechas son válidas, obtiene los registros de horas 
        extras correspondientes al rango de fechas y actualiza el contenido de la tabla 
        en la interfaz de usuario.
        """
        fecha_inicio = formato_fecha_bd(txt_fecha1.current.value)
        fecha_fin = formato_fecha_bd(txt_fecha2.current.value)

        # Validar si la fecha inicial es mayor a la fecha final
        if fecha_inicio > fecha_fin:
            show_snackbar("La fecha inicial no puede ser mayor que la fecha final.")
            return  # Salir de la función si las fechas no son válidas

        # Obtener los registros y actualizar la tabla
        registros = get_horas_por_fecha_tabla(fecha_inicio, fecha_fin)
        nueva_tabla = crear_tabla_horas(registros)
        tabla_container.content = nueva_tabla
        page.update()
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def sumar_tiempo(horas):
        """
        Suma una lista de tiempos en formato HH:MM y devuelve el resultado como HH:MM.
        Args:
            horas (list of str): Lista de tiempos en formato HH:MM.
        Returns:
            str: El tiempo total sumado en formato HH:MM.
        """
        """Suma una lista de tiempos en formato HH:MM y devuelve el resultado como HH:MM."""
        total_horas = 0
        total_minutos = 0

        for hora in horas:
            if isinstance(hora, str):
                partes = list(map(int, hora.split(":")))
                total_horas += partes[0]
                total_minutos += partes[1]

        # Convertir minutos sobrantes a horas
        total_horas += total_minutos // 60
        total_minutos = total_minutos % 60

        return f"{total_horas:02}:{total_minutos:02}"
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def abrir_carpeta_reporte(e):
        """
        Abre la carpeta de reportes en el explorador de Windows.
        Este método intenta abrir una carpeta específica llamada "reportes" dentro del directorio base
        obtenido por la función `get_base_dir()`. Si la carpeta no existe, se crea automáticamente.
        Luego, se abre la carpeta en el explorador de archivos de Windows.
        Args:
            e: Evento que desencadena la acción (puede ser un evento de interfaz de usuario).
        Raises:
            Exception: Si ocurre un error al intentar abrir la carpeta, se captura y muestra un mensaje
            de error en una snackbar.
        """
        """Abre la carpeta de reportes en el explorador"""
        try:
            # Obtener directorio base y construir ruta
            base_dir = get_base_dir()
            directorio_reportes = os.path.join(base_dir, "reportes")
            
            # Crear directorio si no existe
            if not os.path.exists(directorio_reportes):
                os.makedirs(directorio_reportes)
                show_snackbar("Carpeta de reportes creada")
            
            # Abrir la carpeta en el explorador de Windows
            os.startfile(directorio_reportes)
            show_snackbar("Abriendo carpeta de reportes...")
            
        except Exception as error:
            show_snackbar(f"Error al abrir carpeta: {str(error)}")
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def exportar_pdf(registros, fecha_inicio, fecha_fin):
        """
        Exporta los registros a un archivo PDF agrupados por empleado.
        Args:
            registros (list): Lista de registros donde cada registro es una lista con los siguientes elementos:
                [fecha (str), código (str), nombre (str), horas_35 (str), horas_100 (str), comentario (str)].
            fecha_inicio (str): Fecha de inicio del reporte en formato 'YYYY-MM-DD'.
            fecha_fin (str): Fecha de fin del reporte en formato 'YYYY-MM-DD'.
        Returns:
            bool: True si el PDF se generó exitosamente, False en caso contrario.
        Raises:
            FileNotFoundError: Si el logo no se encuentra en la ruta especificada.
            Exception: Cualquier otra excepción que ocurra durante la generación del PDF.
        """
        """Exporta los registros a PDF agrupados por empleado"""
        try:
            # Obtener directorio base y construir rutas
            base_dir = get_base_dir()
            directorio_reportes = os.path.join(base_dir, "reportes")
            directorio_imagenes = os.path.join(base_dir, "imagenes")
            
            # Crear directorio si no existe
            if not os.path.exists(directorio_reportes):
                os.makedirs(directorio_reportes)
                
            # Ruta del logo
            logo_path = os.path.join(directorio_imagenes, "Logo.png")
            
            # Verificar que existe el logo
            if not os.path.exists(logo_path):
                raise FileNotFoundError(f"Logo no encontrado en: {logo_path}")
            
            pdf_path = os.path.join(directorio_reportes, f'Reporte_{fecha_inicio}_{fecha_fin}.pdf')
            doc = SimpleDocTemplate(
                    pdf_path, 
                    pagesize=landscape(letter),  # Cambia orientación a horizontal
                    topMargin=0.5*inch,
                    bottomMargin=0.5*inch,
                    leftMargin=0.5*inch,
                    rightMargin=0.5*inch
                )
            elements = []
            
            # Estilo de párrafos para comentarios
            estilos = getSampleStyleSheet()
            estilo_comentarios = estilos["BodyText"]
            estilo_comentarios.wordWrap = 'CJK'  # Permite ajuste de texto
            estilo_comentarios.alignment = TA_CENTER  # Centra el texto
            
            # Agrupar por empleado
            registros.sort(key=itemgetter(2))
            for nombre, grupo in groupby(registros, key=itemgetter(2)):
                datos_empleado = list(grupo)
                
                # Calcular totales
                total_horas_35 = sumar_tiempo([reg[3] for reg in datos_empleado])
                total_horas_100 = sumar_tiempo([reg[4] for reg in datos_empleado])
                
                # Nombre para mostrar en la fila de totales
                Nombre_total = datos_empleado[0][2]
                
                # Encabezados
                encabezados = [['Fecha', 'Código', 'Nombre', 'Horas 35%', 'Horas 100%', 'Destino/Comentario']]
                
                def convertir_formato_fecha_para_tablas(fecha_str):
                    """
                    Convierte una fecha de formato 'YYYY-MM-DD' a 'DD-MMM-YYYY'.

                    Args:
                        fecha_str (str): Fecha en formato 'YYYY-MM-DD'.

                    Returns:
                        str: Fecha en formato 'DD-MMM-YYYY' si la conversión es exitosa, 
                             de lo contrario, devuelve la cadena original.
                    """
                    """Convierte fecha de YYYY-MM-DD a YYYYMMM-DD"""
                    try:
                        fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
                        meses_abrev = {
                            1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR',
                            5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AGO',
                            9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DIC'
                        }
                        return f"{fecha.day:02d}-{meses_abrev[fecha.month]}-{fecha.year}"
                    except ValueError:
                        return fecha_str
                
                # Datos + fila de totales
                datos = [
                    [
                        convertir_formato_fecha_para_tablas(reg[0]),  # Fecha
                        reg[1],  # Código
                        reg[2],  # Nombre
                        reg[3],  # Horas 35%
                        reg[4],  # Horas 100%
                        Paragraph(reg[5], estilo_comentarios),  # Comentario como párrafo
                    ]
                    for reg in datos_empleado
                ]
                datos.append(['TOTAL', '', Nombre_total, total_horas_35, total_horas_100, ''])
                
                tabla_data = encabezados + datos
                # Después de crear tabla_data, definir anchos de columna
                tabla = Table(
                    tabla_data,
                    colWidths=[
                        0.9*inch,     # Fecha
                        0.6*inch,     # Código
                        3.5*inch,       # Nombre
                        0.8*inch,     # Horas 35%
                        1.2*inch,     # Horas 100%
                        3*inch      # Comentario
                    ])

                
                # Estilo tabla
                estilo = TableStyle([
                    ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
                    ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
                    ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                    ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
                    ('FONTSIZE', (0, 0), (-1, 0), 10),
                    ('BOTTOMPADDING', (0, 0), (-1, -1), 8),  # Padding inferior
                    ('TOPPADDING', (0, 0), (-1, -1), 8),     # Padding superior
                    ('ROWHEIGHT', (0, 0), (-1, -1), 5),  # Define altura mínima de las filas
                    ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),
                    ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),
                    ('WORDWRAP', (0, 0), (-1, -1), True),     # Wrap automático
                    ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),   # Alineación vertical
                    ('GRID', (0, 0), (-1, -1), 1, colors.black),  # Add grid lines
                ])
                tabla.setStyle(estilo)
                
                elements.append(tabla)
                elements.append(Spacer(1, 30))
                
            def convertir_formato_fecha(fecha_str):
                """
                Convierte una fecha de formato 'YYYY-MM-DD' a 'DD-mes-YYYY'.

                Args:
                    fecha_str (str): Fecha en formato 'YYYY-MM-DD'.

                Returns:
                    str: Fecha en formato 'DD-mes-YYYY' con el mes en abreviatura de tres letras en español.
                          Si la fecha no es válida, se devuelve el string original.
                """
                """Convierte fecha de YYYY-MM-DD a DD-mes-YYYY"""
                try:
                    fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
                    meses = {
                        1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR',
                        5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AGO',
                        9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DIC'
                    }
                    return f"{fecha.day}-{meses[fecha.month]}-{fecha.year}"
                except ValueError:
                    return fecha_str
            
            
            def encabezado(canvas, doc):
                """
                Genera el encabezado para el reporte PDF.
                Esta función agrega un título con el rango de fechas del reporte alineado a la derecha y un logo alineado a la izquierda.
                Args:
                    canvas (Canvas): El objeto canvas para dibujar.
                    doc (Document): El objeto documento.
                Variables:
                    logo_path (str): La ruta del archivo de la imagen del logo.
                    fecha_inicio_formato (str): La fecha de inicio del reporte formateada.
                    fecha_fin_formato (str): La fecha de fin del reporte formateada.
                Funciones:
                    convertir_formato_fecha (function): Función para convertir el formato de la fecha.
                Notas:
                    Se espera que la imagen del logo esté ubicada en el directorio "imagenes" relativo al directorio de imágenes.
                """                
                logo_path = os.path.join(os.path.dirname(directorio_imagenes), "imagenes", "Logo.png")
                canvas.saveState()
                canvas.setFont("Helvetica-Bold", 14)
                
                # Título alineado a la derecha
                fecha_inicio_formato = convertir_formato_fecha(fecha_inicio)
                fecha_fin_formato = convertir_formato_fecha(fecha_fin)
                canvas.drawRightString(750, 580, f"Reporte del: {fecha_inicio_formato} al {fecha_fin_formato}")
                
                # Logo alineado a la izquierda
                if os.path.exists(logo_path):
                    canvas.drawImage(logo_path, 50, 520, width=1.5*inch, height=1.8*inch)
                
                canvas.restoreState()
        
            # Crear template de página con encabezado
            frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 0.25 * inch, id='normal')
            template = PageTemplate(id='encabezado', frames=frame, onPage=encabezado)
            doc.addPageTemplates([template])
            
            # Generar PDF
            doc.build(elements)
            show_snackbar("Reporte PDF generado exitosamente")
            abrir_carpeta_reporte(e=None)  # Abre la carpeta
            return True
            
        except Exception as e:
            show_snackbar(f"Error al exportar PDF: {str(e)}")
            return False
    # Agregar botón para exportar en la interfaz
    boton_exportar = ft.ElevatedButton(
        "Exportar a PDF",
        icon=ft.icons.PICTURE_AS_PDF,
        on_click=lambda e: exportar_pdf(
            get_horas_por_fecha_pdf(formato_fecha_bd(txt_fecha1.current.value), formato_fecha_bd(txt_fecha2.current.value)),
            txt_fecha1.current.value,
            txt_fecha2.current.value
        )
    )
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def formato_fecha_usuario(fecha_str):
            """
            Convierte una fecha de formato 'YYYY-MM-DD' a 'DD-MMM-YYYY'.

            Args:
                fecha_str (str): Fecha en formato 'YYYY-MM-DD'.

            Returns:
                str: Fecha en formato 'DD-MMM-YYYY' si la conversión es exitosa, 
                        de lo contrario, devuelve la cadena original.
            """
            """Convierte fecha de YYYY-MM-DD a YYYYMMM-DD"""
            try:
                fecha = datetime.datetime.strptime(fecha_str, '%Y-%m-%d')
                meses_abrev = {
                    1: 'ENE', 2: 'FEB', 3: 'MAR', 4: 'ABR',
                    5: 'MAY', 6: 'JUN', 7: 'JUL', 8: 'AGO',
                    9: 'SEPT', 10: 'OCT', 11: 'NOV', 12: 'DIC'
                }
                return f"{fecha.day:02d}-{meses_abrev[fecha.month]}-{fecha.year}"
            except ValueError:
                return fecha_str
            
    def formato_fecha_bd(fecha_str):
        """
        Convierte una fecha de formato 'DD-MMM-YYYY' a 'YYYY-MM-DD'.

        Args:
            fecha_str (str): Fecha en formato 'DD-MMM-YYYY'.

        Returns:
            str: Fecha en formato 'YYYY-MM-DD' si la conversión es exitosa, 
                    de lo contrario, devuelve la cadena original.
        """
        meses_abrev = {
            'ENE': 1, 'FEB': 2, 'MAR': 3, 'ABR': 4,
            'MAY': 5, 'JUN': 6, 'JUL': 7, 'AGO': 8,
            'SEPT': 9, 'OCT': 10, 'NOV': 11, 'DIC': 12
        }
        try:
            dia, mes, año = fecha_str.split('-')
            fecha = datetime.datetime(int(año), meses_abrev[mes], int(dia))
            return fecha.strftime('%Y-%m-%d')
        except ValueError:
            return fecha_str
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    
    mainTab = ft.Tabs(
        selected_index=1,  # Pestaña seleccionada por defecto al iniciar la ventana
        animation_duration=300,
        expand=True,        
        # Contenedor de tabs
        tabs=[
            ft.Tab(
                icon=ft.Icons.LIST_ALT_OUTLINED,
                text="Reportes",
                content=ft.Column(                    
                    [
                        ft.Text("Reportes de Horas Extras"),
                        ft.Row([
                            ft.Text("Desde"),
                            ft.TextField(ref=txt_fecha1, value=formato_fecha_usuario(fecha_actual1.strftime("%Y-%m-%d")), width=200, read_only=True, on_click=mostrar_datepicker),
                            ft.Text("Hasta"),
                            ft.TextField(ref=txt_fecha2, value=formato_fecha_usuario(fecha_actual2.strftime("%Y-%m-%d")), width=200, read_only=True, on_click=mostrar_datepicker2),
                            ft.ElevatedButton(text="Atras", icon=ft.Icons.ARROW_BACK, width=150, on_click=tab_registro),
                            boton_exportar,
                        ]),
                        tabla_container,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=15,
                ),
            ),
        ],
    )
    actualizar_tabla(e=None)
    page.add(mainTab)
    page.update()