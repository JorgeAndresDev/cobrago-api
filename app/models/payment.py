from sqlalchemy import Column, Float, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID
from datetime import datetime
from app.database.config import Base
from app.database.mixins import BaseModelMixin

class Payment(Base, BaseModelMixin):
    __tablename__ = "payments"

    monto = Column(Float, nullable=False)
    fecha = Column(DateTime, default=datetime.utcnow, nullable=False)
    client_id = Column(UUID(as_uuid=True), ForeignKey("clients.id"), nullable=False)

    client = relationship("Client", back_populates="payments")
