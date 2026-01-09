"""
Explainability API Routes
FastAPI endpoints for explainability artifact generation
"""

from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel, Field
from typing import List, Dict, Any, Optional
from explainability import ExplainabilityIntegration


# ============================================================================
# Pydantic Models
# ============================================================================

class SkillMatch(BaseModel):
    """Skill match information"""
    skill: str
    present: bool
    confidence: float = Field(0.0, ge=0.0, le=1.0)
    evidence: Optional[str] = None


class SkillGaps(BaseModel):
    """Skill gaps information"""
    missing_skills: List[str] = []
    unclear_sections: List[str] = []


class SkillAnalysis(BaseModel):
    """Complete skill analysis"""
    matched_skills: List[SkillMatch]
    gaps: SkillGaps


class InterviewDataRequest(BaseModel):
    """Complete interview data for explainability"""
    candidate_name: str
    overall_score: float = Field(0, ge=0, le=100)
    technical_score: float = Field(0, ge=0, le=100)
    experience_score: float = Field(0, ge=0, le=100)
    education_score: float = Field(0, ge=0, le=100)
    skill_analysis: SkillAnalysis
    reasoning: str
    strengths: str
    areas_for_growth: str
    experience_level: str = "mid"  # junior, mid, senior
    learning_velocity: float = 1.0
    include_candidate_feedback: bool = False


class JobRequirements(BaseModel):
    """Job role requirements"""
    title: str
    level: str  # junior, mid, senior, lead
    required_skills: List[str]
    nice_to_have: List[str] = []


class ExplainabilityResponse(BaseModel):
    """Explainability artifact response"""
    candidate_name: str
    overall_score: float
    recruiter_explanation: str
    candidate_explanation: Optional[str]
    score_rationale: Dict[str, str]
    training_plan: Dict[str, Any]
    investment_summary: Dict[str, Any]


class RoleAnalysisResponse(BaseModel):
    """Role-specific analysis response"""
    candidate_name: str
    overall_score: float
    job_role: str
    job_level: str
    role_fit_analysis: Dict[str, Any]
    recruiter_explanation: str
    training_plan: Dict[str, Any]
    investment_summary: Dict[str, Any]


class HiringDecisionResponse(BaseModel):
    """Complete hiring decision package"""
    candidate_name: str
    overall_score: float
    recruiter_explanation: str
    candidate_explanation: Optional[str]
    training_plan: Dict[str, Any]
    investment_summary: Dict[str, Any]
    hiring_decision: Dict[str, Any]
    role_fit_analysis: Optional[Dict[str, Any]]


# ============================================================================
# Router Setup
# ============================================================================

router = APIRouter(
    prefix="/api/v1/explainability",
    tags=["explainability"]
)

# Initialize integration
integration = ExplainabilityIntegration()


# ============================================================================
# Endpoints
# ============================================================================

@router.post(
    "/generate",
    response_model=ExplainabilityResponse,
    summary="Generate Explainability Artifact",
    description="Generate recruiter and candidate-friendly explanations with training requirements"
)
async def generate_explainability(request: InterviewDataRequest) -> Dict[str, Any]:
    """
    Generate complete explainability artifact
    
    **Features:**
    - Recruiter-friendly explanation with hiring recommendation
    - Optional candidate-friendly feedback
    - Training plan with time and resource estimates
    - Investment analysis with ROI projections
    - Score rationale breakdown
    
    **Example Output:**
    - "Score reduced by 12 points due to missing Docker experience; however, growth potential remains high"
    - Training timeline: 8 weeks, estimated cost: $500-800
    - Break-even point: 10 weeks
    """
    
    try:
        interview_data = request.dict()
        result = integration.generate_from_interview(
            interview_data,
            include_candidate_feedback=request.include_candidate_feedback
        )
        
        return {
            "candidate_name": result["candidate_name"],
            "overall_score": result["overall_score"],
            "recruiter_explanation": result["recruiter_explanation"],
            "candidate_explanation": result["candidate_explanation"],
            "score_rationale": result["score_rationale"],
            "training_plan": result["training_plan"],
            "investment_summary": result["investment_summary"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating explainability artifact: {str(e)}"
        )


@router.post(
    "/generate/role-fit",
    response_model=RoleAnalysisResponse,
    summary="Generate Role-Specific Analysis",
    description="Analyze candidate fit for a specific job role"
)
async def generate_role_analysis(
    interview_request: InterviewDataRequest,
    job_requirements: JobRequirements
) -> Dict[str, Any]:
    """
    Generate role-specific explainability analysis
    
    **Includes:**
    - Skill matching against required skills
    - Required vs. nice-to-have skills breakdown
    - Role readiness level (Immediate Fit / Trainable / Growth Hire)
    - Time to productivity for specific role
    - Customized training plan for role requirements
    
    **Example:**
    - Required Skills Met: 4/4 (100%)
    - Readiness: "TRAINABLE - Can reach full productivity with training"
    - Time to Productivity: 6 weeks
    """
    
    try:
        interview_data = interview_request.dict()
        job_reqs = job_requirements.dict()
        
        result = integration.generate_for_job_role(
            interview_data,
            job_reqs,
            include_candidate_feedback=False
        )
        
        return {
            "candidate_name": result["candidate_name"],
            "overall_score": result["overall_score"],
            "job_role": result["job_role"],
            "job_level": result["job_level"],
            "role_fit_analysis": result["role_fit_analysis"],
            "recruiter_explanation": result["recruiter_explanation"],
            "training_plan": result["training_plan"],
            "investment_summary": result["investment_summary"]
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating role analysis: {str(e)}"
        )


@router.post(
    "/generate/hiring-decision",
    response_model=HiringDecisionResponse,
    summary="Generate Hiring Decision Package",
    description="Generate complete hiring decision package with all components"
)
async def generate_hiring_decision(
    interview_request: InterviewDataRequest,
    job_requirements: Optional[JobRequirements] = None
) -> Dict[str, Any]:
    """
    Generate complete hiring decision package
    
    **Includes:**
    - Recruiter and candidate explanations
    - Training plan and investment analysis
    - Hiring recommendation (STRONG_HIRE / HIRE_WITH_TRAINING / CONDITIONAL_HIRE / RECONSIDER)
    - Confidence score
    - Time to productivity
    - Role-specific fit analysis (if job requirements provided)
    
    **Decision Levels:**
    - STRONG_HIRE (Score >= 80): Ready for immediate impact
    - HIRE_WITH_TRAINING (Score 70-79): Good foundation with training
    - CONDITIONAL_HIRE (Score 60-69): Requires mentorship and structured plan
    - RECONSIDER (Score < 60): Consider alternative experience levels
    """
    
    try:
        interview_data = interview_request.dict()
        job_reqs = job_requirements.dict() if job_requirements else None
        
        result = integration.generate_hiring_decision_package(
            interview_data,
            job_reqs
        )
        
        return {
            "candidate_name": result["candidate_name"],
            "overall_score": result["overall_score"],
            "recruiter_explanation": result["recruiter_explanation"],
            "candidate_explanation": result["candidate_explanation"],
            "training_plan": result["training_plan"],
            "investment_summary": result["investment_summary"],
            "hiring_decision": result["hiring_decision"],
            "role_fit_analysis": result.get("role_fit_analysis")
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error generating hiring decision package: {str(e)}"
        )


@router.get(
    "/training-resources/{skill}",
    summary="Get Training Resources for Skill",
    description="Get recommended training resources for a specific skill"
)
async def get_training_resources(skill: str) -> Dict[str, Any]:
    """
    Get training resources and estimates for a specific skill
    
    **Returns:**
    - Estimated training hours
    - Recommended resources and platforms
    - Difficulty level
    - Priority level
    - Cost estimate
    """
    
    try:
        skill_map = integration.generator.skill_training_map
        
        if skill not in skill_map:
            raise HTTPException(
                status_code=404,
                detail=f"Skill '{skill}' not found in training map"
            )
        
        skill_info = skill_map[skill]
        
        return {
            "skill": skill,
            "estimated_hours": skill_info["hours"],
            "estimated_weeks": int(skill_info["hours"] / 10),
            "difficulty": skill_info["difficulty"],
            "priority": skill_info["priority"],
            "resources": skill_info["resources"],
            "estimated_cost": f"${skill_info['hours'] * 10:.0f}",  # Approximate
            "breakdown": {
                "self_study": f"{int(skill_info['hours'] * 0.6)} hours",
                "projects": f"{int(skill_info['hours'] * 0.3)} hours",
                "review": f"{int(skill_info['hours'] * 0.1)} hours"
            }
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving training resources: {str(e)}"
        )


@router.get(
    "/available-skills",
    summary="List Available Skills",
    description="Get list of all skills with training estimates"
)
async def list_available_skills() -> Dict[str, Any]:
    """
    Get complete list of skills with training information
    
    **Returns:**
    - All available skills
    - Training hours for each
    - Difficulty level
    - Priority ranking
    """
    
    try:
        skills = []
        skill_map = integration.generator.skill_training_map
        
        for skill, info in skill_map.items():
            skills.append({
                "skill": skill,
                "hours": info["hours"],
                "weeks": int(info["hours"] / 10),
                "difficulty": info["difficulty"],
                "priority": info["priority"]
            })
        
        # Sort by priority, then by skill name
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        skills.sort(key=lambda x: (priority_order.get(x["priority"], 4), x["skill"]))
        
        return {
            "total_skills": len(skills),
            "skills": skills,
            "difficulty_breakdown": {
                "easy": len([s for s in skills if s["difficulty"] == "easy"]),
                "medium": len([s for s in skills if s["difficulty"] == "medium"]),
                "hard": len([s for s in skills if s["difficulty"] == "hard"])
            }
        }
    
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error listing skills: {str(e)}"
        )
