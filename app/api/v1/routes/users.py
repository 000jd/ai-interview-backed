from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import crud
from app.schemas import user as user_schemas
from app.db.database import get_db
from app.api.deps import get_current_active_user

router = APIRouter()

@router.get("/me", response_model=user_schemas.User)
async def read_users_me(current_user = Depends(get_current_active_user)):
    """Get current user profile"""
    return current_user

@router.put("/me", response_model=user_schemas.User)
async def update_user_me(
    user_update: user_schemas.UserUpdate,
    current_user = Depends(get_current_active_user),
    db: Session = Depends(get_db)
):
    """Update current user profile"""
    if user_update.full_name is not None:
        current_user.full_name = user_update.full_name
    if user_update.is_active is not None and current_user.is_superuser:
        current_user.is_active = user_update.is_active
    
    db.commit()
    db.refresh(current_user)
    return current_user