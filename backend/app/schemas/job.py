from typing import Optional, List
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class SeniorityLevel(str, Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    DIRECTOR = "director"

class JobBase(BaseModel):
    title: str
    company_name: Optional[str] = None
    raw_text: str
    seniority_level: Optional[SeniorityLevel] = None
    location: Optional[str] = None

class JobCreate(JobBase):
    pass

class JobUpdate(JobBase):
    pass

class JobInDBBase(JobBase):
    id: UUID
    user_id: Optional[UUID] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Job(JobInDBBase):
    pass
