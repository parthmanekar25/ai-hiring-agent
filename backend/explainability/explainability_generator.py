"""
Explainability Artifact Generator
Generates recruiter-friendly and candidate-friendly explanations with training requirements
"""

import json
from typing import Dict, Any, Optional, List
from dataclasses import dataclass
from enum import Enum


class ExplanationType(str, Enum):
    """Type of explanation to generate"""
    RECRUITER = "recruiter"  # For hiring team
    CANDIDATE = "candidate"  # For candidate feedback (optional)


@dataclass
class TrainingRequirement:
    """Training requirement for skill gaps"""
    skill: str
    estimated_hours: int
    resources: List[str]
    difficulty: str  # easy, medium, hard
    priority: str    # critical, high, medium, low


@dataclass
class ExplainabilityArtifact:
    """Complete explainability artifact with explanations and training plan"""
    recruiter_explanation: str
    candidate_explanation: Optional[str]
    score_rationale: Dict[str, str]
    training_plan: Dict[str, Any]
    investment_summary: Dict[str, Any]


class ExplainabilityGenerator:
    """Generate explainable AI artifacts for hiring decisions"""
    
    def __init__(self):
        self.skill_training_map = self._initialize_skill_map()
    
    def _initialize_skill_map(self) -> Dict[str, Dict[str, Any]]:
        """Initialize training requirements for common skills"""
        return {
            "Python": {
                "hours": 80,
                "resources": ["Codecademy", "Real Python", "LeetCode"],
                "difficulty": "medium",
                "priority": "critical"
            },
            "FastAPI": {
                "hours": 40,
                "resources": ["Official FastAPI docs", "Miguel Grinberg's courses", "Udemy FastAPI course"],
                "difficulty": "medium",
                "priority": "high"
            },
            "PostgreSQL": {
                "hours": 60,
                "resources": ["PostgreSQL official docs", "Udacity", "Pluralsight"],
                "difficulty": "medium",
                "priority": "high"
            },
            "Docker": {
                "hours": 30,
                "resources": ["Docker documentation", "Play with Docker", "Udemy Docker course"],
                "difficulty": "easy",
                "priority": "high"
            },
            "Kubernetes": {
                "hours": 100,
                "resources": ["Kubernetes official docs", "Linux Academy", "Certified Kubernetes courses"],
                "difficulty": "hard",
                "priority": "high"
            },
            "AWS": {
                "hours": 120,
                "resources": ["AWS free tier", "AWS training", "A Cloud Guru"],
                "difficulty": "hard",
                "priority": "medium"
            },
            "Machine Learning": {
                "hours": 150,
                "resources": ["Andrew Ng's ML course", "Fast.ai", "Kaggle"],
                "difficulty": "hard",
                "priority": "medium"
            },
            "React": {
                "hours": 60,
                "resources": ["React official docs", "Scrimba", "Udemy React course"],
                "difficulty": "medium",
                "priority": "medium"
            },
            "Vue": {
                "hours": 50,
                "resources": ["Vue official docs", "Vue Mastery", "Udemy Vue course"],
                "difficulty": "medium",
                "priority": "low"
            },
            "Leadership": {
                "hours": 40,
                "resources": ["Manager training programs", "Coursera Leadership", "Executive coaching"],
                "difficulty": "hard",
                "priority": "high"
            },
            "Edge Deployment": {
                "hours": 70,
                "resources": ["TensorFlow Lite docs", "Edge Impulse", "NVIDIA Jetson docs"],
                "difficulty": "hard",
                "priority": "high"
            },
            "Hybrid ML Pipelines": {
                "hours": 100,
                "resources": ["Apache Airflow docs", "Kubeflow", "ML Pipelines courses"],
                "difficulty": "hard",
                "priority": "high"
            },
            "Cloud Computing": {
                "hours": 80,
                "resources": ["AWS training", "Azure fundamentals", "GCP courses"],
                "difficulty": "hard",
                "priority": "high"
            },
            "Time-Series Analysis": {
                "hours": 60,
                "resources": ["Statsmodels docs", "Time Series courses", "Kaggle competitions"],
                "difficulty": "medium",
                "priority": "medium"
            },
            "Network Intelligence": {
                "hours": 90,
                "resources": ["Network analysis courses", "Graph neural networks", "NetworkX docs"],
                "difficulty": "hard",
                "priority": "medium"
            },
            "Large Language Models": {
                "hours": 120,
                "resources": ["OpenAI API docs", "Hugging Face tutorials", "LangChain docs"],
                "difficulty": "hard",
                "priority": "high"
            },
            "TypeScript": {
                "hours": 50,
                "resources": ["TypeScript official docs", "Udemy TypeScript", "TypeScript Deep Dive"],
                "difficulty": "medium",
                "priority": "high"
            },
            "Node.js": {
                "hours": 60,
                "resources": ["Node.js official docs", "Express.js tutorials", "Node.js courses"],
                "difficulty": "medium",
                "priority": "high"
            },
            "MongoDB": {
                "hours": 50,
                "resources": ["MongoDB university", "MongoDB docs", "Udemy MongoDB"],
                "difficulty": "medium",
                "priority": "medium"
            },
            "Redis": {
                "hours": 40,
                "resources": ["Redis official docs", "Redis University", "Pluralsight Redis"],
                "difficulty": "medium",
                "priority": "medium"
            },
        }
    
    def _get_skill_hours(self, skill: str) -> Dict[str, Any]:
        """Get training hours for a skill, with fallback for unknown skills"""
        if skill in self.skill_training_map:
            return self.skill_training_map[skill]
        
        # Fallback for unknown skills - estimate based on keyword analysis
        skill_lower = skill.lower()
        
        # Determine difficulty and hours based on keywords
        if any(keyword in skill_lower for keyword in ["ml", "ai", "machine learning", "deep", "neural", "llm"]):
            return {
                "hours": 100,
                "resources": ["Official documentation", "Online courses", "Hands-on projects"],
                "difficulty": "hard",
                "priority": "high"
            }
        elif any(keyword in skill_lower for keyword in ["cloud", "aws", "azure", "gcp", "deployment", "infrastructure"]):
            return {
                "hours": 80,
                "resources": ["Official cloud documentation", "Cloud training", "Hands-on labs"],
                "difficulty": "hard",
                "priority": "high"
            }
        elif any(keyword in skill_lower for keyword in ["frontend", "ui", "ux", "web", "react", "vue", "angular"]):
            return {
                "hours": 60,
                "resources": ["Framework documentation", "Online tutorials", "Code examples"],
                "difficulty": "medium",
                "priority": "high"
            }
        elif any(keyword in skill_lower for keyword in ["database", "sql", "nosql", "postgres", "mongo"]):
            return {
                "hours": 50,
                "resources": ["Database documentation", "SQL tutorials", "Database courses"],
                "difficulty": "medium",
                "priority": "high"
            }
        elif any(keyword in skill_lower for keyword in ["devops", "ci", "cd", "jenkins", "docker", "kubernetes"]):
            return {
                "hours": 70,
                "resources": ["DevOps documentation", "Pipeline courses", "Hands-on labs"],
                "difficulty": "hard",
                "priority": "high"
            }
        else:
            # Generic skill - estimate medium difficulty
            return {
                "hours": 40,
                "resources": ["Official documentation", "Online courses", "Practice projects"],
                "difficulty": "medium",
                "priority": "medium"
            }
    
    def generate_recruiter_explanation(
        self,
        candidate_name: str,
        overall_score: float,
        technical_fit: float,
        experience_fit: float,
        education_fit: float,
        skill_matches: List[Dict[str, Any]],
        gaps: Dict[str, Any],
        reasoning: str
    ) -> str:
        """Generate recruiter-friendly explanation"""
        
        present_skills = [s for s in skill_matches if s.get("present")]
        missing_skills = gaps.get("missing_skills", [])
        
        explanation = f"""
RECRUITER SUMMARY FOR {candidate_name.upper()}
{'='*60}

OVERALL ASSESSMENT: {overall_score}/100
{'─'*60}
{reasoning}

SCORE BREAKDOWN:
  • Technical Fit:    {technical_fit}/100 - {self._interpret_score(technical_fit)}
  • Experience Fit:   {experience_fit}/100 - {self._interpret_score(experience_fit)}
  • Education Fit:    {education_fit}/100 - {self._interpret_score(education_fit)}

STRENGTHS:
"""
        
        for skill in present_skills[:5]:  # Top 5 strengths
            confidence = skill.get("confidence", 0)
            explanation += f"  ✓ {skill.get('skill')}: {skill.get('evidence')} (Confidence: {confidence*100:.0f}%)\n"
        
        if missing_skills:
            explanation += f"\nCRITICAL GAPS ({len(missing_skills)} areas):\n"
            for gap in missing_skills:
                explanation += f"  ✗ {gap} - Can be trained (see training plan below)\n"
        
        unclear = gaps.get("unclear_sections", [])
        if unclear:
            explanation += f"\nARES FOR CLARIFICATION:\n"
            for item in unclear[:3]:
                explanation += f"  ? {item}\n"
        
        explanation += f"""

HIRING RECOMMENDATION:
{self._generate_hiring_recommendation(overall_score, missing_skills, experience_fit)}

NEXT STEPS:
  1. If score > 75: Proceed to technical interview
  2. If score 60-75: Conduct skills assessment on key gaps
  3. If score < 60: Consider for junior/entry-level roles
"""
        
        return explanation
    
    def generate_candidate_explanation(
        self,
        candidate_name: str,
        overall_score: float,
        skill_matches: List[Dict[str, Any]],
        gaps: Dict[str, Any],
        strengths: str,
        areas_for_growth: str
    ) -> str:
        """Generate candidate-friendly explanation (for feedback)"""
        
        present_skills = [s for s in skill_matches if s.get("present")]
        missing_skills = gaps.get("missing_skills", [])
        
        explanation = f"""
EVALUATION FEEDBACK FOR {candidate_name}
{'='*60}

Thank you for applying! Here's detailed feedback on your evaluation:

YOUR OVERALL SCORE: {overall_score}/100
{'─'*60}

WHAT WE LIKED:
{strengths}

YOUR KEY STRENGTHS:
"""
        
        for skill in present_skills[:5]:
            confidence = skill.get("confidence", 0)
            explanation += f"  ✓ {skill.get('skill')}: Strong demonstrated experience\n"
        
        if missing_skills:
            explanation += f"\nAREAS FOR GROWTH:\n{areas_for_growth}\n"
            
            explanation += f"\nSkills to develop:\n"
            for gap in missing_skills:
                explanation += f"  • {gap}\n"
        
        explanation += f"""

NEXT STEPS:
  • We'll follow up with you within 1-2 weeks
  • If selected, we can discuss training opportunities
  • Feel free to develop the skills mentioned above in the meantime

Best of luck! We appreciate your interest.
"""
        
        return explanation
    
    def generate_training_plan(
        self,
        gaps: Dict[str, Any],
        experience_level: str = "mid",
        learning_velocity: float = 1.0
    ) -> Dict[str, Any]:
        """Generate training plan with time and resource estimates"""
        
        missing_skills = gaps.get("missing_skills", [])
        training_requirements = []
        
        total_hours = 0
        total_cost_estimate = 0
        
        for skill in missing_skills:
            # Use fallback function that handles unknown skills
            skill_info = self._get_skill_hours(skill)
            
            # Adjust hours based on learning velocity
            adjusted_hours = int(skill_info["hours"] / learning_velocity)
            
            training_requirements.append({
                "skill": skill,
                "estimated_hours": adjusted_hours,
                "resources": skill_info["resources"],
                "difficulty": skill_info["difficulty"],
                "priority": skill_info["priority"],
                "estimated_weeks": int(adjusted_hours / 10),  # Assuming 10 hrs/week
                "estimated_cost": self._estimate_cost(skill_info, adjusted_hours)
            })
            
            total_hours += adjusted_hours
            total_cost_estimate += self._estimate_cost(skill_info, adjusted_hours)
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        training_requirements.sort(key=lambda x: priority_order.get(x["priority"], 4))
        
        return {
            "training_requirements": training_requirements,
            "summary": {
                "total_skills_to_develop": len(training_requirements),
                "total_estimated_hours": total_hours,
                "total_estimated_weeks": int(total_hours / 10),  # 10 hrs/week
                "estimated_cost_range": f"${total_cost_estimate * 0.5:.0f} - ${total_cost_estimate:.0f}",
                "recommended_pace": "Part-time (10 hrs/week) or Full-time intensive (40 hrs/week)"
            }
        }
    
    def generate_investment_summary(
        self,
        overall_score: float,
        training_plan: Dict[str, Any],
        experience_fit: float,
        technical_fit: float
    ) -> Dict[str, Any]:
        """Generate investment summary with ROI analysis"""
        
        training_summary = training_plan.get("summary", {})
        total_hours = training_summary.get("total_estimated_hours", 0)
        total_weeks = training_summary.get("total_estimated_weeks", 0)
        
        # Calculate ROI (productivity vs training investment)
        if total_hours > 0:
            ramp_up_weeks = max(2, int(total_weeks / 2))  # Ramp up time
            productivity_impact = (100 - overall_score) / 100  # Lower score = more training needed
            roi_weeks = int(ramp_up_weeks + total_weeks)
        else:
            roi_weeks = 2
            productivity_impact = 0
        
        investment_level = self._calculate_investment_level(
            overall_score,
            total_hours,
            technical_fit
        )
        
        return {
            "investment_level": investment_level,
            "breakdown": {
                "training_hours": total_hours,
                "training_weeks": total_weeks,
                "ramp_up_weeks": max(2, int(total_weeks / 2)),
                "time_to_productivity": f"{roi_weeks} weeks",
                "mentor_hours_needed": int(total_hours * 0.3),  # 30% mentoring
                "team_support_hours": int(total_hours * 0.2),  # 20% team support
            },
            "resources_required": {
                "training_budget": training_summary.get("estimated_cost_range", "$0"),
                "mentorship": "Recommended" if total_hours > 100 else "Optional",
                "tools_and_subscriptions": self._get_recommended_subscriptions(training_plan),
                "team_time": f"~{int(total_hours * 0.2)} hours for onboarding/mentoring"
            },
            "roi_analysis": {
                "break_even_point": f"{roi_weeks} weeks",
                "productivity_by_month": {
                    "month_1": f"{max(0, 30 - productivity_impact*100):.0f}%",
                    "month_3": f"{max(0, 70 - productivity_impact*50):.0f}%",
                    "month_6": f"{min(100, 90 + productivity_impact*20):.0f}%"
                },
                "recommendation": self._get_investment_recommendation(investment_level)
            }
        }
    
    def generate_complete_artifact(
        self,
        candidate_name: str,
        overall_score: float,
        technical_fit: float,
        experience_fit: float,
        education_fit: float,
        skill_matches: List[Dict[str, Any]],
        gaps: Dict[str, Any],
        reasoning: str,
        strengths: str,
        areas_for_growth: str,
        experience_level: str = "mid",
        learning_velocity: float = 1.0,
        include_candidate_feedback: bool = False
    ) -> ExplainabilityArtifact:
        """Generate complete explainability artifact"""
        
        recruiter_exp = self.generate_recruiter_explanation(
            candidate_name,
            overall_score,
            technical_fit,
            experience_fit,
            education_fit,
            skill_matches,
            gaps,
            reasoning
        )
        
        candidate_exp = None
        if include_candidate_feedback:
            candidate_exp = self.generate_candidate_explanation(
                candidate_name,
                overall_score,
                skill_matches,
                gaps,
                strengths,
                areas_for_growth
            )
        
        training_plan = self.generate_training_plan(
            gaps,
            experience_level,
            learning_velocity
        )
        
        investment = self.generate_investment_summary(
            overall_score,
            training_plan,
            experience_fit,
            technical_fit
        )
        
        score_rationale = {
            "technical_fit": f"{technical_fit}/100 - {self._interpret_score(technical_fit)}",
            "experience_fit": f"{experience_fit}/100 - {self._interpret_score(experience_fit)}",
            "education_fit": f"{education_fit}/100 - {self._interpret_score(education_fit)}",
            "overall_fit": f"{overall_score}/100"
        }
        
        return ExplainabilityArtifact(
            recruiter_explanation=recruiter_exp,
            candidate_explanation=candidate_exp,
            score_rationale=score_rationale,
            training_plan=training_plan,
            investment_summary=investment
        )
    
    # Helper methods
    
    def _interpret_score(self, score: float) -> str:
        """Interpret score as text"""
        if score >= 90:
            return "Excellent fit"
        elif score >= 75:
            return "Strong fit"
        elif score >= 60:
            return "Moderate fit"
        elif score >= 45:
            return "Basic fit"
        else:
            return "Needs development"
    
    def _generate_hiring_recommendation(
        self,
        score: float,
        missing_skills: List[str],
        experience_fit: float
    ) -> str:
        """Generate hiring recommendation"""
        
        if score >= 80:
            return "🟢 STRONG RECOMMEND - Ready for immediate onboarding with minimal training"
        elif score >= 70:
            return "🟡 RECOMMEND WITH TRAINING - Good foundation, invest in skill development"
        elif score >= 60:
            return "🟡 CONSIDER - Viable for mid-level role with structured training plan"
        elif score >= 50:
            return "🔴 JUNIOR/ENTRY-LEVEL - Consider for entry position with mentorship"
        else:
            return "🔴 NOT RECOMMENDED - Better fit for alternative roles or experience levels"
    
    def _estimate_cost(self, skill_info: Dict[str, Any], hours: int) -> float:
        """Estimate training cost for a skill"""
        # Base costs per hour for different difficulties
        cost_per_hour = {
            "easy": 5,
            "medium": 10,
            "hard": 15
        }
        
        difficulty = skill_info.get("difficulty", "medium")
        return hours * cost_per_hour.get(difficulty, 10)
    
    def _calculate_investment_level(
        self,
        score: float,
        hours: int,
        technical_fit: float
    ) -> str:
        """Calculate investment level"""
        
        if score >= 80 or hours <= 30:
            return "LOW"
        elif score >= 60 and hours <= 80:
            return "MEDIUM"
        elif score >= 50 and hours <= 150:
            return "HIGH"
        else:
            return "VERY_HIGH"
    
    def _get_recommended_subscriptions(self, training_plan: Dict[str, Any]) -> List[str]:
        """Get recommended training subscriptions"""
        
        subscriptions = set()
        requirements = training_plan.get("training_requirements", [])
        
        for req in requirements:
            resources = req.get("resources", [])
            
            # Map resources to subscriptions
            for resource in resources:
                if "Udemy" in resource or "Coursera" in resource or "Pluralsight" in resource:
                    subscriptions.add("Online Learning Platform ($10-30/month)")
                if "Kaggle" in resource or "Fast.ai" in resource:
                    subscriptions.add("Kaggle/Fast.ai (Free)")
                if "official docs" in resource.lower():
                    subscriptions.add("Official Documentation (Free)")
        
        return list(subscriptions) if subscriptions else ["None required"]
    
    def _get_investment_recommendation(self, investment_level: str) -> str:
        """Get investment recommendation"""
        
        recommendations = {
            "LOW": "Excellent candidate - minimal training needed, quick ROI",
            "MEDIUM": "Good investment - structured training will yield productive team member",
            "HIGH": "Significant investment - requires dedicated training program and mentorship",
            "VERY_HIGH": "Major investment - only pursue if strategic hiring goal or strong cultural fit"
        }
        
        return recommendations.get(investment_level, "Evaluate case-by-case")
    
    def export_as_json(self, artifact: ExplainabilityArtifact) -> str:
        """Export artifact as JSON"""
        
        return json.dumps({
            "recruiter_explanation": artifact.recruiter_explanation,
            "candidate_explanation": artifact.candidate_explanation,
            "score_rationale": artifact.score_rationale,
            "training_plan": artifact.training_plan,
            "investment_summary": artifact.investment_summary
        }, indent=2)
    
    def export_as_text(self, artifact: ExplainabilityArtifact) -> str:
        """Export artifact as readable text"""
        
        text = artifact.recruiter_explanation + "\n"
        
        if artifact.candidate_explanation:
            text += "\n" + "="*60 + "\n"
            text += artifact.candidate_explanation + "\n"
        
        text += "\n" + "="*60 + "\n"
        text += "TRAINING PLAN AND INVESTMENT ANALYSIS\n"
        text += "="*60 + "\n"
        
        text += f"\nTRAINING REQUIREMENTS:\n"
        for req in artifact.training_plan.get("training_requirements", []):
            text += f"\n  {req['skill']} ({req['difficulty'].upper()}) - PRIORITY: {req['priority'].upper()}\n"
            text += f"    • Estimated Time: {req['estimated_hours']} hours (~{req['estimated_weeks']} weeks)\n"
            text += f"    • Resources: {', '.join(req['resources'][:2])}\n"
            text += f"    • Cost: ${req['estimated_cost']:.0f}\n"
        
        text += f"\n\nSUMMARY:\n"
        summary = artifact.training_plan.get("summary", {})
        text += f"  • Total Skills to Develop: {summary.get('total_skills_to_develop')}\n"
        text += f"  • Total Training Hours: {summary.get('total_estimated_hours')}\n"
        text += f"  • Timeline: {summary.get('total_estimated_weeks')} weeks (10 hrs/week)\n"
        text += f"  • Cost Range: {summary.get('estimated_cost_range')}\n"
        
        text += f"\n\nINVESTMENT ANALYSIS:\n"
        investment = artifact.investment_summary
        text += f"  • Investment Level: {investment.get('investment_level')}\n"
        text += f"  • Break-even Point: {investment.get('roi_analysis', {}).get('break_even_point')}\n"
        text += f"  • Recommendation: {investment.get('roi_analysis', {}).get('recommendation')}\n"
        
        return text
