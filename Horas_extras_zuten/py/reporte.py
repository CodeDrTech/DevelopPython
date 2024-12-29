import flet as ft
from flet import ScrollMode
from consultas import get_horas_por_fecha_pdf, get_horas_por_fecha_tabla
import os, datetime, calendar

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
    page.scroll = ScrollMode.ADAPTIVE
    page.bgcolor = "#e7e7e7"
    page.theme_mode = ft.ThemeMode.LIGHT

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    #Funcion para manejar diferentes eventos al seleccionar algunos de los tab
    def tab_registro(e):
            page.clean()

            # Importamos y ejecutamos la función y sus controles en la página actual
            from registro import registro
            registro(page)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------    
    # funciones y control para abrir cuadro de dialogo para avisar al usuario que faltan datos en tab Registrar Usuario.
    def open_dlg_modal(e):
        e.control.page.overlay.append(dlg_modal)
        dlg_modal.open = True
        e.control.page.update()
        
    def close_dlg(e):
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

    # Función para mostrar el DatePicker del primer TextField
    def mostrar_datepicker(e):
        page.overlay.append(date_picker_dialog1)
        date_picker_dialog1.open = True
        page.update()

    # Función para mostrar el DatePicker del segundo TextField
    def mostrar_datepicker2(e):
        page.overlay.append(date_picker_dialog2)
        date_picker_dialog2.open = True
        page.update()

    # Función para seleccionar la fecha del primer TextField
    def seleccionar_fecha1(e):
        fecha_seleccionada = date_picker_dialog1.value
        if fecha_seleccionada:
            fecha_solo = fecha_seleccionada.date()
            txt_fecha1.current.value = fecha_solo.strftime("%Y-%m-%d")
            date_picker_dialog1.open = False
            page.update()

    # Función para seleccionar la fecha del segundo TextField
    def seleccionar_fecha2(e):
        fecha_seleccionada = date_picker_dialog2.value
        if fecha_seleccionada:
            fecha_solo = fecha_seleccionada.date()
            txt_fecha2.current.value = fecha_solo.strftime("%Y-%m-%d")
            date_picker_dialog2.open = False
            page.update()

    # DatePicker para el primer TextField
    date_picker_dialog1 = ft.DatePicker(
        first_date=fecha_actual1.replace(day=1),
        last_date=fecha_actual1.replace(day=calendar.monthrange(fecha_actual1.year, fecha_actual1.month)[1]),
        current_date=datetime.datetime.now(),
        on_change=seleccionar_fecha1
    )

    # DatePicker para el segundo TextField
    date_picker_dialog2 = ft.DatePicker(
        first_date=fecha_actual2.replace(day=1),
        last_date=fecha_actual2.replace(day=calendar.monthrange(fecha_actual2.year, fecha_actual2.month)[1]),
        current_date=datetime.datetime.now(),
        on_change=seleccionar_fecha2
    )

#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_tabla_horas(registros):
        """Crea DataTable con registros de horas"""
        columns = [
            ft.DataColumn(ft.Text("Fecha")),
            ft.DataColumn(ft.Text("Código")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Horas 35%")),
            ft.DataColumn(ft.Text("Horas 100%")),
            ft.DataColumn(ft.Text("Nocturnas")),
        ]
        
        rows = [
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(reg[0])),  # Fecha
                    ft.DataCell(ft.Text(str(reg[1]))),  # Código
                    ft.DataCell(ft.Text(reg[2])),  # Nombre
                    ft.DataCell(ft.Text(reg[3])),  # Horas 35
                    ft.DataCell(ft.Text(reg[4])),  # Horas 100
                    ft.DataCell(ft.Text(reg[5])),  # Nocturnas
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
    # Contenedor para la tabla
    tabla_container = ft.Container(content=crear_tabla_horas([]))
    def actualizar_tabla(e):
        fecha_inicio = txt_fecha1.current.value
        fecha_fin = txt_fecha2.current.value

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
    def abrir_carpeta_reporte():
        # Ruta donde se guarda el PDF
        ruta_reporte = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "reportes")
        
        # Asegurar que la carpeta existe
        if not os.path.exists(ruta_reporte):
            os.makedirs(ruta_reporte)
        
        # Abrir la carpeta en el explorador de Windows
        os.startfile(ruta_reporte)
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def exportar_pdf(registros, fecha_inicio, fecha_fin):
        """Exporta los registros a PDF agrupados por empleado"""
        try:
            # Obtener directorio actual y construir ruta
            directorio_actual = os.path.dirname(os.path.abspath(__file__))
            directorio_reportes = os.path.join(os.path.dirname(directorio_actual), "reportes")
            
            # Crear directorio si no existe
            if not os.path.exists(directorio_reportes):
                os.makedirs(directorio_reportes)
            
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
            
            # Estilo de párrafos
            estilos = getSampleStyleSheet()
            
            
            # Agrupar por empleado
            registros.sort(key=itemgetter(2))
            for nombre, grupo in groupby(registros, key=itemgetter(2)):
                datos_empleado = list(grupo)
                
                # Calcular totales
                total_horas_35 = sumar_tiempo([reg[3] for reg in datos_empleado])
                total_horas_100 = sumar_tiempo([reg[4] for reg in datos_empleado])
                total_horas_noc = sumar_tiempo([reg[5] for reg in datos_empleado])
                
                # Nombre para mostrar en la fila de totales
                Nombre_total = datos_empleado[0][2]
                
                # Encabezados
                encabezados = [['Fecha', 'Código', 'Nombre', 'Horas 35%', 'Horas 100%', 'Nocturnas']]
                
                def convertir_formato_fecha_para_tablas(fecha_str):
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
                        reg[5],  # Nocturnas
                    ]
                    for reg in datos_empleado
                ]
                datos.append(['TOTAL', '', Nombre_total, total_horas_35, total_horas_100, total_horas_noc])
                
                tabla_data = encabezados + datos
                # Después de crear tabla_data, definir anchos de columna
                tabla = Table(
                    tabla_data,
                    colWidths=[
                        0.9*inch,     # Fecha
                        0.6*inch,     # Código
                        3*inch,       # Nombre
                        0.8*inch,     # Horas 35%
                        1.2*inch,     # Horas 100%
                        3.4*inch      # Comentario
                    ])

                
                # Estilo tabla
                estilo = TableStyle([
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Encabezados en negrita
                ('FONTNAME', (0, -1), (-1, -1), 'Helvetica-Bold'),  # Totales en negrita
                ('FONTSIZE', (0, 0), (-1, -1), 10),
                ('GRID', (0, 0), (-1, -1), 1, colors.black),
                ('BACKGROUND', (0, 0), (-1, 0), colors.lightgrey),  # Fondo gris para encabezados
                ('BACKGROUND', (0, -1), (-1, -1), colors.lightgrey),  # Fondo gris para totales
                
                ])
                tabla.setStyle(estilo)
                
                elements.append(tabla)
                elements.append(Spacer(1, 30))
                
            def convertir_formato_fecha(fecha_str):
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
            
            # Definir encabezado con logo y título
            def encabezado(canvas, doc):
                logo_path = os.path.join(os.path.dirname(directorio_actual), "imagenes", "Logo.png")
                canvas.saveState()
                canvas.setFont("Helvetica-Bold", 14)
                
                # Título alineado a la derecha
                fecha_inicio_formato = convertir_formato_fecha(fecha_inicio)
                fecha_fin_formato = convertir_formato_fecha(fecha_fin)
                canvas.drawRightString(750, 580, f"Reporte del: {fecha_inicio_formato} al {fecha_fin_formato}")
                
                # Logo alineado a la izquierda
                if os.path.exists(logo_path):
                    canvas.drawImage(logo_path, 50, 520, width=1.5*inch, height=1*inch)
                
                canvas.restoreState()
        
            # Crear template de página con encabezado
            frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height - 0.7 * inch, id='normal')
            template = PageTemplate(id='encabezado', frames=frame, onPage=encabezado)
            doc.addPageTemplates([template])
            
            # Generar PDF
            doc.build(elements)
            show_snackbar("Reporte PDF generado exitosamente")
            abrir_carpeta_reporte()  # Abre la carpeta
            return True
            
        except Exception as e:
            show_snackbar(f"Error al exportar PDF: {str(e)}")
            return False
    # Agregar botón para exportar en la interfaz
    boton_exportar = ft.ElevatedButton(
        "Exportar a PDF",
        icon=ft.icons.PICTURE_AS_PDF,
        on_click=lambda e: exportar_pdf(
            get_horas_por_fecha_pdf(txt_fecha1.current.value, txt_fecha2.current.value),
            txt_fecha1.current.value,
            txt_fecha2.current.value
        )
    )


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
                            ft.TextField(ref=txt_fecha1, value=fecha_actual1.strftime("%Y-%m-%d"), width=200, read_only=True, on_click=mostrar_datepicker),
                            ft.Text("Hasta"),
                            ft.TextField(ref=txt_fecha2, value=fecha_actual2.strftime("%Y-%m-%d"), width=200, read_only=True, on_click=mostrar_datepicker2),
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