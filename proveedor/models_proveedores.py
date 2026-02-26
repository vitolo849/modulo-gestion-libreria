# models_proveedores.py
from datetime import date
from libreria_cafe_edd_db import crear_sesion
from libreria_cafe_edd_db import Proveedor, OrdenReposicion
from sqlalchemy import func, or_

def obtener_proveedores(busqueda=""):
    session = crear_sesion()
    try:
        query = session.query(
            Proveedor.id,
            Proveedor.nombre_empresa,
            Proveedor.rif_nit,
            Proveedor.telefono,
            Proveedor.email
        )
        
        if busqueda:
            query = query.filter(
                or_(
                    Proveedor.nombre_empresa.ilike(f"%{busqueda}%"),
                    Proveedor.rif_nit.ilike(f"%{busqueda}%"),
                    Proveedor.telefono.ilike(f"%{busqueda}%"),
                    Proveedor.email.ilike(f"%{busqueda}%")
                )
            )
        
        proveedores = query.order_by(Proveedor.nombre_empresa).all()
        
        return [{
            "id": p.id,
            "nombre_empresa": p.nombre_empresa,
            "rif_nit": p.rif_nit,
            "telefono": p.telefono or "N/A",
            "email": p.email or "N/A"
        } for p in proveedores]
    finally:
        session.close()

def obtener_proveedor_por_id(id_proveedor):
    """Obtiene un proveedor específico por su ID"""
    session = crear_sesion()
    try:
        proveedor = session.query(Proveedor).get(id_proveedor)
        if not proveedor:
            return None
        
        return {
            "id": proveedor.id,
            "nombre_empresa": proveedor.nombre_empresa,
            "rif_nit": proveedor.rif_nit,
            "telefono": proveedor.telefono or "",
            "email": proveedor.email or ""
        }
    finally:
        session.close()

def crear_proveedor(datos):
    """Crea un nuevo proveedor"""
    session = crear_sesion()
    try:
        # Verificar si ya existe un proveedor con el mismo RIF
        existe = session.query(Proveedor).filter(Proveedor.rif_nit == datos["rif_nit"]).first()
        if existe:
            return {"success": False, "error": "Ya existe un proveedor con este RIF/NIT"}
        
        proveedor = Proveedor(
            nombre_empresa=datos["nombre_empresa"],
            rif_nit=datos["rif_nit"],
            telefono=datos.get("telefono") or None,
            email=datos.get("email") or None
        )
        
        session.add(proveedor)
        session.commit()
        
        return {
            "success": True, 
            "message": "Proveedor creado correctamente",
            "id": proveedor.id
        }
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()

def actualizar_proveedor(id_proveedor, datos):
    """Actualiza los datos de un proveedor"""
    session = crear_sesion()
    try:
        proveedor = session.query(Proveedor).get(id_proveedor)
        if not proveedor:
            return {"success": False, "error": "Proveedor no encontrado"}
        
        # Verificar si ya existe otro proveedor con el mismo RIF
        if "rif_nit" in datos:
            existe = session.query(Proveedor).filter(
                Proveedor.rif_nit == datos["rif_nit"],
                Proveedor.id != id_proveedor
            ).first()
            if existe:
                return {"success": False, "error": "Ya existe otro proveedor con este RIF/NIT"}
        
        # Actualizar campos
        campos_actualizables = ["nombre_empresa", "rif_nit", "telefono", "email"]
        for campo in campos_actualizables:
            if campo in datos:
                setattr(proveedor, campo, datos[campo])
        
        session.commit()
        return {"success": True, "message": "Proveedor actualizado correctamente"}
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()

def eliminar_proveedor(id_proveedor):
    """Elimina un proveedor si no tiene órdenes asociadas"""
    session = crear_sesion()
    try:
        proveedor = session.query(Proveedor).get(id_proveedor)
        if not proveedor:
            return {"success": False, "error": "Proveedor no encontrado"}
        
        
        ordenes = session.query(OrdenReposicion).filter(OrdenReposicion.id_proveedor == id_proveedor).first()
        if ordenes:
            return {"success": False, "error": "No se puede eliminar el proveedor porque tiene órdenes de reposición asociadas"}
        
        session.delete(proveedor)
        session.commit()
        return {"success": True, "message": "Proveedor eliminado correctamente"}
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()

def verificar_rif_unico(rif_nit, id_proveedor=None):
    session = crear_sesion()
    try:
        query = session.query(Proveedor).filter(Proveedor.rif_nit == rif_nit)
        if id_proveedor:
            query = query.filter(Proveedor.id != id_proveedor)
        
        existe = query.first()
        return not existe
    finally:
        session.close()