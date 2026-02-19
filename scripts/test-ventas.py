import sys
import os
from datetime import date
from reportes.models import verificar_datos_ventas, productos_mas_vendidos, ventas_por_dia

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

print("=== VERIFICANDO FUNCIONES ===")
verificar_datos_ventas()

print("\n=== PROBANDO productos_mas_vendidos ===")
data = productos_mas_vendidos()
print(f"Registros obtenidos: {len(data)-1}")
if len(data) > 1:
    print("Primeros 3 registros:")
    for i, row in enumerate(data[1:4]):
        print(f"  {i+1}. {row}")

print("\n=== PROBANDO ventas_por_dia CON FECHA ESPECÍFICA ===")
fecha_con_datos = date(2026, 2, 17)
data_dia = ventas_por_dia(fecha_con_datos)
print(f"Ventas del {fecha_con_datos}: {data_dia}")

print("\n=== PROBANDO ventas_por_dia (hoy) ===")
data_dia_hoy = ventas_por_dia()
print(f"Ventas de hoy: {data_dia_hoy}")