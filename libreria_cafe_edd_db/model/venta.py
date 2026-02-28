from sqlalchemy import ForeignKey, String, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .enum.tipo_venta import TipoVenta
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .factura import Factura

class Venta(Base):
    __tablename__ = 'venta'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    cantidad: Mapped[int] = mapped_column()
    precio: Mapped[float] = mapped_column()
    nombre_mostrado: Mapped[str] = mapped_column(String(255))
    tipo: Mapped[TipoVenta] = mapped_column(Enum(TipoVenta))
    id_producto: Mapped[int] = mapped_column()
    id_factura: Mapped[int] = mapped_column(ForeignKey('factura.id'))
    
    factura: Mapped["Factura"] = relationship(back_populates="ventas")