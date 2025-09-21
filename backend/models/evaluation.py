# Evaluation database model
# TODO: Implement Evaluation SQLAlchemy model

from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Float, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from core.database import Base

class Evaluation(Base):
    __tablename__ = "evaluations"
    
    id = Column(Integer, primary_key=True, index=True)
    essay_id = Column(Integer, ForeignKey("essays.id"), nullable=False)
    overall_band_score = Column(Float, nullable=False)
    task_achievement_score = Column(Integer, nullable=False)
    coherence_score = Column(Integer, nullable=False)
    lexical_score = Column(Integer, nullable=False)
    grammar_score = Column(Integer, nullable=False)
    feedback_json = Column(JSON, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Relationships
    essay = relationship("Essay", back_populates="evaluations")
