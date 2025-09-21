# Payment database model
# TODO: Implement Payment SQLAlchemy model

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Payment(Base):
    __tablename__ = "payments"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    amount = Column(Integer, nullable=False)  # Amount in smallest currency unit (e.g., paisa)
    credits_purchased = Column(Integer, nullable=False)
    sslcommerz_transaction_id = Column(String(255), unique=True, nullable=True)
    status = Column(String(50), default="pending")  # pending, completed, failed, cancelled
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    user = relationship("User", back_populates="payments")
