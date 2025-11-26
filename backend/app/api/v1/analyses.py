from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import uuid

from app.db.session import get_db
from app.models.analysis import Analysis, AnalysisStatus
from app.schemas import analysis as analysis_schema
# from app.workers.celery_app import celery_app

router = APIRouter()

@router.post("/", response_model=analysis_schema.Analysis)
async def create_analysis(
    *,
    db: AsyncSession = Depends(get_db),
    analysis_in: analysis_schema.AnalysisCreate,
) -> Any:
    # TODO: Get current user
    
    analysis = Analysis(
        resume_id=analysis_in.resume_id,
        job_id=analysis_in.job_id,
        llm_provider=analysis_in.llm_provider,
        llm_model_name=analysis_in.llm_model_name,
        status=AnalysisStatus.PENDING,
        # user_id=current_user.id
    )
    db.add(analysis)
    await db.commit()
    await db.refresh(analysis)
    
    # Trigger Celery task
    # celery_app.send_task("app.workers.tasks.run_analysis", args=[str(analysis.id)])
    
    return analysis

@router.get("/{analysis_id}", response_model=analysis_schema.Analysis)
async def read_analysis(
    analysis_id: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
    analysis = result.scalars().first()
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    return analysis
