from fastapi import APIRouter
from app.routes.auth import router as auth_router
from app.routes.client import router as client_router
from app.routes.payment import router as payment_router

api_router = APIRouter()

api_router.include_router(auth_router, prefix="/auth", tags=["auth"])
api_router.include_router(client_router, prefix="/clients", tags=["clients"])
api_router.include_router(payment_router, prefix="/payments", tags=["payments"])
