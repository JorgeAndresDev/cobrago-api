from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database.config import get_db
from app.schemas.payment import PaymentCreate, PaymentResponse
from app.models.user import User
from app.core.dependencies import get_current_user
from app.services import payment as payment_service
from app.services import client as client_service

router = APIRouter()

@router.post("/", response_model=PaymentResponse, status_code=status.HTTP_201_CREATED)
def create_payment(
    payment: PaymentCreate, 
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Verify client exists
    db_client = client_service.get_client(db, client_id=payment.client_id)
    if not db_client:
        raise HTTPException(status_code=404, detail="Client not found")
        
    return payment_service.create_payment(db=db, payment=payment)
