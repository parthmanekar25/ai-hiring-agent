"""
Test Explainability Generator
Demonstrates recruiter and candidate-friendly explanations with training plans
"""

import json
from backend.explainability import (
    ExplainabilityGenerator,
    ExplainabilityIntegration
)


def test_explainability_generator():
    """Test basic explainability generator"""
    
    print("="*80)
    print("TESTING EXPLAINABILITY GENERATOR")
    print("="*80)
    
    generator = ExplainabilityGenerator()
    
    # Sample interview data - candidate with some gaps
    candidate_data = {
        "candidate_name": "Alice Johnson",
        "overall_score": 72,
        "technical_score": 75,
        "experience_score": 68,
        "education_score": 70,
        "skill_analysis": {
            "matched_skills": [
                {
                    "skill": "Python",
                    "present": True,
                    "confidence": 0.95,
                    "evidence": "5+ years production experience"
                },
                {
                    "skill": "FastAPI",
                    "present": True,
                    "confidence": 0.85,
                    "evidence": "2 major projects built"
                },
                {
                    "skill": "PostgreSQL",
                    "present": True,
                    "confidence": 0.80,
                    "evidence": "Strong SQL knowledge demonstrated"
                },
                {
                    "skill": "Docker",
                    "present": False,
                    "confidence": 0
                }
            ],
            "gaps": {
                "missing_skills": ["Docker", "Kubernetes", "AWS"],
                "unclear_sections": ["Experience with microservices", "AWS deployment experience"]
            }
        },
        "reasoning": "Score reduced by 12 points due to missing Docker and Kubernetes experience; however, growth potential remains high based on learning velocity indicators and strong Python foundation.",
        "strengths": "Strong Python developer with solid FastAPI experience. Good problem-solving skills and ability to learn quickly.",
        "areas_for_growth": "Needs hands-on experience with containerization and cloud deployment technologies.",
        "experience_level": "mid",
        "learning_velocity": 1.2
    }
    
    # Generate complete artifact
    artifact = generator.generate_complete_artifact(
        candidate_name=candidate_data["candidate_name"],
        overall_score=candidate_data["overall_score"],
        technical_fit=candidate_data["technical_score"],
        experience_fit=candidate_data["experience_score"],
        education_fit=candidate_data["education_score"],
        skill_matches=candidate_data["skill_analysis"]["matched_skills"],
        gaps=candidate_data["skill_analysis"]["gaps"],
        reasoning=candidate_data["reasoning"],
        strengths=candidate_data["strengths"],
        areas_for_growth=candidate_data["areas_for_growth"],
        experience_level=candidate_data["experience_level"],
        learning_velocity=candidate_data["learning_velocity"],
        include_candidate_feedback=True
    )
    
    # Print recruiter explanation
    print("\n📋 RECRUITER EXPLANATION:\n")
    print(artifact.recruiter_explanation)
    
    # Print candidate explanation
    if artifact.candidate_explanation:
        print("\n" + "="*80)
        print("💬 CANDIDATE FEEDBACK:\n")
        print(artifact.candidate_explanation)
    
    # Print training plan
    print("\n" + "="*80)
    print("📚 TRAINING PLAN:\n")
    
    for req in artifact.training_plan["training_requirements"]:
        print(f"\n{req['skill'].upper()} ({req['difficulty'].upper()}) - {req['priority'].upper()} PRIORITY")
        print(f"  ├─ Time: {req['estimated_hours']} hours (~{req['estimated_weeks']} weeks)")
        print(f"  ├─ Resources: {', '.join(req['resources'][:2])}")
        print(f"  └─ Cost: ${req['estimated_cost']:.0f}")
    
    summary = artifact.training_plan["summary"]
    print(f"\n{'─'*80}")
    print(f"SUMMARY:")
    print(f"  • Total skills to develop: {summary['total_skills_to_develop']}")
    print(f"  • Total training hours: {summary['total_estimated_hours']}")
    print(f"  • Timeline: {summary['total_estimated_weeks']} weeks")
    print(f"  • Cost range: {summary['estimated_cost_range']}")
    
    # Print investment analysis
    print("\n" + "="*80)
    print("💼 INVESTMENT ANALYSIS:\n")
    
    investment = artifact.investment_summary
    print(f"Investment Level: {investment['investment_level']}")
    print(f"Training Hours: {investment['breakdown']['training_hours']}")
    print(f"Ramp-up Time: {investment['breakdown']['ramp_up_weeks']} weeks")
    print(f"Mentorship Required: {investment['resources_required']['mentorship']}")
    print(f"Mentor Hours: {investment['breakdown']['mentor_hours_needed']} hours")
    print(f"Team Support: {investment['breakdown']['team_support_hours']} hours")
    
    print(f"\nROI Analysis:")
    print(f"  • Break-even: {investment['roi_analysis']['break_even_point']}")
    print(f"  • Month 1: {investment['roi_analysis']['productivity_by_month']['month_1']}")
    print(f"  • Month 3: {investment['roi_analysis']['productivity_by_month']['month_3']}")
    print(f"  • Month 6: {investment['roi_analysis']['productivity_by_month']['month_6']}")
    print(f"  • Recommendation: {investment['roi_analysis']['recommendation']}")


def test_integration_with_job_role():
    """Test integration with specific job role"""
    
    print("\n" + "="*80)
    print("TESTING INTEGRATION WITH JOB ROLE")
    print("="*80)
    
    integration = ExplainabilityIntegration()
    
    interview_data = {
        "candidate_name": "Bob Smith",
        "overall_score": 78,
        "technical_score": 82,
        "experience_score": 76,
        "education_score": 75,
        "skill_analysis": {
            "matched_skills": [
                {"skill": "Python", "present": True, "confidence": 0.90},
                {"skill": "FastAPI", "present": True, "confidence": 0.85},
                {"skill": "PostgreSQL", "present": True, "confidence": 0.88},
                {"skill": "Docker", "present": True, "confidence": 0.70},
                {"skill": "React", "present": False}
            ],
            "gaps": {
                "missing_skills": ["Kubernetes", "AWS"],
                "unclear_sections": []
            }
        },
        "reasoning": "Strong backend developer with good deployment experience.",
        "strengths": "Excellent technical skills and leadership potential.",
        "areas_for_growth": "Cloud and orchestration technologies.",
        "experience_level": "senior",
        "learning_velocity": 1.0
    }
    
    job_requirements = {
        "title": "Senior Backend Engineer",
        "level": "senior",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "nice_to_have": ["Kubernetes", "AWS", "Redis"]
    }
    
    result = integration.generate_for_job_role(
        interview_data,
        job_requirements,
        include_candidate_feedback=True
    )
    
    print(f"\n🎯 ROLE: {result['job_role']} ({result['job_level'].upper()})")
    print(f"Required Skills: {', '.join(job_requirements['required_skills'])}")
    
    print("\n📊 ROLE FIT ANALYSIS:")
    fit = result["role_fit_analysis"]
    print(f"  • Required Skills Met: {fit['required_skills_met']}")
    print(f"  • Coverage: {fit['required_percentage']}")
    print(f"  • Readiness: {fit['readiness_level']}")
    print(f"  • Immediate Productivity: {'✓' if fit['immediate_productivity'] else '✗'}")


def test_hiring_decision_package():
    """Test complete hiring decision package"""
    
    print("\n" + "="*80)
    print("TESTING HIRING DECISION PACKAGE")
    print("="*80)
    
    integration = ExplainabilityIntegration()
    
    interview_data = {
        "candidate_name": "Carol Davis",
        "overall_score": 85,
        "technical_score": 88,
        "experience_score": 83,
        "education_score": 80,
        "skill_analysis": {
            "matched_skills": [
                {"skill": "Python", "present": True, "confidence": 0.95},
                {"skill": "FastAPI", "present": True, "confidence": 0.92},
                {"skill": "PostgreSQL", "present": True, "confidence": 0.90},
                {"skill": "Docker", "present": True, "confidence": 0.85}
            ],
            "gaps": {
                "missing_skills": ["Kubernetes"],
                "unclear_sections": []
            }
        },
        "reasoning": "Excellent technical fit with strong production experience across all required areas.",
        "strengths": "Outstanding technical skills, proven ability to deliver complex projects.",
        "areas_for_growth": "Orchestration tools are the only minor gap.",
        "experience_level": "senior",
        "learning_velocity": 1.3
    }
    
    job_requirements = {
        "title": "Staff Backend Engineer",
        "level": "senior",
        "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
        "nice_to_have": ["Kubernetes"]
    }
    
    package = integration.generate_hiring_decision_package(
        interview_data,
        job_requirements
    )
    
    print(f"\n🎯 CANDIDATE: {package['candidate_name']}")
    print(f"📊 OVERALL SCORE: {package['overall_score']}/100")
    
    hiring_decision = package["hiring_decision"]
    print(f"\n{'='*80}")
    print(f"🚀 HIRING DECISION: {hiring_decision['recommendation']}")
    print(f"   Confidence: {hiring_decision['confidence']}")
    print(f"   Time to Productivity: {hiring_decision['time_to_productivity']}")
    print(f"   Justification: {hiring_decision['justification']}")


if __name__ == "__main__":
    test_explainability_generator()
    test_integration_with_job_role()
    test_hiring_decision_package()
    
    print("\n" + "="*80)
    print("✅ ALL TESTS COMPLETED")
    print("="*80)
