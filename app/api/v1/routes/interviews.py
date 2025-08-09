from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from typing import List, Optional

from app import crud
from app.schemas import interview as interview_schemas
from app.db.database import get_db
from app.api.deps import get_current_active_user, get_api_key_user
from app.core.livekit_manager import LiveKitManager

router = APIRouter()

def get_livekit_manager(request: Request) -> LiveKitManager:
    """Reuse app-scoped LiveKitManager singleton when available."""
    if hasattr(request.app.state, "livekit_manager") and request.app.state.livekit_manager:
        return request.app.state.livekit_manager
    return LiveKitManager()

@router.post("/", response_model=interview_schemas.Interview)
async def create_interview(
    interview: interview_schemas.InterviewCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    livekit_manager: LiveKitManager = Depends(get_livekit_manager)
):
    """Create new interview session"""
    db_interview = crud.create_interview(db=db, interview=interview, user_id=current_user.id)
    
    room_created = await livekit_manager.create_room(
        room_name=db_interview.room_name,
        empty_timeout=1800  # 30 minutes
    )
    
    if not room_created:
        crud.update_interview(
            db, 
            db_interview.id, 
            interview_schemas.InterviewUpdate(status="room_creation_failed")
        )
    
    return db_interview

@router.get("/", response_model=List[interview_schemas.Interview])
async def list_interviews(
    skip: int = 0,
    limit: int = 100,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List user's interviews"""
    return crud.get_user_interviews(db, user_id=current_user.id, skip=skip, limit=limit)

@router.get("/{interview_id}", response_model=interview_schemas.Interview)
async def get_interview(
    interview_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Get interview details"""
    db_interview = crud.get_interview(db, interview_id=interview_id)
    
    if not db_interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    if db_interview.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    return db_interview

@router.put("/{interview_id}", response_model=interview_schemas.Interview)
async def update_interview(
    interview_id: str,
    interview_update: interview_schemas.InterviewUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update interview"""
    db_interview = crud.get_interview(db, interview_id=interview_id)
    
    if not db_interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    if db_interview.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    updated_interview = crud.update_interview(db, interview_id, interview_update)
    return updated_interview

@router.post("/{interview_id}/token", response_model=interview_schemas.InterviewToken)
async def generate_interview_token(
    interview_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db),
    livekit_manager: LiveKitManager = Depends(get_livekit_manager)
):
    """Generate LiveKit token for interview participant"""
    db_interview = crud.get_interview(db, interview_id=interview_id)
    
    if not db_interview:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    if db_interview.creator_id != current_user.id and not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not enough permissions"
        )
    
    token = livekit_manager.generate_token(
        room_name=db_interview.room_name,
        participant_name=db_interview.candidate_name,
        identity=f"candidate-{db_interview.id}"
    )
    
    return interview_schemas.InterviewToken(
        token=token,
        room_name=db_interview.room_name,
        participant_name=db_interview.candidate_name
    )

@router.post("/api/create", response_model=interview_schemas.Interview)
async def api_create_interview(
    interview: interview_schemas.InterviewCreate,
    current_user = Depends(get_api_key_user),
    db: Session = Depends(get_db),
    livekit_manager: LiveKitManager = Depends(get_livekit_manager)
):
    """Create interview via API key (for integrations)"""
    db_interview = crud.create_interview(db=db, interview=interview, user_id=current_user.id)
    
    room_created = await livekit_manager.create_room(
        room_name=db_interview.room_name,
        empty_timeout=1800  # 30 minutes
    )
    
    if not room_created:
        crud.update_interview(
            db, 
            db_interview.id, 
            interview_schemas.InterviewUpdate(status="room_creation_failed")
        )
    
    return db_interview

@router.post("/api/{interview_id}/token", response_model=interview_schemas.InterviewToken)
async def api_generate_interview_token(
    interview_id: str,
    current_user = Depends(get_api_key_user),
    db: Session = Depends(get_db),
    livekit_manager: LiveKitManager = Depends(get_livekit_manager)
):
    """Generate interview token via API key"""
    db_interview = crud.get_interview(db, interview_id=interview_id)
    
    if not db_interview or db_interview.creator_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Interview not found"
        )
    
    token = livekit_manager.generate_token(
        room_name=db_interview.room_name,
        participant_name=db_interview.candidate_name,
        identity=f"candidate-{db_interview.id}"
    )
    
    return interview_schemas.InterviewToken(
        token=token,
        room_name=db_interview.room_name,
        participant_name=db_interview.candidate_name
    )
