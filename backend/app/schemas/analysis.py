from typing import Optional, List, Dict, Any
from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from enum import Enum

class AnalysisStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class AnalysisBase(BaseModel):
    resume_id: UUID
    job_id: UUID
    llm_provider: Optional[str] = "openai"
    llm_model_name: Optional[str] = "gpt-3.5-turbo"

class AnalysisCreate(AnalysisBase):
    pass

class AnalysisInDBBase(AnalysisBase):
    id: UUID
    user_id: Optional[UUID] = None
    status: AnalysisStatus
    match_score: Optional[float] = None
    must_have_coverage: Optional[float] = None
    nice_to_have_coverage: Optional[float] = None
    overall_skill_coverage: Optional[float] = None
    experience_alignment_score: Optional[float] = None
    raw_result_json: Optional[Dict[str, Any]] = None
    error_message: Optional[str] = None
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class Analysis(AnalysisInDBBase):
    pass
