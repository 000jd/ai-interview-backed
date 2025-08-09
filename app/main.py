from fastapi import FastAPI, Depends, HTTPException, status
from scalar_fastapi import get_scalar_api_reference
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from contextlib import asynccontextmanager
import logging
from app.core.logging_config import setup_logging
import uvicorn

# Import all modules
from app.core.config import settings
from app.core.security import get_password_hash, verify_password, create_access_token, decode_access_token
from app.db.database import engine, get_db
from app.db import models
from app import schemas, crud
from app.api.api import api_router
from app.core.livekit_manager import LiveKitManager

setup_logging()
logger = logging.getLogger("app")

models.Base.metadata.create_all(bind=engine)

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan management"""
    logger.info("Starting ")
    
    app.state.livekit_manager = LiveKitManager()
    
    yield
    
    logger.info("Shutting down")

app = FastAPI(
    title="AI Interview Platform",
    description="AI-powered interview platform with LiveKit integration",
    version="1.0.0",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")

@app.get("/scalar", include_in_schema=False)
async def scalar_html():
    return get_scalar_api_reference(
        openapi_url=app.openapi_url,
        title=app.title,
    )

@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "message": "AI Interview Platform API is running",
        "version": "1.0.0",
        "status": "healthy"
    }

@app.get("/health")
async def health_check():
    """Detailed health check"""
    return {
        "status": "healthy",
        "database": "connected",
        "livekit": "configured",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
