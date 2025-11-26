from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.db.session import get_db
from app.models.job import JobDescription
from app.schemas import job as job_schema

router = APIRouter()

@router.post("/", response_model=job_schema.Job)
async def create_job(
    *,
    db: AsyncSession = Depends(get_db),
    job_in: job_schema.JobCreate,
) -> Any:
    # TODO: Get current user
    
    job = JobDescription(
        title=job_in.title,
        company_name=job_in.company_name,
        raw_text=job_in.raw_text,
        seniority_level=job_in.seniority_level,
        location=job_in.location,
        # user_id=current_user.id
    )
    db.add(job)
    await db.commit()
    await db.refresh(job)
    
    # Trigger background task for skill extraction
    
    return job

@router.get("/", response_model=List[job_schema.Job])
async def read_jobs(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(select(JobDescription).offset(skip).limit(limit))
    jobs = result.scalars().all()
    return jobs

@router.get("/{job_id}", response_model=job_schema.Job)
async def read_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(select(JobDescription).where(JobDescription.id == job_id))
    job = result.scalars().first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")
    return job
