from sqlalchemy import Column, String, Float
from sqlalchemy.orm import relationship
from app.database.config import Base
from app.database.mixins import BaseModelMixin

class Client(Base, BaseModelMixin):
    __tablename__ = "clients"

    nombre = Column(String, index=True, nullable=False)
    cedula = Column(String, unique=True, index=True, nullable=False)
    direccion = Column(String)
    latitud = Column(Float, nullable=True)
    longitud = Column(Float, nullable=True)
    monto_total = Column(Float, default=0.0, nullable=False) # Initial debt

    payments = relationship("Payment", back_populates="client", cascade="all, delete-orphan")
