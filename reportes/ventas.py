from reportes.models import (
    obtener_ventas_por_periodo, 
    productos_mas_vendidos, 
    ventas_por_dia,
    ingresos_por_metodo_pago
)
from reportes.pdf import getPdfTable
from datetime import date, timedelta

def view(content_area, ft):
    def generar_reporte(e):
        if dropdown.value == "ventasDia":
            data = ventas_por_dia()
            tabla_data = [("Fecha", "Ventas", "Total", "Promedio")]
            tabla_data.append((
                data["fecha"],
                str(data["num_ventas"]),
                f"${data['total_dia']:.2f}",
                f"${data['promedio_venta']:.2f}"
            ))
            getPdfTable(tabla_data)
            
        elif dropdown.value == "ventasPeriodo":
            fin = date.today()
            inicio = fin - timedelta(days=30)
            data = obtener_ventas_por_periodo(inicio, fin)
            getPdfTable(data)
            
        elif dropdown.value == "productosMasVendidos":
            data = productos_mas_vendidos()
            getPdfTable(data)
            
        elif dropdown.value == "ingresosMetodoPago":
            fin = date.today()
            inicio = fin - timedelta(days=30)
            data = ingresos_por_metodo_pago(inicio, fin)
            getPdfTable(data)
    
    dropdown = ft.Dropdown(
        label="Seleccionar reporte",
        hint_text="Elige una opción...",
        width=400,
        options=[
            ft.dropdown.Option("ventasDia", "Ventas del día"),
            ft.dropdown.Option("ventasPeriodo", "Ventas de los últimos 30 días"),
            ft.dropdown.Option("productosMasVendidos", "Productos más vendidos"),
            ft.dropdown.Option("ingresosMetodoPago", "Ingresos por método de pago"),
        ],
    )
    
    content_area.content = ft.Column([
        ft.Text("REPORTES DE VENTAS", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20),
        ft.Container(
            content=ft.Column([
                ft.Text("Seleccione el tipo de reporte:", size=16),
                dropdown,
                ft.ElevatedButton("Generar Reporte PDF", on_click=generar_reporte, width=200),
            ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.Alignment(0, 0),
            expand=True,
        ),
    ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER)