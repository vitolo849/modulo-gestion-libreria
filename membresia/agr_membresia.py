def view(content_area, ft):
    nombre = ft.TextField(label="Nombre del Plan", width=350)
    precio = ft.TextField(label="Precio", hint_text="Ej. 19.99", width=200, keyboard_type=ft.KeyboardType.NUMBER)

    periodicidad = ft.Dropdown(
        width=200,
        options=[
            ft.dropdown.Option("Mensual", "mensual"),
            ft.dropdown.Option("Semestral", "semestral"),
            ft.dropdown.Option("Anual", "anual"),
        ],
        value="mensual",
        label="Periodicidad",
    )

    # Beneficios (checklist)
    descuento_check = ft.Checkbox(label="Descuento fijo (activar para definir %)")
    descuento_pct = ft.TextField(label="% Descuento", width=120, value="10")
    envio_gratis = ft.Checkbox(label="Envío Gratis")
    libro_mes = ft.Checkbox(label="Libro del Mes")
    acceso_eventos = ft.Checkbox(label="Acceso a Eventos")
    limite_uso = ft.TextField(label="Límite de uso (ej. 'todos' o 'por género')", width=300)

    # Color / Icono (selección simple)
    color_selector = ft.Dropdown(
        width=180,
        options=[
            ft.dropdown.Option("Dorado", "#FFD700"),
            ft.dropdown.Option("Plata", "#C0C0C0"),
            ft.dropdown.Option("Bronce", "#CD7F32"),
            ft.dropdown.Option("Rojo", "#741717"),
        ],
        value="#FFD700",
        label="Color identificador",
    )

    icon_selector = ft.Dropdown(
        width=180,
        options=[
            ft.dropdown.Option("Estrella", "STAR"),
            ft.dropdown.Option("Libro", "BOOK"),
            ft.dropdown.Option("Corazón", "FAVORITE"),
        ],
        value="STAR",
        label="Icono",
    )

    info = ft.Text("")

    def on_desc_toggle(e):
        descuento_pct.disabled = not descuento_check.value
        e.page.update()

    descuento_check.on_change = on_desc_toggle

    def guardar(e):
        plan = {
            "nombre": (nombre.value or "").strip(),
            "precio": (precio.value or "").strip(),
            "periodicidad": periodicidad.value,
            "beneficios": {
                "descuento_activo": bool(descuento_check.value),
                "descuento_pct": (descuento_pct.value or "").strip(),
                "envio_gratis": bool(envio_gratis.value),
                "libro_del_mes": bool(libro_mes.value),
                "acceso_eventos": bool(acceso_eventos.value),
                "limite_uso": (limite_uso.value or "").strip(),
            },
            "color": color_selector.value,
            "icono": icon_selector.value,
        }

        # Aquí puedes guardar en archivo/BD. Ahora lo mostramos en un diálogo:
        dlg = ft.AlertDialog(
            title=ft.Text("Plan creado"),
            content=ft.Text(str(plan)),
            actions=[ft.TextButton("OK", on_click=lambda ev: ev.page.dialog.dismiss())],
        )
        e.page.dialog = dlg
        dlg.open = True
        e.page.update()

    boton_guardar = ft.ElevatedButton("Guardar Plan", on_click=guardar)

    content_area.content = ft.Column(
        [
            ft.Text("Crear / Configurar Plan de Membresía", size=22),
            ft.Row([nombre, ft.Column([precio, periodicidad])], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
            ft.Text("Beneficios", weight=ft.FontWeight.BOLD),
            ft.Row([descuento_check, descuento_pct], alignment=ft.MainAxisAlignment.START),
            ft.Row([envio_gratis, libro_mes, acceso_eventos], spacing=20),
            ft.Row([ft.Text("Límite de uso:"), limite_uso], alignment=ft.MainAxisAlignment.START),
            ft.Divider(),
            ft.Row([color_selector, icon_selector], spacing=20),
            ft.Divider(),
            ft.Row([boton_guardar, info], alignment=ft.MainAxisAlignment.START),
        ],
        spacing=12,
    )