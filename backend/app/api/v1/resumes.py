from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import shutil
import os
import uuid

from app.db.session import get_db
from app.models.resume import Resume
from app.schemas import resume as resume_schema

router = APIRouter()

UPLOAD_DIR = "/app/uploads/resumes"
os.makedirs(UPLOAD_DIR, exist_ok=True)

@router.post("/", response_model=resume_schema.Resume)
async def create_resume(
    *,
    db: AsyncSession = Depends(get_db),
    file: UploadFile = File(...),
    title: str = Form(None),
) -> Any:
    # TODO: Get current user
    
    file_id = uuid.uuid4()
    file_extension = os.path.splitext(file.filename)[1]
    file_path = f"{UPLOAD_DIR}/{file_id}{file_extension}"
    
    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    resume = Resume(
        title=title or file.filename,
        file_path=file_path,
        original_filename=file.filename,
        # user_id=current_user.id
    )
    db.add(resume)
    await db.commit()
    await db.refresh(resume)
    
    # Trigger background task for parsing
    
    return resume

@router.get("/", response_model=List[resume_schema.Resume])
async def read_resumes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(select(Resume).offset(skip).limit(limit))
    resumes = result.scalars().all()
    return resumes

@router.get("/{resume_id}", response_model=resume_schema.Resume)
async def read_resume(
    resume_id: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(select(Resume).where(Resume.id == resume_id))
    resume = result.scalars().first()
    if not resume:
        raise HTTPException(status_code=404, detail="Resume not found")
    return resume
