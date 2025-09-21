# Admin API endpoints
# TODO: Implement admin endpoints for user and payment management

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from core.database import get_db

router = APIRouter(prefix='/admin', tags=['admin'])

@router.get('/users')
async def get_all_users(db: Session = Depends(get_db)):
    """Get all users (admin only)"""
    # TODO: Implement admin authentication check
    # TODO: Implement get all users
    return {'users': []}

@router.get('/payments')
async def get_all_payments(db: Session = Depends(get_db)):
    """Get all payments (admin only)"""
    # TODO: Implement admin authentication check
    # TODO: Implement get all payments
    return {'payments': []}

@router.get('/stats')
async def get_system_stats(db: Session = Depends(get_db)):
    """Get system statistics (admin only)"""
    # TODO: Implement admin authentication check
    # TODO: Implement system stats
    return {'stats': {'total_users': 0, 'total_evaluations': 0, 'total_revenue': 0}}