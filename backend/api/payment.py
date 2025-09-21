# Payment API endpoints
# TODO: Implement SSLCommerz payment endpoints

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db
from services.payment_service import PaymentService

router = APIRouter(prefix="/payment", tags=["payment"])

@router.post("/initiate")
async def initiate_payment(db: Session = Depends(get_db)):
    """Initiate SSLCommerz payment"""
    # TODO: Implement payment initiation
    pass

@router.post("/success")
async def payment_success_callback(db: Session = Depends(get_db)):
    """Handle successful payment callback"""
    # TODO: Implement success callback
    pass

@router.post("/cancel")
async def payment_cancel_callback(db: Session = Depends(get_db)):
    """Handle cancelled payment callback"""
    # TODO: Implement cancel callback
    pass

@router.get("/history")
async def get_payment_history(db: Session = Depends(get_db)):
    """Get user payment history"""
    # TODO: Implement payment history
    pass
