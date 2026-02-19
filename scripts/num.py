
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from libreria_cafe_edd_db.model.enum.metodo_pago import MetodoPago

print("=== VALORES DEL ENUM METODOPAGO ===")
for metodo in MetodoPago:
    print(f"  - {metodo.name} = {metodo.value}")