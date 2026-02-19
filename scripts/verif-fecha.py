import sys
import os
from datetime import date, timedelta
from sqlalchemy import func
from libreria_cafe_edd_db import crear_sesion
from reportes.models import Factura

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

session = crear_sesion()

print("=== FECHAS DE FACTURAS EN LA BD ===")
print(f"Hoy es: {date.today()}\n")

fechas = session.query(
    Factura.fecha, 
    func.count(Factura.id).label('total')
).group_by(Factura.fecha).order_by(Factura.fecha.desc()).all()

print("Facturas agrupadas por fecha:")
for fecha, total in fechas:
    print(f"  {fecha}: {total} facturas")

facturas_hoy = session.query(Factura).filter(Factura.fecha == date.today()).count()
print(f"\nFacturas de hoy ({date.today()}): {facturas_hoy}")

print(f"\nFacturas de los últimos 5 días:")
for i in range(5):
    fecha = date.today() - timedelta(days=i)
    count = session.query(Factura).filter(Factura.fecha == fecha).count()
    print(f"  {fecha}: {count} facturas")

session.close()