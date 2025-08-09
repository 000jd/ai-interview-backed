from datetime import datetime, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, HTTPBearer, HTTPAuthorizationCredentials
from jose import JWTError
from sqlalchemy.orm import Session
from app.db import models
from app.db.database import get_db
from app.core.security import decode_access_token
from app import crud
from typing import Optional

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/v1/auth/login")
http_bearer = HTTPBearer()

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:
    """Get current authenticated user, checking for token revocation."""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = decode_access_token(token)
        email: str = payload.get("sub")
        jti: str = payload.get("jti")
        exp: int = payload.get("exp")
        
        if email is None or jti is None or exp is None:
            raise credentials_exception
        
        expire_time = datetime.fromtimestamp(int(exp), tz=timezone.utc)
        
        if datetime.now(timezone.utc) > expire_time:
             raise credentials_exception
             
        if crud.is_token_blocklisted(db, jti=jti):
            raise credentials_exception

        user = crud.get_user_by_email(db, email=email)
        if user is None:
            raise credentials_exception
        
        return user

    except JWTError:
        raise credentials_exception

async def get_current_active_user(current_user: models.User = Depends(get_current_user)):
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
async def get_api_key_user(
    credentials: HTTPAuthorizationCredentials = Depends(http_bearer),
    db: Session = Depends(get_db)
):
    """Authenticate using API key"""
    api_key = credentials.credentials
    
    db_api_key = crud.get_api_key(db, key=api_key)
    if not db_api_key or not db_api_key.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or inactive API key"
        )
    
    crud.update_api_key_usage(db, db_api_key.id)
    
    return db_api_key.owner
