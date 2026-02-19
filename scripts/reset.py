import sys
import os
import random
from datetime import date, timedelta
from libreria_cafe_edd_db import crear_sesion
from libreria_cafe_edd_db import Cliente, Membresia, Factura, Venta, ConsumoLibro, ConsumoCafe
from libreria_cafe_edd_db.model.enum.metodo_pago import MetodoPago

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def resetear_y_cargar():
    print("=== RESETEANDO BASE DE DATOS ===")
    session = crear_sesion()
    
    try:
        print("Eliminando datos existentes...")
        session.query(Venta).delete()
        session.query(Factura).delete()
        session.query(ConsumoLibro).delete()
        session.query(ConsumoCafe).delete()
        session.query(Cliente).delete()
        session.query(Membresia).delete()
        session.commit()
        print("Datos eliminados.")
        
        print("Cargando nuevos datos de prueba...")
        
        membresias = []
        for i in range(3):
            membresia = Membresia(
                fecha_inicio=date.today() - timedelta(days=random.randint(30, 365)),
                fecha_vencimiento=date.today() + timedelta(days=random.randint(30, 365)),
                cantidad_libros=random.choice([3, 5, 10]),
                descuento_cafe=random.choice([5, 10, 15]),
                monto=random.randint(50000, 200000),
                cantidad_cafe_gratis=random.choice([1, 2, 3]),
                tiempo_mesa=random.choice([60, 90, 120])
            )
            session.add(membresia)
            membresias.append(membresia)
        
        session.flush()
        
        nombres = [
            "Juan Pérez", "María González", "Carlos Rodríguez", "Ana Martínez", 
            "Luis Sánchez", "Carmen López", "José García", "Laura Fernández",
            "Miguel Ángel", "Sofía Torres", "Ricardo Gómez", "Valentina Díaz",
            "Andrés Morales", "Camila Ruiz", "Javier Castro", "Isabel Vargas",
            "Fernando Rojas", "Paula Méndez", "Roberto Silva", "Daniela Herrera"
        ]
        
        clientes = []
        for i in range(20):
            cliente = Cliente(
                id_membresia=random.choice([None, membresias[0].id, membresias[1].id, membresias[2].id]),
                nombre=nombres[i],
                cedula=10000000 + i,
                fecha_ingreso=date.today() - timedelta(days=random.randint(1, 365)),
                fecha_cumple=date(date.today().year, random.randint(1, 12), random.randint(1, 28)) if random.random() > 0.3 else None,
                frecuencia=0,
                razon_social=f"Empresa {nombres[i].split()[0]}" if random.random() > 0.7 else None,
                direccion_fiscal=f"Calle {random.randint(1, 100)}, Ciudad" if random.random() > 0.7 else None,
                telefono=f"0412-{random.randint(1000000, 9999999)}"
            )
            session.add(cliente)
            clientes.append(cliente)
        
        session.flush()
        
        productos = [
            ("Cien años de soledad", "LIBRO", 35000),
            ("Don Quijote de la Mancha", "LIBRO", 42000),
            ("El principito", "LIBRO", 28000),
            ("1984", "LIBRO", 32000),
            ("Crimen y castigo", "LIBRO", 38000),
            ("Espresso", "CAFE", 4500),
            ("Cappuccino", "CAFE", 5500),
            ("Latte", "CAFE", 6000),
            ("Mocha", "CAFE", 6500),
            ("Americano", "CAFE", 4000),
        ]
        
        metodos_pago = [
            MetodoPago.EFECTIVO,
            MetodoPago.DIVISAS,
            MetodoPago.PUNTO,
            MetodoPago.BIOPAGO,
            MetodoPago.PAGO_MOVIL,
            MetodoPago.TRANSFERENCIA
        ]
        
        total_facturas = 0
        for cliente in clientes:
            num_facturas = random.randint(3, 10)
            
            for _ in range(num_facturas):
                fecha_factura = date.today() - timedelta(days=random.randint(1, 90))
                metodo_pago = random.choice(metodos_pago)
                
                factura = Factura(
                    fecha=fecha_factura,
                    metodo_pago=metodo_pago,
                    subtotal=0,
                    monto_iva=0,
                    monto_igtf=0,
                    monto_total=0,
                    id_cliente=cliente.id
                )
                session.add(factura)
                session.flush()
                
                num_productos = random.randint(2, 6)
                subtotal = 0
                
                for _ in range(num_productos):
                    producto = random.choice(productos)
                    nombre, tipo, precio = producto
                    cantidad = random.randint(1, 4)
                    
                    venta = Venta(
                        cantidad=cantidad,
                        precio=precio,
                        nombre_mostrado=nombre,
                        tipo=tipo,
                        id_producto=random.randint(1, 100),
                        id_factura=factura.id
                    )
                    session.add(venta)
                    
                    subtotal += cantidad * precio
                
                iva = subtotal * 0.16
                igtf = subtotal * 0.03 if metodo_pago == MetodoPago.DIVISAS else 0
                total = subtotal + iva + igtf
                
                factura.subtotal = subtotal
                factura.monto_iva = iva
                factura.monto_igtf = igtf
                factura.monto_total = total
                
                total_facturas += 1
        
        session.commit()
        
        num_clientes = session.query(Cliente).count()
        num_facturas = session.query(Factura).count()
        num_ventas = session.query(Venta).count()
        
        print("\n" + "="*50)
        print("BASE DE DATOS RESETEADA Y CARGADA")
        print("="*50)
        print(f"Clientes: {num_clientes}")
        print(f"Membresías: {session.query(Membresia).count()}")
        print(f"Facturas: {num_facturas}")
        print(f"Ventas: {num_ventas}")
        print("="*50)
        
        print("\nEjemplos de facturas creadas:")
        facturas_ejemplo = session.query(Factura).limit(5).all()
        for f in facturas_ejemplo:
            print(f"  Factura {f.id}: {f.fecha} - {f.metodo_pago.name} - ${f.monto_total:.2f}")
        
    except Exception as e:
        session.rollback()
        print(f"ERROR: {e}")
        import traceback
        traceback.print_exc()
    finally:
        session.close()

if __name__ == "__main__":
    resetear_y_cargar()