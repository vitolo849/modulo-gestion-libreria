import flet as ft

from datetime import date, timedelta
from libreria_cafe_edd_db import crear_sesion, establecer_logs, Membresia

from productos.agregar import view as agregarProductos
from productos.inventario import view as inventariosProductos
from productos.eliminar import view as eliminarProducto
from clientes.agg_cliente import view as agregarCliente

from membresia.ver_membresia import view as verMemebresia

from membresia.activas_membresia import view as agregarMembresia

## Importación de sección de reportes 
from reportes.clientes import view as clientesReportes
from reportes.compras import view as comprasReportes
from reportes.ventas import view as ventasReportes
from reportes.proveedores import view as proveedoresReportes


def main(page: ft.Page):
    page.title = "Administración Usuario"
    page.padding = 0
    page.bgcolor = "#741717"

    content_area = ft.Container(
        content=ft.Text("Modulo de administración y reportes", size=20),
        padding=40,
        alignment=ft.Alignment(0, 0),
        expand=True,
        bgcolor="#CBA68B"
    )

    def cambiar_vista(e):

        if e.control.data == "productos":
            content_area.content = ft.Text("Sección de Productos ", size=25)
        elif e.control.data == "membresias":
            content_area.content = ft.Text(
                "Sección de Membresías de Clientes", size=25)
        elif e.control.data == "ventas":
            content_area.content = ft.Text("Sección de ventas", size=25)
        elif e.control.data == "cliente":
            content_area.content = ft.Text("Sección de clientes", size=25)
        elif e.control.data == "reportes":
            content_area.content = ft.Text("Sección de clientes", size=25)
        page.update()

    def menu_item_click(e):
        accion = e.control.data
        if accion == "agregar_producto":
            content_area.alignment = ft.Alignment(0, 0)
            agregarProductos(content_area, ft)

        elif accion == "eliminar_producto":
            content_area.content = ft.Text("Eliminar producto", size=25)
            eliminarProducto(content_area, ft)
        elif accion == "ver_productos":
            content_area.alignment = ft.Alignment(0, 0)
            inventariosProductos(content_area, ft)
        elif accion == "ver_membresias":
            verMemebresia(content_area, ft)
        elif accion == "clientes":
            content_area.content = ft.Text("seccion de clientes", size=25)
            agregarCliente(content_area, ft)
        elif accion == "ver_ventas":
            content_area.content = ft.Text("Historial de ventas", size=25)
        elif accion == "reporte_ventas":
            content_area.content = ft.Text("Reporte de ventas", size=25)
        ###############################################
        ##Menu de reprotes
        elif accion == "reportesClientes":
            clientesReportes(content_area, ft)
        elif accion == "reportesVentas":
            ventasReportes(content_area, ft)
        elif accion == "reportesProveedores":
            proveedoresReportes(content_area, ft)
        elif accion == "reportesCompras":
            comprasReportes(content_area, ft)
        #################################################
        page.update()

    nav_bar = ft.Row(
        controls=[
            ft.PopupMenuButton(

                content=ft.Container(
                    content=ft.Row(
                        ##ICONO, Victor esto es importante poner el icono dentro del array de controls
                        controls=[
                            ft.Icon(ft.Icons.INVENTORY,
                                    color=ft.Colors.WHITE, size=20),
                            ft.Text("Productos", size=16,
                                    weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    width=150,
                    height=60,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#741717"
                ),
                items=[
                    ft.PopupMenuItem(
                        "Agregar Producto", data="agregar_producto", on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Eliminar Producto", data="eliminar_producto", on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Ver Productos", data="ver_productos", on_click=menu_item_click),
                ],
            ),

            ft.Container(width=50),  # Espaciador entre el título y los botones
            ft.Text("Modulo de administración y reportes",
                    size=15, color="#C7C8CA"),


            ft.Container(width=100),  # Espaciador para separar los botones

            ft.PopupMenuButton(

                content=ft.Container(

                    content=ft.Text(
                        "Membresías", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    width=150,
                    height=60,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#741717",

                ),
                items=[
                    ft.PopupMenuItem(
                        "Ver Membresías", data="ver_membresias", on_click=menu_item_click),
                ],
            ),

            ft.PopupMenuButton(
                content=ft.Container(

                    content=ft.Text(
                        "Ventas", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    width=150,
                    height=60,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#741717",
                ),
                items=[
                    ft.PopupMenuItem(
                        "Ver Ventas", data="ver_ventas", on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Reporte de Ventas", data="reporte_ventas", on_click=menu_item_click),
                ],
            ),

            ft.PopupMenuButton(
                content=ft.Container(

                    content=ft.Text(
                        "Clientes", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    width=150,
                    height=60,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#741717",
                ),
                items=[
                    ft.PopupMenuItem(
                        "Ver Clientes", data="clientes", on_click=menu_item_click),
                    ft.PopupMenuItem("Clientes con Membresía Activa",
                                     data="clientes_membresia", on_click=menu_item_click),
                ],
            ),

            ft.PopupMenuButton(
                content=ft.Container(

                    content=ft.Text(
                        "Reportes", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                    width=150,
                    height=60,
                    alignment=ft.Alignment(0, 0),
                    bgcolor="#741717",
                ),
                items=[
                    ft.PopupMenuItem(
                        "Clientes", data="reportesClientes", on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Ventas", data="reportesVentas", on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Compras", data="reportesCompras", on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Proveedores", data="reportesProveedores", on_click=menu_item_click),
                ],
            )
        ],
        spacing=0,
        alignment=ft.MainAxisAlignment.START,

    )

    page.add(
        ft.Column(
            controls=[
                nav_bar,
                ft.Divider(height=1, color=ft.Colors.BLACK),
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
