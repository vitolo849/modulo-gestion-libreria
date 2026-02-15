import flet as ft
from datetime import date
from libreria_cafe_edd_db import crear_sesion, establecer_logs, Cliente

def view(area_contenido, ft):
    nombre = ft.TextField(label="Nombre del cliente", width=300)
    cedula = ft.TextField(label="Cédula (número)", width=300, keyboard_type=ft.KeyboardType.NUMBER)
    telefono = ft.TextField(label="Teléfono", width=300, keyboard_type=ft.KeyboardType.PHONE)
    guardar_btn = ft.ElevatedButton("Guardar", on_click=lambda e: guardar_cliente(e, nombre, cedula, telefono))

    area_contenido.content = ft.Column([
        ft.Text("Agregar / Editar Cliente", size=25),
        nombre,
        cedula,
        telefono,
        guardar_btn
    ], spacing=10)

def guardar_cliente(e, nombre_field, cedula_field, telefono_field):
    nombre_val = (nombre_field.value or "").strip()
    cedula_val = (cedula_field.value or "").strip()
    telefono_val = (telefono_field.value or "").strip() or None
# validacion por si no se ingresan datos o si la cedula no es un numero entero
    if not nombre_val or not cedula_val:
        dlg = ft.AlertDialog(
            title=ft.Text("Datos incompletos"),
            content=ft.Text("Nombre y cédula son obligatorios."),
            actions=[ft.TextButton("OK", on_click=lambda ev: ev.page.dialog.dismiss())],
        )
        e.page.dialog = dlg
        dlg.open = True
        e.page.update()
        return

    try: # convertir cedula a entero para validacion y para guardar en la base de datos si es un numero entero, si no mostrar mensaje de error
        cedula_int = int(cedula_val)
    except ValueError:
        dlg = ft.AlertDialog(
            title=ft.Text("Cédula inválida"),
            content=ft.Text("La cédula debe ser un número entero."),
            actions=[ft.TextButton("OK", on_click=lambda ev: ev.page.dialog.dismiss())],
        )
        e.page.dialog = dlg
        dlg.open = True
        e.page.update()
        return

    session = crear_sesion() # se crea una sesión para interactuar con la base de datos, se debe cerrar al finalizar la operación para liberar recursos
    try:
        existente = session.query(Cliente).filter_by(cedula=cedula_int).first()
        if existente:
            dlg = ft.AlertDialog(
                title=ft.Text("Ya existe"),
                content=ft.Text(f"Ya existe un cliente con cédula {cedula_int}."),
                actions=[ft.TextButton("OK", on_click=lambda ev: ev.page.dialog.dismiss())],
            )
            e.page.dialog = dlg
            dlg.open = True
            e.page.update()
            return

        nuevo = Cliente( # se crea un nuevo objeto Cliente con los datos ingresados, se asigna la fecha de ingreso como la fecha actual
            nombre=nombre_val,
            cedula=cedula_int,
            fecha_ingreso=date.today(),
            telefono=telefono_val
        )
        session.add(nuevo)
        session.commit()

        dlg = ft.AlertDialog( # se muestra un diálogo de confirmación al guardar el cliente correctamente, se limpian los campos del formulario para permitir ingresar un nuevo cliente
            title=ft.Text("Cliente guardado"),
            content=ft.Text(f"Cliente {nombre_val} guardado correctamente."),
            actions=[ft.TextButton("OK", on_click=lambda ev: ev.page.dialog.dismiss())],
        )
        e.page.dialog = dlg
        dlg.open = True
        # limpiar campos
        nombre_field.value = ""
        cedula_field.value = ""
        telefono_field.value = ""
        e.page.update()
    except Exception as ex: # en caso de error al guardar el cliente, se hace rollback de la sesión para deshacer cualquier cambio pendiente y se muestra un mensaje de error al usuario
        session.rollback()
        dlg = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(f"Ocurrió un error al guardar: {ex}"),
            actions=[ft.TextButton("OK", on_click=lambda ev: ev.page.dialog.dismiss())],
        )
        e.page.dialog = dlg 
        dlg.open = True
        e.page.update()
    finally:
        session.close()
