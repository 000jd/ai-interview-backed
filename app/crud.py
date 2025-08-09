from sqlalchemy.orm import Session
from typing import Optional, List
from app.db import models
from app import schemas
from app.core.security import get_password_hash, verify_password, generate_api_key, generate_api_secret
from datetime import datetime

# User CRUD operations
def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """Get user by email"""
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """Get user by username"""
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate) -> models.User:
    """Create new user"""
    hashed_password = get_password_hash(user.password)
    db_user = models.User(
        email=user.email,
        username=user.username,
        full_name=user.full_name,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def authenticate_user(db: Session, email: str, password: str) -> Optional[models.User]:
    """Authenticate user"""
    user = get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user

# API Key CRUD operations
def create_api_key(db: Session, api_key: schemas.APIKeyCreate, user_id: int) -> models.APIKey:
    """Create new API key"""
    key = generate_api_key()
    secret = generate_api_secret()
    
    db_api_key = models.APIKey(
        name=api_key.name,
        key=key,
        secret=secret,
        owner_id=user_id
    )
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key

def get_user_api_keys(db: Session, user_id: int) -> List[models.APIKey]:
    """Get all API keys for a user"""
    return db.query(models.APIKey).filter(models.APIKey.owner_id == user_id).all()

def get_api_key(db: Session, key: str) -> Optional[models.APIKey]:
    """Get API key by key"""
    return db.query(models.APIKey).filter(models.APIKey.key == key).first()

def update_api_key_usage(db: Session, api_key_id: int):
    """Update API key usage statistics"""
    db_api_key = db.query(models.APIKey).filter(models.APIKey.id == api_key_id).first()
    if db_api_key:
        db_api_key.usage_count += 1
        db_api_key.last_used_at = datetime.utcnow()
        db.commit()

def deactivate_api_key(db: Session, key_id: int, user_id: int) -> bool:
    """Deactivate API key"""
    db_api_key = db.query(models.APIKey).filter(
        models.APIKey.id == key_id,
        models.APIKey.owner_id == user_id
    ).first()
    
    if db_api_key:
        db_api_key.is_active = False
        db.commit()
        return True
    return False

# Interview CRUD operations
def create_interview(db: Session, interview: schemas.InterviewCreate, user_id: int) -> models.Interview:
    """Create new interview"""
    import uuid
    room_name = f"interview-{uuid.uuid4().hex[:12]}"
    
    db_interview = models.Interview(
        **interview.dict(),
        room_name=room_name,
        creator_id=user_id
    )
    db.add(db_interview)
    db.commit()
    db.refresh(db_interview)
    return db_interview

def get_user_interviews(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Interview]:
    """Get interviews created by user"""
    return db.query(models.Interview).filter(
        models.Interview.creator_id == user_id
    ).offset(skip).limit(limit).all()

def get_interview(db: Session, interview_id: int) -> Optional[models.Interview]:
    """Get interview by ID"""
    return db.query(models.Interview).filter(models.Interview.id == interview_id).first()

def update_interview(db: Session, interview_id: int, interview_update: schemas.InterviewUpdate) -> Optional[models.Interview]:
    """Update interview"""
    db_interview = db.query(models.Interview).filter(models.Interview.id == interview_id).first()
    if not db_interview:
        return None
    
    update_data = interview_update.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_interview, field, value)
    
    db.commit()
    db.refresh(db_interview)
    return db_interview

def add_token_to_blocklist(db: Session, jti: str, expires_at: datetime):
    """Add a token's JTI to the blocklist."""
    db_token = models.TokenBlocklist(jti=jti, expires_at=expires_at)
    db.add(db_token)
    db.commit()
    db.refresh(db_token)
    return db_token

def is_token_blocklisted(db: Session, jti: str) -> bool:
    """Check if a token's JTI is in the blocklist."""
    token = db.query(models.TokenBlocklist).filter(models.TokenBlocklist.jti == jti).first()
    return token is not None