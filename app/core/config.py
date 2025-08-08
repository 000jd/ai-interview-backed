import os
from typing import Optional
from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    """Application settings"""
    
    # Database
    DATABASE_URL: str = "sqlite:///./ai_interview.db"
    
    # Security
    SECRET_KEY: str = "your-super-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    
    # LiveKit Configuration
    LIVEKIT_URL: str = Field(default="", description="LiveKit server URL")
    LIVEKIT_API_KEY: str = Field(default="", description="LiveKit API key")
    LIVEKIT_API_SECRET: str = Field(default="", description="LiveKit API secret")
    
    # AI Services
    GOOGLE_API_KEY: Optional[str] = None
    DEEPGRAM_API_KEY: Optional[str] = None
    CARTESIA_API_KEY: Optional[str] = None
    ELEVENLABS_API_KEY: Optional[str] = None
    
    # Application Settings
    API_KEY_PREFIX: str = "lk_"
    MAX_API_KEYS_PER_USER: int = 5
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()
