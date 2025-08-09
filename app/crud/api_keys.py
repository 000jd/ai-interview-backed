from typing import List, Optional
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db import models
from app import schemas
from app.core.security import generate_api_key, generate_api_secret


def create_api_key(db: Session, api_key: schemas.APIKeyCreate, user_id: str) -> models.APIKey:
    key = generate_api_key()
    secret = generate_api_secret()
    db_api_key = models.APIKey(name=api_key.name, key=key, secret=secret, owner_id=user_id)
    db.add(db_api_key)
    db.commit()
    db.refresh(db_api_key)
    return db_api_key


def get_user_api_keys(db: Session, user_id: str) -> List[models.APIKey]:
    return db.query(models.APIKey).filter(models.APIKey.owner_id == user_id).all()


def get_api_key(db: Session, key: str) -> Optional[models.APIKey]:
    return db.query(models.APIKey).filter(models.APIKey.key == key).first()


def update_api_key_usage(db: Session, api_key_id: str):
    db_api_key = db.query(models.APIKey).filter(models.APIKey.id == api_key_id).first()
    if db_api_key:
        db_api_key.usage_count += 1
        db_api_key.last_used_at = datetime.now(timezone.utc)
        db.commit()


def deactivate_api_key(db: Session, key_id: str, user_id: str) -> bool:
    db_api_key = (
        db.query(models.APIKey)
        .filter(models.APIKey.id == key_id, models.APIKey.owner_id == user_id)
        .first()
    )
    if db_api_key:
        db_api_key.is_active = False
        db.commit()
        return True
    return False
