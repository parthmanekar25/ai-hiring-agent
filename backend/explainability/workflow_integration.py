"""
Explainability Integration Example
Shows how to integrate explainability into the main hiring workflow
"""

from backend.explainability import ExplainabilityIntegration
from typing import Dict, Any


class EnhancedHiringWorkflow:
    """Enhanced hiring workflow with explainability artifacts"""
    
    def __init__(self):
        self.explainability = ExplainabilityIntegration()
    
    def evaluate_candidate_with_explanation(
        self,
        interview_results: Dict[str, Any],
        job_requirements: Dict[str, Any] = None,
        include_candidate_feedback: bool = False
    ) -> Dict[str, Any]:
        """
        Evaluate candidate and generate comprehensive explainability artifact
        
        Typical workflow:
        1. Run scoring agent on interview
        2. Get interview_results with scores
        3. Call this function
        4. Returns complete artifact with explanations
        """
        
        # Generate complete hiring decision package
        package = self.explainability.generate_hiring_decision_package(
            interview_results,
            job_requirements
        )
        
        return {
            "evaluation_summary": {
                "candidate": interview_results.get("candidate_name"),
                "score": interview_results.get("overall_score"),
                "hiring_decision": package.get("hiring_decision")
            },
            "for_recruiters": {
                "explanation": package.get("recruiter_explanation"),
                "role_fit_analysis": package.get("role_fit_analysis"),
                "hiring_decision": package.get("hiring_decision")
            },
            "for_candidates": {
                "explanation": package.get("candidate_explanation")
            } if include_candidate_feedback else None,
            "training_investment": {
                "plan": package.get("training_plan"),
                "investment_summary": package.get("investment_summary")
            },
            "export_formats": {
                "json": package.get("export_formats", {}).get("json"),
                "text": package.get("export_formats", {}).get("text")
            }
        }
    
    def generate_recruiter_report(
        self,
        interview_results: Dict[str, Any],
        job_requirements: Dict[str, Any] = None
    ) -> str:
        """Generate detailed recruiter report"""
        
        package = self.explainability.generate_hiring_decision_package(
            interview_results,
            job_requirements
        )
        
        report = f"""
{'='*80}
HIRING EVALUATION REPORT
{'='*80}

CANDIDATE: {interview_results.get('candidate_name', 'Unknown')}
OVERALL SCORE: {interview_results.get('overall_score', 0)}/100

{'─'*80}
HIRING DECISION
{'─'*80}

Decision: {package.get('hiring_decision', {}).get('recommendation')}
Confidence: {package.get('hiring_decision', {}).get('confidence')}
Time to Productivity: {package.get('hiring_decision', {}).get('time_to_productivity')}
Justification: {package.get('hiring_decision', {}).get('justification')}

{'─'*80}
EVALUATION DETAILS
{'─'*80}

{package.get('recruiter_explanation', '')}

{'─'*80}
TRAINING & INVESTMENT
{'─'*80}

Training Requirements:
{self._format_training_requirements(package.get('training_plan', {}))}

Investment Analysis:
{self._format_investment(package.get('investment_summary', {}))}

{'='*80}
END OF REPORT
{'='*80}
"""
        
        return report
    
    def generate_candidate_feedback(
        self,
        interview_results: Dict[str, Any],
        job_requirements: Dict[str, Any] = None
    ) -> str:
        """Generate candidate feedback email"""
        
        package = self.explainability.generate_hiring_decision_package(
            interview_results,
            job_requirements
        )
        
        feedback = f"""
Dear {interview_results.get('candidate_name', 'Candidate')},

Thank you for your interest in {job_requirements.get('title', 'our company') if job_requirements else 'our company'}!

We've completed our evaluation of your application and interview. Here's your feedback:

{package.get('candidate_explanation', '')}

We appreciate your application and wish you the best in your career!

Best regards,
The Hiring Team
"""
        
        return feedback
    
    def _format_training_requirements(self, training_plan: Dict[str, Any]) -> str:
        """Format training requirements for report"""
        
        requirements = training_plan.get("training_requirements", [])
        if not requirements:
            return "  • No additional training required"
        
        formatted = ""
        for req in requirements:
            formatted += f"""
  • {req['skill']} ({req['difficulty'].upper()})
    - Time: {req['estimated_hours']} hours (~{req['estimated_weeks']} weeks)
    - Priority: {req['priority'].upper()}
    - Resources: {', '.join(req['resources'][:2])}
    - Cost: ${req['estimated_cost']:.0f}
"""
        
        summary = training_plan.get("summary", {})
        formatted += f"""
  TOTAL:
    - Skills to develop: {summary.get('total_skills_to_develop')}
    - Hours: {summary.get('total_estimated_hours')}
    - Timeline: {summary.get('total_estimated_weeks')} weeks
    - Budget: {summary.get('estimated_cost_range')}
"""
        
        return formatted
    
    def _format_investment(self, investment_summary: Dict[str, Any]) -> str:
        """Format investment analysis for report"""
        
        breakdown = investment_summary.get("breakdown", {})
        roi = investment_summary.get("roi_analysis", {})
        
        formatted = f"""
  Investment Level: {investment_summary.get('investment_level')}
  
  Breakdown:
    - Training hours: {breakdown.get('training_hours')}
    - Ramp-up weeks: {breakdown.get('ramp_up_weeks')}
    - Mentor hours needed: {breakdown.get('mentor_hours_needed')}
    - Team support hours: {breakdown.get('team_support_hours')}
  
  ROI Analysis:
    - Break-even point: {roi.get('break_even_point')}
    - Month 1 productivity: {roi.get('productivity_by_month', {}).get('month_1')}
    - Month 3 productivity: {roi.get('productivity_by_month', {}).get('month_3')}
    - Month 6 productivity: {roi.get('productivity_by_month', {}).get('month_6')}
  
  Recommendation: {roi.get('recommendation')}
"""
        
        return formatted


# ============================================================================
# Example Usage
# ============================================================================

def example_usage():
    """Example of how to use enhanced workflow"""
    
    workflow = EnhancedHiringWorkflow()
    
    # Simulated interview results from scoring agent
    interview_results = {
        "candidate_name": "John Doe",
        "overall_score": 78,
        "technical_score": 82,
        "experience_score": 76,
        "education_score": 72,
        "skill_analysis": {
            "matched_skills": [
                {"skill": "Python", "present": True, "confidence": 0.90},
                {"skill": "FastAPI", "present": True, "confidence": 0.85},
                {"skill": "PostgreSQL", "present": True, "confidence": 0.88},
                {"skill": "Docker", "present": False}
            ],
            "gaps": {
                "missing_skills": ["Docker", "Kubernetes"],
                "unclear_sections": []
            }
        },
        "reasoning": "Strong backend engineer with solid experience",
        "strengths": "Excellent technical skills",
        "areas_for_growth": "Container technologies",
        "experience_level": "senior",
        "learning_velocity": 1.1
    }
    
    job_requirements = {
        "title": "Senior Backend Engineer",
        "level": "senior",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "nice_to_have": ["Kubernetes"]
    }
    
    # Generate evaluation with explanation
    result = workflow.evaluate_candidate_with_explanation(
        interview_results,
        job_requirements,
        include_candidate_feedback=True
    )
    
    print("EVALUATION SUMMARY:")
    print(f"  Candidate: {result['evaluation_summary']['candidate']}")
    print(f"  Score: {result['evaluation_summary']['score']}/100")
    print(f"  Decision: {result['evaluation_summary']['hiring_decision']['recommendation']}")
    
    # Generate recruiter report
    recruiter_report = workflow.generate_recruiter_report(
        interview_results,
        job_requirements
    )
    print("\n" + recruiter_report)
    
    # Generate candidate feedback
    candidate_feedback = workflow.generate_candidate_feedback(
        interview_results,
        job_requirements
    )
    print("\nCANDIDATE FEEDBACK EMAIL:")
    print(candidate_feedback)


if __name__ == "__main__":
    example_usage()
