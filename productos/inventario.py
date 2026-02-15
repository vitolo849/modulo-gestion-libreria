def view(content_area, ft):
    productos = [
        ["Lhgfhf", "978-3-16-148410-0", "$1200", "15"],
        ["Moudfgfdgdse gfgd", "978-0-13-110362-8", "$25", "50"],
        ["gdf dfgdgd", "978-0-596-52068-7", "$45", "30"],
        ["Mdfgdgonitor dfgd dfgdfgdg", "978-1-4919-1889-0", "$300", "10"],
    ]
    
    def mostrar_menu(e, producto, isbn, precio, stock):
        content_area.page.dialog = ft.AlertDialog(
            title=ft.Text(f"Producto: {producto}"),
            content=ft.Column([
                ft.Text(f"ISBN: {isbn}"),
                ft.Text(f"Precio: {precio}"),
                ft.Text(f"Stock: {stock}"),
                ft.Divider(),
                ft.Text("Opciones:", weight=ft.FontWeight.BOLD),
            ], spacing=10, height=200),
            actions=[
                ft.TextButton("Editar", on_click=lambda e: print(f"Editar {producto}")),
                ft.TextButton("Eliminar", on_click=lambda e: print(f"Eliminar {producto}")),
                ft.TextButton("Ver Detalles", on_click=lambda e: print(f"Detalles {producto}")),
                ft.TextButton("Cancelar", on_click=cerrar_menu),
            ],
            actions_alignment=ft.MainAxisAlignment.END,
        )
        content_area.page.dialog.open = True
        content_area.page.update()
    
    def cerrar_menu(e):
        content_area.page.dialog.open = False
        content_area.page.update()
    
    filas = []
    for p in productos:
        fila = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(p[0])),
                ft.DataCell(ft.Text(p[1])),
                ft.DataCell(ft.Text(p[2])),
                ft.DataCell(
                    ft.Container(
                        content=ft.IconButton(
                            icon="MENU",
                            icon_size=20,
                            on_click=lambda e, prod=p[0], isbn=p[1], precio=p[2], stock=p[3]: mostrar_menu(e, prod, isbn, precio, stock),
                        ),
                        alignment=ft.Alignment(0, 0),
                    )
                ),
            ],
        )
        filas.append(fila)
    
    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Producto")),
            ft.DataColumn(ft.Text("ISBN")),
            ft.DataColumn(ft.Text("Precio")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=filas,
        border=ft.border.all(1, "BLACK"),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, "BLACK"),
        horizontal_lines=ft.border.BorderSide(1, "BLACK"),
    )
    
    content_area.content = ft.Column([
        ft.Text("INVENTARIO DE PRODUCTOS", size=30, weight=ft.FontWeight.BOLD),
        ft.Container(
            content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
            height=400,
            border=ft.border.all(1, "BLACK"),
            border_radius=5,
            padding=10,
        ),
    ], spacing=10)