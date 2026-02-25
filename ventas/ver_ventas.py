import flet as ft

def view(content_area, flet_module):
    # 1. Datos originales (nuestra fuente de verdad)
    ventas_datos = [
        ["001", "24/02/2026", "Juan Pérez", "$1,250.00", "Efectivo", "Pagado"],
        ["002", "24/02/2026", "María García", "$450.00", "Tarjeta", "Pagado"],
        ["003", "23/02/2026", "Luis López", "$2,100.00", "Transferencia", "Pendiente"],
    ]

    # 2. Esta función creará las filas de la tabla 
    def crear_filas(lista_datos):
        filas = [] # Aquí guardaremos las filas
        for v in lista_datos:
            color_estado = "#1B5E20" if v[5] == "Pagado" else "#0D47A1"
            if v[5] == "Anulado": color_estado = "#B71C1C"
            
            filas.append(
                ft.DataRow(cells=[
                    ft.DataCell(ft.Text(v[0], weight="bold", color="#000000")),
                    ft.DataCell(ft.Text(v[1], color="#212121")),
                    ft.DataCell(ft.Text(v[2], color="#000000", weight="w500")),
                    ft.DataCell(ft.Text(v[3], color="#1B5E20", weight="bold")),
                    ft.DataCell(ft.Text(v[4], color="#424242")),
                    ft.DataCell(
                        ft.Container(
                            content=ft.Text(v[5], color="white", size=11, weight="bold"),
                            bgcolor=color_estado, padding=ft.padding.symmetric(horizontal=10, vertical=2), border_radius=8
                        )
                    ),
                ])
            )
        return filas

    # 3. La lógica de búsqueda real
    def filtrar_ventas(e):
        texto = buscador.value.lower() # Lo que el usuario escribe
        # Filtramos: Si el folio o el cliente contienen el texto, se quedan
        datos_filtrados = [
            v for v in ventas_datos 
            if texto in v[0].lower() or texto in v[2].lower()
        ]
        # Actualizamos las filas de la tabla
        tabla_ventas.rows = crear_filas(datos_filtrados)
        content_area.update()

    # Componentes de la interfaz
    buscador = ft.TextField(
        hint_text="Buscar por folio o cliente...",
        hint_style=ft.TextStyle(color="#424242"),
        color="#000000",
        prefix_icon=ft.Icons.SEARCH,
        expand=True,
        height=45,
        border_color="#212121",
        border_radius=10,
        on_change=filtrar_ventas # <--- ESTO activa la búsqueda mientras escribes
    )

    tabla_ventas = ft.DataTable(
        heading_row_color="#8D695D",
        heading_row_height=50,
        column_spacing=40,
        columns=[
            ft.DataColumn(ft.Text("FOLIO", color="white", weight="bold")),
            ft.DataColumn(ft.Text("FECHA", color="white", weight="bold")),
            ft.DataColumn(ft.Text("CLIENTE", color="white", weight="bold")),
            ft.DataColumn(ft.Text("TOTAL", color="white", weight="bold")),
            ft.DataColumn(ft.Text("MÉTODO", color="white", weight="bold")),
            ft.DataColumn(ft.Text("ESTADO", color="white", weight="bold")),
        ],
        rows=crear_filas(ventas_datos), # Filas iniciales
    )

    # Contenedor principal (mismo que ya tenías)
    contenedor_ventas = ft.Container(
        content=ft.Column([
            ft.Row([
                ft.Icon(ft.Icons.RECEIPT_LONG, color="#4A322B"),
                ft.Text("Historial de Ventas", size=22, weight="bold", color="#212121"),
            ]),
            ft.Divider(height=1, color="#212121"),
            ft.Row([buscador]),
            ft.Column([tabla_ventas], scroll=ft.ScrollMode.AUTO, expand=True),
        ], spacing=20),
        bgcolor="white", padding=30, border_radius=25, width=1000, border=ft.border.all(1, "#212121"),
    )

    content_area.content = ft.Column([
        ft.Text("REPORTE DE VENTAS", size=32, weight="bold", color="white"),
        contenedor_ventas,
    ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=25)

    content_area.update()