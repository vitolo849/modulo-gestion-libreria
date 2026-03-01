# libreria_cafe_edd_db/model/detalles_reposicion_cafe.py
from sqlalchemy import ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .orden_reposicion import OrdenReposicion
    from .cafe import Cafe

class DetallesReposicionCafe(Base):
    __tablename__ = 'detalles_reposicion_cafe'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_orden: Mapped[int] = mapped_column(ForeignKey('orden_reposicion.id'))
    id_cafe: Mapped[int] = mapped_column(ForeignKey('cafe.id'))
    cantidad: Mapped[int] = mapped_column()
    precio: Mapped[float] = mapped_column()
    
    # Relaciones
    orden: Mapped["OrdenReposicion"] = relationship()
    cafe: Mapped["Cafe"] = relationship(back_populates="detalles_reposicion")