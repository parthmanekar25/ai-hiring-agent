"""
Explainability Integration
Connects explainability generator to the main scoring workflow
"""

from typing import Dict, Any, Optional
from backend.explainability.explainability_generator import ExplainabilityGenerator


class ExplainabilityIntegration:
    """Integration layer for explainability in hiring workflow"""
    
    def __init__(self):
        self.generator = ExplainabilityGenerator()
    
    def generate_from_interview(
        self,
        interview_data: Dict[str, Any],
        include_candidate_feedback: bool = False
    ) -> Dict[str, Any]:
        """
        Generate explainability artifact from complete interview data
        
        Args:
            interview_data: Complete interview evaluation data
            include_candidate_feedback: Whether to generate candidate-friendly explanation
            
        Returns:
            Dictionary with all explainability components
        """
        
        # Extract components from interview data
        candidate_name = interview_data.get("candidate_name", "Unknown")
        overall_score = interview_data.get("overall_score", 0)
        technical_score = interview_data.get("technical_score", 0)
        experience_score = interview_data.get("experience_score", 0)
        education_score = interview_data.get("education_score", 0)
        
        skill_matches = interview_data.get("skill_analysis", {}).get("matched_skills", [])
        gaps = interview_data.get("skill_analysis", {}).get("gaps", {})
        
        reasoning = interview_data.get("reasoning", "")
        strengths = interview_data.get("strengths", "")
        areas_for_growth = interview_data.get("areas_for_growth", "")
        
        experience_level = interview_data.get("experience_level", "mid")
        learning_velocity = interview_data.get("learning_velocity", 1.0)
        
        # Generate artifact
        artifact = self.generator.generate_complete_artifact(
            candidate_name=candidate_name,
            overall_score=overall_score,
            technical_fit=technical_score,
            experience_fit=experience_score,
            education_fit=education_score,
            skill_matches=skill_matches,
            gaps=gaps,
            reasoning=reasoning,
            strengths=strengths,
            areas_for_growth=areas_for_growth,
            experience_level=experience_level,
            learning_velocity=learning_velocity,
            include_candidate_feedback=include_candidate_feedback
        )
        
        return {
            "candidate_name": candidate_name,
            "overall_score": overall_score,
            "recruiter_explanation": artifact.recruiter_explanation,
            "candidate_explanation": artifact.candidate_explanation,
            "score_rationale": artifact.score_rationale,
            "training_plan": artifact.training_plan,
            "investment_summary": artifact.investment_summary,
            "export_formats": {
                "json": self.generator.export_as_json(artifact),
                "text": self.generator.export_as_text(artifact)
            }
        }
    
    def generate_for_job_role(
        self,
        interview_data: Dict[str, Any],
        job_requirements: Dict[str, Any],
        include_candidate_feedback: bool = False
    ) -> Dict[str, Any]:
        """
        Generate explainability artifact tailored to a specific job role
        
        Args:
            interview_data: Complete interview evaluation data
            job_requirements: Job role requirements and expectations
            include_candidate_feedback: Whether to generate candidate feedback
            
        Returns:
            Artifact customized to job requirements
        """
        
        result = self.generate_from_interview(
            interview_data,
            include_candidate_feedback
        )
        
        # Add job-specific context
        result["job_role"] = job_requirements.get("title", "Unknown")
        result["job_level"] = job_requirements.get("level", "mid")
        result["required_skills"] = job_requirements.get("required_skills", [])
        result["nice_to_have_skills"] = job_requirements.get("nice_to_have", [])
        
        # Analyze fit for specific role
        fit_analysis = self._analyze_role_fit(
            interview_data,
            job_requirements
        )
        result["role_fit_analysis"] = fit_analysis
        
        return result
    
    def _analyze_role_fit(
        self,
        interview_data: Dict[str, Any],
        job_requirements: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Analyze how well candidate fits specific role"""
        
        required_skills = job_requirements.get("required_skills", [])
        nice_to_have = job_requirements.get("nice_to_have", [])
        
        matched_skills = interview_data.get("skill_analysis", {}).get("matched_skills", [])
        gaps = interview_data.get("skill_analysis", {}).get("gaps", {})
        
        matched_skill_names = [s.get("skill") for s in matched_skills if s.get("present")]
        missing = gaps.get("missing_skills", [])
        
        # Check required skills
        required_met = sum(1 for skill in required_skills if skill in matched_skill_names)
        required_missing = sum(1 for skill in required_skills if skill in missing)
        
        # Check nice-to-have
        nice_met = sum(1 for skill in nice_to_have if skill in matched_skill_names)
        nice_missing = sum(1 for skill in nice_to_have if skill in missing)
        
        # Calculate percentage
        total_required = len(required_skills) if required_skills else 1
        required_percentage = (required_met / total_required) * 100 if total_required > 0 else 0
        
        # Determine readiness
        if required_percentage >= 80 and required_missing == 0:
            readiness = "IMMEDIATE FIT - Ready to start with minimal onboarding"
        elif required_percentage >= 60:
            readiness = "TRAINABLE - Can reach full productivity with training"
        elif required_percentage >= 40:
            readiness = "POTENTIAL - Will need significant training investment"
        else:
            readiness = "GROWTH HIRE - Best for mentorship/junior role"
        
        return {
            "role_title": job_requirements.get("title", "Unknown"),
            "role_level": job_requirements.get("level", "mid"),
            "required_skills_met": f"{required_met}/{len(required_skills)}",
            "required_skills_missing": required_missing,
            "nice_to_have_met": nice_met,
            "required_percentage": f"{required_percentage:.0f}%",
            "readiness_level": readiness,
            "trainable_skills": required_missing,
            "immediate_productivity": required_percentage >= 80
        }
    
    def generate_hiring_decision_package(
        self,
        interview_data: Dict[str, Any],
        job_requirements: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Generate complete hiring decision package with all components
        
        Args:
            interview_data: Interview evaluation data
            job_requirements: Optional job role requirements
            
        Returns:
            Complete decision package
        """
        
        # Generate base explainability
        explainability = self.generate_from_interview(
            interview_data,
            include_candidate_feedback=True
        )
        
        # Add role-specific analysis if provided
        if job_requirements:
            role_analysis = self._analyze_role_fit(
                interview_data,
                job_requirements
            )
            explainability["role_fit_analysis"] = role_analysis
        
        # Add hiring decision
        overall_score = interview_data.get("overall_score", 0)
        missing_count = len(interview_data.get("skill_analysis", {}).get("gaps", {}).get("missing_skills", []))
        
        decision = self._make_hiring_decision(
            overall_score,
            missing_count,
            interview_data.get("experience_level", "mid")
        )
        explainability["hiring_decision"] = decision
        
        return explainability
    
    def _make_hiring_decision(
        self,
        score: float,
        gaps: int,
        experience_level: str
    ) -> Dict[str, Any]:
        """Make hiring decision recommendation"""
        
        if score >= 80:
            decision = "STRONG_HIRE"
            confidence = "95%"
            timeline = "1 week"
        elif score >= 70:
            decision = "HIRE_WITH_TRAINING"
            confidence = "80%"
            timeline = f"{gaps * 2} weeks"
        elif score >= 60:
            decision = "CONDITIONAL_HIRE"
            confidence = "60%"
            timeline = f"{gaps * 3} weeks"
        else:
            decision = "RECONSIDER"
            confidence = "40%"
            timeline = f"{gaps * 4} weeks"
        
        return {
            "recommendation": decision,
            "confidence": confidence,
            "time_to_productivity": timeline,
            "justification": self._get_decision_justification(decision, score, gaps)
        }
    
    def _get_decision_justification(
        self,
        decision: str,
        score: float,
        gaps: int
    ) -> str:
        """Generate decision justification"""
        
        justifications = {
            "STRONG_HIRE": f"Excellent candidate with score {score}/100. Ready for immediate impact with minimal training.",
            "HIRE_WITH_TRAINING": f"Good foundation ({score}/100) with {gaps} skill gaps. Training plan will result in productive team member.",
            "CONDITIONAL_HIRE": f"Moderate fit ({score}/100) with {gaps} gaps. Hire pending structured training and mentorship.",
            "RECONSIDER": f"Score {score}/100 indicates need for different role level or experience profile."
        }
        
        return justifications.get(decision, "Review candidate profile individually")
