import flet as ft
import matplotlib
matplotlib.use('Agg')  # Set Agg backend before importing pyplot
import matplotlib.pyplot as plt
import io
import base64
from consultas import get_estado_pagos, get_total_pagos_mes_actual
from threading import Lock

plot_lock = Lock()

def crear_tab_finanzas(page: ft.Page, mainTab: ft.Tabs):
    """Crea el tab de finanzas con gráficos estadísticos."""
    
    def calcular_datos_financieros():
        """Calcula los datos financieros para los gráficos."""
        registros = get_estado_pagos()
        deuda_total = sum(reg[8] for reg in registros)
        pagos_mes = get_total_pagos_mes_actual()
        ganancia = pagos_mes - deuda_total
        return deuda_total, pagos_mes, ganancia

    def crear_grafico_barras():
        """Crea el gráfico de barras y lo convierte en imagen para Flet."""
        with plot_lock:  # Use lock for thread safety
            deuda_total, pagos_mes, ganancia = calcular_datos_financieros()
            
            # Create a new figure
            fig = plt.figure(figsize=(10, 6))
            ax = fig.add_subplot(111)
            
            # Datos para el gráfico
            categorias = ["Deuda Total", "Pagado este mes", "Ganancia"]
            valores = [deuda_total, pagos_mes, ganancia]
            colores = ["#FF4444", "#4444FF", "#44FF44"]
            
            # Crear barras
            bars = ax.bar(categorias, valores, color=colores)
            
            # Personalizar gráfico
            ax.set_title("Resumen Financiero", pad=20)
            ax.set_ylabel("Monto ($)")
            
            # Añadir valores sobre las barras
            for bar in bars:
                height = bar.get_height()
                ax.text(
                    bar.get_x() + bar.get_width()/2.,
                    height,
                    f'${height:,.0f}',
                    ha='center',
                    va='bottom'
                )
            
            # Ajustar layout
            plt.tight_layout()
            
            # Convertir el gráfico a imagen
            buf = io.BytesIO()
            fig.savefig(buf, format='png', dpi=300, bbox_inches='tight')
            buf.seek(0)
            img_str = base64.b64encode(buf.getvalue()).decode()
            
            # Clean up
            plt.close(fig)
            
            return img_str

    # Crear contenedor para la imagen
    img_container = ft.Container(
        content=ft.Image(
            src_base64=crear_grafico_barras(),
            width=800,
            height=500,
            fit=ft.ImageFit.CONTAIN,
        ),
        padding=20,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        bgcolor=ft.colors.WHITE,
    )

    

    # Crear layout principal
    contenido = ft.Column([
        ft.Row([
            ft.Text("Resumen Financiero", size=20, weight="bold"), # type: ignore
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
        img_container
    ])

    return contenido