import flet as ft

def view(content_area, ft):
    # Estilo base compatible
    estilo_input = {
        "border_color": "#8D695D",
        "border_radius": 15,
        "focused_border_color": "#12B3B3",
        "bgcolor": "#F7F2F0",
        "label_style": ft.TextStyle(color="#4A322B", weight="bold"),
        "content_padding": 15,
    }

    # Definimos el ancho total que queremos para los campos largos
    ANCHO_TOTAL = 720 

    # CAMPOS LARGOS (Con ancho fijo para que se vean alargados horizontalmente)
    txt_nombre = ft.TextField(
        label="Nombre del Producto",
        hint_text="Escribe el nombre aquí...",
        prefix_icon=ft.Icons.SHOPPING_BAG,
        width=ANCHO_TOTAL, # <--- Alargado horizontalmente
        **estilo_input
    )

    txt_isbn = ft.TextField(
        label="ID / ISBN",
        hint_text="Código único",
        prefix_icon=ft.Icons.QR_CODE,
        width=ANCHO_TOTAL, # <--- Alargado horizontalmente
        **estilo_input
    )

    # CAMPOS EN FILA (Estos se reparten el ancho total entre los dos)
    txt_precio = ft.TextField(
        label="Precio (USD)",
        hint_text="0.00",
        prefix_icon=ft.Icons.MONETIZATION_ON,
        expand=True,
        **estilo_input
    )

    txt_stock = ft.TextField(
        label="Stock Mínimo",
        hint_text="Cantidad",
        prefix_icon=ft.Icons.INVENTORY_2,
        expand=True,
        **estilo_input
    )

    # Tarjeta principal
    tarjeta = ft.Container(
        content=ft.Column([
            # Cabecera
            ft.Row([
                ft.Icon(ft.Icons.ADD_CIRCLE_OUTLINE, color="#8D695D", size=30),
                ft.Text("Registro de Nuevo Producto", size=24, weight="bold", color="#4A322B"),
            ], alignment=ft.MainAxisAlignment.START),

            ft.Divider(height=10, color="#EEEEEE"),

            # Campos largos (Se apilan uno sobre otro por estar en la Column)
            txt_nombre,
            txt_isbn,
            
            # Fila de abajo (Precio y Stock) que sumados miden lo mismo que los de arriba
            ft.Row([
                txt_precio,
                txt_stock
            ], spacing=20, width=ANCHO_TOTAL), # Mismo ancho total para alinear

            ft.Divider(height=20, color="transparent"),

            # Botones
            ft.Row([
                ft.ElevatedButton(
                    "Cancelar", 
                    color="#8D695D",
                    bgcolor="#EEEEEE",
                ),
                ft.ElevatedButton(
                    "Guardar Producto",
                    bgcolor="#741717",
                    color="white",
                    height=45,
                ),
            ], alignment=ft.MainAxisAlignment.END, spacing=15, width=ANCHO_TOTAL),

        ], spacing=15, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="white",
        padding=40,
        border_radius=30,
        width=800, 
        border=ft.border.all(1, "#E0E0E0"), 
    )

    content_area.content = ft.Column([
        ft.Text("MÓDULO DE INVENTARIO", size=30, weight="bold", color="white"),
        tarjeta,
    ], spacing=30, horizontal_alignment=ft.CrossAxisAlignment.CENTER)
    
    content_area.update()