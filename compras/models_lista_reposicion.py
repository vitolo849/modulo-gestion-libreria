# models_lista_reposicion.py
from datetime import date
from libreria_cafe_edd_db import crear_sesion
from libreria_cafe_edd_db import OrdenReposicion
from libreria_cafe_edd_db import DetallesReposicion
from libreria_cafe_edd_db import Proveedor
from libreria_cafe_edd_db import Libro
from sqlalchemy import func, desc, and_

def obtener_ordenes_pendientes():
    """Obtiene todas las órdenes pendientes y enviadas"""
    session = crear_sesion()
    try:
        ordenes = session.query(
            OrdenReposicion.id,
            OrdenReposicion.fecha_solicitud,
            OrdenReposicion.estado,
            OrdenReposicion.total_orden,
            Proveedor.nombre_empresa
        ).join(Proveedor, OrdenReposicion.id_proveedor == Proveedor.id
        ).filter(OrdenReposicion.estado.in_(["Pendiente", "Enviada"])
        ).order_by(OrdenReposicion.fecha_solicitud.desc()).all()
        
        return [{
            "id": o.id,
            "fecha": o.fecha_solicitud.strftime("%d/%m/%Y"),
            "proveedor": o.nombre_empresa,
            "estado": o.estado,
            "total": f"${o.total_orden:.2f}"
        } for o in ordenes]
    finally:
        session.close()

def obtener_ordenes_completadas(limite=10):
    """Obtiene las órdenes completadas (Recibidas)"""
    session = crear_sesion()
    try:
        ordenes = session.query(
            OrdenReposicion.id,
            OrdenReposicion.fecha_solicitud,
            OrdenReposicion.fecha_entrega,
            OrdenReposicion.total_orden,
            Proveedor.nombre_empresa
        ).join(Proveedor, OrdenReposicion.id_proveedor == Proveedor.id
        ).filter(OrdenReposicion.estado == "Recibida"
        ).order_by(OrdenReposicion.fecha_entrega.desc()).limit(limite).all()
        
        return [{
            "id": o.id,
            "fecha_solicitud": o.fecha_solicitud.strftime("%d/%m/%Y"),
            "fecha_entrega": o.fecha_entrega.strftime("%d/%m/%Y") if o.fecha_entrega else "N/A",
            "proveedor": o.nombre_empresa,
            "total": f"${o.total_orden:.2f}"
        } for o in ordenes]
    finally:
        session.close()

def obtener_detalle_orden_completo(id_orden):
    """Obtiene el detalle completo de una orden"""
    session = crear_sesion()
    try:
        orden = session.query(OrdenReposicion).get(id_orden)
        if not orden:
            return None
        
        proveedor = session.query(Proveedor).get(orden.id_proveedor)
        
        detalles = session.query(
            DetallesReposicion,
            Libro.titulo,
            Libro.isbn
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
                "nombre": proveedor.nombre_empresa,
                "rif": proveedor.rif_nit,
                "telefono": proveedor.telefono,
                "email": proveedor.email
            },
            "detalles": [{
                "id_libro": d.DetallesReposicion.id_libro,
                "isbn": d.isbn,
                "titulo": d.titulo,
                "cantidad": d.DetallesReposicion.cantidad,
                "precio": d.DetallesReposicion.precio,
                "subtotal": d.DetallesReposicion.cantidad * d.DetallesReposicion.precio
            } for d in detalles]
        }
    finally:
        session.close()

def actualizar_estado_orden(id_orden, nuevo_estado, fecha_entrega=None):
    """
    Actualiza el estado de una orden
    Si el estado es "Recibida", actualiza el stock de los libros
    """
    session = crear_sesion()
    try:
        orden = session.query(OrdenReposicion).get(id_orden)
        if not orden:
            return {"success": False, "error": "Orden no encontrada"}
        
        # Si la orden ya estaba recibida, no permitir cambios
        if orden.estado == "Recibida" and nuevo_estado != "Recibida":
            return {"success": False, "error": "No se puede cambiar el estado de una orden ya recibida"}
        
        estado_anterior = orden.estado
        orden.estado = nuevo_estado
        
        if nuevo_estado == "Recibida":
            # Usar fecha actual si no se proporciona
            orden.fecha_entrega = fecha_entrega or date.today()
            
            # Actualizar stock de libros
            detalles = session.query(DetallesReposicion).filter(DetallesReposicion.id_orden == id_orden).all()
            for detalle in detalles:
                libro = session.query(Libro).get(detalle.id_libro)
                if libro:
                    libro.stock_actual += detalle.cantidad
                    print(f"Stock actualizado: {libro.titulo} +{detalle.cantidad} = {libro.stock_actual}")
        
        session.commit()
        return {
            "success": True,
            "message": f"Orden #{id_orden} actualizada a {nuevo_estado}",
            "estado_anterior": estado_anterior,
            "nuevo_estado": nuevo_estado
        }
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()

def obtener_historial_ordenes(limite=20):
    """Obtiene historial completo de órdenes"""
    session = crear_sesion()
    try:
        ordenes = session.query(
            OrdenReposicion.id,
            OrdenReposicion.fecha_solicitud,
            OrdenReposicion.fecha_entrega,
            OrdenReposicion.estado,
            OrdenReposicion.total_orden,
            Proveedor.nombre_empresa
        ).join(Proveedor, OrdenReposicion.id_proveedor == Proveedor.id
        ).order_by(OrdenReposicion.fecha_solicitud.desc()).limit(limite).all()
        
        return [{
            "id": o.id,
            "fecha_solicitud": o.fecha_solicitud.strftime("%d/%m/%Y"),
            "fecha_entrega": o.fecha_entrega.strftime("%d/%m/%Y") if o.fecha_entrega else "-",
            "proveedor": o.nombre_empresa,
            "estado": o.estado,
            "total": f"${o.total_orden:.2f}"
        } for o in ordenes]
    finally:
        session.close()