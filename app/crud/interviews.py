from typing import Optional, List
from sqlalchemy.orm import Session
import uuid
from app.db import models
from app.schemas import interview as interview_schemas


def create_interview(db: Session, interview: interview_schemas.InterviewCreate, user_id: str) -> models.Interview:
    """Create new interview with server-generated room_name."""
    generated_room_name = f"interview-{uuid.uuid4().hex[:12]}"
    db_interview = models.Interview(
        **interview.model_dump(),
        room_name=generated_room_name,
        creator_id=user_id,
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

 

def get_user_interviews(db: Session, user_id: str, skip: int = 0, limit: int = 100) -> List[models.Interview]:
    return (
        db.query(models.Interview)
        .filter(models.Interview.creator_id == user_id)
        .offset(skip)
        .limit(limit)
        .all()
    )


def get_interview(db: Session, interview_id: str) -> Optional[models.Interview]:
    return db.query(models.Interview).filter(models.Interview.id == interview_id).first()


def update_interview(
    db: Session, interview_id: str, interview_update: interview_schemas.InterviewUpdate
) -> Optional[models.Interview]:
    db_interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not db_interview:
        return None
    update_data = interview_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_interview, field, value)
    db.commit()
    db.refresh(db_interview)
    return db_interview
