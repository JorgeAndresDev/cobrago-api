from sqlalchemy.orm import Session
from uuid import UUID
from app.models.payment import Payment
from app.schemas.payment import PaymentCreate

def create_payment(db: Session, payment: PaymentCreate) -> Payment:
    db_payment = Payment(
        monto=payment.monto,
        fecha=payment.fecha or None,  # Will use default if None
        synced=payment.synced,
        client_id=payment.client_id
    )
    db.add(db_payment)
    db.commit()
    db.refresh(db_payment)
    return db_payment

def get_payments_by_client(db: Session, client_id: UUID, skip: int = 0, limit: int = 100) -> list[Payment]:
    return db.query(Payment).filter(Payment.client_id == client_id).order_by(Payment.fecha.desc()).offset(skip).limit(limit).all()
