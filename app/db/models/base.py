import uuid
from sqlalchemy import Column, DateTime
from sqlalchemy.sql import func
from app.db.database import Base

class CreatedAtMixin:
    """Mixin providing a timezone-aware created_at column."""
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class UpdatedAtMixin:
    """Mixin providing a timezone-aware updated_at column."""
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
