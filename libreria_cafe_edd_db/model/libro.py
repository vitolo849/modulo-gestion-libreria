from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .detalles_reposicion import DetallesReposicion

class Libro(Base):
    __tablename__ = 'libro'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    isbn: Mapped[str] = mapped_column(String(20), unique=True)
    titulo: Mapped[str] = mapped_column(String(255))
    stock_actual: Mapped[int] = mapped_column(default=0)
    stock_minimo: Mapped[int] = mapped_column(default=0)
    precio: Mapped[float] = mapped_column()
    
    detalles_reposicion: Mapped[List["DetallesReposicion"]] = relationship(back_populates="libro")