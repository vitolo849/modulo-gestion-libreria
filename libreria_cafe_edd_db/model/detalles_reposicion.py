from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .orden_reposicion import OrdenReposicion
    from .libro import Libro

class DetallesReposicion(Base):
    __tablename__ = 'detalles_reposicion'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_orden: Mapped[int] = mapped_column(ForeignKey('orden_reposicion.id'))
    id_libro: Mapped[int] = mapped_column(ForeignKey('libro.id'))
    cantidad: Mapped[int] = mapped_column()
    precio: Mapped[float] = mapped_column()
    
    orden: Mapped["OrdenReposicion"] = relationship(back_populates="detalles")
    libro: Mapped["Libro"] = relationship(back_populates="detalles_reposicion")