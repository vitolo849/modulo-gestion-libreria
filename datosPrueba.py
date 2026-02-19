
from reportes.models import cargar_datos_prueba
from reportes import models

if __name__ == "__main__":
    print("Iniciando carga de datos de prueba...")
    models.cargar_datos_prueba(force=True)
    print("Carga completada.")