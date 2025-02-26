import flet as ft
from consultas import get_estado_pagos, get_total_pagos_mes_actual, get_pagos_por_mes, get_ultimas_deudas, get_top_pagos_mes

def crear_tab_finanzas(page: ft.Page, mainTab: ft.Tabs):
    """Crea el tab de finanzas con gráficos estadísticos."""
    
    def calcular_datos_financieros():
        registros = get_estado_pagos()
        deuda_total = sum(reg[8] for reg in registros)
        pagos_mes = get_total_pagos_mes_actual()
        ganancia = pagos_mes - deuda_total
        return deuda_total, pagos_mes, ganancia
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_grafico_barras():
        deuda_total, pagos_mes, ganancia = calcular_datos_financieros()
        max_value = max(deuda_total, pagos_mes, abs(ganancia))
        max_value = ((max_value // 5000) + 1) * 5000

        def format_to_mil(value):
            """Convert number to 'mil' format, handling negative values"""
            abs_value = abs(value)
            if abs_value >= 1000:
                formatted = f"{int(abs_value/1000)} mil"
            else:
                formatted = str(abs_value)
            return f"-{formatted}" if value < 0 else formatted
        
        chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=0,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=deuda_total,
                            width=40,
                            color=ft.colors.RED_400,
                            tooltip=f"${deuda_total:,.0f}",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=1,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=pagos_mes,
                            width=40,
                            color=ft.colors.BLUE_400,
                            tooltip=f"${pagos_mes:,.0f}",
                            border_radius=0,
                        ),
                    ],
                ),
                ft.BarChartGroup(
                    x=2,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=ganancia,
                            width=40,
                            color=ft.colors.GREEN_400,
                            tooltip=f"${ganancia:,.0f}",
                            border_radius=0,
                        ),
                    ],
                ),
            ],
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=i, label=ft.Text(format_to_mil(i)))
                    for i in range(int(-max_value), int(max_value) + 5000, 5000)
                ],
                labels_size=50
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0,
                        label=ft.Container(ft.Text("Deuda Total"), padding=1)
                    ),
                    ft.ChartAxisLabel(
                        value=1,
                        label=ft.Container(ft.Text("Pagado"), padding=1)
                    ),
                    ft.ChartAxisLabel(
                        value=2,
                        label=ft.Container(ft.Text("Ganancia"), padding=1)
                    ),
                ],
                labels_size=35,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300,
                width=1,
                dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
            max_y=max_value,
            interactive=True,
            height=300
        )
        return chart
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_grafico_meses():
        pagos_mensuales = get_pagos_por_mes()
        valores = [pago[1] for pago in pagos_mensuales]
        max_value = max(valores) * 1.1 if valores else 1000
        max_value = ((max_value // 5000) + 1) * 5000
        
        def format_to_mil(value):
            """Convert number to 'mil' format"""
            abs_value = abs(value)
            if abs_value >= 1000:
                formatted = f"{int(abs_value/1000)} mil"
            else:
                formatted = str(abs_value)
            return f"-{formatted}" if value < 0 else formatted

        meses = ["ENE", "FEB", "MAR", "ABR", "MAY", "JUN", 
                 "JUL", "AGO", "SEP", "OCT", "NOV", "DIC"]

        chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=valor,
                            width=30,
                            color=ft.colors.BLUE_400,
                            tooltip=f"${valor:,.0f}",
                            border_radius=0,
                        ),
                    ],
                ) for i, valor in enumerate(valores)
            ],
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=i, label=ft.Text(format_to_mil(i)))
                    for i in range(0, int(max_value) + 5000, 5000)
                ],
                labels_size=35
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Container(ft.Text(mes), padding=1)
                    ) for i, mes in enumerate(meses)
                ],
                labels_size=35,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300,
                width=1,
                dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
            max_y=max_value,
            interactive=True,
            height=300
        )
        return chart
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_grafico_deudas():
        deudas = get_ultimas_deudas()
        if not deudas:
            return ft.Text("No hay deudas pendientes", size=16, color=ft.colors.GREY_600)
            
        max_value = 500

        chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=min(deuda[1], max_value),
                            width=30,
                            color=ft.colors.RED_300,
                            tooltip=deuda[0],
                            border_radius=0,
                        ),
                    ],
                ) for i, deuda in enumerate(deudas)
            ],
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=i, label=ft.Text(f"${i}"))
                    for i in range(0, max_value + 100, 100)
                ],
                labels_size=35,
                title=ft.Text("Deuda ($)"),
                title_size=35
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Container(
                            ft.Text(f"$ {deuda[1]}", size=12),
                            padding=1
                        )
                    ) for i, deuda in enumerate(deudas)
                ],
                labels_size=35,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300,
                width=1,
                dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.5, ft.colors.GREY_300),
            max_y=max_value,
            interactive=True,
            height=200
        )
        return chart
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    def crear_grafico_top_pagos():
        pagos = get_top_pagos_mes()
        if not pagos:
            return ft.Text("No hay pagos este mes", size=16, color=ft.colors.GREY_600)
            
        max_value = max(pago[1] for pago in pagos)
        # Redondear max_value al siguiente múltiplo de 200
        max_value = ((max_value + 199) // 200) * 200 + 200

        # Crear lista de valores para el eje Y
        y_values = list(range(0, max_value + 200, 200))

        chart = ft.BarChart(
            bar_groups=[
                ft.BarChartGroup(
                    x=i,
                    bar_rods=[
                        ft.BarChartRod(
                            from_y=0,
                            to_y=pago[1],
                            width=30,
                            color=ft.colors.GREEN_300,
                            tooltip=f"{pago[0]}",
                            border_radius=0,
                        ),
                    ],
                ) for i, pago in enumerate(pagos)
            ],
            border=ft.border.all(1, ft.colors.GREY_400),
            left_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(value=y, label=ft.Text(f"${y:,.0f}"))
                    for y in y_values
                ],
                labels_size=45
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=i,
                        label=ft.Container(
                            ft.Text(f"${pago[1]:,.0f}", size=12),
                            padding=1
                        )
                    ) for i, pago in enumerate(pagos)
                ],
                labels_size=35,
            ),
            horizontal_grid_lines=ft.ChartGridLines(
                color=ft.colors.GREY_300,
                width=1,
                dash_pattern=[3, 3]
            ),
            tooltip_bgcolor=ft.colors.with_opacity(0.7, ft.colors.GREY_900),
            max_y=max_value,
            interactive=True,
            height=300
        )
        return chart
#-------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------------------------------------------
    chart_container = ft.Container(
        content=crear_grafico_barras(),
        padding=25,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        width=500,
        height=400
    )
    
    chart_container_meses = ft.Container(
        content=crear_grafico_meses(),
        padding=25,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        width=500,
        height=400
    )
    
    chart_container_deudas = ft.Container(
        content=crear_grafico_deudas(),
        padding=25,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        width=500,
        height=400
    )
    
    chart_container_top_pagos = ft.Container(
        content=crear_grafico_top_pagos(),
        padding=25,
        border=ft.border.all(1, ft.colors.GREY_400),
        border_radius=10,
        bgcolor=ft.colors.WHITE,
        width=500,
        height=400
    )

    contenido = ft.Column([
        ft.Text("Resumen Financiero", size=20, weight="bold"), # type: ignore
        ft.Column([
            ft.Row([
                ft.Column([
                    ft.Text("Balance del Mes Actual", size=16, weight="bold", text_align=ft.TextAlign.CENTER), # type: ignore
                    chart_container,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("Pagos Mensuales del Año", size=16, weight="bold", text_align=ft.TextAlign.CENTER), # type: ignore
                    chart_container_meses,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER),
            ft.Row([
                ft.Column([
                    ft.Text("Top 10 Deudas Pendientes", size=16, weight="bold", text_align=ft.TextAlign.CENTER), # type: ignore
                    chart_container_deudas,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
                ft.Column([
                    ft.Text("Top 10 Pagos del Mes", size=16, weight="bold", text_align=ft.TextAlign.CENTER), # type: ignore
                    chart_container_top_pagos,
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            ], alignment=ft.MainAxisAlignment.CENTER),
        ], spacing=20),
    ])

    return contenido