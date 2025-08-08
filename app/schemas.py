from pydantic import BaseModel, EmailStr
from typing import Optional, List, Dict, Any
from datetime import datetime

# User schemas
class UserBase(BaseModel):
    email: EmailStr
    username: str
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserUpdate(BaseModel):
    full_name: Optional[str] = None
    is_active: Optional[bool] = None

class User(UserBase):
    id: int
    is_active: bool
    is_superuser: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

# Authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

# API Key schemas
class APIKeyBase(BaseModel):
    name: str

class APIKeyCreate(APIKeyBase):
    pass

class APIKey(APIKeyBase):
    id: int
    key: str
    is_active: bool
    usage_count: int
    created_at: datetime
    last_used_at: Optional[datetime] = None
    
    class Config:
        from_attributes = True

class APIKeyWithSecret(APIKey):
    secret: str

# Interview schemas
class InterviewBase(BaseModel):
    title: str
    candidate_name: str
    candidate_email: Optional[str] = None
    position: str

class InterviewCreate(InterviewBase):
    interview_config: Optional[Dict[str, Any]] = None
    scheduled_at: Optional[datetime] = None

class InterviewUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[str] = None
    technical_score: Optional[int] = None
    behavioral_score: Optional[int] = None
    overall_feedback: Optional[str] = None

class Interview(InterviewBase):
    id: int
    status: str
    room_name: str
    technical_score: int
    behavioral_score: int
    created_at: datetime
    creator_id: int
    
    class Config:
        from_attributes = True

class InterviewToken(BaseModel):
    token: str
    room_name: str
    participant_name: str
