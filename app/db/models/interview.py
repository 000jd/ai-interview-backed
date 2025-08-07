from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.db.base import Base
import datetime

class Interview(Base):
    __tablename__ = "interviews"
    id = Column(Integer, primary_key=True, index=True)
    position = Column(String, index=True)
    status = Column(String, default="scheduled")
    scheduled_at = Column(DateTime, default=datetime.datetime.utcnow)
    livekit_room_name = Column(String, unique=True)
    report = Column(JSON, nullable=True)
    candidate_id = Column(Integer, ForeignKey("users.id"))
    candidate = relationship("User", back_populates="interviews")