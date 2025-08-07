from pydantic import BaseModel
from typing import Optional, Any
from datetime import datetime

class InterviewBase(BaseModel):
    position: str

class InterviewCreate(InterviewBase):
    candidate_id: int

class InterviewUpdate(BaseModel):
    status: Optional[str] = None
    report: Optional[dict[str, Any]] = None

class Interview(InterviewBase):
    id: int
    candidate_id: int
    status: str
    scheduled_at: datetime
    livekit_room_name: str

    class Config:
        orm_mode = True