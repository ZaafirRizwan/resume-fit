from typing import Dict, Any, List
from rapidfuzz import fuzz

class ScoringService:
    @staticmethod
    def normalize_skill(name: str) -> str:
        return name.lower().strip()

    @staticmethod
    def compute_match(resume_profile: Dict[str, Any], job_profile: Dict[str, Any]) -> Dict[str, Any]:
        resume_skills = {ScoringService.normalize_skill(s['name']): s for s in resume_profile.get('skills', [])}
        job_skills = job_profile.get('required_skills', [])
        
        must_have_total = 0
        must_have_matched = 0
        nice_to_have_total = 0
        nice_to_have_matched = 0
        
        matched_skills = []
        missing_skills = []
        
        for job_skill in job_skills:
            name = ScoringService.normalize_skill(job_skill['name'])
            weight = job_skill.get('weight', 1.0)
            req_type = job_skill.get('requirement_type', 'must_have')
            
            # Fuzzy match
            best_match = None
            best_score = 0
            
            if name in resume_skills:
                best_match = name
                best_score = 100
            else:
                for r_skill in resume_skills:
                    score = fuzz.ratio(name, r_skill)
                    if score > 80: # Threshold
                        if score > best_score:
                            best_score = score
                            best_match = r_skill
            
            is_match = best_score > 80
            
            if req_type == 'must_have':
                must_have_total += weight
                if is_match:
                    must_have_matched += weight
            else:
                nice_to_have_total += weight
                if is_match:
                    nice_to_have_matched += weight
            
            if is_match:
                matched_skills.append({
                    "job_skill": name,
                    "resume_skill": best_match,
                    "score": best_score,
                    "type": req_type
                })
            else:
                missing_skills.append({
                    "job_skill": name,
                    "type": req_type
                })

        must_have_score = (must_have_matched / must_have_total * 100) if must_have_total > 0 else 100
        nice_to_have_score = (nice_to_have_matched / nice_to_have_total * 100) if nice_to_have_total > 0 else 100
        
        # Weighted overall score (e.g., 70% must-have, 30% nice-to-have)
        overall_score = (must_have_score * 0.7) + (nice_to_have_score * 0.3)
        
        return {
            "overall_score": round(overall_score, 2),
            "must_have_score": round(must_have_score, 2),
            "nice_to_have_score": round(nice_to_have_score, 2),
            "matched_skills": matched_skills,
            "missing_skills": missing_skills
        }
