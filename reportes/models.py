from datetime import date, timedelta
from libreria_cafe_edd_db import crear_sesion, Cliente, Factura, Venta
from sqlalchemy import func, desc

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