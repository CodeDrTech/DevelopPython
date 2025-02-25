import flet as ft
from consultas import get_estado_pagos, get_total_pagos_mes_actual, get_pagos_por_mes

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
        max_value = max(deuda_total, pagos_mes, abs(ganancia)) * 1.1

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
                    ft.ChartAxisLabel(value=0, label=ft.Text("$0")),
                    ft.ChartAxisLabel(value=max_value/2, label=ft.Text(f"${max_value/2:,.0f}")),
                    ft.ChartAxisLabel(value=max_value, label=ft.Text(f"${max_value:,.0f}")),
                ],
                labels_size=35
            ),
            bottom_axis=ft.ChartAxis(
                labels=[
                    ft.ChartAxisLabel(
                        value=0,
                        label=ft.Container(ft.Text("Deuda Total"), padding=1)
                    ),
                    ft.ChartAxisLabel(
                        value=1,
                        label=ft.Container(ft.Text("Pagado Mes"), padding=1)
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

        meses = ["ENE-", "FEB-", "MAR-", "ABR-", "MAY-", "JUN-", 
                 "JUL-", "AGO-", "SEP-", "OCT-", "NOV-", "DIC-"]

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
                    ft.ChartAxisLabel(value=0, label=ft.Text("$0")),
                    ft.ChartAxisLabel(value=max_value/2, label=ft.Text(f"${max_value/2:,.0f}")),
                    ft.ChartAxisLabel(value=max_value, label=ft.Text(f"${max_value:,.0f}")),
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

    contenido = ft.Column([
        ft.Text("Datos financieros", size=20, weight="bold"), # type: ignore
        ft.Row([
            chart_container,
            chart_container_meses
        ], alignment=ft.MainAxisAlignment.CENTER)
    ])

    return contenido