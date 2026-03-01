# sesion.py
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# IMPORTANTE: Importar TODOS los modelos ANTES de crear las tablas
from .model.base import Base
from .model.cliente import Cliente
from .model.membresia import Membresia
from .model.proveedor import Proveedor
from .model.libro import Libro
from .model.cafe import Cafe  # <-- NUEVO
from .model.factura import Factura
from .model.venta import Venta
from .model.orden_reposicion import OrdenReposicion
from .model.detalles_reposicion import DetallesReposicion
from .model.detalles_reposicion_cafe import DetallesReposicionCafe  
from .model.consumo_libro import ConsumoLibro
from .model.consumo_cafe import ConsumoCafe
from .model.recomendacion_libro import RecomendacionLibro

logging.basicConfig()
logger = logging.getLogger('sqlalchemy.engine')

engine = create_engine('sqlite:///db.sqlite')


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)

def crear_sesion():
    return Session()

def establecer_logs(habilitados: bool):
    level = logging.INFO if habilitados else logging.WARNING
    logger.setLevel(level)