from fastapi import APIRouter, Depends, HTTPException, Header, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app import schemas, crud
from app.db.database import get_db
from app.core.config import settings
from app.core.security import create_access_token, decode_access_token
from app.api.deps import get_current_active_user

router = APIRouter()

@router.post("/register", response_model=schemas.User)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user already exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(
            status_code=400,# Updated return type hint
            detail="Email already registered"
        )
    
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(
            status_code=400,
            detail="Username already taken"
        )
    
    # Create user
    return crud.create_user(db=db, user=user)

@router.post("/login", response_model=schemas.Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login user and return access token"""
    user = crud.authenticate_user(db, email=form_data.username, password=form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout(
    authorization: str = Header(...),
    db: Session = Depends(get_db)
):
    """
    Logout user by adding the current token to the blocklist.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid token for logout",
    )
    
    # The header is expected to be "Bearer <token>"
    token = authorization.split(" ")[1] if " " in authorization else None
    if not token:
        raise credentials_exception

    try:
        payload = decode_access_token(token)
        jti = payload.get("jti")
        exp = payload.get("exp")
        
        if not jti or not exp:
            raise credentials_exception
            
        expires_at = datetime.fromtimestamp(exp)
        
        # Add token to blocklist
        crud.add_token_to_blocklist(db, jti=jti, expires_at=expires_at)
        
    except HTTPException:
        # Re-raise the exception from decode_access_token if it's invalid
        raise
    except Exception:
        # Catch any other potential errors
        raise credentials_exception

    return {"message": "Successfully logged out"}

'''
@router.get("/me", response_model=schemas.User)
async def read_users_me(current_user = Depends(get_current_active_user)):
    """Get current user information"""
    return current_user
'''
