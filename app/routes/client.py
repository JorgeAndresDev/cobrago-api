from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from app.database.config import get_db
from app.schemas.client import ClientCreate, ClientUpdate, ClientResponse
from app.schemas.payment import PaymentResponse
from app.models.user import User
from app.core.dependencies import get_current_user
from app.services import client as client_service
from app.services import payment as payment_service

router = APIRouter()

@router.post("/", response_model=ClientResponse, status_code=status.HTTP_201_CREATED)
def create_client(
    client: ClientCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Optional logic: verify if cedula already exists and raise 400
    created = client_service.create_client(db=db, client=client)
    created.saldo = client_service.calculate_saldo(db, created.id)
    return created

@router.get("/", response_model=list[ClientResponse])
def read_clients(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    clients = client_service.get_clients(db, skip=skip, limit=limit)
    for c in clients:
        c.saldo = client_service.calculate_saldo(db, c.id)
    return clients

@router.get("/{client_id}", response_model=ClientResponse)
def read_client(
    client_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_client = client_service.get_client(db, client_id=client_id)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db_client.saldo = client_service.calculate_saldo(db, db_client.id)
    return db_client

@router.patch("/{client_id}", response_model=ClientResponse)
def update_client(
    client_id: UUID, 
    client_update: ClientUpdate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    db_client = client_service.update_client(db, client_id=client_id, client_update=client_update)
    if db_client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    db_client.saldo = client_service.calculate_saldo(db, db_client.id)
    return db_client

@router.delete("/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_client(
    client_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    success = client_service.delete_client(db, client_id=client_id)
    if not success:
        raise HTTPException(status_code=404, detail="Client not found")

@router.get("/{client_id}/saldo", response_model=dict)
def get_client_saldo(
    client_id: UUID, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    saldo = client_service.calculate_saldo(db, client_id)
    if saldo is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return {"client_id": client_id, "saldo": saldo}

@router.get("/{client_id}/abonos", response_model=list[PaymentResponse])
def get_client_payments(
    client_id: UUID, 
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify client exists
    db_client = client_service.get_client(db, client_id=client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
        
    return payment_service.get_payments_by_client(db, client_id=client_id, skip=skip, limit=limit)
