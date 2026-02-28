from typing import List
from datetime import date, datetime
from .enum.metodo_pago import MetodoPago
from sqlalchemy import ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cliente import Cliente
    from .venta import Venta

class Factura(Base):
    __tablename__ = 'factura'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    fecha: Mapped[datetime] = mapped_column()
    metodo_pago: Mapped[MetodoPago] = mapped_column(Enum(MetodoPago))
    subtotal: Mapped[float] = mapped_column()
    monto_iva: Mapped[float] = mapped_column()
    monto_igtf: Mapped[float] = mapped_column()
    monto_total: Mapped[float] = mapped_column()
    id_cliente: Mapped[int] = mapped_column(ForeignKey('cliente.id'))
    
    cliente: Mapped["Cliente"] = relationship(back_populates="facturas")
    ventas: Mapped[List["Venta"]] = relationship(back_populates="factura")