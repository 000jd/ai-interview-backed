import uuid
from sqlalchemy import Column, String, DateTime
from app.db.database import Base
from .base import CreatedAtMixin

class TokenBlocklist(Base, CreatedAtMixin):
    """Stores revoked JWT tokens"""
    __tablename__ = "token_blocklist"

    id = Column(String(36), primary_key=True, index=True, default=lambda: str(uuid.uuid4()))
    jti = Column(String, unique=True, index=True, nullable=False)
    # When the JWT naturally expires. Used for cleanup of old blocklist entries.
    expires_at = Column(DateTime(timezone=True), nullable=True)
