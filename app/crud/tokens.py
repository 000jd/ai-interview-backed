from typing import Optional
from sqlalchemy.orm import Session
from datetime import datetime, timezone
from app.db import models


def add_token_to_blocklist(db: Session, jti: str, expires_at: datetime):
    token = models.TokenBlocklist(jti=jti, expires_at=expires_at)
    db.add(token)
    db.commit()
    db.refresh(token)
    return token


def is_token_blocklisted(db: Session, jti: str) -> bool:
    token = db.query(models.TokenBlocklist).filter(models.TokenBlocklist.jti == jti).first()
    return token is not None


def cleanup_expired_blocklisted_tokens(db: Session) -> int:
    now = datetime.now(timezone.utc)
    deleted_count = (
        db.query(models.TokenBlocklist)
        .filter(models.TokenBlocklist.expires_at.isnot(None), models.TokenBlocklist.expires_at < now)
        .delete(synchronize_session=False)
    )
    db.commit()
    return int(deleted_count or 0)
