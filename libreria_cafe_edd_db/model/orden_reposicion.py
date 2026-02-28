from typing import Optional, List
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from datetime import date
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .proveedor import Proveedor
    from .detalles_reposicion import DetallesReposicion

class OrdenReposicion(Base):
    __tablename__ = 'orden_reposicion'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_proveedor: Mapped[int] = mapped_column(ForeignKey('proveedor.id'))
    fecha_ingreso: Mapped[date] = mapped_column()
    fecha_solicitud: Mapped[date] = mapped_column()
    fecha_entrega: Mapped[Optional[date]] = mapped_column()
    estado: Mapped[str] = mapped_column(String(50))
    total_orden: Mapped[float] = mapped_column()
    
    proveedor: Mapped["Proveedor"] = relationship(back_populates="ordenes")
    detalles: Mapped[List["DetallesReposicion"]] = relationship(back_populates="orden")