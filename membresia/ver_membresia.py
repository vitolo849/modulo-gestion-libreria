def view(content_area, ft):
    productos = [
        ["Lhgfhf", "978-3-16-148410-0", "$1200", "15"],
        ["Moudfgfdgdse gfgd", "978-0-13-110362-8", "$25", "50"],
        ["gdf dfgdgd", "978-0-596-52068-7", "$45", "30"],
        ["Mdfgdgonitor dfgd dfgdfgdg", "978-1-4919-1889-0", "$300", "10"],
    ]

    def acciones_menu(e):
        print(f"Acción seleccionada sobre {e.control.data}")

    filas = []
    for p in productos:
        fila = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(p[0])),
                ft.DataCell(ft.Text(p[1])),
                ft.DataCell(ft.Text(p[2])),
                ft.DataCell(
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem("Editar", on_click=acciones_menu, data=p[0]),
                            ft.PopupMenuItem("Eliminar", on_click=acciones_menu, data=p[0]),
                            ft.PopupMenuItem("Ver Detalles", on_click=acciones_menu, data=p[0]),
                        ],
                    )
                ),
            ],
        )
        filas.append(fila)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("ID/ISBN")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=filas,
        border=ft.border.all(1, "BLACK"),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, "#EEEEEE"),
    )

    content_area.content = ft.Column([
        ft.Text("INVENTARIO DE PRODUCTOS", size=30, weight=ft.FontWeight.BOLD),
        ft.Container(
            content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
            height=500,
            border=ft.border.all(2, "BLACK"),
            border_radius=5,
            padding=10,
        ),
    ], spacing=10)