import asyncio
from celery import shared_task
from app.db.session import SessionLocal
from app.models.analysis import Analysis, AnalysisStatus
from app.models.resume import Resume
from app.models.job import JobDescription
from app.services.pdf_service import PDFService
from app.services.llm_client import get_llm_client
from app.services.scoring_service import ScoringService
from sqlalchemy import select
import json

async def _run_analysis_async(analysis_id: str):
    async with SessionLocal() as db:
        try:
            # 1. Load Analysis, Resume, Job
            result = await db.execute(select(Analysis).where(Analysis.id == analysis_id))
            analysis = result.scalars().first()
            if not analysis:
                return

            analysis.status = AnalysisStatus.PROCESSING
            await db.commit()

            result = await db.execute(select(Resume).where(Resume.id == analysis.resume_id))
            resume = result.scalars().first()
            
            result = await db.execute(select(JobDescription).where(JobDescription.id == analysis.job_id))
            job = result.scalars().first()

            # 2. Ensure Resume Parsed
            if not resume.parsed_text:
                resume.parsed_text = PDFService.extract_text_from_pdf(resume.file_path)
                await db.commit()

            # 3. LLM Extraction
            llm_client = get_llm_client(analysis.llm_provider)
            
            resume_profile = await llm_client.extract_resume_profile(resume.parsed_text)
            job_profile = await llm_client.extract_job_profile(job.raw_text)

            # 4. Compute Match
            match_result = ScoringService.compute_match(resume_profile, job_profile)
            
            # 5. Generate Explanation
            explanation = await llm_client.generate_explanation(match_result)
            match_result["explanation"] = explanation

            # 6. Update Analysis
            analysis.match_score = match_result["overall_score"]
            analysis.must_have_coverage = match_result["must_have_score"]
            analysis.nice_to_have_coverage = match_result["nice_to_have_score"]
            analysis.overall_skill_coverage = match_result["overall_score"] # Simplified
            analysis.raw_result_json = match_result
            analysis.status = AnalysisStatus.COMPLETED
            
            await db.commit()

        except Exception as e:
            print(f"Analysis failed: {e}")
            if analysis:
                analysis.status = AnalysisStatus.FAILED
                analysis.error_message = str(e)
                await db.commit()

@shared_task(name="app.workers.tasks.run_analysis")
def run_analysis(analysis_id: str):
    loop = asyncio.get_event_loop()
    loop.run_until_complete(_run_analysis_async(analysis_id))
