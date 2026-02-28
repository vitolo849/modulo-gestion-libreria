import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .model.base import Base

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