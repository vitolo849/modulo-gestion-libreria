from datetime import date, timedelta, datetime
from libreria_cafe_edd_db import crear_sesion, Proveedor, Libro, OrdenReposicion, DetallesReposicion
from sqlalchemy import func, desc, and_
import random
def obtener_proveedores():
    """Obtiene lista de proveedores para el combobox"""
    session = crear_sesion()
    try:
        proveedores = session.query(Proveedor).order_by(Proveedor.nombre_empresa).all()
        return [{"id": p.id, "nombre_empresa": p.nombre_empresa, "rif_nit": p.rif_nit} for p in proveedores]
    finally:
        session.close()
def obtener_productos_por_tipo(tipo):
    """Obtiene productos según el tipo (solo LIBRO para reposición)"""
    session = crear_sesion()
    try:
        if tipo == "LIBRO":
            productos = session.query(Libro).order_by(Libro.titulo).all()
            return [{"id": p.id, "nombre": p.titulo, "precio": p.precio, "stock_actual": p.stock_actual, "stock_minimo": p.stock_minimo} for p in productos]
        return []
    finally:
        session.close()
def crear_orden_reposicion(datos_orden):
    """
    Crea una nueva orden de reposición
    Args:
        datos_orden: Dict con:
            - id_proveedor: int
            - fecha_solicitud: date
            - items: Lista de dicts con id_producto, cantidad, precio_compra
            - total: float
    """
    session = crear_sesion()
    try:
        fecha_actual = date.today()
        orden = OrdenReposicion(
            id_proveedor=datos_orden["id_proveedor"],
            fecha_ingreso=fecha_actual,
            fecha_solicitud=datos_orden["fecha_solicitud"],
            fecha_entrega=None,
            estado="Pendiente",
            total_orden=datos_orden["total"]
        )
        session.add(orden)
        session.flush()
        for item in datos_orden["items"]:
            detalle = DetallesReposicion(
                id_orden=orden.id,
                id_libro=item["id_producto"],
                cantidad=item["cantidad"],
                precio=item["precio_compra"]
            )
            session.add(detalle)
        session.commit()
        return {"success": True, "orden_id": orden.id, "message": "Orden creada exitosamente"}
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()
def obtener_ordenes_recientes(limite=10):
    """Obtiene las órdenes de reposición más recientes"""
    session = crear_sesion()
    try:
        ordenes = session.query(
            OrdenReposicion.id,
            OrdenReposicion.fecha_solicitud,
            OrdenReposicion.estado,
            OrdenReposicion.total_orden,
            Proveedor.nombre_empresa
        ).join(Proveedor, OrdenReposicion.id_proveedor == Proveedor.id
        ).order_by(desc(OrdenReposicion.fecha_solicitud)
        ).limit(limite).all()
        return [{
            "id": o.id,
            "fecha": o.fecha_solicitud.strftime("%d/%m/%Y"),
            "proveedor": o.nombre_empresa,
            "estado": o.estado,
            "total": f"${o.total_orden:.2f}"
        } for o in ordenes]
    finally:
        session.close()
def obtener_detalle_orden(id_orden):
    """Obtiene el detalle de una orden específica"""
    session = crear_sesion()
    try:
        orden = session.query(OrdenReposicion).get(id_orden)
        if not orden:
            return None
        proveedor = session.query(Proveedor).get(orden.id_proveedor)
        detalles = session.query(
            DetallesReposicion,
            Libro.titulo
        ).join(Libro, DetallesReposicion.id_libro == Libro.id
        ).filter(DetallesReposicion.id_orden == id_orden).all()
        return {
            "orden": {
                "id": orden.id,
                "fecha_solicitud": orden.fecha_solicitud.strftime("%d/%m/%Y"),
                "fecha_ingreso": orden.fecha_ingreso.strftime("%d/%m/%Y"),
                "fecha_entrega": orden.fecha_entrega.strftime("%d/%m/%Y") if orden.fecha_entrega else "Pendiente",
                "estado": orden.estado,
                "total": orden.total_orden
            },
            "proveedor": {
                "id": proveedor.id,
                "nombre": proveedor.nombre_empresa,
                "rif": proveedor.rif_nit,
                "telefono": proveedor.telefono,
                "email": proveedor.email
            },
            "detalles": [{
                "id_libro": d.DetallesReposicion.id_libro,
                "titulo": d.titulo,
                "cantidad": d.DetallesReposicion.cantidad,
                "precio": d.DetallesReposicion.precio,
                "subtotal": d.DetallesReposicion.cantidad * d.DetallesReposicion.precio
            } for d in detalles]
        }
    finally:
        session.close()
def actualizar_estado_orden(id_orden, nuevo_estado, fecha_entrega=None):
    """Actualiza el estado de una orden y opcionalmente la fecha de entrega"""
    session = crear_sesion()
    try:
        orden = session.query(OrdenReposicion).get(id_orden)
        if not orden:
            return {"success": False, "error": "Orden no encontrada"}
        orden.estado = nuevo_estado
        if fecha_entrega and nuevo_estado == "Recibida":
            orden.fecha_entrega = fecha_entrega
            detalles = session.query(DetallesReposicion).filter(DetallesReposicion.id_orden == id_orden).all()
            for detalle in detalles:
                libro = session.query(Libro).get(detalle.id_libro)
                if libro:
                    libro.stock_actual += detalle.cantidad
        session.commit()
        return {"success": True, "message": f"Orden actualizada a {nuevo_estado}"}
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()
def libros_bajo_stock():
    """Libros cuyo stock actual está por debajo del mínimo"""
    session = crear_sesion()
    try:
        resultados = session.query(
            Libro.id,
            Libro.isbn,
            Libro.titulo,
            Libro.stock_actual,
            Libro.stock_minimo,
            (Libro.stock_minimo - Libro.stock_actual).label('faltante')
        ).filter(Libro.stock_actual < Libro.stock_minimo
        ).order_by(desc('faltante')).all()
        return [{
            "id": r.id,
            "isbn": r.isbn,
            "titulo": r.titulo,
            "stock_actual": r.stock_actual,
            "stock_minimo": r.stock_minimo,
            "faltante": r.faltante
        } for r in resultados]
    finally:
        session.close()
def sugerir_cantidad_reposicion(id_libro):
    """Sugiere una cantidad de reposición basada en el historial de ventas"""
    session = crear_sesion()
    try:
        libro = session.query(Libro).get(id_libro)
        if not libro:
            return 0
        fecha_limite = date.today() - timedelta(days=30)
        from libreria_cafe_edd_db import Venta
        from libreria_cafe_edd_db  import Factura
        ventas = session.query(
            func.sum(Venta.cantidad).label('total')
        ).join(Factura, Venta.id_factura == Factura.id
        ).filter(
            Venta.id_producto == id_libro,
            Venta.tipo == "LIBRO",
            Factura.fecha >= fecha_limite
        ).first()
        ventas_mensuales = ventas.total or 0
        sugerencia = max(ventas_mensuales // 2, libro.stock_minimo * 2)
        return sugerencia
    finally:
        session.close()