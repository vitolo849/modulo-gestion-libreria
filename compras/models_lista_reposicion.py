from datetime import date
from libreria_cafe_edd_db import crear_sesion
from libreria_cafe_edd_db import OrdenReposicion
from libreria_cafe_edd_db import DetallesReposicion
from libreria_cafe_edd_db import DetallesReposicionCafe 
from libreria_cafe_edd_db import Proveedor
from libreria_cafe_edd_db import Libro
from libreria_cafe_edd_db import Cafe 
from sqlalchemy import func, desc, and_

def obtener_ordenes_pendientes():
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
    session = crear_sesion()
    try:
        orden = session.query(OrdenReposicion).get(id_orden)
        if not orden:
            return None
        
        proveedor = session.query(Proveedor).get(orden.id_proveedor)
        
        detalles_libros = session.query(
            DetallesReposicion,
            Libro.titulo,
            Libro.isbn
        ).join(Libro, DetallesReposicion.id_libro == Libro.id
        ).filter(DetallesReposicion.id_orden == id_orden).all()
        
        detalles_cafe = session.query(
            DetallesReposicionCafe,
            Cafe.nombre
        ).join(Cafe, DetallesReposicionCafe.id_cafe == Cafe.id
        ).filter(DetallesReposicionCafe.id_orden == id_orden).all()
        
        todos_detalles = []
        
        for d in detalles_libros:
            todos_detalles.append({
                "id_producto": d.DetallesReposicion.id_libro,
                "isbn": d.isbn,
                "titulo": d.titulo,
                "cantidad": d.DetallesReposicion.cantidad,
                "precio": d.DetallesReposicion.precio,
                "subtotal": d.DetallesReposicion.cantidad * d.DetallesReposicion.precio,
                "tipo": "LIBRO"
            })
        
        for d in detalles_cafe:
            todos_detalles.append({
                "id_producto": d.DetallesReposicionCafe.id_cafe,
                "isbn": f"CAF-{d.DetallesReposicionCafe.id_cafe}",
                "titulo": d.nombre,
                "cantidad": d.DetallesReposicionCafe.cantidad,
                "precio": d.DetallesReposicionCafe.precio,
                "subtotal": d.DetallesReposicionCafe.cantidad * d.DetallesReposicionCafe.precio,
                "tipo": "CAFE"
            })
        
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
            "detalles": todos_detalles
        }
    finally:
        session.close()

def actualizar_estado_orden(id_orden, nuevo_estado, fecha_entrega=None):
    
    session = crear_sesion()
    try:
        orden = session.query(OrdenReposicion).get(id_orden)
        if not orden:
            return {"success": False, "error": "Orden no encontrada"}
        
        if orden.estado == "Recibida" and nuevo_estado != "Recibida":
            return {"success": False, "error": "No se puede cambiar el estado de una orden ya recibida"}
        
        estado_anterior = orden.estado
        orden.estado = nuevo_estado
        
        if nuevo_estado == "Recibida":
            orden.fecha_entrega = fecha_entrega or date.today()
            
            detalles_libros = session.query(DetallesReposicion).filter(DetallesReposicion.id_orden == id_orden).all()
            for detalle in detalles_libros:
                libro = session.query(Libro).get(detalle.id_libro)
                if libro:
                    libro.stock_actual += detalle.cantidad
                    print(f"Stock actualizado (libro): {libro.titulo} +{detalle.cantidad} = {libro.stock_actual}")
            
            detalles_cafe = session.query(DetallesReposicionCafe).filter(DetallesReposicionCafe.id_orden == id_orden).all()
            for detalle in detalles_cafe:
                cafe = session.query(Cafe).get(detalle.id_cafe)
                if cafe:
                    cafe.stock_actual += detalle.cantidad
                    print(f"Stock actualizado (café): {cafe.nombre} +{detalle.cantidad} = {cafe.stock_actual}")
        
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