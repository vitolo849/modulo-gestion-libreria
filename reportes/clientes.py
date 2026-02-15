
from models import clientesMasGastan, clientesMasCompras

from pdf import getPdfTable


def view(content_area, ft):
    def dropdown_changed(e):
        print(f"Opción seleccionada: {dropdown.value}")
    
    def guardar_producto(e):
        print(f"Valor seleccionado: {dropdown.value}")
        if (dropdown.value=="clienteTrancurridos"):
            getPdfTable(clientesMasCompras())
            print("")
    
    dropdown = ft.Dropdown(
        label="Seleccionar reporte",
        hint_text="Elige una opción...",
        width=300,
        options=[
            ft.dropdown.Option("clienteTrancurridos", "Clientes mas transcurridos"),
        ],
    )
    
    content_area.content = ft.Column([
        ft.Text("Agregar nuevo producto", size=25),
        dropdown,
        ft.ElevatedButton("Guardar", on_click=guardar_producto),
    ], spacing=10)