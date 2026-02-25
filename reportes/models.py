from datetime import date, timedelta, datetime
from libreria_cafe_edd_db import crear_sesion, Cliente, Factura, Venta, Libro, ConsumoLibro, ConsumoCafe, Membresia, Proveedor, OrdenReposicion, DetallesReposicion, Libro
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
            session.query(DetallesReposicion).delete()
            session.query(OrdenReposicion).delete()
            session.query(Proveedor).delete()
            session.query(Libro).delete()
            session.query(Cliente).delete()
            session.query(Membresia).delete()
            session.commit()
        
        # ===== MEMBRESÍAS =====
        membresia_basica = Membresia(
            fecha_inicio=date(2025, 1, 1), 
            fecha_vencimiento=date(2025, 12, 31), 
            cantidad_libros=3, 
            descuento_cafe=5, 
            monto=50000, 
            cantidad_cafe_gratis=1, 
            tiempo_mesa=60
        )
        membresia_premium = Membresia(
            fecha_inicio=date(2025, 6, 1), 
            fecha_vencimiento=date(2026, 5, 31), 
            cantidad_libros=10, 
            descuento_cafe=15, 
            monto=120000, 
            cantidad_cafe_gratis=3, 
            tiempo_mesa=120
        )
        membresia_vip = Membresia(
            fecha_inicio=date(2025, 3, 15), 
            fecha_vencimiento=date(2026, 3, 14), 
            cantidad_libros=5, 
            descuento_cafe=10, 
            monto=85000, 
            cantidad_cafe_gratis=2, 
            tiempo_mesa=90
        )
        
        session.add_all([membresia_basica, membresia_premium, membresia_vip])
        session.flush()
        
        # ===== CLIENTES =====
        datos_clientes = [
            {"nombre": "Juan Pérez", "cedula": 12345678, "telefono": "0412-1234567", "membresia": membresia_basica},
            {"nombre": "María González", "cedula": 23456789, "telefono": "0414-2345678", "membresia": membresia_premium},
            {"nombre": "Carlos Rodríguez", "cedula": 34567890, "telefono": "0426-3456789", "membresia": None},
            {"nombre": "Ana Martínez", "cedula": 45678901, "telefono": "0416-4567890", "membresia": membresia_vip},
            {"nombre": "Luis Sánchez", "cedula": 56789012, "telefono": "0424-5678901", "membresia": membresia_basica},
        ]
        
        clientes = []
        for d in datos_clientes:
            cliente = Cliente(
                id_membresia=d["membresia"].id if d["membresia"] else None, 
                nombre=d["nombre"], 
                cedula=d["cedula"], 
                fecha_ingreso=date.today() - timedelta(days=random.randint(30, 180)),
                telefono=d["telefono"]
            )
            session.add(cliente)
            clientes.append(cliente)
        session.flush()

        # ===== FACTURAS Y VENTAS (para reportes de ventas) =====
        productos = [
            ("Cien años de soledad", "LIBRO", 35000),
            ("Don Quijote", "LIBRO", 42000),
            ("El principito", "LIBRO", 28000),
            ("1984", "LIBRO", 32000),
            ("Espresso", "CAFE", 4500),
            ("Cappuccino", "CAFE", 5500),
        ]
        
        metodos_pago = [MetodoPago.EFECTIVO, MetodoPago.PUNTO, MetodoPago.TRANSFERENCIA, MetodoPago.DIVISAS]
        
        for i, cliente in enumerate(clientes):
            for j in range(random.randint(2, 5)):
                fecha_factura = date.today() - timedelta(days=random.randint(0, 60))
                metodo_pago = random.choice(metodos_pago)
                
                subtotal = 0
                num_productos = random.randint(1, 4)
                ventas_list = []
                
                for _ in range(num_productos):
                    producto = random.choice(productos)
                    cantidad = random.randint(1, 3)
                    subtotal += cantidad * producto[2]
                    ventas_list.append((producto[0], producto[1], producto[2], cantidad))
                
                iva = subtotal * 0.16
                igtf = subtotal * 0.03 if metodo_pago == MetodoPago.DIVISAS else 0
                total = subtotal + iva + igtf
                
                factura = Factura(
                    fecha=fecha_factura,
                    metodo_pago=metodo_pago,
                    subtotal=subtotal,
                    monto_iva=iva,
                    monto_igtf=igtf,
                    monto_total=total,
                    id_cliente=cliente.id
                )
                session.add(factura)
                session.flush()
                
                for nombre, tipo, precio, cantidad in ventas_list:
                    venta = Venta(
                        cantidad=cantidad,
                        precio=precio,
                        nombre_mostrado=nombre,
                        tipo=tipo,
                        id_producto=random.randint(1, 100),
                        id_factura=factura.id
                    )
                    session.add(venta)
        
        # ===== PROVEEDORES =====
        
        proveedores_data = [
            {"nombre_empresa": "Distribuidora Los Andes", "rif_nit": "J-12345678-9", "telefono": "0212-5551234", "email": "ventas@andes.com"},
            {"nombre_empresa": "Librería Universal", "rif_nit": "J-23456789-0", "telefono": "0212-5555678", "email": "pedidos@universal.com"},
            {"nombre_empresa": "Editorial Planeta", "rif_nit": "J-34567890-1", "telefono": "0212-5559012", "email": "ventas@planeta.com"},
            {"nombre_empresa": "Books & Co.", "rif_nit": "J-45678901-2", "telefono": "0212-5553456", "email": "info@booksco.com"},
            {"nombre_empresa": "Distribuidora del Sur", "rif_nit": "J-56789012-3", "telefono": "0212-5557890", "email": "ventas@south.com"},
        ]
        
        proveedores = []
        for p_data in proveedores_data:
            proveedor = Proveedor(**p_data)
            session.add(proveedor)
            proveedores.append(proveedor)
        session.flush()

        # ===== LIBROS =====
        
        libros_data = [
            {"isbn": "978-84-376-0494-7", "titulo": "Cien años de soledad", "stock_actual": 15, "stock_minimo": 8, "precio": 35000},
            {"isbn": "978-84-206-5132-3", "titulo": "Don Quijote de la Mancha", "stock_actual": 12, "stock_minimo": 5, "precio": 42000},
            {"isbn": "978-84-9759-229-5", "titulo": "El principito", "stock_actual": 20, "stock_minimo": 10, "precio": 28000},
            {"isbn": "978-84-339-0025-0", "titulo": "1984", "stock_actual": 8, "stock_minimo": 6, "precio": 32000},
            {"isbn": "978-84-376-0495-4", "titulo": "Crimen y castigo", "stock_actual": 6, "stock_minimo": 5, "precio": 38000},
            {"isbn": "978-84-376-0496-1", "titulo": "Rayuela", "stock_actual": 5, "stock_minimo": 4, "precio": 33000},
            {"isbn": "978-84-376-0497-8", "titulo": "El túnel", "stock_actual": 7, "stock_minimo": 3, "precio": 29000},
        ]
        
        libros = []
        for l_data in libros_data:
            libro = Libro(**l_data)
            session.add(libro)
            libros.append(libro)
        session.flush()

        # ===== ÓRDENES DE REPOSICIÓN =====
        
        estados = ["Pendiente", "Enviada", "Recibida", "Cancelada"]
        
        # Fechas para las órdenes (últimos 3 meses)
        fechas_orden = [
            date.today() - timedelta(days=85),
            date.today() - timedelta(days=70),
            date.today() - timedelta(days=55),
            date.today() - timedelta(days=40),
            date.today() - timedelta(days=30),
            date.today() - timedelta(days=20),
            date.today() - timedelta(days=10),
            date.today() - timedelta(days=5),
            date.today() - timedelta(days=2),
            date.today(),
        ]
        
        # Órdenes de reposición: [proveedor_idx, fecha_idx, estado_idx, [(libro_idx, cantidad)]]
        ordenes_data = [
            # Proveedor 0 - Los Andes
            [0, 0, 2, [(0, 15), (1, 10)]],      # Recibida - Cien años (15), Quijote (10)
            [0, 3, 2, [(2, 20), (3, 12)]],      # Recibida - Principito (20), 1984 (12)
            [0, 6, 2, [(0, 10), (4, 8)]],       # Recibida - Cien años (10), Crimen (8)
            
            # Proveedor 1 - Universal
            [1, 1, 2, [(2, 25), (5, 10)]],      # Recibida - Principito (25), Rayuela (10)
            [1, 4, 1, [(3, 15), (6, 8)]],       # Enviada - 1984 (15), El túnel (8)
            [1, 7, 0, [(1, 12), (2, 15)]],      # Pendiente - Quijote (12), Principito (15)
            
            # Proveedor 2 - Planeta
            [2, 2, 2, [(4, 12), (5, 8)]],       # Recibida - Crimen (12), Rayuela (8)
            [2, 5, 2, [(0, 10), (6, 10)]],      # Recibida - Cien años (10), El túnel (10)
            [2, 8, 1, [(3, 10), (4, 5)]],       # Enviada - 1984 (10), Crimen (5)
            
            # Proveedor 3 - Books & Co.
            [3, 2, 2, [(1, 8), (2, 10)]],       # Recibida - Quijote (8), Principito (10)
            [3, 5, 2, [(5, 12), (6, 8)]],       # Recibida - Rayuela (12), El túnel (8)
            [3, 9, 0, [(0, 15), (3, 10)]],      # Pendiente - Cien años (15), 1984 (10)
            
            # Proveedor 4 - Distribuidora del Sur
            [4, 3, 2, [(4, 10), (5, 10)]],      # Recibida - Crimen (10), Rayuela (10)
            [4, 7, 1, [(1, 15), (2, 20)]],      # Enviada - Quijote (15), Principito (20)
            [4, 9, 0, [(0, 20), (6, 12)]],      # Pendiente - Cien años (20), El túnel (12)
        ]
        
        for o_data in ordenes_data:
            proveedor_idx, fecha_idx, estado_idx, detalles = o_data
            fecha_solicitud = fechas_orden[fecha_idx]
            
            # Calcular días de entrega según estado
            if estado_idx == 2:  # Recibida
                fecha_entrega = fecha_solicitud + timedelta(days=random.randint(3, 8))
            elif estado_idx == 1:  # Enviada
                fecha_entrega = None
            else:  # Pendiente o Cancelada
                fecha_entrega = None
            
            # Calcular total de la orden
            total_orden = 0
            for libro_idx, cantidad in detalles:
                total_orden += libros[libro_idx].precio * cantidad
            
            orden = OrdenReposicion(
                id_proveedor=proveedores[proveedor_idx].id,
                fecha_ingreso=fecha_solicitud - timedelta(days=random.randint(0, 2)),
                fecha_solicitud=fecha_solicitud,
                fecha_entrega=fecha_entrega,
                estado=estados[estado_idx],
                total_orden=float(total_orden)
            )
            session.add(orden)
            session.flush()
            
            for libro_idx, cantidad in detalles:
                detalle = DetallesReposicion(
                    id_orden=orden.id,
                    id_libro=libros[libro_idx].id,
                    cantidad=cantidad,
                    precio=float(libros[libro_idx].precio)
                )
                session.add(detalle)
                
                # Actualizar stock si la orden ya fue recibida
                if estado_idx == 2:  # Recibida
                    libros[libro_idx].stock_actual += cantidad
        
        session.commit()
        
        # Mostrar resumen
        print("\n" + "="*60)
        print("DATOS DE PRUEBA CARGADOS EXITOSAMENTE")
        print("="*60)
        print(f"Clientes: {session.query(Cliente).count()}")
        print(f"Membresías: {session.query(Membresia).count()}")
        print(f"Facturas: {session.query(Factura).count()}")
        print(f"Ventas: {session.query(Venta).count()}")
        print(f"Proveedores: {session.query(Proveedor).count()}")
        print(f"Libros: {session.query(Libro).count()}")
        print(f"Órdenes de reposición: {session.query(OrdenReposicion).count()}")
        print(f"Detalles de reposición: {session.query(DetallesReposicion).count()}")
        print("="*60)
        
    except Exception as e:
        session.rollback()
        print(f"Error al cargar datos: {e}")
        raise e
    finally:
        session.close()


















def compras_por_proveedor(fecha_inicio=None, fecha_fin=None):
    """Compras agrupadas por proveedor en un período"""
    session = crear_sesion()
    try:
        query = session.query(
            Proveedor.id,
            Proveedor.nombre_empresa,
            Proveedor.rif_nit,
            func.count(OrdenReposicion.id).label('num_ordenes'),
            func.sum(OrdenReposicion.total_orden).label('total_compras'),
            func.sum(DetallesReposicion.cantidad).label('total_libros')
        ).join(OrdenReposicion, Proveedor.id == OrdenReposicion.id_proveedor
        ).join(DetallesReposicion, OrdenReposicion.id == DetallesReposicion.id_orden
        ).group_by(Proveedor.id, Proveedor.nombre_empresa, Proveedor.rif_nit)
        
        if fecha_inicio and fecha_fin:
            query = query.filter(
                and_(OrdenReposicion.fecha_solicitud >= fecha_inicio, 
                     OrdenReposicion.fecha_solicitud <= fecha_fin)
            )
        
        resultados = query.order_by(desc('total_compras')).all()
        session.close()
        
        data = [("ID", "Proveedor", "RIF", "Órdenes", "Total Comprado", "Libros")]
        for r in resultados:
            data.append((
                str(r.id),
                r.nombre_empresa,
                r.rif_nit,
                str(r.num_ordenes),
                f"${r.total_compras:.2f}",
                str(r.total_libros or 0)
            ))
        return data
    finally:
        session.close()

def libros_mas_reordenados(limite=10):
    """Libros que más se han reordenado a proveedores"""
    session = crear_sesion()
    try:
        resultados = session.query(
            Libro.id,
            Libro.isbn,
            Libro.titulo,
            func.sum(DetallesReposicion.cantidad).label('total_reordenado'),
            func.count(DetallesReposicion.id_orden).label('veces_reordenado'),
            func.sum(DetallesReposicion.cantidad * DetallesReposicion.precio).label('costo_total')
        ).join(DetallesReposicion, Libro.id == DetallesReposicion.id_libro
        ).group_by(Libro.id, Libro.isbn, Libro.titulo
        ).order_by(desc('total_reordenado')
        ).limit(limite).all()
        session.close()
        
        data = [("ID", "ISBN", "Título", "Total Reordenado", "Veces", "Costo Total")]
        for r in resultados:
            data.append((
                str(r.id),
                r.isbn,
                r.titulo,
                str(r.total_reordenado),
                str(r.veces_reordenado),
                f"${r.costo_total:.2f}"
            ))
        return data
    finally:
        session.close()

def ordenes_reposicion_por_estado():
    """Órdenes de reposición agrupadas por estado"""
    session = crear_sesion()
    try:
        resultados = session.query(
            OrdenReposicion.estado,
            func.count(OrdenReposicion.id).label('num_ordenes'),
            func.sum(OrdenReposicion.total_orden).label('monto_total')
        ).group_by(OrdenReposicion.estado).all()
        session.close()
        
        data = [("Estado", "N° Órdenes", "Monto Total")]
        for r in resultados:
            data.append((
                r.estado,
                str(r.num_ordenes),
                f"${r.monto_total:.2f}"
            ))
        return data
    finally:
        session.close()

def proveedores_tiempo_entrega():
    """Tiempo promedio de entrega por proveedor"""
    session = crear_sesion()
    try:
        resultados = session.query(
            Proveedor.id,
            Proveedor.nombre_empresa,
            func.avg(
                func.julianday(OrdenReposicion.fecha_entrega) - 
                func.julianday(OrdenReposicion.fecha_solicitud)
            ).label('dias_promedio'),
            func.count(OrdenReposicion.id).label('ordenes_completadas')
        ).join(OrdenReposicion, Proveedor.id == OrdenReposicion.id_proveedor
        ).filter(OrdenReposicion.fecha_entrega.isnot(None)
        ).group_by(Proveedor.id, Proveedor.nombre_empresa
        ).all()
        session.close()
        
        data = [("ID", "Proveedor", "Días Promedio", "Órdenes")]
        for r in resultados:
            data.append((
                str(r.id),
                r.nombre_empresa,
                f"{r.dias_promedio:.1f}" if r.dias_promedio else "N/A",
                str(r.ordenes_completadas)
            ))
        return data
    finally:
        session.close()

def ordenes_por_mes(año=None):
    """Órdenes de reposición por mes"""
    if año is None:
        año = date.today().year
    
    session = crear_sesion()
    try:
        resultados = session.query(
            func.extract('month', OrdenReposicion.fecha_solicitud).label('mes'),
            func.count(OrdenReposicion.id).label('num_ordenes'),
            func.sum(OrdenReposicion.total_orden).label('total_mes')
        ).filter(
            func.extract('year', OrdenReposicion.fecha_solicitud) == año
        ).group_by(
            func.extract('month', OrdenReposicion.fecha_solicitud)
        ).order_by('mes').all()
        session.close()
        
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        
        data = [("Mes", "N° Órdenes", "Total Comprado")]
        for r in resultados:
            data.append((
                meses[int(r.mes)-1],
                str(r.num_ordenes),
                f"${r.total_mes:.2f}"
            ))
        return data
    finally:
        session.close()


















def proveedores_mas_compras(limite=10):
    """Proveedores con mayor monto de compras"""
    session = crear_sesion()
    try:
        resultados = session.query(
            Proveedor.id,
            Proveedor.nombre_empresa,
            Proveedor.rif_nit,
            func.count(OrdenReposicion.id).label('num_ordenes'),
            func.sum(OrdenReposicion.total_orden).label('total_compras')
        ).join(OrdenReposicion, Proveedor.id == OrdenReposicion.id_proveedor
        ).group_by(Proveedor.id, Proveedor.nombre_empresa, Proveedor.rif_nit
        ).order_by(desc('total_compras')
        ).limit(limite).all()
        session.close()
        
        data = [("ID", "Proveedor", "RIF", "N° Órdenes", "Total Compras")]
        for r in resultados:
            data.append((
                str(r.id),
                r.nombre_empresa,
                r.rif_nit,
                str(r.num_ordenes),
                f"${r.total_compras:.2f}"
            ))
        return data
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
        session.close()
        
        data = [("ID", "ISBN", "Título", "Stock Actual", "Stock Mínimo", "Faltante")]
        for r in resultados:
            data.append((
                str(r.id),
                r.isbn,
                r.titulo,
                str(r.stock_actual),
                str(r.stock_minimo),
                str(r.faltante)
            ))
        return data
    finally:
        session.close()

def ordenes_pendientes():
    """Órdenes de reposición pendientes y su detalle"""
    session = crear_sesion()
    try:
        resultados = session.query(
            OrdenReposicion.id,
            OrdenReposicion.fecha_solicitud,
            Proveedor.nombre_empresa,
            OrdenReposicion.total_orden,
            func.count(DetallesReposicion.id).label('items')
        ).join(Proveedor, OrdenReposicion.id_proveedor == Proveedor.id
        ).join(DetallesReposicion, OrdenReposicion.id == DetallesReposicion.id_orden
        ).filter(OrdenReposicion.estado.in_(["Pendiente", "Enviada"])
        ).group_by(OrdenReposicion.id, OrdenReposicion.fecha_solicitud, Proveedor.nombre_empresa, OrdenReposicion.total_orden
        ).order_by(OrdenReposicion.fecha_solicitud).all()
        session.close()
        
        data = [("ID Orden", "Fecha Solicitud", "Proveedor", "Total", "Items")]
        for r in resultados:
            data.append((
                str(r.id),
                r.fecha_solicitud.strftime("%d/%m/%Y"),
                r.nombre_empresa,
                f"${r.total_orden:.2f}",
                str(r.items)
            ))
        return data
    finally:
        session.close()

def resumen_compras_anual(año=None):
    """Resumen de compras agrupado por mes y proveedor"""
    if año is None:
        año = date.today().year
    
    session = crear_sesion()
    try:
        resultados = session.query(
            func.extract('month', OrdenReposicion.fecha_solicitud).label('mes'),
            Proveedor.nombre_empresa,
            func.sum(OrdenReposicion.total_orden).label('total_mes')
        ).join(Proveedor, OrdenReposicion.id_proveedor == Proveedor.id
        ).filter(
            func.extract('year', OrdenReposicion.fecha_solicitud) == año
        ).group_by(
            func.extract('month', OrdenReposicion.fecha_solicitud),
            Proveedor.nombre_empresa
        ).order_by('mes', desc('total_mes')).all()
        session.close()
        
        meses = ["Ene", "Feb", "Mar", "Abr", "May", "Jun", "Jul", "Ago", "Sep", "Oct", "Nov", "Dic"]
        
        data = [("Mes", "Proveedor", "Total Comprado")]
        for r in resultados:
            data.append((
                meses[int(r.mes)-1],
                r.nombre_empresa,
                f"${r.total_mes:.2f}"
            ))
        return data
    finally:
        session.close()