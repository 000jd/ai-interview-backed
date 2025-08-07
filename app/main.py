from fastapi import FastAPI
from app.api.routers import auth, interviews, users
from app.db.base import Base, engine

# This creates the database tables if they don't exist
# In a production setup, you would use Alembic for migrations
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI Interview Platform",
    description="The backend for the AI Interview Platform.",
    version="0.1.0"
)

# Include API routers
app.include_router(auth.router, prefix="/api/v1/auth", tags=["auth"])
app.include_router(interviews.router, prefix="/api/v1/interviews", tags=["interviews"])
app.include_router(users.router, prefix="/api/v1/users", tags=["users"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the AI Interview Platform API"}