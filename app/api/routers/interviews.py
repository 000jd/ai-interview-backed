from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import uuid

from app import schemas, crud, db
from app.api import deps

router = APIRouter()

@router.post("/", response_model=schemas.Interview)
def create_interview(
    *,
    db: Session = Depends(deps.get_db),
    interview_in: schemas.InterviewCreate,
    current_user: db.models.user.User = Depends(deps.get_current_user)
):
    """
    Create new interview.
    (Here you would add logic to create a LiveKit room and store its name)
    """
    # Placeholder for LiveKit room creation
    livekit_room_name = f"interview-{interview_in.candidate_id}-{str(uuid.uuid4())}"
    
    # Create the interview object using a dedicated CRUD function
    # You would expand crud_interview to handle this.
    # interview = crud.interview.create_with_candidate(db=db, obj_in=interview_in, candidate_id=current_user.id, room_name=livekit_room_name)
    
    # Simplified example:
    db_interview = db.models.interview.Interview(
        **interview_in.dict(), 
        livekit_room_name=livekit_room_name
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

@router.get("/{interview_id}", response_model=schemas.Interview)
def read_interview(
    *,
    db: Session = Depends(deps.get_db),
    interview_id: int,
    current_user: db.models.user.User = Depends(deps.get_current_user)
):
    """
    Get interview by ID.
    """
    # You would use a crud function here, e.g., crud.interview.get(db, id=interview_id)
    interview = db.query(db.models.interview.Interview).filter(db.models.interview.Interview.id == interview_id).first()
    if not interview:
        raise HTTPException(status_code=404, detail="Interview not found")
    # Add logic here to check if the current_user has permission to view this
    return interview