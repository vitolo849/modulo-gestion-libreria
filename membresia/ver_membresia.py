import flet as ft

def view(content_area, ft):
    # Datos de ejemplo
    membresias = [
        ["Ana Pérez", "M-001", "Premium", "2026-08-15"],
        ["Carlos Ruiz", "M-012", "Básica", "2025-12-01"],
        ["María López", "M-034", "Estándar", "2026-03-20"],
    ]

    def acciones_menu(e):
        print(f"Acción seleccionada sobre {e.control.data}")

    filas = []
    for m in membresias:
        # Lógica de colores para los "Badges" (Etiquetas)
        color_tag = "#8D695D" 
        if m[2] == "Premium": color_tag = "#D48806" # Oro oscuro para legibilidad
        elif m[2] == "Básica": color_tag = "#546E7A" # Gris azulado
        elif m[2] == "Estándar": color_tag = "#1976D2" # Azul fuerte

        filas.append(
            ft.DataRow(
                cells=[
                    # CLIENTE: Negro suave para máxima claridad
                    ft.DataCell(ft.Text(m[0], weight="bold", color="#212121", size=14)),
                    
                    # ID: Gris muy oscuro (fácil de leer pero secundario)
                    ft.DataCell(ft.Text(m[1], color="#424242", font_family="monospace", size=13)),
                    
                    # TIPO: Badge con texto blanco sobre fondo colorido
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(m[2], color="white", size=11, weight="bold"),
                            bgcolor=color_tag,
                            padding=ft.padding.symmetric(horizontal=12, vertical=5),
                            border_radius=12
                        )
                    ),
                    
                    # VENCIMIENTO: Color oscuro fuerte
                    ft.DataCell(ft.Text(m[3], color="#212121", size=13, weight="w500")),
                    
                    # ACCIONES: Tres puntos en el color de tu marca
                    ft.DataCell(
                        ft.PopupMenuButton(
                            icon=ft.Icons.MORE_VERT,
                            icon_color="#8D695D",
                            items=[
                                ft.PopupMenuItem("Renovar", on_click=acciones_menu, data=m[1]),
                                ft.PopupMenuItem("Ver Detalles", on_click=acciones_menu, data=m[1]),
                                ft.PopupMenuItem("Cancelar", on_click=acciones_menu, data=m[1]),
                            ],
                        )
                    ),
                ],
            )
        )

    # Tabla con diseño limpio
    tabla = ft.DataTable(
        heading_row_color="#8D695D",
        heading_row_height=55,
        data_row_min_height=60, # Un poco más de aire entre filas
        column_spacing=50,
        columns=[
            ft.DataColumn(ft.Text("CLIENTE", color="white", weight="bold")),
            ft.DataColumn(ft.Text("ID", color="white", weight="bold")),
            ft.DataColumn(ft.Text("TIPO", color="white", weight="bold")),
            ft.DataColumn(ft.Text("VENCIMIENTO", color="white", weight="bold")),
            ft.DataColumn(ft.Text("ACCIONES", color="white", weight="bold")),
        ],
        rows=filas,
    )

    # Contenedor Blanco (Tarjeta)
    tarjeta = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.CARD_MEMBERSHIP, color="#8D695D", size=30),
                ft.Text("Gestión de Membresías", size=24, weight="bold", color="#4A322B"),
            ], alignment=ft.MainAxisAlignment.CENTER),
            
            ft.Divider(height=10, color="#EEEEEE"),
            
            # Área de scroll para la tabla
            ft.Column([tabla], scroll=ft.ScrollMode.AUTO),
            
        ], spacing=25, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        bgcolor="white",
        padding=35,
        border_radius=20,
        width=1000, # Ajustamos ancho fijo para evitar errores de max_width
        shadow=ft.BoxShadow(
            blur_radius=25,
            color=ft.Colors.with_opacity(0.2, "black"),
            offset=ft.Offset(0, 10)
        ),
    )

    # Contenedor final que se inyecta en el main
    content_area.content = ft.Column([
        ft.Text("PANEL DE SOCIOS", size=32, weight="bold", color="white"),
        tarjeta,
    ], 
    spacing=30, 
    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    scroll=ft.ScrollMode.ADAPTIVE
    )
    
    content_area.update()