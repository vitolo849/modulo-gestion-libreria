from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cliente import Cliente

class ConsumoCafe(Base):
    __tablename__ = 'consumo_cafe'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey('cliente.id'))
    nombre_cafe: Mapped[str] = mapped_column(String(255))
    tamano: Mapped[int] = mapped_column()
    precio: Mapped[int] = mapped_column()
    
    cliente: Mapped["Cliente"] = relationship(back_populates="consumos_cafe")