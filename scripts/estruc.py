from libreria_cafe_edd_db import crear_sesion
from sqlalchemy import inspect

def ver_estructura_bd():
    session = crear_sesion()
    inspector = inspect(session.bind)
    
    print("="*60)
    print("ESTRUCTURA DE LA BASE DE DATOS")
    print("="*60)
    
    tablas = inspector.get_table_names()
    
    for tabla in tablas:
        print(f"\nTabla: {tabla.upper()}")
        print("-"*40)
        
        columnas = inspector.get_columns(tabla)
        for col in columnas:
            print(f"  - {col['name']}: {col['type']} (nullable: {col['nullable']})")
        
        fks = inspector.get_foreign_keys(tabla)
        if fks:
            print("\n  Llaves foraneas:")
            for fk in fks:
                print(f"    {fk['constrained_columns']} -> {fk['referred_table']}.{fk['referred_columns']}")
    
    session.close()

if __name__ == "__main__":
    ver_estructura_bd()