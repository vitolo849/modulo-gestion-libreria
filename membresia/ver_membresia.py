def view(content_area, ft):
    membresias = [
        ["Ana Pérez", "M-001", "Premium", "2026-08-15"],
        ["Carlos Ruiz", "M-012", "Básica", "2025-12-01"],
        ["María López", "M-034", "Estándar", "2026-03-20"],
    ]

    def acciones_menu(e):
        print(f"Acción seleccionada sobre {e.control.data}")

    filas = []
    for m in membresias:
        fila = ft.DataRow(
            cells=[
                ft.DataCell(ft.Text(m[0])),
                ft.DataCell(ft.Text(m[1])),
                ft.DataCell(ft.Text(m[2])),
                ft.DataCell(ft.Text(m[3])),
                ft.DataCell(
                    ft.PopupMenuButton(
                        items=[
                            ft.PopupMenuItem("Renovar", on_click=acciones_menu, data=m[1]),
                            ft.PopupMenuItem("Cancelar", on_click=acciones_menu, data=m[1]),
                            ft.PopupMenuItem("Ver Detalles", on_click=acciones_menu, data=m[1]),
                        ],
                    )
                ),
            ],
        )
        filas.append(fila)

    tabla = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Tipo")),
            ft.DataColumn(ft.Text("Vencimiento")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=filas,
        border=ft.border.all(1, "BLACK"),
        border_radius=10,
        vertical_lines=ft.border.BorderSide(1, "#EEEEEE"),
    )

    content_area.content = ft.Column([
        ft.Row([ft.Text("MEMBRESÍAS", size=30, weight=ft.FontWeight.BOLD)], alignment=ft.MainAxisAlignment.CENTER),
        ft.Divider(height=20),
        ft.Row([ft.Container(content=ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
        height=500,
        border=ft.border.all(2, "BLACK"),
        border_radius=5,
        padding=10,
        )],
        alignment=ft.MainAxisAlignment.CENTER,
    ),
    ], spacing=10)