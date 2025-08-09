from datetime import datetime, timedelta, timezone
from typing import Dict, Optional, Union, Any
import uuid
from passlib.context import CryptContext
from jose import jwt, JWTError
from fastapi import HTTPException, status
import secrets
import string

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token with a unique jti claim""" 
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # + Add unique identifier (jti) and expiration time (exp as int timestamp) to the claims
    to_encode.update({
        "exp": int(expire.timestamp()),
        "jti": uuid.uuid4().hex
    })
    
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str) -> Dict[str, Any]:
    """Decode and validate JWT token, returning its payload"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload 
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials (token error)"
        )

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password against hash"""
    return pwd_context.verify(plain_password, hashed_password)

def get_password_hash(password: str) -> str:
    """Hash password"""
    return pwd_context.hash(password)

def generate_api_key() -> str:
    """Generate secure API key"""
    # Generate 32 character random string
    characters = string.ascii_letters + string.digits
    api_key = ''.join(secrets.choice(characters) for _ in range(32))
    return f"{settings.API_KEY_PREFIX}{api_key}"

def generate_api_secret() -> str:
    """Generate secure API secret"""
    # Generate 64 character random string for secret
    characters = string.ascii_letters + string.digits + "! @#$%^&*"
    return ''.join(secrets.choice(characters) for _ in range(64))
