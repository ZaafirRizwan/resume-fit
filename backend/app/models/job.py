import uuid
from sqlalchemy import Column, String, Text, ForeignKey, DateTime, func, Enum, Float, UniqueConstraint, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class SeniorityLevel(str, enum.Enum):
    JUNIOR = "junior"
    MID = "mid"
    SENIOR = "senior"
    LEAD = "lead"
    DIRECTOR = "director"

class JobDescription(Base):
    __tablename__ = "job_descriptions"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    title = Column(String)
    company_name = Column(String)
    raw_text = Column(Text)
    language = Column(String(10), default="en")
    seniority_level = Column(Enum(SeniorityLevel), nullable=True)
    location = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="jobs")
    required_skills = relationship("JobRequiredSkill", back_populates="job")
    analyses = relationship("Analysis", back_populates="job")

class RequirementType(str, enum.Enum):
    MUST_HAVE = "must_have"
    NICE_TO_HAVE = "nice_to_have"

class JobRequiredSkill(Base):
    __tablename__ = "job_required_skills"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    job_id = Column(UUID(as_uuid=True), ForeignKey("job_descriptions.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    requirement_type = Column(Enum(RequirementType), default=RequirementType.MUST_HAVE)
    is_explicit = Column(Boolean, default=True)
    weight = Column(Float, default=1.0)

    job = relationship("JobDescription", back_populates="required_skills")
    skill = relationship("Skill") # Assuming Skill is imported in base or available

    __table_args__ = (
        UniqueConstraint('job_id', 'skill_id', 'requirement_type', name='unique_job_skill_req'),
    )
