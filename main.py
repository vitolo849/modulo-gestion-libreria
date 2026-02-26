import flet as ft
from datetime import date, timedelta
from libreria_cafe_edd_db import crear_sesion, establecer_logs, Membresia
from productos.agregar import view as agregarProductos
from productos.inventario import view as inventariosProductos
from productos.eliminar import view as eliminarProducto
from clientes.agg_cliente import view as agregarCliente
from membresia.ver_membresia import view as verMemebresia
from membresia.activas_membresia import view as agregarMembresia
from ventas.ver_ventas import view as verVentas
from reportes.clientes import view as clientesReportes
from reportes.compras import view as comprasReportes
from reportes.ventas import view as ventasReportes
from reportes.proveedores import view as proveedoresReportes
from reportes.models import cargar_datos_prueba
from compras.reposicion import view as reposicionCompras
from compras.lista_reposicion import view as ordenesCompras

from clientes.Gestion import view as gestionClientes

from proveedor.Agregar import view as agregarProveedor

def crear_boton_acceso(titulo, icono, data_accion, menu_click_func):
    return ft.Container(
        content=ft.Column([
            ft.Icon(icono, size=40, color="white"),
            ft.Text(titulo, size=16, weight="bold", color="white"),
        ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
        width=250,
        height=180,
        bgcolor="#8D695D",
        border_radius=15,
        animate_scale=300,
        data=data_accion,
        on_click=menu_click_func,
        on_hover=lambda e: (setattr(
            e.control, "scale", 1.05 if e.data == "true" else 1.0), e.control.update()),
    )
def main(page: ft.Page):
    page.title = "Administración Usuario"
    page.padding = 0
    page.bgcolor = "#741717"
    content_area = ft.Container(
        padding=40,
        alignment=ft.Alignment(0, 0),
        expand=True,
        bgcolor="#CBA68B",
        content=ft.Column(scroll=ft.ScrollMode.ADAPTIVE)
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
        content_area.content = ft.Column(scroll=ft.ScrollMode.ADAPTIVE)
        if accion == "agregar_producto":
            content_area.alignment = ft.Alignment(0, 0)
            agregarProductos(content_area, ft)
        elif accion == "eliminar_producto":
            eliminarProducto(content_area, ft)
        elif accion == "ver_productos":
            content_area.alignment = ft.Alignment(0, 0)
            inventariosProductos(content_area, ft)
        elif accion == "ver_membresias":
            verMemebresia(content_area, ft)
        elif accion == "clientes" or accion == "ver_clientes":
            content_area.content.controls.append(
                ft.Text("Sección de Clientes", size=25))
            agregarCliente(content_area, ft)
        elif accion == "ver_ventas" :
            verVentas(content_area, ft)
        elif accion == "reportesClientes" or accion == "reporte_clientes":
            clientesReportes(content_area, ft)
        elif accion == "reportesVentas":
            ventasReportes(content_area, ft)
        elif accion == "reportesProveedores":
            proveedoresReportes(content_area, ft)
        elif accion == "reportesCompras":
            comprasReportes(content_area, ft)
        elif accion == "comprasReposicion":
            reposicionCompras(content_area, ft)
        elif accion == "comprasOrdenes":
            ordenesCompras(content_area, ft)
        elif accion == "gestionClientes":
            gestionClientes(content_area, ft)
        elif accion == "proveedorAgregar":
            agregarProveedor(content_area, ft)
        elif accion == "TEST_TEMP":
            cargar_datos_prueba()
        page.update()


    def mostrar_dashboard():
        content_area.content = ft.Row(
            controls=[
                crear_boton_acceso(
                    "Ventas de Hoy", ft.Icons.SHOPPING_CART, "ver_ventas", menu_item_click),
                crear_boton_acceso(
                    "Ver Clientes", ft.Icons.PERSON_ADD, "clientes", menu_item_click),
                crear_boton_acceso(
                    "Stock / Inventario", ft.Icons.INVENTORY, "ver_productos", menu_item_click),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=30
        )
        page.update()
    def ir_al_inicio(e):
        content_area.alignment = ft.Alignment(0, 0)
        mostrar_dashboard()
        page.update()
    nav_bar = ft.Row(
        controls=[
            ft.IconButton(
                icon=ft.Icons.HOME_ROUNDED,
                icon_color=ft.Colors.WHITE,
                icon_size=30,
                tooltip="Ir al Inicio",
                on_click=ir_al_inicio
            ),
            ft.PopupMenuButton(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    width=150, height=60, alignment=ft.Alignment(0, 0), bgcolor="#741717"
                ),
            ),
            ft.VerticalDivider(width=20, color=ft.Colors.TRANSPARENT),
            ft.Text("Modulo de administración y reportes",
                    size=15, color="#C7C8CA"),
            ft.Container(expand=True),


            
            ft.PopupMenuButton(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.FACTORY_OUTLINED,
                                    color=ft.Colors.WHITE, size=20),
                            ft.Text("Proveedores", size=16,
                                    weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    width=120, height=60, alignment=ft.Alignment(0, 0), bgcolor="#741717"
                ),
                items=[
                    ft.PopupMenuItem("Agregar", data="proveedorAgregar",
                                     on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Temporal", data="reporte_ventas", on_click=menu_item_click),
                ],
            ),



            ft.PopupMenuButton(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.SELL_OUTLINED,
                                    color=ft.Colors.WHITE, size=20),
                            ft.Text("Compras", size=16,
                                    weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    width=120, height=60, alignment=ft.Alignment(0, 0), bgcolor="#741717"
                ),
                items=[
                    ft.PopupMenuItem("Reposición", data="comprasReposicion",
                                     on_click=menu_item_click),
                    ft.PopupMenuItem("Ordenes", data="comprasOrdenes",
                                     on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Temporal", data="reporte_ventas", on_click=menu_item_click),
                ],
            ),

            ft.PopupMenuButton(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.PERSON,
                                    color=ft.Colors.WHITE, size=20),
                            ft.Text("Clientes", size=16,
                                    weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    width=110, height=60, alignment=ft.Alignment(0, 0), bgcolor="#741717"
                ),
                items=[
                    ft.PopupMenuItem(
                        "Gestión", data="gestionClientes", on_click=menu_item_click),
                ],
            ),
            ft.PopupMenuButton(
                content=ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(ft.Icons.BAR_CHART,
                                    color=ft.Colors.WHITE, size=20),
                            ft.Text("Reportes", size=16,
                                    weight=ft.FontWeight.BOLD, color=ft.Colors.WHITE),
                        ],
                        alignment=ft.MainAxisAlignment.CENTER,
                        spacing=8,
                    ),
                    width=120, height=60, alignment=ft.Alignment(0, 0), bgcolor="#741717"
                ),
                items=[
                    ft.PopupMenuItem(
                        "Clientes", data="reportesClientes", on_click=menu_item_click),
                    ft.PopupMenuItem("Ventas", data="reportesVentas",
                                     on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Compras", data="reportesCompras", on_click=menu_item_click),
                    ft.PopupMenuItem(
                        "Proveedores", data="reportesProveedores", on_click=menu_item_click),
                    ft.PopupMenuItem("TEST_TEMP", data="TEST_TEMP",
                                     on_click=menu_item_click),
                ],
            )
        ],
        spacing=10,
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
    mostrar_dashboard()
if __name__ == "__main__":
    establecer_logs(True)
    session = crear_sesion()
    ft.app(target=main)
