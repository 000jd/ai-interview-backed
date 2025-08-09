from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.crud.api_keys import (
    create_api_key,
    get_user_api_keys,
    deactivate_api_key as deactivate_api_key_crud,
)
from app.schemas import api_key as api_key_schemas
from app.db.database import get_db
from app.api.deps import get_current_active_user
from app.core.config import settings

router = APIRouter()

@router.post("/", response_model=api_key_schemas.APIKeyWithSecret)
async def create_api_key(
    api_key: api_key_schemas.APIKeyCreate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Create new API key"""
    existing_keys = get_user_api_keys(db, user_id=current_user.id)
    active_keys = [k for k in existing_keys if k.is_active]
    
    if len(active_keys) >= settings.MAX_API_KEYS_PER_USER:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Maximum number of API keys ({settings.MAX_API_KEYS_PER_USER}) reached"
        )
    
    return create_api_key(db=db, api_key=api_key, user_id=current_user.id)

@router.get("/", response_model=List[api_key_schemas.APIKey])
async def list_api_keys(
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """List user's API keys"""
    return get_user_api_keys(db, user_id=current_user.id)

@router.delete("/{key_id}")
async def deactivate_api_key(
    key_id: str,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Deactivate API key"""
    success = deactivate_api_key_crud(db, key_id=key_id, user_id=current_user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="API key not found"
        )
    return {"message": "API key deactivated successfully"}