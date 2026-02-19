from reportes.models import clientesMasGastan, clientesMasCompras, clientesMasProductos, rankingClientes, clientesTopPorPeriodo
from reportes.pdf import getPdfTable

def view(content_area, ft):
    def dropdown_changed(e):
        print(f"Opción seleccionada: {dropdown.value}")
    
    def generar_reporte(e):
        print(f"Valor seleccionado: {dropdown.value}")
        if dropdown.value == "clienteMasCompras":
            data = clientesMasCompras()
            print(f"Datos obtenidos: {len(data)-1} registros")
            getPdfTable(data)
            print("Reporte de clientes más compradores ")
        elif dropdown.value == "clienteMasGastan":
            data = clientesMasGastan()
            getPdfTable(data)
            print("Reporte de clientes que más gastan ")
        elif dropdown.value == "clienteMasProductos":
            data = clientesMasProductos()
            getPdfTable(data)
            print("Reporte de clientes con más productos ")
        elif dropdown.value == "ranking":
            data = rankingClientes()
            getPdfTable(data)
            print("Reporte ranking de clientes ")
        elif dropdown.value == "periodo":
            data = clientesTopPorPeriodo()
            getPdfTable(data)
            print("Reporte clientes por período ")
    
    dropdown = ft.Dropdown(
        label="Seleccionar reporte",
        hint_text="Elige una opción...",
        width=400,
        options=[
            ft.dropdown.Option("clienteMasCompras", "Clientes más compradores"),
            ft.dropdown.Option("clienteMasGastan", "Clientes que más gastan"),
            ft.dropdown.Option("clienteMasProductos", "Clientes con más productos"),
            ft.dropdown.Option("ranking", "Ranking completo de clientes"),
            ft.dropdown.Option("periodo", "Clientes de los ultimos 30 días"),
        ],
    )
    
    content_area.content = ft.Column([
        ft.Text("REPORTES DE PROVEEDORES", size=30, weight=ft.FontWeight.BOLD),
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