import uuid
from sqlalchemy import Column, String, Text, Numeric, ForeignKey, DateTime, func, Enum, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base
import enum

class Skill(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, index=True, nullable=False)
    category = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Resume(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True, index=True)
    title = Column(String)
    file_path = Column(String, nullable=False)
    original_filename = Column(String)
    parsed_text = Column(Text)
    language = Column(String(10), default="en")
    total_years_experience = Column(Numeric)
    headline = Column(String)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    user = relationship("User", back_populates="resumes")
    skills = relationship("ResumeSkill", back_populates="resume")
    analyses = relationship("Analysis", back_populates="resume")

class SkillLevel(str, enum.Enum):
    BASIC = "basic"
    INTERMEDIATE = "intermediate"
    ADVANCED = "advanced"
    EXPERT = "expert"

class ResumeSkill(Base):
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resume_id = Column(UUID(as_uuid=True), ForeignKey("resumes.id"), nullable=False)
    skill_id = Column(UUID(as_uuid=True), ForeignKey("skills.id"), nullable=False)
    declared_level = Column(Enum(SkillLevel), nullable=True)
    years_used = Column(Numeric)
    source = Column(String) # llm, manual
    confidence = Column(Float)

    resume = relationship("Resume", back_populates="skills")
    skill = relationship("Skill")

    __table_args__ = (
        UniqueConstraint('resume_id', 'skill_id', name='unique_resume_skill'),
    )
