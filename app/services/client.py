from sqlalchemy.orm import Session
from sqlalchemy import func
from uuid import UUID
from app.models.client import Client
from app.models.payment import Payment
from app.schemas.client import ClientCreate, ClientUpdate

def get_client(db: Session, client_id: UUID) -> Client | None:
    return db.query(Client).filter(Client.id == client_id).first()

def get_clients(db: Session, skip: int = 0, limit: int = 100) -> list[Client]:
    return db.query(Client).offset(skip).limit(limit).all()

def create_client(db: Session, client: ClientCreate) -> Client:
    db_client = Client(
        nombre=client.nombre,
        cedula=client.cedula,
        direccion=client.direccion,
        latitud=client.latitud,
        longitud=client.longitud,
        monto_total=client.monto_total,
        synced=client.synced
    )
    db.add(db_client)
    db.commit()
    db.refresh(db_client)
    return db_client

def update_client(db: Session, client_id: UUID, client_update: ClientUpdate) -> Client | None:
    db_client = get_client(db, client_id)
    if not db_client:
        return None
    
    update_data = client_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_client, key, value)
        
    db.commit()
    db.refresh(db_client)
    return db_client

def delete_client(db: Session, client_id: UUID) -> bool:
    db_client = get_client(db, client_id)
    if not db_client:
        return False
    db.delete(db_client)
    db.commit()
    return True

def calculate_saldo(db: Session, client_id: UUID) -> float | None:
    client = get_client(db, client_id)
    if not client:
        return None
    
    total_payments = db.query(func.sum(Payment.monto)).filter(Payment.client_id == client_id).scalar() or 0.0
    return client.monto_total - float(total_payments)
