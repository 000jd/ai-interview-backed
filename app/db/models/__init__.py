from app.db.database import Base

# Import all models so Alembic/metadata sees them
from .user import User
from .api_key import APIKey
from .interview import Interview
from .token_blocklist import TokenBlocklist
