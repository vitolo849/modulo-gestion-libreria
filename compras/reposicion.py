# reposicion.py
from datetime import date
from compras.models import (
    obtener_proveedores,
    obtener_productos_por_tipo,
    crear_orden_reposicion,
    obtener_ordenes_recientes,
    libros_bajo_stock
)

def view(content_area, ft):
    items_orden = []
    
    def cargar_productos(e):
        print("Cargando productos...")
        productos = obtener_productos_por_tipo("LIBRO")
        print(f"Productos encontrados: {len(productos)}")
        
        if productos:
            opciones = []
            for p in productos:
                print(f"  - {p['nombre']} (ID: {p['id']})")
                opciones.append(
                    ft.dropdown.Option(
                        key=str(p["id"]),
                        text=f"{p['nombre']} (Stock: {p['stock_actual']})"
                    )
                )
            producto_dropdown.options = opciones
            producto_dropdown.update()
    
    def producto_selected(e):
        print(f"Producto seleccionado: {producto_dropdown.value}")
        if producto_dropdown.value:
            productos = obtener_productos_por_tipo("LIBRO")
            for p in productos:
                if str(p["id"]) == producto_dropdown.value:
                    precio_input.value = str(p["precio"])
                    precio_input.update()
                    print(f"Precio cargado: {p['precio']}")
                    break
    
    def agregar_item(e):
        print("=== AGREGAR ITEM ===")
        print(f"Producto value: {producto_dropdown.value}")
        print(f"Cantidad value: {cantidad_input.value}")
        print(f"Precio value: {precio_input.value}")
        
        try:
            if not producto_dropdown.value:
                print("Error: No hay producto seleccionado")
                mostrar_mensaje("Seleccione un producto")
                return
            
            if not cantidad_input.value:
                print("Error: No hay cantidad")
                mostrar_mensaje("Ingrese una cantidad")
                return
            
            if not precio_input.value:
                print("Error: No hay precio")
                mostrar_mensaje("Ingrese un precio")
                return
            
            productos = obtener_productos_por_tipo("LIBRO")
            nombre_producto = ""
            for p in productos:
                if str(p["id"]) == producto_dropdown.value:
                    nombre_producto = p["nombre"]
                    print(f"Producto encontrado: {nombre_producto}")
                    break
            
            item = {
                "id_producto": int(producto_dropdown.value),
                "nombre": nombre_producto,
                "tipo": "LIBRO",
                "cantidad": int(cantidad_input.value),
                "precio_compra": float(precio_input.value)
            }
            print(f"Item creado: {item}")
            
            items_orden.append(item)
            print(f"Items en orden ahora: {len(items_orden)}")
            
            actualizar_lista_items()
            limpiar_campos_producto()
            mostrar_mensaje(f"Producto agregado: {nombre_producto}")
                
        except Exception as ex:
            print(f"Error al agregar item: {ex}")
            mostrar_mensaje(f"Error: {str(ex)}")
    
    def eliminar_item(index):
        print(f"Eliminando item {index}")
        items_orden.pop(index)
        actualizar_lista_items()
    
    def actualizar_lista_items():
        print(f"Actualizando lista. Items: {len(items_orden)}")
        items_list.controls.clear()
        
        for i, item in enumerate(items_orden):
            subtotal = item["cantidad"] * item["precio_compra"]
            
            # Usar Alignment(0,0) en lugar de alignment.center
            btn_eliminar = ft.Container(
                content=ft.Text("✖", size=20, color=ft.Colors.RED),
                width=40,
                height=40,
                alignment=ft.Alignment(0, 0),  # Cambiado de ft.alignment.center
                on_click=lambda _, idx=i: eliminar_item(idx)
            )
            
            items_list.controls.append(
                ft.Container(
                    content=ft.Row([
                        ft.Text(f"{item['nombre']} - {item['cantidad']} x ${item['precio_compra']:.2f} = ${subtotal:.2f}"),
                        btn_eliminar
                    ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                    padding=5,
                    border=ft.border.all(1, ft.Colors.GREY_300),
                    border_radius=5
                )
            )
        
        items_list.update()
        
        total = sum(item["cantidad"] * item["precio_compra"] for item in items_orden)
        total_label.value = f"Total: ${total:.2f}"
        total_label.update()
    
    def limpiar_campos_producto():
        print("Limpiando campos")
        producto_dropdown.value = None
        cantidad_input.value = ""
        precio_input.value = ""
        producto_dropdown.update()
        cantidad_input.update()
        precio_input.update()
    
    def guardar_orden(e):
        print("=== GUARDAR ORDEN ===")
        print(f"Items: {len(items_orden)}")
        print(f"Proveedor: {proveedor_dropdown.value}")
        
        if not items_orden:
            mostrar_mensaje("No hay productos en la orden")
            return
        
        if not proveedor_dropdown.value:
            mostrar_mensaje("Seleccione un proveedor")
            return
        
        total = sum(item["cantidad"] * item["precio_compra"] for item in items_orden)
        orden_data = {
            "id_proveedor": int(proveedor_dropdown.value),
            "fecha_solicitud": date.today(),
            "items": items_orden.copy(),
            "total": total
        }
        print(f"Datos de orden: {orden_data}")
        
        resultado = crear_orden_reposicion(orden_data)
        print(f"Resultado: {resultado}")
        
        if resultado["success"]:
            items_orden.clear()
            proveedor_dropdown.value = None
            actualizar_lista_items()
            libros_alertas = libros_bajo_stock()
            actualizar_alertas_stock(libros_alertas)
            mostrar_mensaje(f"Orden #{resultado['orden_id']} creada exitosamente")
            limpiar_campos_producto()
        else:
            mostrar_mensaje(f"Error: {resultado['error']}")
    
    def mostrar_mensaje(texto):
        print(f"MENSAJE: {texto}")
        snack = ft.SnackBar(content=ft.Text(texto))
        content_area.page.overlay.append(snack)
        snack.open = True
        content_area.page.update()
    
    def actualizar_alertas_stock(libros_alertas):
        alertas_container.controls.clear()
        if libros_alertas:
            for libro in libros_alertas[:3]:
                alertas_container.controls.append(
                    ft.Container(
                        content=ft.Row([
                            ft.Text("⚠️", size=20),
                            ft.Text(f"{libro['titulo']}: Stock {libro['stock_actual']} (Mínimo {libro['stock_minimo']})"),
                        ]),
                        bgcolor=ft.Colors.ORANGE_50,
                        padding=5,
                        border_radius=5
                    )
                )
        else:
            alertas_container.controls.append(
                ft.Text("Todos los productos tienen stock suficiente", color=ft.Colors.GREEN)
            )
        alertas_container.update()
    
    # ===== CONTROLES UI =====
    proveedores = obtener_proveedores()
    opciones_proveedor = []
    for p in proveedores:
        opciones_proveedor.append(
            ft.dropdown.Option(key=str(p["id"]), text=p["nombre_empresa"])
        )
    
    proveedor_dropdown = ft.Dropdown(
        label="Seleccionar Proveedor",
        hint_text="Elige un proveedor...",
        width=400,
        options=opciones_proveedor
    )
    
    btn_cargar_productos = ft.ElevatedButton(
        "Cargar Productos",
        on_click=cargar_productos,
        width=200
    )
    
    producto_dropdown = ft.Dropdown(
        label="Producto",
        hint_text="Elige un producto...",
        width=400,
        options=[]
    )
    producto_dropdown.on_change = producto_selected
    
    cantidad_input = ft.TextField(
        label="Cantidad",
        width=150,
        keyboard_type=ft.KeyboardType.NUMBER,
        value="1"
    )
    
    precio_input = ft.TextField(
        label="Precio de Compra",
        width=200,
        keyboard_type=ft.KeyboardType.NUMBER
    )
    
    btn_agregar = ft.ElevatedButton(
        "Agregar a la Orden",
        on_click=agregar_item
    )
    
    items_list = ft.Column(spacing=5)
    
    total_label = ft.Text("Total: $0.00", size=18, weight=ft.FontWeight.BOLD)
    
    btn_guardar = ft.ElevatedButton(
        "Guardar Orden",
        on_click=guardar_orden,
        width=200
    )
    
    btn_cancelar = ft.ElevatedButton(
        "Cancelar",
        width=200,
        on_click=lambda _: limpiar_campos_producto()
    )
    
    alertas_container = ft.Column(spacing=5)
    
    ordenes_recientes = obtener_ordenes_recientes()
    ordenes_container = ft.Column(spacing=5)
    for orden in ordenes_recientes:
        ordenes_container.controls.append(
            ft.Container(
                content=ft.Row([
                    ft.Text(f"{orden['fecha']} - {orden['proveedor']}"),
                    ft.Text(orden['estado'], color=ft.Colors.BLUE),
                    ft.Text(orden['total'], weight=ft.FontWeight.BOLD)
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                padding=5,
                border=ft.border.all(1, ft.Colors.GREY_300),
                border_radius=5
            )
        )
    
    # ===== CONTENIDO PRINCIPAL =====
    contenido_principal = ft.Column([
        ft.Text("REPOSICIÓN DE PRODUCTOS", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Alertas de Stock Bajo", size=16, weight=ft.FontWeight.BOLD),
                alertas_container,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            bgcolor=ft.Colors.ORANGE_50,
            border_radius=5,
            width=600
        ),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Nueva Orden de Reposición", size=16, weight=ft.FontWeight.BOLD),
                proveedor_dropdown,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            width=600
        ),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Agregar Producto", size=16, weight=ft.FontWeight.BOLD),
                btn_cargar_productos,
                producto_dropdown,
                ft.Row([cantidad_input, precio_input], spacing=10, alignment=ft.MainAxisAlignment.CENTER),
                btn_agregar,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            width=600
        ),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Productos en la Orden", size=16, weight=ft.FontWeight.BOLD),
                items_list,
                ft.Divider(),
                total_label,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            width=600
        ),
        
        ft.Row([btn_guardar, btn_cancelar], alignment=ft.MainAxisAlignment.CENTER, spacing=20),
        
        ft.Divider(height=20),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Órdenes Recientes", size=16, weight=ft.FontWeight.BOLD),
                ordenes_container,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=10,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            width=600
        ),
        
    ], spacing=20, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
    
    contenedor_blanco = ft.Container(
        content=contenido_principal,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        padding=20,
        width=700,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.GREY_300
        )
    )
    
    contenido_final = ft.Row(
        controls=[contenedor_blanco],
        alignment=ft.MainAxisAlignment.CENTER,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
        expand=True
    )
    
    content_area.content = contenido_final
    content_area.update()
    
    libros_alertas = libros_bajo_stock()
    actualizar_alertas_stock(libros_alertas)
    
    print("=== REPOSICIÓN INICIADA ===")