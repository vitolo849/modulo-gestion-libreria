# models_clientes.py
from datetime import date
from libreria_cafe_edd_db import crear_sesion
from libreria_cafe_edd_db import Cliente
from libreria_cafe_edd_db import Membresia,Factura,RecomendacionLibro,Venta,ConsumoLibro,ConsumoCafe
from sqlalchemy import func, or_

def obtener_clientes(busqueda=""):
    """Obtiene lista de clientes con opción de búsqueda"""
    session = crear_sesion()
    try:
        query = session.query(
            Cliente.id,
            Cliente.nombre,
            Cliente.cedula,
            Cliente.telefono,
            Cliente.fecha_ingreso,
            Cliente.frecuencia,
            Membresia.id.label('membresia_id'),
            Membresia.cantidad_libros,
            Membresia.descuento_cafe
        ).outerjoin(Membresia, Cliente.id_membresia == Membresia.id)
        
        if busqueda:
            query = query.filter(
                or_(
                    Cliente.nombre.ilike(f"%{busqueda}%"),
                    Cliente.cedula.ilike(f"%{busqueda}%"),
                    Cliente.telefono.ilike(f"%{busqueda}%")
                )
            )
        
        clientes = query.order_by(Cliente.nombre).all()
        
        return [{
            "id": c.id,
            "nombre": c.nombre,
            "cedula": c.cedula,
            "telefono": c.telefono or "N/A",
            "fecha_ingreso": c.fecha_ingreso.strftime("%d/%m/%Y"),
            "frecuencia": c.frecuencia,
            "membresia": "Sí" if c.membresia_id else "No",
            "beneficios": f"{c.cantidad_libros or 0} libros, {c.descuento_cafe or 0}% café" if c.membresia_id else "Sin membresía"
        } for c in clientes]
    finally:
        session.close()

def obtener_cliente_por_id(id_cliente):
    """Obtiene un cliente específico por su ID"""
    session = crear_sesion()
    try:
        cliente = session.query(Cliente).get(id_cliente)
        if not cliente:
            return None
        
        membresia = None
        if cliente.id_membresia:
            membresia = session.query(Membresia).get(cliente.id_membresia)
        
        return {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "cedula": cliente.cedula,
            "telefono": cliente.telefono or "",
            "fecha_ingreso": cliente.fecha_ingreso,
            "fecha_cumple": cliente.fecha_cumple,
            "frecuencia": cliente.frecuencia,
            "razon_social": cliente.razon_social or "",
            "direccion_fiscal": cliente.direccion_fiscal or "",
            "id_membresia": cliente.id_membresia,
            "membresia_nombre": membresia.id if membresia else None
        }
    finally:
        session.close()

def actualizar_cliente(id_cliente, datos):
    """Actualiza los datos de un cliente"""
    session = crear_sesion()
    try:
        cliente = session.query(Cliente).get(id_cliente)
        if not cliente:
            return {"success": False, "error": "Cliente no encontrado"}
        
        # Actualizar campos permitidos
        campos_actualizables = [
            "nombre", "cedula", "telefono", "fecha_cumple", 
            "razon_social", "direccion_fiscal", "id_membresia"
        ]
        
        for campo in campos_actualizables:
            if campo in datos:
                setattr(cliente, campo, datos[campo])
        
        session.commit()
        return {"success": True, "message": "Cliente actualizado correctamente"}
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()

def eliminar_cliente(id_cliente):
    """Elimina un cliente y todos sus registros asociados"""
    session = crear_sesion()
    try:
        cliente = session.query(Cliente).get(id_cliente)
        if not cliente:
            return {"success": False, "error": "Cliente no encontrado"}

        session.query(RecomendacionLibro).filter(RecomendacionLibro.id_cliente == id_cliente).delete()

        facturas = session.query(Factura).filter(Factura.id_cliente == id_cliente).all()
        facturas_ids = [f.id for f in facturas]

        if facturas_ids:
            session.query(Venta).filter(Venta.id_factura.in_(facturas_ids)).delete(synchronize_session=False)

            for factura in facturas:
                session.delete(factura)

        session.query(ConsumoLibro).filter(ConsumoLibro.id_cliente == id_cliente).delete()

        session.query(ConsumoCafe).filter(ConsumoCafe.id_cliente == id_cliente).delete()

        session.delete(cliente)
        session.commit()
        return {"success": True, "message": "Cliente y todos sus registros asociados eliminados correctamente"}

    except Exception as e:
        session.rollback()
        return {"success": False, "error": f"Error al eliminar: {str(e)}"}
    finally:
        session.close()

def obtener_membresias():
    """Obtiene lista de membresías para el combo box"""
    session = crear_sesion()
    try:
        membresias = session.query(Membresia).all()
        return [{"id": m.id, "nombre": f"Membresía {m.id}"} for m in membresias]
    finally:
        session.close()