import uuid
from sqlalchemy import Column, String, ForeignKey, DateTime, func, Enum, Float, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class AnalysisStatus(str, enum.Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_descriptions.id"), nullable=False)
    
    status = Column(Enum(AnalysisStatus), default=AnalysisStatus.PENDING, index=True)
    
    match_score = Column(Numeric, nullable=True)
    must_have_coverage = Column(Numeric, nullable=True)
    nice_to_have_coverage = Column(Numeric, nullable=True)
    overall_skill_coverage = Column(Numeric, nullable=True)
    experience_alignment_score = Column(Numeric, nullable=True)
    
    llm_model_name = Column(String)
    llm_provider = Column(String)
    raw_result_json = Column(JSONB)
    error_message = Column(Text, nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="analyses")
    resume = relationship("Resume", back_populates="analyses")
    job = relationship("JobDescription", back_populates="analyses")
