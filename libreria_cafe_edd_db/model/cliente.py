from typing import Optional, List
from datetime import date
from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .membresia import Membresia
    from .consumo_libro import ConsumoLibro
    from .consumo_cafe import ConsumoCafe
    from .factura import Factura
    from .recomendacion_libro import RecomendacionLibro

class Cliente(Base):
    __tablename__ = 'cliente'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    id_membresia: Mapped[Optional[int]] = mapped_column(ForeignKey('membresia.id'))
    nombre: Mapped[str] = mapped_column(String(255))
    cedula: Mapped[int] = mapped_column(unique=True)
    fecha_ingreso: Mapped[date] = mapped_column()
    fecha_cumple: Mapped[Optional[date]] = mapped_column()
    frecuencia: Mapped[int] = mapped_column(default=0)
    razon_social: Mapped[Optional[str]] = mapped_column(String(255))
    direccion_fiscal: Mapped[Optional[str]] = mapped_column(String(500))
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    
    membresia: Mapped[Optional["Membresia"]] = relationship(back_populates="clientes")
    consumos_libros: Mapped[List["ConsumoLibro"]] = relationship(back_populates="cliente")
    consumos_cafe: Mapped[List["ConsumoCafe"]] = relationship(back_populates="cliente")
    facturas: Mapped[List["Factura"]] = relationship(back_populates="cliente")
    recomendaciones: Mapped[List["RecomendacionLibro"]] = relationship(back_populates="cliente")