from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


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
    id: str
    status: str
    room_name: str
    technical_score: int
    behavioral_score: int
    created_at: datetime
    creator_id: str

    class Config:
        from_attributes = True


class InterviewToken(BaseModel):
    token: str
    room_name: str
    participant_name: str
