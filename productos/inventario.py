import flet as ft

def view(content_area, ft):
    # Datos de ejemplo
    productos = [
        ["Lhgfhf", "978-3-16-148410-0", "$1200", 15, 5],
        ["Moudfgfdgdse gfgd", "978-0-13-110362-8", "$25", 3, 5], 
        ["Gdf dfgdgd", "978-0-596-52068-7", "$45", 0, 2], 
    ]

    filas = []
    for p in productos:
        # Colores de stock oscuros para legibilidad
        color_stock = "#1B5E20" # Verde bosque
        if p[3] == 0: color_stock = "#B71C1C" # Rojo sangre
        elif p[3] <= p[4]: color_stock = "#E65100" # Naranja quemado

        filas.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p[0], weight="bold", color="#000000")),
                    
                    # ID: Ahora en negro sólido para que no se pierda
                    ft.DataCell(ft.Text(p[1], font_family="monospace", color="#000000", size=14, weight="w500")),
                    
                    ft.DataCell(ft.Text(p[2], weight="bold", color="#1B5E20")),
                    
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(str(p[3]), color="white", size=12, weight="bold"),
                            bgcolor=color_stock,
                            padding=ft.padding.symmetric(horizontal=12, vertical=4),
                            border_radius=10,
                        )
                    ),
                    
                    # ACCIONES: Usamos un icono de color negro para los tres puntos
                    ft.DataCell(
                        ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            # Nota: Si tu versión no permite icon_color aquí, 
                            # el color por defecto será negro/gris oscuro.
                            items=[
                                ft.PopupMenuItem("Editar Stock", icon=ft.Icons.EDIT),
                                ft.PopupMenuItem("Eliminar", icon=ft.Icons.DELETE_OUTLINE),
                            ],
                        )
                    ),
                ]
            )
        )

    # Buscador: Mejoramos el contraste del texto de ayuda
    buscador = ft.TextField(
        hint_text="Buscar producto...",
        hint_style=ft.TextStyle(color="#424242", weight="w500"), # Gris muy oscuro
        color="#000000", # Texto que escribe el usuario en negro puro
        prefix_icon=ft.Icons.SEARCH,
        height=48,
        text_size=16,
        border_radius=12,
        bgcolor="#F5F5F5",
        border_color="#212121", # Borde negro fino para definir la caja
    )

    tabla = ft.DataTable(
        heading_row_color="#8D695D",
        heading_row_height=55,
        columns=[
            ft.DataColumn(ft.Text("PRODUCTO", color="white", weight="bold")),
            ft.DataColumn(ft.Text("ID / ISBN", color="white", weight="bold")),
            ft.DataColumn(ft.Text("PRECIO", color="white", weight="bold")),
            ft.DataColumn(ft.Text("STOCK", color="white", weight="bold")),
            ft.DataColumn(ft.Text("ACCIONES", color="white", weight="bold")),
        ],
        rows=filas,
    )

    tarjeta_inventario = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.INVENTORY, color="#4A322B"),
                ft.Text("Listado de Inventario", size=22, weight="bold", color="#212121"),
                ft.Container(expand=True),
                ft.IconButton(ft.Icons.REFRESH, icon_color="#212121"),
            ]),
            ft.Divider(height=1, color="#212121"),
            
            buscador,
            
            ft.Column([tabla], scroll=ft.ScrollMode.AUTO, expand=True),
        ], spacing=20),
        bgcolor="white",
        padding=30,
        border_radius=25,
        width=1000, # Un poco más ancho para que respire la información
        border=ft.border.all(1, "#212121"), # Contorno definido
    )

    content_area.content = ft.Column([
        ft.Text("ADMINISTRACIÓN DE STOCK", size=32, weight="bold", color="white"),
        tarjeta_inventario,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=25)
    
    content_area.update()