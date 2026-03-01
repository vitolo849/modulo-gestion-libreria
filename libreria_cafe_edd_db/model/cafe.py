# libreria_cafe_edd_db/model/cafe.py
from typing import Optional, List
from sqlalchemy import ForeignKey, String, Integer, Float
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .proveedor import Proveedor
    from .detalles_reposicion_cafe import DetallesReposicionCafe

class Cafe(Base):
    __tablename__ = 'cafe'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String(255), unique=True)
    descripcion: Mapped[Optional[str]] = mapped_column(String(500))
    tamano: Mapped[int] = mapped_column()
    precio: Mapped[float] = mapped_column()
    stock_actual: Mapped[int] = mapped_column(default=0)
    stock_minimo: Mapped[int] = mapped_column(default=0)
    proveedor_id: Mapped[Optional[int]] = mapped_column(ForeignKey('proveedor.id'))
    
    # Relaciones (solo lectura, no afecta a Proveedor)
    proveedor: Mapped[Optional["Proveedor"]] = relationship()
    detalles_reposicion: Mapped[List["DetallesReposicionCafe"]] = relationship(back_populates="cafe")