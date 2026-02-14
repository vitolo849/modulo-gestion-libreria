import flet as ft

def main(page: ft.Page):
    page.title = "Administración Usuario"
    page.padding =0 
    #page.theme_mode = ft.ThemeMode.LIGHT
    
    # --- ÁREA DE CONTENIDO ---
    content_area = ft.Container(

        content=ft.Text("Modulo de administración y reportes", size=20),

        padding=40,
        alignment=ft.Alignment(-1, -1), 
        expand=True,
        bgcolor=ft.Colors.BLACK
    )
    
    
    def cambiar_vista(e):
        if e.control.data == "productos":
            content_area.content = ft.Text("Sección de Productos ", size=25)
        elif e.control.data == "membresias":
            content_area.content = ft.Text("Sección de Membresías de Clientes", size=25)
        elif e.control.data == "Ventas":
            content_area.content = ft.Text("Sección de ventas", size=25)
        page.update()

    # --- BARRA DE NAVEGACIÓN ---
    nav_bar = ft.Row(
        controls=[
            ft.ElevatedButton(
                "Productos",
                data="productos", 
                on_click=cambiar_vista,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
                width=150,
                height=60,
            ),
            ft.ElevatedButton(
                "Membresias",
                data="membresias", # Etiqueta para identificar el botón
                on_click=cambiar_vista,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
                width=150,
                height=60,
            ),
            ft.ElevatedButton(
                "Ventas",
                data="Ventas",
                on_click=cambiar_vista,
                style=ft.ButtonStyle(shape=ft.RoundedRectangleBorder(radius=0)),
                width=150,
                height=60,
            ),
        ],
        spacing=0 
    )
    
    page.add(
        ft.Column(
            controls=[
                nav_bar,
                ft.Divider(height=1, color=ft.Colors.GREY_400),
                content_area
            ],
            spacing=0,
            expand=True
        )
    )

if __name__ == "__main__":
    ft.app(target=main)

