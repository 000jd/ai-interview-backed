from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class APIKeyBase(BaseModel):
    name: str


class APIKeyCreate(APIKeyBase):
    pass


class APIKey(APIKeyBase):
    id: str
    key: str
    is_active: bool
    usage_count: int
    created_at: datetime
    last_used_at: Optional[datetime] = None

    class Config:
        from_attributes = True


class APIKeyWithSecret(APIKey):
    secret: str
