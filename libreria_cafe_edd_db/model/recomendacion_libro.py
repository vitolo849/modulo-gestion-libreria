from typing import Optional
from datetime import date
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .cliente import Cliente
    
class RecomendacionLibro(Base):
    __tablename__ = 'recomendacion_libro'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_cliente: Mapped[int] = mapped_column(ForeignKey('cliente.id'))
    isbn: Mapped[str] = mapped_column(String(20))
    fecha_recomendacion: Mapped[date] = mapped_column()
    tipo_recomendacion: Mapped[Optional[str]] = mapped_column(String(100))
    
    cliente: Mapped["Cliente"] = relationship(back_populates="recomendaciones")