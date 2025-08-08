from fastapi import APIRouter
from app.api.v1.routes import auth, users, interviews, api_keys

v1_router = APIRouter(prefix="/v1")

v1_router.include_router(auth.router, prefix="/auth", tags=["Authentication"])
v1_router.include_router(users.router, prefix="/users", tags=["Users"])
v1_router.include_router(interviews.router, prefix="/interviews", tags=["Interviews"])
v1_router.include_router(api_keys.router, prefix="/api-keys", tags=["API Keys"])

api_router = APIRouter()
api_router.include_router(v1_router)
