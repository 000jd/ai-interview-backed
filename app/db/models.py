import uuid
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, Text, JSON
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.database import Base

class User(Base):
    """User model"""
    __tablename__ = "users"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    email = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    full_name = Column(String)
    is_active = Column(Boolean, default=True)
    is_superuser = Column(Boolean, default=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Relationships
    api_keys = relationship("APIKey", back_populates="owner")
    interviews = relationship("Interview", back_populates="creator")

class APIKey(Base):
    """API Key model for managing user API keys"""
    __tablename__ = "api_keys"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    name = Column(String, nullable=False)
    key = Column(String, unique=True, index=True, nullable=False)
    secret = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    usage_count = Column(Integer, default=0)
    last_used_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    # Foreign key
    owner_id = Column(String(36), ForeignKey("users.id"))
    
    # Relationships
    owner = relationship("User", back_populates="api_keys")

class Interview(Base):
    """Interview session model"""
    __tablename__ = "interviews"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    title = Column(String, nullable=False)
    candidate_name = Column(String, nullable=False)
    candidate_email = Column(String)
    position = Column(String, nullable=False)
    status = Column(String, default="scheduled")  # scheduled, active, completed, cancelled
    room_name = Column(String, unique=True, nullable=False)
    interview_token = Column(String)
    
    # Interview configuration
    interview_config = Column(JSON)
    
    # Results
    technical_score = Column(Integer, default=0)
    behavioral_score = Column(Integer, default=0)
    overall_feedback = Column(Text)
    interview_data = Column(JSON)  # Store questions, responses, etc.
    
    # Timestamps
    scheduled_at = Column(DateTime(timezone=True))
    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    
    # Foreign key
    creator_id = Column(String(36), ForeignKey("users.id"))
    
    # Relationships
    creator = relationship("User", back_populates="interviews")
    
class TokenBlocklist(Base):
    """Stores revoked JWT tokens"""
    __tablename__ = "token_blocklist"
    
    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    jti = Column(String, unique=True, index=True, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
