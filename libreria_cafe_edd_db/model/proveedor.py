from typing import Optional, List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .base import Base
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .orden_reposicion import OrdenReposicion

class Proveedor(Base):
    __tablename__ = 'proveedor'
    
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    nombre_empresa: Mapped[str] = mapped_column(String(255))
    rif_nit: Mapped[str] = mapped_column(String(50), unique=True)
    telefono: Mapped[Optional[str]] = mapped_column(String(20))
    email: Mapped[Optional[str]] = mapped_column(String(255))
    
    ordenes: Mapped[List["OrdenReposicion"]] = relationship(back_populates="proveedor")