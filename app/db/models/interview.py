import uuid
from sqlalchemy import Column, String, Integer, DateTime, Text, JSON, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from .base import CreatedAtMixin, UpdatedAtMixin

class Interview(Base, CreatedAtMixin, UpdatedAtMixin):
    """Interview session model"""
    __tablename__ = "interviews"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    candidate_name = Column(String, nullable=False)
    candidate_email = Column(String)
    position = Column(String, nullable=False)
    status = Column(String, default="scheduled")
    room_name = Column(String, unique=True, nullable=False)
    interview_token = Column(String)

    # Interview configuration
    interview_config = Column(JSON)

    # Results
    technical_score = Column(Integer, default=0)
    behavioral_score = Column(Integer, default=0)
    overall_feedback = Column(Text)
    interview_data = Column(JSON)

    # Timestamps
    scheduled_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # Foreign key
    creator_id = Column(String(36), ForeignKey("users.id"))

    # Relationships
    creator = relationship("User", back_populates="interviews")
