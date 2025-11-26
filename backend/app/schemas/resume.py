from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime

class ResumeBase(BaseModel):
    title: Optional[str] = None
    headline: Optional[str] = None

class ResumeCreate(ResumeBase):
    pass

class ResumeUpdate(ResumeBase):
    pass

class ResumeInDBBase(ResumeBase):
    id: UUID
    user_id: Optional[UUID] = None
    file_path: str
    original_filename: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Resume(ResumeInDBBase):
    pass
