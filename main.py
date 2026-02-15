import flet as ft
from datetime import date, timedelta
from libreria_cafe_edd_db import crear_sesion, establecer_logs, Membresia

from productos.agregar  import view as agregarProductos


def main(page: ft.Page):
    page.title = "Administración Usuario"
    page.padding = 0
    page.bgcolor = "#741717"
    
    content_area = ft.Container(
        content=ft.Text("Modulo de administración y reportes", size=20),
        padding=40,
        alignment=ft.Alignment(-1, -1), 
        expand=True,
        bgcolor="#CBA68B"
    )
    
    def cambiar_vista(e):
        
        if e.control.data == "productos":
            content_area.content = ft.Text("Sección de Productos ", size=25)
        elif e.control.data == "membresias":
            content_area.content = ft.Text("Sección de Membresías de Clientes", size=25)
        elif e.control.data == "ventas":
            content_area.content = ft.Text("Sección de ventas", size=25)
        page.update()
    
    def menu_item_click(e):
        accion = e.control.data
        if accion == "agregar_producto":
            content_area.alignment= ft.Alignment(0,0)
            agregarProductos(content_area,ft)
            
        elif accion == "eliminar_producto":
            content_area.content = ft.Text("Eliminar producto", size=25)
        elif accion == "ver_productos":
            content_area.content = ft.Text("Lista de productos", size=25)
        elif accion == "agregar_membresia":
            content_area.content = ft.Text("Agregar nueva membresía", size=25)
        elif accion == "ver_membresias":
            content_area.content = ft.Text("Lista de membresías", size=25)
        elif accion == "ver_ventas":
            content_area.content = ft.Text("Historial de ventas", size=25)
        elif accion == "reporte_ventas":
            content_area.content = ft.Text("Reporte de ventas", size=25)
        page.update()

    nav_bar = ft.Row(
        controls=[
            ft.PopupMenuButton(
                content=ft.Container(
                    content=ft.Text("Productos", size=16, weight=ft.FontWeight.BOLD),
                    width=150,
                    height=60,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#741717",
                ),
                items=[
                    ft.PopupMenuItem("Agregar Producto", data="agregar_producto", on_click=menu_item_click),
                    ft.PopupMenuItem("Eliminar Producto", data="eliminar_producto", on_click=menu_item_click),
                    ft.PopupMenuItem("Ver Productos", data="ver_productos", on_click=menu_item_click),
                ],
            ),
            
            ft.PopupMenuButton(
                content=ft.Container(
                    content=ft.Text("Membresías", size=16, weight=ft.FontWeight.BOLD),
                    width=150,
                    height=60,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#741717",
                ),
                items=[
                    ft.PopupMenuItem("Agregar Membresía", data="agregar_membresia", on_click=menu_item_click),
                    ft.PopupMenuItem("Ver Membresías", data="ver_membresias", on_click=menu_item_click),
                ],
            ),
            
            ft.PopupMenuButton(
                content=ft.Container(
                    content=ft.Text("Ventas", size=16, weight=ft.FontWeight.BOLD),
                    width=150,
                    height=60,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#741717",
                ),
                items=[
                    ft.PopupMenuItem("Ver Ventas", data="ver_ventas", on_click=menu_item_click),
                    ft.PopupMenuItem("Reporte de Ventas", data="reporte_ventas", on_click=menu_item_click),
                ],
            ),
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START,
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
    # Habilitar o deshabilitar los logs de las queries de la base de datos
    establecer_logs(True)

# Crear una sesión de base de datos
    session = crear_sesion()
    ft.app(target=main)