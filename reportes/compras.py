from reportes.models import (
    compras_por_proveedor,
    libros_mas_reordenados,
    ordenes_reposicion_por_estado,
    proveedores_tiempo_entrega,
    ordenes_por_mes
)
from reportes.pdf import getPdfTable
from datetime import date, timedelta
def view(content_area, ft):
    def dropdown_changed(e):
        print(f"Opción seleccionada: {dropdown.value}")
    def generar_reporte(e):
        print(f"Valor seleccionado: {dropdown.value}")
        if dropdown.value == "comprasProveedor":
            fin = date.today()
            inicio = fin - timedelta(days=90)
            data = compras_por_proveedor(inicio, fin)
            getPdfTable(data)
        elif dropdown.value == "librosReordenados":
            data = libros_mas_reordenados()
            getPdfTable(data)
        elif dropdown.value == "ordenesEstado":
            data = ordenes_reposicion_por_estado()
            getPdfTable(data)
        elif dropdown.value == "tiempoEntrega":
            data = proveedores_tiempo_entrega()
            getPdfTable(data)
        elif dropdown.value == "ordenesMes":
            data = ordenes_por_mes()
            getPdfTable(data)
    dropdown = ft.Dropdown(
        label="Seleccionar reporte",
        hint_text="Elige una opción...",
        width=450,
        options=[
            ft.dropdown.Option("comprasProveedor", "Compras por proveedor (últimos 90 días)"),
            ft.dropdown.Option("librosReordenados", "Libros más reordenados"),
            ft.dropdown.Option("ordenesEstado", "Órdenes por estado"),
            ft.dropdown.Option("tiempoEntrega", "Tiempo de entrega por proveedor"),
            ft.dropdown.Option("ordenesMes", "Órdenes por mes"),
        ],
    )
    content_area.content = ft.Column([
        ft.Text("REPORTES DE COMPRAS A PROVEEDORES", size=30, weight=ft.FontWeight.BOLD),
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