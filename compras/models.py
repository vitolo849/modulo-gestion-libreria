
from datetime import date, timedelta, datetime
from libreria_cafe_edd_db import crear_sesion, Proveedor, Libro, OrdenReposicion, DetallesReposicion
from libreria_cafe_edd_db import Cafe
from libreria_cafe_edd_db import DetallesReposicionCafe
from sqlalchemy import func, desc, and_
import random

def obtener_proveedores():
    session = crear_sesion()
    try:
        proveedores = session.query(Proveedor).order_by(Proveedor.nombre_empresa).all()
        return [{"id": p.id, "nombre_empresa": p.nombre_empresa, "rif_nit": p.rif_nit} for p in proveedores]
    finally:
        session.close()

def obtener_productos_por_tipo(tipo):
    session = crear_sesion()
    try:
        if tipo == "LIBRO":
            productos = session.query(Libro).order_by(Libro.titulo).all()
            return [{
                "id": p.id, 
                "nombre": p.titulo, 
                "precio": p.precio, 
                "stock_actual": p.stock_actual, 
                "stock_minimo": p.stock_minimo,
                "tipo": "LIBRO",
                "proveedor_id": None
            } for p in productos]
        
        elif tipo == "CAFE":
            productos = session.query(Cafe).order_by(Cafe.nombre).all()
            
            if not productos:
                cafes_default = [
                    {"nombre": "Espresso", "precio": 4500, "stock": 50, "minimo": 20, "tamano": 30},
                    {"nombre": "Cappuccino", "precio": 5500, "stock": 40, "minimo": 15, "tamano": 250},
                    {"nombre": "Latte", "precio": 6000, "stock": 35, "minimo": 15, "tamano": 300},
                    {"nombre": "Mocha", "precio": 6500, "stock": 30, "minimo": 10, "tamano": 300},
                    {"nombre": "Americano", "precio": 4000, "stock": 45, "minimo": 20, "tamano": 250},
                ]
                
                for cafe_data in cafes_default:
                    cafe = Cafe(
                        nombre=cafe_data["nombre"],
                        precio=cafe_data["precio"],
                        stock_actual=cafe_data["stock"],
                        stock_minimo=cafe_data["minimo"],
                        tamano=cafe_data["tamano"]
                    )
                    session.add(cafe)
                session.commit()
                
                productos = session.query(Cafe).order_by(Cafe.nombre).all()
            
            return [{
                "id": p.id,
                "nombre": p.nombre,
                "precio": p.precio,
                "stock_actual": p.stock_actual,
                "stock_minimo": p.stock_minimo,
                "tipo": "CAFE",
                "tamano": p.tamano,
                "proveedor_id": p.proveedor_id
            } for p in productos]
        
        return []
    finally:
        session.close()

def crear_orden_reposicion(datos_orden):
    
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
            if item["tipo"] == "LIBRO":
                detalle = DetallesReposicion(
                    id_orden=orden.id,
                    id_libro=item["id_producto"],
                    cantidad=item["cantidad"],
                    precio=item["precio_compra"]
                )
                session.add(detalle)
            
            elif item["tipo"] == "CAFE":
                detalle = DetallesReposicionCafe(
                    id_orden=orden.id,
                    id_cafe=item["id_producto"],
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
    session = crear_sesion()
    try:
        orden = session.query(OrdenReposicion).get(id_orden)
        if not orden:
            return None
        
        proveedor = session.query(Proveedor).get(orden.id_proveedor)
        
        detalles_libros = session.query(
            DetallesReposicion,
            Libro.titulo
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
                "nombre": d.titulo,
                "tipo": "LIBRO",
                "cantidad": d.DetallesReposicion.cantidad,
                "precio": d.DetallesReposicion.precio,
                "subtotal": d.DetallesReposicion.cantidad * d.DetallesReposicion.precio
            })
        
        for d in detalles_cafe:
            todos_detalles.append({
                "id_producto": d.DetallesReposicionCafe.id_cafe,
                "nombre": d.nombre,
                "tipo": "CAFE",
                "cantidad": d.DetallesReposicionCafe.cantidad,
                "precio": d.DetallesReposicionCafe.precio,
                "subtotal": d.DetallesReposicionCafe.cantidad * d.DetallesReposicionCafe.precio
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
                "id": proveedor.id,
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
    """Actualiza el estado de una orden y opcionalmente la fecha de entrega"""
    session = crear_sesion()
    try:
        orden = session.query(OrdenReposicion).get(id_orden)
        if not orden:
            return {"success": False, "error": "Orden no encontrada"}
        
        orden.estado = nuevo_estado
        
        if fecha_entrega and nuevo_estado == "Recibida":
            orden.fecha_entrega = fecha_entrega
            
            detalles_libros = session.query(DetallesReposicion).filter(DetallesReposicion.id_orden == id_orden).all()
            for detalle in detalles_libros:
                libro = session.query(Libro).get(detalle.id_libro)
                if libro:
                    libro.stock_actual += detalle.cantidad
            
            detalles_cafe = session.query(DetallesReposicionCafe).filter(DetallesReposicionCafe.id_orden == id_orden).all()
            for detalle in detalles_cafe:
                cafe = session.query(Cafe).get(detalle.id_cafe)
                if cafe:
                    cafe.stock_actual += detalle.cantidad
        
        session.commit()
        return {"success": True, "message": f"Orden actualizada a {nuevo_estado}"}
    
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()

def productos_bajo_stock():
    """Productos (libros y café) cuyo stock actual está por debajo del mínimo"""
    session = crear_sesion()
    try:
        libros = session.query(
            Libro.id,
            Libro.isbn,
            Libro.titulo,
            Libro.stock_actual,
            Libro.stock_minimo,
            (Libro.stock_minimo - Libro.stock_actual).label('faltante')
        ).filter(Libro.stock_actual < Libro.stock_minimo
        ).order_by(desc('faltante')).all()
        
        cafes = session.query(
            Cafe.id,
            Cafe.nombre,
            Cafe.stock_actual,
            Cafe.stock_minimo,
            (Cafe.stock_minimo - Cafe.stock_actual).label('faltante')
        ).filter(Cafe.stock_actual < Cafe.stock_minimo
        ).order_by(desc('faltante')).all()
        
        resultados = []
        
        for l in libros:
            resultados.append({
                "id": l.id,
                "codigo": l.isbn,
                "nombre": l.titulo,
                "stock_actual": l.stock_actual,
                "stock_minimo": l.stock_minimo,
                "faltante": l.faltante,
                "tipo": "LIBRO"
            })
        
        for c in cafes:
            resultados.append({
                "id": c.id,
                "codigo": f"CAF-{c.id}",
                "nombre": c.nombre,
                "stock_actual": c.stock_actual,
                "stock_minimo": c.stock_minimo,
                "faltante": c.faltante,
                "tipo": "CAFE"
            })
        
        return resultados
    finally:
        session.close()

def sugerir_cantidad_reposicion(id_producto, tipo="LIBRO"):
    session = crear_sesion()
    try:
        fecha_limite = date.today() - timedelta(days=30)
        
        if tipo == "LIBRO":
            libro = session.query(Libro).get(id_producto)
            if not libro:
                return 0
            
            from libreria_cafe_edd_db import Venta, Factura
            ventas = session.query(
                func.sum(Venta.cantidad).label('total')
            ).join(Factura, Venta.id_factura == Factura.id
            ).filter(
                Venta.id_producto == id_producto,
                Venta.tipo == "LIBRO",
                Factura.fecha >= fecha_limite
            ).first()
            
            ventas_mensuales = ventas.total or 0
            sugerencia = max(ventas_mensuales // 2, libro.stock_minimo * 2)
            return sugerencia
        
        elif tipo == "CAFE":
            cafe = session.query(Cafe).get(id_producto)
            if not cafe:
                return 0
            
            from libreria_cafe_edd_db import ConsumoCafe
            consumos = session.query(
                func.count(ConsumoCafe.id).label('total')
            ).filter(
                ConsumoCafe.nombre_cafe == cafe.nombre,
                ConsumoCafe.fecha >= fecha_limite
            ).first()
            
            consumos_mensuales = consumos.total or 0
            sugerencia = max(consumos_mensuales // 2, cafe.stock_minimo * 2)
            return sugerencia
        
        return 0
    finally:
        session.close()