from pydantic import BaseModel, Field
from typing import List, Optional
from enum import Enum

class ResumeFile(BaseModel):
    filename: str
    content: str

class JobDescriptionRequest(BaseModel):
    job_description: str
    resumes: List[ResumeFile]

class SkillMatch(BaseModel):
    skill: str
    present: bool
    evidence: Optional[str] = None
    confidence: float = Field(ge=0, le=1)

class GapAnalysis(BaseModel):
    missing_skills: List[str]
    unclear_sections: List[str]
    inconsistencies: List[str]

class CandidateScore(BaseModel):
    overall_score: float = Field(ge=0, le=100)
    technical_fit: float = Field(ge=0, le=100)
    experience_fit: float = Field(ge=0, le=100)
    education_fit: float = Field(ge=0, le=100)
    reasoning: str

class InterviewQuestion(BaseModel):
    question: str
    category: str
    reasoning: str

class CandidateEvaluation(BaseModel):
    candidate_name: str
    filename: str
    score: CandidateScore
    skill_matches: List[SkillMatch]
    gaps: GapAnalysis
    interview_questions: List[InterviewQuestion]
    summary: str

class EvaluationResponse(BaseModel):
    evaluations: List[CandidateEvaluation]
    processing_time: float
    errors: Optional[List[dict]] = []
    total_files: int = 0
    successful: int = 0
    failed: int = 0