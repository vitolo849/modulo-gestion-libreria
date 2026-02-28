from typing import Optional
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cliente import Cliente

class ConsumoLibro(Base):
    __tablename__ = 'consumo_libro'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey('cliente.id'))
    nombre_libro: Mapped[str] = mapped_column(String(255))
    genero: Mapped[Optional[str]] = mapped_column(String(100))
    autor: Mapped[Optional[str]] = mapped_column(String(255))
    precio: Mapped[int] = mapped_column()
    
    cliente: Mapped["Cliente"] = relationship(back_populates="consumos_libros")