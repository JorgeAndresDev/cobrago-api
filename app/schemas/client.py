from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ClientBase(BaseModel):
    nombre: str
    cedula: str
    direccion: str | None = None
    latitud: float | None = None
    longitud: float | None = None
    monto_total: float = 0.0
    synced: bool = False

class ClientCreate(ClientBase):
    pass

class ClientUpdate(BaseModel):
    nombre: str | None = None
    direccion: str | None = None
    latitud: float | None = None
    longitud: float | None = None
    monto_total: float | None = None
    synced: bool | None = None

class ClientResponse(ClientBase):
    id: UUID
    created_at: datetime
    updated_at: datetime
    saldo: float | None = None # Calculated field

    class Config:
        from_attributes = True
