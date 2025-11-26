import pytest
from app.services.scoring_service import ScoringService

def test_normalize_skill():
    assert ScoringService.normalize_skill(" Python ") == "python"
    assert ScoringService.normalize_skill("React.js") == "react.js"

def test_compute_match_perfect():
    resume_profile = {
        "skills": [
            {"name": "python", "years_used": 5},
            {"name": "fastapi", "years_used": 2}
        ]
    }
    job_profile = {
        "required_skills": [
            {"name": "Python", "requirement_type": "must_have", "weight": 1},
            {"name": "FastAPI", "requirement_type": "must_have", "weight": 1}
        ]
    }
    
    result = ScoringService.compute_match(resume_profile, job_profile)
    assert result["overall_score"] == 100
    assert result["must_have_score"] == 100
    assert len(result["matched_skills"]) == 2

def test_compute_match_partial():
    resume_profile = {
        "skills": [
            {"name": "python", "years_used": 5}
        ]
    }
    job_profile = {
        "required_skills": [
            {"name": "Python", "requirement_type": "must_have", "weight": 1},
            {"name": "FastAPI", "requirement_type": "must_have", "weight": 1}
        ]
    }
    
    result = ScoringService.compute_match(resume_profile, job_profile)
    # 1 out of 2 must-haves matched = 50% must-have score
    # Overall score = 50 * 0.7 + 100 * 0.3 (since no nice-to-haves, nice-to-have score is 100 by default logic if total is 0, wait let's check logic)
    # Logic: if nice_to_have_total > 0 else 100. Here nice_to_have_total is 0. So 100.
    # Overall = 35 + 30 = 65.
    
    assert result["must_have_score"] == 50.0
    assert result["overall_score"] == 65.0
    assert len(result["matched_skills"]) == 1
    assert len(result["missing_skills"]) == 1
