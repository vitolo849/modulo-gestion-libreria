import flet as ft

def view(content_area, ft):
    productos = [
        ["Lhgfhf", "978-3-16-148410-0", "$1200", "15"],
        ["Moudfgfdgdse gfgd", "978-0-13-110362-8", "$25", "50"],
        ["gdf dfgdgd", "978-0-596-52068-7", "$45", "30"],
        ["Mdfgdgonitor dfgd dfgdfgdg", "978-1-4919-1889-0", "$300", "10"],
    ]

    def acciones_menu(e):
        print(f"Acción sobre: {e.control.data}")

    filas = []
    for p in productos:
        filas.append(
            ft.DataRow(
                cells=[
                    ft.DataCell(ft.Text(p[0], weight="w500", color="#4A322B")),
                    ft.DataCell(ft.Text(p[1], color=ft.Colors.BLUE_GREY_400)),
                    ft.DataCell(ft.Text(p[2], weight="bold", color="green")),
                    ft.DataCell(
                        ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT, # Este es el de los tres puntos
                            icon_color="BLACK",    # AQUÍ eliges el color (puedes usar "blue", "red", etc.)
                            icon_size=20,
                            items=[
                                # CORRECCIÓN: Quitamos 'text=' y usamos el string directo
                                ft.PopupMenuItem("Editar", icon=ft.Icons.EDIT, on_click=acciones_menu, data=p[0]),
                                ft.PopupMenuItem("Eliminar", icon=ft.Icons.DELETE, on_click=acciones_menu, data=p[0]),
                            ],
                        )
                    ),
                ],
            )
        )

    tabla = ft.DataTable(
        heading_row_color="#8D695D",
        heading_row_height=50,
        
        columns=[
            ft.DataColumn(ft.Text("PRODUCTO", color="white", weight="bold")),
            ft.DataColumn(ft.Text("ID / ISBN", color="white", weight="bold")),
            ft.DataColumn(ft.Text("PRECIO", color="white", weight="bold")),
            ft.DataColumn(ft.Text("ACCIONES", color="white", weight="bold")),
        ],
        rows=filas,
            
    )

    # Contenedor principal estilizado
    tarjeta = ft.Container(
        content=ft.Column([
            ft.Row([
                # CORRECCIÓN: Quitamos 'name='
                ft.Icon(ft.Icons.INVENTORY_2, color="#8D695D", size=30),
                ft.Text("Listado de Inventario", size=22, weight="bold", color="#4A322B"),
            ]),
            ft.Divider(height=1, color="#EEEEEE"),
            ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
        ], spacing=15),
        bgcolor="white",
        padding=25,
        border_radius=15,
        shadow=ft.BoxShadow(blur_radius=15, color=ft.Colors.with_opacity(0.1, "black")),
    )

    content_area.content = ft.Column([
        ft.Text("ADMINISTRACIÓN DE STOCK", size=28, weight="bold", color="white"),
        tarjeta,
    ], spacing=20
    )
    
    
    content_area.update()