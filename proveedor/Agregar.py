# proveedores.py
from datetime import date
from proveedor.models_proveedores import (
    obtener_proveedores,
    obtener_proveedor_por_id,
    crear_proveedor,
    actualizar_proveedor,
    eliminar_proveedor,
    verificar_rif_unico
)

def view(content_area, ft):
    proveedor_seleccionado = None
    busqueda_actual = ""
    modo_edicion = False
    
    def cargar_proveedores(busqueda=""):
        print(f"Cargando proveedores... Búsqueda: '{busqueda}'")
        proveedores = obtener_proveedores(busqueda)
        
        # Limpiar tabla
        tabla_proveedores.rows.clear()
        
        if proveedores:
            for proveedor in proveedores:
                btn_modificar = ft.Container(
                    content=ft.Text("✏️", size=20),
                    tooltip="Modificar",
                    on_click=lambda _, pid=proveedor["id"]: abrir_modal_modificar(pid),
                    padding=5
                )
                
                btn_eliminar = ft.Container(
                    content=ft.Text("🗑️", size=20),
                    tooltip="Eliminar",
                    on_click=lambda _, pid=proveedor["id"], nom=proveedor["nombre_empresa"]: confirmar_eliminar(pid, nom),
                    padding=5
                )
                
                tabla_proveedores.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(proveedor["id"]))),
                            ft.DataCell(ft.Text(proveedor["nombre_empresa"])),
                            ft.DataCell(ft.Text(proveedor["rif_nit"])),
                            ft.DataCell(ft.Text(proveedor["telefono"])),
                            ft.DataCell(ft.Text(proveedor["email"])),
                            ft.DataCell(ft.Row([btn_modificar, btn_eliminar]))
                        ]
                    )
                )
        else:
            # Crear una fila con un mensaje centrado (sin usar col_span)
            tabla_proveedores.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("")),  # Celda vacía para ID
                        ft.DataCell(ft.Text("")),  # Celda vacía para Empresa
                        ft.DataCell(ft.Text("")),  # Celda vacía para RIF
                        ft.DataCell(ft.Text("")),  # Celda vacía para Teléfono
                        ft.DataCell(ft.Text("")),  # Celda vacía para Email
                        ft.DataCell(
                            ft.Container(
                                content=ft.Text("No hay proveedores", text_align=ft.TextAlign.CENTER),
                                alignment=ft.Alignment(0, 0),
                                width=200,
                                padding=10
                            )
                        )
                    ]
                )
            )
        
        tabla_proveedores.update()
        lbl_resultados.value = f"Mostrando {len(proveedores)} proveedores"
        lbl_resultados.update()
    
    def buscar_proveedores(e):
        nonlocal busqueda_actual
        busqueda_actual = txt_busqueda.value if txt_busqueda.value else ""
        cargar_proveedores(busqueda_actual)
    
    def limpiar_busqueda(e):
        txt_busqueda.value = ""
        nonlocal busqueda_actual
        busqueda_actual = ""
        cargar_proveedores()
        txt_busqueda.update()
    
    def abrir_modal_nuevo(e):
        nonlocal modo_edicion, proveedor_seleccionado
        modo_edicion = False
        proveedor_seleccionado = None
        print("Abriendo modal para nuevo proveedor")
        
        # Crear campos vacíos
        txt_nombre = ft.TextField(label="Nombre de la Empresa", width=350)
        txt_rif = ft.TextField(label="RIF/NIT", width=350, hint_text="Ej: J-12345678-9")
        txt_telefono = ft.TextField(label="Teléfono", width=350, hint_text="Opcional")
        txt_email = ft.TextField(label="Email", width=350, hint_text="Opcional")
        
        def guardar_nuevo(e):
            
            if not txt_nombre.value:
                mostrar_mensaje("El nombre de la empresa es obligatorio")
                return
            
            if not txt_rif.value:
                mostrar_mensaje("El RIF/NIT es obligatorio")
                return
            
            datos = {
                "nombre_empresa": txt_nombre.value,
                "rif_nit": txt_rif.value,
                "telefono": txt_telefono.value or None,
                "email": txt_email.value or None
            }
            
            
            resultado = crear_proveedor(datos)
            
            
            if resultado["success"]:
                modal.open = False
                content_area.page.update()
                cargar_proveedores(busqueda_actual)
                mostrar_mensaje("Proveedor creado correctamente")
            else:
                mostrar_mensaje(f"Error: {resultado['error']}")
        
        def cancelar_modal(e):
            cerrar_modal()
        
        # Botones
        btn_guardar = ft.ElevatedButton(
            "Guardar", 
            on_click=guardar_nuevo, 
            bgcolor=ft.Colors.GREEN, 
            color=ft.Colors.WHITE
        )
        
        btn_cancelar = ft.ElevatedButton(
            "Cancelar", 
            on_click=cancelar_modal
        )
        
        # Crear contenido del modal
        modal_content = ft.Column([
            ft.Text("Nuevo Proveedor", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10),
            txt_nombre,
            txt_rif,
            txt_telefono,
            txt_email,
            ft.Row([btn_guardar, btn_cancelar], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        modal.content = ft.Container(
            content=modal_content,
            padding=20,
            width=450,
            height=500
        )
        
        modal.open = True
        content_area.page.update()
    
    def abrir_modal_modificar(id_proveedor):
        nonlocal modo_edicion, proveedor_seleccionado
        modo_edicion = True
        
        datos = obtener_proveedor_por_id(id_proveedor)
        if not datos:
            mostrar_mensaje("No se pudo cargar el proveedor")
            return
        
        proveedor_seleccionado = datos
        
        # Crear campos con valores
        txt_nombre = ft.TextField(label="Nombre de la Empresa", value=datos["nombre_empresa"], width=350)
        txt_rif = ft.TextField(label="RIF/NIT", value=datos["rif_nit"], width=350)
        txt_telefono = ft.TextField(label="Teléfono", value=datos["telefono"] or "", width=350)
        txt_email = ft.TextField(label="Email", value=datos["email"] or "", width=350)
        
        def guardar_cambios(e):
            
            if not txt_nombre.value:
                mostrar_mensaje("El nombre de la empresa es obligatorio")
                return
            
            if not txt_rif.value:
                mostrar_mensaje("El RIF/NIT es obligatorio")
                return
            
            datos_actualizados = {
                "nombre_empresa": txt_nombre.value,
                "rif_nit": txt_rif.value,
                "telefono": txt_telefono.value or None,
                "email": txt_email.value or None
            }
            
            
            resultado = actualizar_proveedor(id_proveedor, datos_actualizados)
            
            
            if resultado["success"]:
                modal.open = False
                content_area.page.update()
                cargar_proveedores(busqueda_actual)
                mostrar_mensaje("Proveedor actualizado correctamente")
            else:
                mostrar_mensaje(f"Error: {resultado['error']}")
        
        def cancelar_modal(e):
            cerrar_modal()
        
        # Botones
        btn_guardar = ft.ElevatedButton(
            "Actualizar", 
            on_click=guardar_cambios, 
            bgcolor=ft.Colors.GREEN, 
            color=ft.Colors.WHITE
        )
        
        btn_cancelar = ft.ElevatedButton(
            "Cancelar", 
            on_click=cancelar_modal
        )
        
        # Crear contenido del modal
        modal_content = ft.Column([
            ft.Text(f"Modificar Proveedor #{id_proveedor}", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10),
            txt_nombre,
            txt_rif,
            txt_telefono,
            txt_email,
            ft.Row([btn_guardar, btn_cancelar], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        modal.content = ft.Container(
            content=modal_content,
            padding=20,
            width=450,
            height=500
        )
        
        modal.open = True
        content_area.page.update()
    
    def confirmar_eliminar(id_proveedor, nombre_proveedor):
        
        def eliminar(e):
            resultado = eliminar_proveedor(id_proveedor)
            if resultado["success"]:
                modal_confirm.open = False
                content_area.page.update()
                cargar_proveedores(busqueda_actual)
                mostrar_mensaje("Proveedor eliminado correctamente")
            else:
                mostrar_mensaje(f"Error: {resultado['error']}")
        
        def cancelar_eliminar(e):
            cerrar_modal()
        
        modal_confirm.content = ft.Container(
            content=ft.Column([
                ft.Text("⚠️", size=50),
                ft.Text("¿Eliminar Proveedor?", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"Está a punto de eliminar a:", size=14),
                ft.Text(f"{nombre_proveedor}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("ID: " + str(id_proveedor), size=12, color=ft.Colors.GREY),
                ft.Text("Esta acción no se puede deshacer.", size=12, color=ft.Colors.RED, italic=True),
                ft.Divider(height=20),
                ft.Row([
                    ft.ElevatedButton("Eliminar", on_click=eliminar, bgcolor=ft.Colors.RED, color=ft.Colors.WHITE),
                    ft.ElevatedButton("Cancelar", on_click=cancelar_eliminar)
                ], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            width=400
        )
        
        modal_confirm.open = True
        content_area.page.update()
    
    def cerrar_modal():
        modal.open = False
        modal_confirm.open = False
        content_area.page.update()
    
    def mostrar_mensaje(texto):
        snack = ft.SnackBar(content=ft.Text(texto))
        content_area.page.overlay.append(snack)
        snack.open = True
        content_area.page.update()
    
    # ===== CONTROLES UI =====
    txt_busqueda = ft.TextField(
        label="Buscar proveedor",
        hint_text="Nombre, RIF, teléfono o email",
        width=400,
        on_submit=buscar_proveedores
    )
    
    btn_buscar = ft.ElevatedButton("🔍 Buscar", on_click=buscar_proveedores)
    btn_limpiar = ft.ElevatedButton("🗑️ Limpiar", on_click=limpiar_busqueda)
    btn_nuevo = ft.ElevatedButton("➕ Nuevo Proveedor", on_click=abrir_modal_nuevo, bgcolor=ft.Colors.BLUE, color=ft.Colors.WHITE)
    
    lbl_resultados = ft.Text("Mostrando 0 proveedores", size=14, color=ft.Colors.GREY)
    
    tabla_proveedores = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Empresa")),
            ft.DataColumn(ft.Text("RIF/NIT")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Email")),
            ft.DataColumn(ft.Text("Acciones")),
        ],
        rows=[],
        width=1000,
        horizontal_margin=10
    )
    
    modal = ft.AlertDialog(modal=True, content=ft.Container())
    modal_confirm = ft.AlertDialog(modal=True, content=ft.Container())
    
    # ===== CONTENIDO PRINCIPAL =====
    contenido_principal = ft.Column([
        ft.Text("GESTIÓN DE PROVEEDORES", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Buscar Proveedores", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([txt_busqueda, btn_buscar, btn_limpiar, btn_nuevo], 
                       alignment=ft.MainAxisAlignment.CENTER, 
                       wrap=True),
                lbl_resultados,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            width=1100
        ),
        
        ft.Container(height=10),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Lista de Proveedores", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=tabla_proveedores,
                    padding=10
                )
            ]),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            width=1100
        ),
        
    ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
    
    contenedor_blanco = ft.Container(
        content=contenido_principal,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        padding=20,
        width=1200,
        shadow=ft.BoxShadow(
            spread_radius=1,
            blur_radius=10,
            color=ft.Colors.GREY_300
        )
    )
    
    contenido_final = ft.Container(
        content=ft.Row(
            controls=[contenedor_blanco],
            alignment=ft.MainAxisAlignment.CENTER,
            vertical_alignment=ft.CrossAxisAlignment.CENTER
        ),
        alignment=ft.Alignment(0, 0),
        expand=True,
        bgcolor=ft.Colors.GREY_100
    )
    
    content_area.content = contenido_final
    content_area.page.overlay.append(modal)
    content_area.page.overlay.append(modal_confirm)
    content_area.update()
    
    cargar_proveedores()