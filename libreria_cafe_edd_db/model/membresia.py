from typing import List
from datetime import date
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cliente import Cliente

class Membresia(Base):
    __tablename__ = 'membresia'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha_inicio: Mapped[date] = mapped_column()
    fecha_vencimiento: Mapped[date] = mapped_column()
    cantidad_libros: Mapped[int] = mapped_column()
    descuento_cafe: Mapped[int] = mapped_column()
    monto: Mapped[int] = mapped_column()
    cantidad_cafe_gratis: Mapped[int] = mapped_column()
    tiempo_mesa: Mapped[int] = mapped_column()
    
    clientes: Mapped[List["Cliente"]] = relationship(back_populates="membresia")