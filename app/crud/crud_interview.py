from sqlalchemy.orm import Session
from app.crud.base import CRUDBase
from app.db.models.interview import Interview
from app.schemas.interview import InterviewCreate, InterviewUpdate

class CRUDInterview(CRUDBase[Interview, InterviewCreate, InterviewUpdate]):
    pass

interview = CRUDInterview(Interview)