import uuid
from sqlalchemy import Column, String, Integer, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.database import Base
from .base import CreatedAtMixin

class APIKey(Base, CreatedAtMixin):
    """API Key model for managing user API keys"""
    __tablename__ = "api_keys"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    key = Column(String, unique=True, index=True, nullable=False)
    secret = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))

    # Foreign key
    owner_id = Column(String(36), ForeignKey("users.id"))

    # Relationships
    owner = relationship("User", back_populates="api_keys")
