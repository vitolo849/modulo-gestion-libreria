# clientes.py
from datetime import date
from clientes.models_clientes import (
    obtener_clientes,
    obtener_cliente_por_id,
    actualizar_cliente,
    eliminar_cliente,
    obtener_membresias
)

def view(content_area, ft):
    cliente_seleccionado = None
    busqueda_actual = ""
    
    def cargar_clientes(busqueda=""):
        print(f"Cargando clientes... Búsqueda: '{busqueda}'")
        clientes = obtener_clientes(busqueda)
        
        # Limpiar tabla
        tabla_clientes.rows.clear()
        
        if clientes:
            for cliente in clientes:
                btn_modificar = ft.Container(
                    content=ft.Text("✏️", size=20),
                    tooltip="Modificar",
                    on_click=lambda _, cid=cliente["id"]: abrir_modal_modificar(cid),
                    padding=5
                )
                
                btn_eliminar = ft.Container(
                    content=ft.Text("🗑️", size=20),
                    tooltip="Eliminar",
                    on_click=lambda _, cid=cliente["id"], nom=cliente["nombre"]: confirmar_eliminar(cid, nom),
                    padding=5
                )
                
                tabla_clientes.rows.append(
                    ft.DataRow(
                        cells=[
                            ft.DataCell(ft.Text(str(cliente["id"]))),
                            ft.DataCell(ft.Text(cliente["nombre"])),
                            ft.DataCell(ft.Text(str(cliente["cedula"]))),
                            ft.DataCell(ft.Text(cliente["telefono"])),
                            ft.DataCell(ft.Text(cliente["fecha_ingreso"])),
                            ft.DataCell(ft.Text(cliente["membresia"])),
                            ft.DataCell(ft.Row([btn_modificar, btn_eliminar]))
                        ]
                    )
                )
        else:
            tabla_clientes.rows.append(
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text("No hay clientes"))
                    ]
                )
            )
        
        tabla_clientes.update()
        lbl_resultados.value = f"Mostrando {len(clientes)} clientes"
        lbl_resultados.update()
    
    def buscar_clientes(e):
        nonlocal busqueda_actual
        busqueda_actual = txt_busqueda.value if txt_busqueda.value else ""
        cargar_clientes(busqueda_actual)
    
    def limpiar_busqueda(e):
        txt_busqueda.value = ""
        nonlocal busqueda_actual
        busqueda_actual = ""
        cargar_clientes()
        txt_busqueda.update()
    
    def abrir_modal_modificar(id_cliente):
        print(f"Abriendo modal para modificar cliente #{id_cliente}")
        datos = obtener_cliente_por_id(id_cliente)
        
        if not datos:
            mostrar_mensaje("No se pudo cargar el cliente")
            return
        
        nonlocal cliente_seleccionado
        cliente_seleccionado = datos
        
        membresias = obtener_membresias()
        opciones_membresia = [ft.dropdown.Option("0", "Sin membresía")]
        for m in membresias:
            opciones_membresia.append(ft.dropdown.Option(str(m["id"]), m["nombre"]))
        
        # Crear campos del formulario
        txt_nombre = ft.TextField(label="Nombre", value=datos["nombre"], width=300)
        txt_cedula = ft.TextField(label="Cédula", value=str(datos["cedula"]), width=300)
        txt_telefono = ft.TextField(label="Teléfono", value=datos["telefono"] or "", width=300)
        
        fecha_cumple_str = ""
        if datos["fecha_cumple"]:
            if isinstance(datos["fecha_cumple"], date):
                fecha_cumple_str = datos["fecha_cumple"].strftime("%Y-%m-%d")
            else:
                fecha_cumple_str = str(datos["fecha_cumple"])
        
        txt_fecha_cumple = ft.TextField(
            label="Fecha de Cumpleaños (YYYY-MM-DD)", 
            value=fecha_cumple_str,
            width=300,
            hint_text="Opcional"
        )
        
        txt_razon_social = ft.TextField(
            label="Razón Social", 
            value=datos["razon_social"] or "", 
            width=300,
            hint_text="Opcional"
        )
        
        txt_direccion = ft.TextField(
            label="Dirección Fiscal", 
            value=datos["direccion_fiscal"] or "", 
            width=300,
            hint_text="Opcional",
            multiline=True,
            min_lines=2,
            max_lines=3
        )
        
        dropdown_membresia = ft.Dropdown(
            label="Membresía",
            width=300,
            options=opciones_membresia,
            value=str(datos["id_membresia"]) if datos["id_membresia"] else "0"
        )
        
        def test_click(e):
            mostrar_mensaje("Botón funcionando")
        
        def guardar_cambios(e):
            mostrar_mensaje("Procesando guardado...")
            
            if not txt_nombre.value:
                mostrar_mensaje("El nombre es obligatorio")
                return
            
            if not txt_cedula.value:
                mostrar_mensaje("La cédula es obligatoria")
                return
            
            try:
                fecha_cumple = None
                if txt_fecha_cumple.value:
                    fecha_cumple = date.fromisoformat(txt_fecha_cumple.value)
                
                datos_actualizados = {
                    "nombre": txt_nombre.value,
                    "cedula": int(txt_cedula.value),
                    "telefono": txt_telefono.value or None,
                    "fecha_cumple": fecha_cumple,
                    "razon_social": txt_razon_social.value or None,
                    "direccion_fiscal": txt_direccion.value or None,
                    "id_membresia": int(dropdown_membresia.value) if dropdown_membresia.value != "0" else None
                }
                
                print(f"Datos a actualizar: {datos_actualizados}")
                
                resultado = actualizar_cliente(id_cliente, datos_actualizados)
                
                print(f"Resultado: {resultado}")
                
                if resultado["success"]:
                    modal.open = False
                    content_area.page.update()
                    cargar_clientes(busqueda_actual)
                    mostrar_mensaje("Cliente actualizado correctamente")
                else:
                    mostrar_mensaje(f"Error: {resultado['error']}")
            
            except ValueError as ex:
                print(f"Error de valor: {ex}")
                mostrar_mensaje(f"Error en los datos: {str(ex)}")
            except Exception as ex:
                mostrar_mensaje(f"Error: {str(ex)}")
        
        def cancelar_modal(e):
            cerrar_modal()
        
        # Botones separados para probar
        btn_guardar = ft.ElevatedButton(
            "Guardar", 
            on_click=guardar_cambios, 
            bgcolor=ft.Colors.GREEN, 
            color=ft.Colors.WHITE
        )
        
        btn_cancelar = ft.ElevatedButton(
            "Cancelar", 
            on_click=cancelar_modal
        )
        
        
        
        # Crear el contenido del modal
        modal_content = ft.Column([
            ft.Text(f"Modificar Cliente #{id_cliente}", size=20, weight=ft.FontWeight.BOLD),
            ft.Divider(height=10),
            txt_nombre,
            txt_cedula,
            txt_telefono,
            txt_fecha_cumple,
            txt_razon_social,
            txt_direccion,
            dropdown_membresia,
              # Botón de prueba
            ft.Row([btn_guardar, btn_cancelar], alignment=ft.MainAxisAlignment.CENTER, spacing=20)
        ], spacing=10, scroll=ft.ScrollMode.AUTO)
        
        modal.content = ft.Container(
            content=modal_content,
            padding=20,
            width=450,
            height=600
        )
        
        modal.open = True
        content_area.page.update()
    
    def confirmar_eliminar(id_cliente, nombre_cliente):
        
        
        def eliminar(e):
            
            resultado = eliminar_cliente(id_cliente)
            if resultado["success"]:
                modal_confirm.open = False
                content_area.page.update()
                cargar_clientes(busqueda_actual)
                mostrar_mensaje("Cliente eliminado correctamente")
            else:
                mostrar_mensaje(f"Error: {resultado['error']}")
        
        def cancelar_eliminar(e):
            
            cerrar_modal()
        
        modal_confirm.content = ft.Container(
            content=ft.Column([
                ft.Text("⚠️", size=50),
                ft.Text("¿Eliminar Cliente?", size=20, weight=ft.FontWeight.BOLD),
                ft.Text(f"Está a punto de eliminar a:", size=14),
                ft.Text(f"{nombre_cliente}", size=16, weight=ft.FontWeight.BOLD),
                ft.Text("ID: " + str(id_cliente), size=12, color=ft.Colors.GREY),
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
        print(f"MENSAJE: {texto}")
        snack = ft.SnackBar(content=ft.Text(texto))
        content_area.page.overlay.append(snack)
        snack.open = True
        content_area.page.update()
    
    # ===== CONTROLES UI =====
    txt_busqueda = ft.TextField(
        label="Buscar cliente",
        hint_text="Nombre, cédula o teléfono",
        width=400,
        on_submit=buscar_clientes
    )
    
    btn_buscar = ft.ElevatedButton("🔍 Buscar", on_click=buscar_clientes)
    btn_limpiar = ft.ElevatedButton("🗑️ Limpiar", on_click=limpiar_busqueda)
    
    lbl_resultados = ft.Text("Mostrando 0 clientes", size=14, color=ft.Colors.GREY)
    
    tabla_clientes = ft.DataTable(
        columns=[
            ft.DataColumn(ft.Text("ID")),
            ft.DataColumn(ft.Text("Nombre")),
            ft.DataColumn(ft.Text("Cédula")),
            ft.DataColumn(ft.Text("Teléfono")),
            ft.DataColumn(ft.Text("Ingreso")),
            ft.DataColumn(ft.Text("Membresía")),
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
        ft.Text("GESTIÓN DE CLIENTES", size=30, weight=ft.FontWeight.BOLD),
        ft.Divider(height=20),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Buscar Clientes", size=16, weight=ft.FontWeight.BOLD),
                ft.Row([txt_busqueda, btn_buscar, btn_limpiar], alignment=ft.MainAxisAlignment.CENTER),
                lbl_resultados,
            ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            width=1000
        ),
        
        ft.Container(height=10),
        
        ft.Container(
            content=ft.Column([
                ft.Text("Lista de Clientes", size=16, weight=ft.FontWeight.BOLD),
                ft.Container(
                    content=tabla_clientes,
                    padding=10
                )
            ]),
            padding=20,
            border=ft.border.all(1, ft.Colors.GREY_400),
            border_radius=5,
            width=1000
        ),
        
    ], spacing=10, horizontal_alignment=ft.CrossAxisAlignment.CENTER, scroll=ft.ScrollMode.AUTO)
    
    contenedor_blanco = ft.Container(
        content=contenido_principal,
        bgcolor=ft.Colors.WHITE,
        border_radius=10,
        padding=20,
        width=1100,
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
    
    cargar_clientes()