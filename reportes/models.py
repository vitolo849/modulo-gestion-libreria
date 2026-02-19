from datetime import date, timedelta, datetime
from libreria_cafe_edd_db import crear_sesion, Cliente, Factura, Venta, Libro, ConsumoLibro, ConsumoCafe, Membresia
from sqlalchemy import func, desc, and_
from libreria_cafe_edd_db.model.enum.tipo_venta import TipoVenta
from libreria_cafe_edd_db.model.enum.metodo_pago import MetodoPago
import random

def clientesMasCompras():
    session = crear_sesion()
    clientes_top = session.query(
        Cliente.id,
        Cliente.nombre,
        Cliente.cedula,
        func.count(Factura.id).label('total_compras')
    ).join(Factura, Cliente.id == Factura.id_cliente
    ).group_by(Cliente.id
    ).order_by(desc('total_compras')
    ).limit(10).all()
    session.close()
    
    data = [("ID", "Nombre", "Cédula", "Total Compras")]
    for c in clientes_top:
        data.append((str(c.id), c.nombre, str(c.cedula), str(c.total_compras)))
    return data

def clientesMasGastan():
    session = crear_sesion()
    clientes_top = session.query(
        Cliente.id,
        Cliente.nombre,
        Cliente.cedula,
        func.sum(Factura.monto_total).label('total_gastado')
    ).join(Factura, Cliente.id == Factura.id_cliente
    ).group_by(Cliente.id
    ).order_by(desc('total_gastado')
    ).limit(10).all()
    session.close()
    
    data = [("ID", "Nombre", "Cédula", "Total Gastado")]
    for c in clientes_top:
        data.append((str(c.id), c.nombre, str(c.cedula), f"${c.total_gastado:.2f}"))
    return data

def clientesMasProductos():
    session = crear_sesion()
    clientes_top = session.query(
        Cliente.id,
        Cliente.nombre,
        Cliente.cedula,
        func.sum(Venta.cantidad).label('total_productos')
    ).join(Factura, Cliente.id == Factura.id_cliente
    ).join(Venta, Factura.id == Venta.id_factura
    ).group_by(Cliente.id
    ).order_by(desc('total_productos')
    ).limit(10).all()
    session.close()
    
    data = [("ID", "Nombre", "Cédula", "Total Productos")]
    for c in clientes_top:
        data.append((str(c.id), c.nombre, str(c.cedula), str(c.total_productos)))
    return data

def rankingClientes():
    session = crear_sesion()
    ranking = session.query(
        Cliente.id,
        Cliente.nombre,
        Cliente.cedula,
        Cliente.telefono,
        func.count(Factura.id).label('num_compras'),
        func.sum(Factura.monto_total).label('total_gastado'),
        func.sum(Venta.cantidad).label('items_comprados')
    ).join(Factura, Cliente.id == Factura.id_cliente
    ).join(Venta, Factura.id == Venta.id_factura
    ).group_by(Cliente.id
    ).order_by(desc('total_gastado')
    ).all()
    session.close()
    
    data = [("ID", "Nombre", "Cédula", "Teléfono", "Compras", "Total Gastado", "Items")]
    for c in ranking:
        data.append((
            str(c.id), 
            c.nombre, 
            str(c.cedula), 
            str(c.telefono) if c.telefono else "",
            str(c.num_compras), 
            f"${c.total_gastado:.2f}", 
            str(c.items_comprados)
        ))
    return data

def clientesTopPorPeriodo(dias=30):
    session = crear_sesion()
    fecha_limite = date.today() - timedelta(days=dias)
    clientes_top = session.query(
        Cliente.id,
        Cliente.nombre,
        Cliente.cedula,
        func.sum(Factura.monto_total).label('total_gastado')
    ).join(Factura, Cliente.id == Factura.id_cliente
    ).filter(Factura.fecha >= fecha_limite
    ).group_by(Cliente.id
    ).order_by(desc('total_gastado')
    ).limit(10).all()
    session.close()
    
    data = [("ID", "Nombre", "Cédula", f"Total Últimos {dias} Días")]
    for c in clientes_top:
        data.append((str(c.id), c.nombre, str(c.cedula), f"${c.total_gastado:.2f}"))
    return data

def crear_venta(id_cliente, items, metodo_pago, fecha=None):
    session = crear_sesion()
    try:
        if fecha is None:
            fecha = date.today()
        
        subtotal = sum(item["cantidad"] * item["precio_unitario"] for item in items)
        iva = subtotal * 0.16
        igtf = subtotal * 0.03 if metodo_pago in [MetodoPago.DIVISA, MetodoPago.TRANSFERENCIA_EXTRANJERA] else 0
        total = subtotal + iva + igtf
        
        factura = Factura(
            fecha=fecha,
            metodo_pago=metodo_pago,
            subtotal=subtotal,
            monto_iva=iva,
            monto_igtf=igtf,
            monto_total=total,
            id_cliente=id_cliente
        )
        session.add(factura)
        session.flush()
        
        for item in items:
            venta = Venta(
                cantidad=item["cantidad"],
                precio=item["precio_unitario"],
                nombre_mostrado=item["nombre"],
                tipo=item["tipo"],
                id_producto=item["id_producto"],
                id_factura=factura.id
            )
            session.add(venta)
            
            if item["tipo"] == TipoVenta.LIBRO:
                libro = session.query(Libro).get(item["id_producto"])
                if libro:
                    libro.stock_actual -= item["cantidad"]
                    consumo = ConsumoLibro(
                        id_cliente=id_cliente,
                        nombre_libro=item["nombre"],
                        precio=item["precio_unitario"]
                    )
                    session.add(consumo)
            
            elif item["tipo"] == TipoVenta.CAFE:
                consumo = ConsumoCafe(
                    id_cliente=id_cliente,
                    nombre_cafe=item["nombre"],
                    tamano=0,
                    precio=item["precio_unitario"]
                )
                session.add(consumo)
        
        cliente = session.query(Cliente).get(id_cliente)
        if cliente:
            cliente.frecuencia += 1
        
        session.commit()
        return {"success": True, "factura_id": factura.id, "total": total}
    except Exception as e:
        session.rollback()
        return {"success": False, "error": str(e)}
    finally:
        session.close()

def obtener_ventas_por_periodo(fecha_inicio, fecha_fin):
    session = crear_sesion()
    ventas = session.query(
        Factura.id,
        Factura.fecha,
        Factura.metodo_pago,
        Factura.monto_total,
        Cliente.nombre.label('cliente_nombre'),
        Cliente.cedula
    ).join(Cliente, Factura.id_cliente == Cliente.id
    ).filter(
        and_(Factura.fecha >= fecha_inicio, Factura.fecha <= fecha_fin)
    ).order_by(Factura.fecha.desc()).all()
    session.close()
    
    data = [("ID", "Fecha", "Cliente", "Cédula", "Método Pago", "Total")]
    for v in ventas:
        data.append((
            str(v.id),
            v.fecha.strftime("%d/%m/%Y"),
            v.cliente_nombre,
            str(v.cedula),
            v.metodo_pago.name,
            f"${v.monto_total:.2f}"
        ))
    return data

def obtener_detalle_venta(id_factura):
    session = crear_sesion()
    factura = session.query(Factura).get(id_factura)
    if not factura:
        session.close()
        return None
    
    ventas = session.query(Venta).filter(Venta.id_factura == id_factura).all()
    cliente = session.query(Cliente).get(factura.id_cliente)
    session.close()
    
    return {
        "factura": {
            "id": factura.id,
            "fecha": factura.fecha,
            "metodo_pago": factura.metodo_pago,
            "subtotal": factura.subtotal,
            "iva": factura.monto_iva,
            "igtf": factura.monto_igtf,
            "total": factura.monto_total
        },
        "cliente": {
            "id": cliente.id,
            "nombre": cliente.nombre,
            "cedula": cliente.cedula
        },
        "ventas": [
            {
                "nombre": v.nombre_mostrado,
                "tipo": v.tipo,
                "cantidad": v.cantidad,
                "precio_unitario": v.precio,
                "subtotal": v.cantidad * v.precio
            }
            for v in ventas
        ]
    }

def ventas_por_dia(fecha=None):
    if fecha is None:
        fecha = date.today()
    
    session = crear_sesion()
    ventas = session.query(
        func.count(Factura.id).label('num_ventas'),
        func.sum(Factura.monto_total).label('total_dia'),
        func.avg(Factura.monto_total).label('promedio_venta')
    ).filter(Factura.fecha == fecha).first()
    session.close()
    
    return {
        "fecha": fecha.strftime("%d/%m/%Y"),
        "num_ventas": ventas.num_ventas or 0,
        "total_dia": float(ventas.total_dia or 0),
        "promedio_venta": float(ventas.promedio_venta or 0)
    }

def ingresos_por_metodo_pago(fecha_inicio, fecha_fin):
    session = crear_sesion()
    resultados = session.query(
        Factura.metodo_pago,
        func.count(Factura.id).label('num_transacciones'),
        func.sum(Factura.monto_total).label('total')
    ).filter(
        and_(Factura.fecha >= fecha_inicio, Factura.fecha <= fecha_fin)
    ).group_by(Factura.metodo_pago).all()
    session.close()
    
    data = [("Método de Pago", "# Transacciones", "Total")]
    for r in resultados:
        data.append((
            r.metodo_pago.name,
            str(r.num_transacciones),
            f"${r.total:.2f}"
        ))
    return data

def verificar_datos_ventas():
    session = crear_sesion()
    try:
        total_ventas = session.query(Venta).count()
        total_facturas = session.query(Factura).count()
        print(f"Total de ventas: {total_ventas}")
        print(f"Total de facturas: {total_facturas}")
    finally:
        session.close()

def productos_mas_vendidos(limite=10, tipo=None):
    session = crear_sesion()
    try:
        query = session.query(
            Venta.nombre_mostrado,
            Venta.tipo,
            func.sum(Venta.cantidad).label('total_vendido'),
            func.sum(Venta.cantidad * Venta.precio).label('ingresos_totales')
        ).group_by(Venta.nombre_mostrado, Venta.tipo)
        
        if tipo:
            query = query.filter(Venta.tipo == tipo)
        
        resultados = query.order_by(desc('total_vendido')).limit(limite).all()
        data = [("Producto", "Tipo", "Cantidad Vendida", "Ingresos")]
        for r in resultados:
            data.append((
                r.nombre_mostrado,
                str(r.tipo),
                str(r.total_vendido),
                f"${r.ingresos_totales:.2f}"
            ))
        return data
    finally:
        session.close()

def cargar_datos_prueba(force=False):
    session = crear_sesion()
    try:
        if not force and session.query(Cliente).count() > 0:
            return
        
        if force:
            session.query(Venta).delete()
            session.query(Factura).delete()
            session.query(ConsumoLibro).delete()
            session.query(ConsumoCafe).delete()
            session.query(Cliente).delete()
            session.query(Membresia).delete()
            session.commit()
        
        membresia_basica = Membresia(fecha_inicio=date(2025, 1, 1), fecha_vencimiento=date(2025, 12, 31), cantidad_libros=3, descuento_cafe=5, monto=50000, cantidad_cafe_gratis=1, tiempo_mesa=60)
        membresia_premium = Membresia(fecha_inicio=date(2025, 6, 1), fecha_vencimiento=date(2026, 5, 31), cantidad_libros=10, descuento_cafe=15, monto=120000, cantidad_cafe_gratis=3, tiempo_mesa=120)
        membresia_vip = Membresia(fecha_inicio=date(2025, 3, 15), fecha_vencimiento=date(2026, 3, 14), cantidad_libros=5, descuento_cafe=10, monto=85000, cantidad_cafe_gratis=2, tiempo_mesa=90)
        
        session.add_all([membresia_basica, membresia_premium, membresia_vip])
        session.flush()
        
        datos_clientes = [
            {"nombre": "Juan Pérez", "cedula": 12345678, "telefono": "0412-1234567", "membresia": membresia_basica},
            {"nombre": "María González", "cedula": 23456789, "telefono": "0414-2345678", "membresia": membresia_premium},
            {"nombre": "Carlos Rodríguez", "cedula": 34567890, "telefono": "0426-3456789", "membresia": None}
        ]
        
        clientes = []
        for d in datos_clientes:
            cliente = Cliente(id_membresia=d["membresia"].id if d["membresia"] else None, nombre=d["nombre"], cedula=d["cedula"], fecha_ingreso=date.today(), telefono=d["telefono"])
            session.add(cliente)
            clientes.append(cliente)
        session.flush()

        # Factura de ejemplo hoy
        factura = Factura(fecha=date.today(), metodo_pago=MetodoPago.EFECTIVO, subtotal=39500, monto_iva=6320, monto_igtf=0, monto_total=45820, id_cliente=clientes[0].id)
        session.add(factura)
        session.flush()

        venta1 = Venta(cantidad=1, precio=35000, nombre_mostrado="Cien años de soledad", tipo="LIBRO", id_producto=1, id_factura=factura.id)
        venta2 = Venta(cantidad=1, precio=4500, nombre_mostrado="Espresso", tipo="CAFE", id_producto=2, id_factura=factura.id)
        session.add_all([venta1, venta2])
        
        session.commit()
    except Exception as e:
        session.rollback()
        raise e
    finally:
        session.close()