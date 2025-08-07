from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List

from app import schemas, crud, db
from app.api import deps

router = APIRouter()

@router.get("/", response_model=List[schemas.User])
def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: db.models.user.User = Depends(deps.get_current_user)
):
    """
    Retrieve users.
    """
    users = crud.crud_user.user.get_multi(db, skip=skip, limit=limit)
    return users