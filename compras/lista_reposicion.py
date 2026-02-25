# lista_reposicion.py
from datetime import date
from compras.models_lista_reposicion import (
    obtener_ordenes_pendientes,
    obtener_ordenes_completadas,
    obtener_detalle_orden_completo,
    actualizar_estado_orden,
    obtener_historial_ordenes
)

def view(content_area, ft):
    orden_seleccionada = None
    
    def cargar_ordenes_pendientes():
        print("Cargando órdenes pendientes...")
        ordenes = obtener_ordenes_pendientes()
        lista_pendientes.controls.clear()
        
        if ordenes:
            for orden in ordenes:
                color_estado = ft.Colors.ORANGE if orden["estado"] == "Pendiente" else ft.Colors.BLUE
                
                orden_container = ft.Container(
                    content=ft.Column([
                        ft.Row([
                            ft.Text(f"Orden #{orden['id']}", weight=ft.FontWeight.BOLD, size=14),
                            ft.Container(
                                content=ft.Text(orden["estado"], color=ft.Colors.WHITE, size=11),
                                bgcolor=color_estado,
                                padding=ft.padding.all(3),
                                border_radius=5
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Text(f"Proveedor: {orden['proveedor']}", size=12),
                        ft.Row([
                            ft.Text(f"Fecha: {orden['fecha']}", size=12),
                            ft.Text(f"Total: {orden['total']}", weight=ft.FontWeight.BOLD, size=12)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        ft.Row([
                            ft.Container(width=0),
                            ft.ElevatedButton(
                                "Ver Detalle",
                                on_click=lambda _, oid=orden["id"]: ver_detalle_orden(oid),
                                width=90,
                                height=30,
                                style=ft.ButtonStyle(padding=5)
                            )
                        ], alignment=ft.MainAxisAlignment.END)
                    ], spacing=5),
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    bgcolor=ft.Colors.WHITE,
                    width=500
                )
                lista_pendientes.controls.append(orden_container)
        else:
            lista_pendientes.controls.append(
                ft.Container(
                    content=ft.Text("No hay órdenes pendientes", color=ft.Colors.GREY, italic=True),
                    padding=20,
                    alignment=ft.Alignment(0, 0)  # Cambiado de ft.alignment.center
                )
            )
        
        lista_pendientes.update()
    
    def cargar_ordenes_completadas():
        print("Cargando órdenes completadas...")
        ordenes = obtener_ordenes_completadas()
        lista_completadas.controls.clear()
        
        if ordenes:
            for orden in ordenes:
                orden_container = ft.Container(
                    content=ft.Column([
                        ft.Text(f"Orden #{orden['id']}", weight=ft.FontWeight.BOLD, size=14),
                        ft.Text(f"Proveedor: {orden['proveedor']}", size=12),
                        ft.Row([
                            ft.Text(f"Solicitud: {orden['fecha_solicitud']}", size=11),
                            ft.Text(f"Entrega: {orden['fecha_entrega']}", size=11)
                        ]),
                        ft.Text(f"Total: {orden['total']}", weight=ft.FontWeight.BOLD, size=12)
                    ], spacing=5),
                    padding=10,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5,
                    bgcolor=ft.Colors.GREY_50,
                    width=500
                )
                lista_completadas.controls.append(orden_container)
        else:
            lista_completadas.controls.append(
                ft.Container(
                    content=ft.Text("No hay órdenes completadas", color=ft.Colors.GREY, italic=True),
                    padding=20,
                    alignment=ft.Alignment(0, 0)  # Cambiado de ft.alignment.center
                )
            )
        
        lista_completadas.update()
    
    def ver_detalle_orden(id_orden):
        print(f"Viendo detalle de orden #{id_orden}")
        datos = obtener_detalle_orden_completo(id_orden)
        
        if not datos:
            mostrar_mensaje("No se pudo cargar el detalle de la orden")
            return
        
        nonlocal orden_seleccionada
        orden_seleccionada = datos
        
        contenido_detalle = ft.Column([], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        contenido_detalle.controls.append(
            ft.Container(
                content=ft.Column([
                    ft.Row([
                        ft.Text(f"ORDEN #{datos['orden']['id']}", size=18, weight=ft.FontWeight.BOLD),
                        ft.Container(
                            content=ft.Text(datos['orden']['estado'], color=ft.Colors.WHITE),
                            bgcolor=ft.Colors.BLUE if datos['orden']['estado'] == "Pendiente" else 
                                   ft.Colors.GREEN if datos['orden']['estado'] == "Recibida" else
                                   ft.Colors.ORANGE,
                            padding=ft.padding.all(5),
                            border_radius=5
                        )
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    ft.Divider(height=10),
                    ft.Row([
                        ft.Column([
                            ft.Text("📅 Fechas:", weight=ft.FontWeight.BOLD),
                            ft.Text(f"  Solicitud: {datos['orden']['fecha_solicitud']}"),
                            ft.Text(f"  Entrega: {datos['orden']['fecha_entrega']}"),
                        ], spacing=5),
                        ft.Column([
                            ft.Text("🏢 Proveedor:", weight=ft.FontWeight.BOLD),
                            ft.Text(f"  {datos['proveedor']['nombre']}"),
                            ft.Text(f"  RIF: {datos['proveedor']['rif']}"),
                            ft.Text(f"  📞 {datos['proveedor']['telefono'] or 'N/A'}"),
                        ], spacing=5)
                    ]),
                ]),
                padding=10,
                bgcolor=ft.Colors.GREY_50,
                border_radius=5
            )
        )
        
        if datos['detalles']:
            productos_list = []
            for d in datos['detalles']:
                productos_list.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Column([
                                ft.Text(d['titulo'], weight=ft.FontWeight.BOLD, size=13),
                                ft.Text(f"ISBN: {d['isbn']}", size=10, color=ft.Colors.GREY),
                            ], expand=True, spacing=2),
                            ft.Container(
                                content=ft.Text(f"${d['subtotal']:.2f}", weight=ft.FontWeight.BOLD, size=12),
                                padding=5
                            )
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                        padding=8,
                        border=ft.border.all(1, ft.Colors.GREY_300),
                        border_radius=5,
                        bgcolor=ft.Colors.WHITE
                    )
                )
            
            contenido_detalle.controls.append(
                ft.Container(
                    content=ft.Column([
                        ft.Text("📦 Productos:", size=14, weight=ft.FontWeight.BOLD),
                        ft.Column(productos_list, spacing=5),
                        ft.Divider(),
                        ft.Row([
                            ft.Text("TOTAL:", size=16, weight=ft.FontWeight.BOLD),
                            ft.Text(f"${datos['orden']['total']:.2f}", size=16, weight=ft.FontWeight.BOLD, color=ft.Colors.GREEN)
                        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
                    ], spacing=8),
                    padding=10
                )
            )
        else:
            contenido_detalle.controls.append(
                ft.Container(
                    content=ft.Text("No hay productos en esta orden", italic=True),
                    padding=20,
                    alignment=ft.Alignment(0, 0)  # Cambiado de ft.alignment.center
                )
            )
        
        if datos['orden']['estado'] in ["Pendiente", "Enviada"]:
            acciones = ft.Container(
                content=ft.Row([
                    ft.ElevatedButton(
                        "📤 Enviada" if datos['orden']['estado'] == "Pendiente" else "📥 Recibida",
                        on_click=lambda _, oid=id_orden: cambiar_estado(oid),
                        bgcolor=ft.Colors.GREEN,
                        color=ft.Colors.WHITE,
                        width=140
                    ),
                    ft.ElevatedButton(
                        "❌ Cancelar",
                        on_click=lambda _, oid=id_orden: cancelar_orden(oid),
                        bgcolor=ft.Colors.RED,
                        color=ft.Colors.WHITE,
                        width=140
                    )
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=10),
                padding=10
            )
            contenido_detalle.controls.append(acciones)
        
        contenido_detalle.controls.append(
            ft.Container(
                content=ft.ElevatedButton("Cerrar Detalle", on_click=cerrar_detalle, width=200),
                padding=10,
                alignment=ft.Alignment(0, 0)  # Cambiado de ft.alignment.center
            )
        )
        
        detalle_container.content = ft.Container(
            content=contenido_detalle,
            padding=10,
            height=480,
            width=580
        )
        detalle_container.update()
    
    def cambiar_estado(id_orden):
        if not orden_seleccionada:
            return
        
        estado_actual = orden_seleccionada['orden']['estado']
        nuevo_estado = "Enviada" if estado_actual == "Pendiente" else "Recibida"
        
        print(f"Cambiando orden #{id_orden} de {estado_actual} a {nuevo_estado}")
        
        resultado = actualizar_estado_orden(id_orden, nuevo_estado)
        
        if resultado["success"]:
            mostrar_mensaje(resultado["message"])
            cargar_ordenes_pendientes()
            cargar_ordenes_completadas()
            ver_detalle_orden(id_orden)
        else:
            mostrar_mensaje(f"Error: {resultado['error']}")
    
    def cancelar_orden(id_orden):
        if not orden_seleccionada:
            return
        
        resultado = actualizar_estado_orden(id_orden, "Cancelada")
        
        if resultado["success"]:
            mostrar_mensaje(f"Orden #{id_orden} cancelada")
            cargar_ordenes_pendientes()
            cerrar_detalle(None)
        else:
            mostrar_mensaje(f"Error: {resultado['error']}")
    
    def cerrar_detalle(e):
        nonlocal orden_seleccionada
        orden_seleccionada = None
        detalle_container.content = ft.Container(
            content=ft.Column([
                ft.Text("📋", size=40),
                ft.Text("Seleccione una orden para ver el detalle", color=ft.Colors.GREY, size=16)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.Alignment(0, 0),  # Cambiado de ft.alignment.center
            height=480
        )
        detalle_container.update()
    
    def mostrar_mensaje(texto):
        snack = ft.SnackBar(content=ft.Text(texto))
        content_area.page.overlay.append(snack)
        snack.open = True
        content_area.page.update()
    
    def recargar_todo(e):
        cargar_ordenes_pendientes()
        cargar_ordenes_completadas()
        cerrar_detalle(None)
    
    # ===== CONTROLES UI =====
    lista_pendientes = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)
    lista_completadas = ft.Column(spacing=8, scroll=ft.ScrollMode.AUTO)
    
    detalle_container = ft.Container(
        content=ft.Container(
            content=ft.Column([
                ft.Text("📋", size=40),
                ft.Text("Seleccione una orden para ver el detalle", color=ft.Colors.GREY, size=16)
            ], alignment=ft.MainAxisAlignment.CENTER, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            alignment=ft.Alignment(0, 0),  # Cambiado de ft.alignment.center
            height=480
        ),
        padding=10,
        border=ft.border.all(1, ft.Colors.GREY_400),
        border_radius=5,
        bgcolor=ft.Colors.WHITE,
        width=600,
        height=500
    )
    
    # ===== CONTENIDO PRINCIPAL =====
    contenido_principal = ft.Column([
        ft.Text("📋 LISTA DE ÓRDENES DE REPOSICIÓN", size=28, weight=ft.FontWeight.BOLD),
        ft.Divider(height=15),
        
        ft.Row([
            ft.ElevatedButton("🔄 Recargar", on_click=recargar_todo),
        ], alignment=ft.MainAxisAlignment.CENTER),
        
        ft.Container(height=10),
        
        ft.Row([
            # Columna izquierda: Listas de órdenes
            ft.Container(
                content=ft.Column([
                    ft.Container(
                        content=ft.Text("⏳ Órdenes Pendientes/Enviadas", size=16, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.BLUE_50,
                        padding=10,
                        border_radius=5
                    ),
                    ft.Container(
                        content=lista_pendientes,
                        height=200,
                        padding=5
                    ),
                    ft.Container(height=10),
                    ft.Container(
                        content=ft.Text("✅ Órdenes Completadas", size=16, weight=ft.FontWeight.BOLD),
                        bgcolor=ft.Colors.GREEN_50,
                        padding=10,
                        border_radius=5
                    ),
                    ft.Container(
                        content=lista_completadas,
                        height=180,
                        padding=5
                    ),
                ], spacing=5, scroll=ft.ScrollMode.AUTO),
                width=550,
                height=480,
                padding=10,
                border=ft.border.all(1, ft.Colors.GREY_400),
                border_radius=5,
                bgcolor=ft.Colors.WHITE
            ),
            
            ft.Container(width=20),
            
            # Columna derecha: Detalle de la orden seleccionada
            ft.Container(
                content=detalle_container,
                width=600,
                height=500,
                padding=5
            )
        ], alignment=ft.MainAxisAlignment.CENTER, vertical_alignment=ft.CrossAxisAlignment.START),
        
    ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER, expand=True)
    
    # Contenedor blanco centrado
    contenedor_blanco = ft.Container(
        content=contenido_principal,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        padding=20,
        width=1250,
        height=650,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.GREY_300
        )
    )
    
    # Centrar perfectamente - usando Alignment(0,0)
    contenido_final = ft.Container(
        content=ft.Row(
            controls=[contenedor_blanco],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.Alignment(0, 0),  # Cambiado de ft.alignment.center
        expand=True,
        bgcolor=ft.Colors.GREY_100
    )
    
    content_area.content = contenido_final
    content_area.update()
    
    # Cargar datos iniciales
    cargar_ordenes_pendientes()
    cargar_ordenes_completadas()