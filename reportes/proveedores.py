# proveedores.py
from reportes.models import (
    compras_por_proveedor,
    libros_mas_reordenados,
    ordenes_reposicion_por_estado,
    proveedores_tiempo_entrega,
    ordenes_por_mes,
    proveedores_mas_compras,
    libros_bajo_stock,
    ordenes_pendientes
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
            print("Reporte de compras por proveedor")
            
        elif dropdown.value == "proveedoresMasCompras":
            data = proveedores_mas_compras()
            getPdfTable(data)
            print("Reporte de proveedores con más compras")
            
        elif dropdown.value == "librosReordenados":
            data = libros_mas_reordenados()
            getPdfTable(data)
            print("Reporte de libros más reordenados")
            
        elif dropdown.value == "ordenesEstado":
            data = ordenes_reposicion_por_estado()
            getPdfTable(data)
            print("Reporte de órdenes por estado")
            
        elif dropdown.value == "tiempoEntrega":
            data = proveedores_tiempo_entrega()
            getPdfTable(data)
            print("Reporte de tiempo de entrega por proveedor")
            
        elif dropdown.value == "ordenesMes":
            data = ordenes_por_mes()
            getPdfTable(data)
            print("Reporte de órdenes por mes")
            
        elif dropdown.value == "librosBajoStock":
            data = libros_bajo_stock()
            getPdfTable(data)
            print("Reporte de libros bajo stock mínimo")
            
        elif dropdown.value == "ordenesPendientes":
            data = ordenes_pendientes()
            getPdfTable(data)
            print("Reporte de órdenes pendientes")
    
    dropdown = ft.Dropdown(
        label="Seleccionar reporte",
        hint_text="Elige una opción...",
        width=500,
        options=[
            ft.dropdown.Option("comprasProveedor", "Compras por proveedor (últimos 90 días)"),
            ft.dropdown.Option("proveedoresMasCompras", "Proveedores con más compras"),
            ft.dropdown.Option("librosReordenados", "Libros más reordenados"),
            ft.dropdown.Option("ordenesEstado", "Órdenes de reposición por estado"),
            ft.dropdown.Option("tiempoEntrega", "Tiempo de entrega por proveedor"),
            ft.dropdown.Option("ordenesMes", "Órdenes por mes"),
            ft.dropdown.Option("librosBajoStock", "Libros bajo stock mínimo"),
            ft.dropdown.Option("ordenesPendientes", "Órdenes pendientes"),
        ],
    )
    
    content_area.content = ft.Column([
        ft.Text("REPORTES DE PROVEEDORES Y COMPRAS", size=30, weight=ft.FontWeight.BOLD),
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