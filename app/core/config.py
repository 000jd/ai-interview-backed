import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./ai_interview.db"
    
    # Security
    SECRET_KEY: str = "dev-secret-key-change-in-prod"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    
    # LiveKit Configuration
    LIVEKIT_URL: str = ""
    LIVEKIT_API_KEY: str = ""
    LIVEKIT_API_SECRET: str = ""
    
    # AI Services
    GOOGLE_API_KEY: Optional[str] 
    DEEPGRAM_API_KEY: Optional[str] 
    CARTESIA_API_KEY: Optional[str] 
    ELEVENLABS_API_KEY: Optional[str] 
    
    # Application Settings
    API_KEY_PREFIX: str = "sk_"
    MAX_API_KEYS_PER_USER: int = 3
    # Comma-separated list of allowed origins for CORS. Use "*" for all (dev only).
    ALLOWED_ORIGINS: str = "*"
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
