export interface User {
    id: string;
    email: string;
    full_name?: string;
}

export interface Resume {
    id: string;
    title?: string;
    file_path: string;
    original_filename?: string;
    created_at: string;
}

export interface Job {
    id: string;
    title: string;
    company_name?: string;
    raw_text: string;
    seniority_level?: string;
    location?: string;
    created_at: string;
}

export interface JobCreate {
    title: string;
    company_name?: string;
    raw_text: string;
    seniority_level?: string;
    location?: string;
}

export interface SkillMatch {
    job_skill: string;
    resume_skill?: string;
    score?: number;
    type: 'must_have' | 'nice_to_have';
}

export interface MatchBreakdown {
    overall_score: number;
    must_have_score: number;
    nice_to_have_score: number;
    matched_skills: SkillMatch[];
    missing_skills: SkillMatch[];
    explanation?: string;
}

export interface Analysis {
    id: string;
    resume_id: string;
    job_id: string;
    status: 'PENDING' | 'PROCESSING' | 'COMPLETED' | 'FAILED';
    match_score?: number;
    must_have_coverage?: number;
    nice_to_have_coverage?: number;
    overall_skill_coverage?: number;
    experience_alignment_score?: number;
    raw_result_json?: MatchBreakdown;
    error_message?: string;
    created_at: string;
}
