from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class PaymentBase(BaseModel):
    monto: float
    fecha: datetime | None = None
    synced: bool = False

class PaymentCreate(PaymentBase):
    client_id: UUID

class PaymentResponse(PaymentBase):
    id: UUID
    client_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
