"""
Explainability Display Components
UI components for displaying explainability artifacts in Streamlit
"""

import streamlit as st
import json
from typing import Dict, Any, Optional
import requests
import os
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")


class ExplainabilityService:
    """Service for calling explainability API endpoints"""
    
    def __init__(self, base_url: str = BACKEND_URL):
        self.base_url = base_url
        self.timeout = 60
    
    def generate_explainability(self, interview_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate basic explainability artifact"""
        try:
            response = requests.post(
                f"{self.base_url}/api/v1/explainability/generate",
                json=interview_data,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def generate_hiring_decision(
        self,
        interview_data: Dict[str, Any],
        job_requirements: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """Generate complete hiring decision package"""
        try:
            payload = {"interview_request": interview_data}
            if job_requirements:
                payload["job_requirements"] = job_requirements
            
            response = requests.post(
                f"{self.base_url}/api/v1/explainability/generate/hiring-decision",
                json=payload,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_training_resources(self, skill: str) -> Dict[str, Any]:
        """Get training resources for a specific skill"""
        try:
            response = requests.get(
                f"{self.base_url}/api/v1/explainability/training-resources/{skill}",
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {"success": True, "data": response.json()}
            else:
                return {"success": False, "error": response.text}
        except Exception as e:
            return {"success": False, "error": str(e)}


# Singleton instance
explainability_service = ExplainabilityService()


def display_hiring_decision(decision: Dict[str, Any]):
    """Display hiring decision prominently"""
    
    recommendation = decision.get("recommendation", "UNKNOWN")
    confidence = decision.get("confidence", "N/A")
    time_to_productivity = decision.get("time_to_productivity", "N/A")
    justification = decision.get("justification", "")
    
    # Determine color based on recommendation
    if "STRONG" in recommendation:
        color = "🟢"
        bg_color = "#d4edda"
        border_color = "#28a745"
    elif "WITH_TRAINING" in recommendation:
        color = "🟡"
        bg_color = "#fff3cd"
        border_color = "#ffc107"
    elif "CONDITIONAL" in recommendation:
        color = "⚠️"
        bg_color = "#ffe5cc"
        border_color = "#ff9800"
    else:  # RECONSIDER
        color = "🔴"
        bg_color = "#f8d7da"
        border_color = "#dc3545"
    
    # Display decision card
    st.markdown(f"""
    <div style="
        background-color: {bg_color};
        border-left: 5px solid {border_color};
        padding: 1.5rem;
        border-radius: 8px;
        margin: 1rem 0;
    ">
        <h3>{color} {recommendation.replace('_', ' ')}</h3>
        <p><strong>Confidence:</strong> {confidence}</p>
        <p><strong>Time to Productivity:</strong> {time_to_productivity}</p>
        <p><strong>Justification:</strong> {justification}</p>
    </div>
    """, unsafe_allow_html=True)


def display_recruiter_explanation(explanation: str):
    """Display recruiter explanation with formatting"""
    
    with st.expander("📋 Recruiter Analysis", expanded=True):
        # Parse and format the explanation
        st.text(explanation)


def display_candidate_feedback(feedback: Optional[str]):
    """Display candidate-friendly feedback"""
    
    if not feedback:
        return
    
    with st.expander("💬 Candidate Feedback (Optional)", expanded=False):
        st.info("This feedback can be shared with the candidate for transparency and growth opportunities.")
        st.text(feedback)


def display_training_plan(training_plan: Dict[str, Any]):
    """Display training plan with timeline and resources"""
    
    with st.expander("📚 Training Plan & Development Path", expanded=True):
        requirements = training_plan.get("training_requirements", [])
        summary = training_plan.get("summary", {})
        
        if not requirements:
            st.info("✅ No additional training required for this candidate!")
            return
        
        # Summary metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Skills to Develop", summary.get("total_skills_to_develop", 0))
        with col2:
            st.metric("Total Hours", summary.get("total_estimated_hours", 0))
        with col3:
            st.metric("Timeline", f"{summary.get('total_estimated_weeks', 0)} weeks")
        with col4:
            st.metric("Budget", summary.get("estimated_cost_range", "N/A"))
        
        st.markdown("---")
        
        # Sort by priority
        priority_order = {"critical": 0, "high": 1, "medium": 2, "low": 3}
        sorted_requirements = sorted(
            requirements,
            key=lambda x: priority_order.get(x.get("priority", "medium"), 4)
        )
        
        # Display each training requirement
        for i, req in enumerate(sorted_requirements, 1):
            skill = req.get("skill", "Unknown")
            hours = req.get("estimated_hours", 0)
            weeks = req.get("estimated_weeks", 0)
            difficulty = req.get("difficulty", "medium").upper()
            priority = req.get("priority", "medium").upper()
            cost = req.get("estimated_cost", 0)
            resources = req.get("resources", [])
            
            # Color code by difficulty
            if difficulty == "EASY":
                difficulty_color = "🟢"
            elif difficulty == "MEDIUM":
                difficulty_color = "🟡"
            else:
                difficulty_color = "🔴"
            
            with st.container():
                col1, col2 = st.columns([3, 1])
                
                with col1:
                    st.markdown(f"""
                    **{i}. {skill}** {difficulty_color} {difficulty} | {priority} PRIORITY
                    """)
                    
                    # Metrics for this skill
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                    with metric_col1:
                        st.caption(f"⏱️ {hours} hours")
                    with metric_col2:
                        st.caption(f"📅 ~{weeks} weeks")
                    with metric_col3:
                        st.caption(f"💰 ${cost:.0f}")
                    with metric_col4:
                        st.caption(f"📚 {len(resources)} resources")
                    
                    # Resources
                    if resources:
                        with st.expander(f"Resources for {skill}", expanded=False):
                            for idx, resource in enumerate(resources, 1):
                                st.write(f"{idx}. {resource}")
                
                with col2:
                    # Visual progress bar representation
                    max_hours = max([r.get("estimated_hours", 0) for r in requirements])
                    if max_hours > 0:
                        bar_width = (hours / max_hours) * 100
                        st.progress(bar_width / 100)
                
                st.markdown("---")
        
        # Recommended pace
        st.info(f"📌 **Recommended Pace:** {summary.get('recommended_pace', 'N/A')}")


def display_investment_analysis(investment: Dict[str, Any]):
    """Display investment analysis and ROI"""
    
    with st.expander("💼 Investment Analysis & ROI", expanded=True):
        breakdown = investment.get("breakdown", {})
        resources = investment.get("resources_required", {})
        roi = investment.get("roi_analysis", {})
        
        # Key metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Training Hours", breakdown.get("training_hours", 0))
        with col2:
            st.metric("Ramp-up Weeks", breakdown.get("ramp_up_weeks", 0))
        with col3:
            st.metric("Time to Productivity", breakdown.get("time_to_productivity", "N/A"))
        with col4:
            st.metric("Mentor Hours", breakdown.get("mentor_hours_needed", 0))
        
        st.markdown("---")
        
        # Resource requirements
        st.subheader("📋 Resource Requirements")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.write("**Training Budget**")
            st.write(resources.get("training_budget", "N/A"))
        
        with col2:
            st.write("**Mentorship**")
            st.write(resources.get("mentorship", "N/A"))
        
        with col3:
            st.write("**Team Support**")
            st.write(resources.get("team_time", "N/A"))
        
        # Subscriptions/Tools
        if resources.get("tools_and_subscriptions"):
            st.write("**Tools & Subscriptions**")
            for tool in resources.get("tools_and_subscriptions", []):
                st.write(f"• {tool}")
        
        st.markdown("---")
        
        # ROI Analysis
        st.subheader("📈 ROI Analysis")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.write("**Break-even Point**")
            st.write(roi.get("break_even_point", "N/A"))
        
        with col2:
            st.write("**Recommendation**")
            st.write(roi.get("recommendation", "N/A"))
        
        # Productivity projections
        st.write("**Productivity Projections**")
        productivity = roi.get("productivity_by_month", {})
        
        proj_col1, proj_col2, proj_col3 = st.columns(3)
        with proj_col1:
            st.metric("Month 1", productivity.get("month_1", "N/A"))
        with proj_col2:
            st.metric("Month 3", productivity.get("month_3", "N/A"))
        with proj_col3:
            st.metric("Month 6", productivity.get("month_6", "N/A"))


def display_role_fit_analysis(role_fit: Dict[str, Any]):
    """Display role-specific fit analysis"""
    
    if not role_fit:
        return
    
    with st.expander("🎯 Role-Specific Fit Analysis", expanded=True):
        role_title = role_fit.get("role_title", "Unknown")
        required_met = role_fit.get("required_skills_met", "0/0")
        percentage = role_fit.get("required_percentage", 0)
        readiness = role_fit.get("readiness_level", "Unknown")
        
        st.markdown(f"### {role_title}")
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Required Skills Met", required_met)
        with col2:
            st.metric("Coverage", f"{percentage:.0f}%")
        with col3:
            st.metric("Trainable Skills", role_fit.get("trainable_skills", 0))
        with col4:
            immediate = "✅" if role_fit.get("immediate_productivity") else "🔲"
            st.metric("Immediate Productivity", immediate)
        
        st.info(f"**Readiness Level:** {readiness}")


def display_score_rationale(rationale: Dict[str, str]):
    """Display score breakdown and rationale"""
    
    with st.expander("📊 Score Breakdown", expanded=False):
        for component, explanation in rationale.items():
            st.write(f"**{component.replace('_', ' ').title()}:** {explanation}")


def export_explainability_report(
    candidate_name: str,
    explainability: Dict[str, Any],
    format: str = "json"
) -> Any:
    """Export explainability report in various formats"""
    
    if format == "json":
        return json.dumps(explainability, indent=2)
    
    elif format == "text":
        text = f"""
HIRING EVALUATION REPORT FOR {candidate_name}
{'='*60}

HIRING DECISION
{'-'*60}
{explainability.get('recruiter_explanation', 'N/A')}

TRAINING PLAN
{'-'*60}
{json.dumps(explainability.get('training_plan', {}), indent=2)}

INVESTMENT ANALYSIS
{'-'*60}
{json.dumps(explainability.get('investment_summary', {}), indent=2)}

{'='*60}
"""
        return text
    
    elif format == "markdown":
        md = f"""# Hiring Evaluation Report - {candidate_name}

## Hiring Decision
{explainability.get('recruiter_explanation', 'N/A')}

## Training Plan
### Summary
- Total Skills: {explainability.get('training_plan', {}).get('summary', {}).get('total_skills_to_develop', 0)}
- Hours: {explainability.get('training_plan', {}).get('summary', {}).get('total_estimated_hours', 0)}
- Timeline: {explainability.get('training_plan', {}).get('summary', {}).get('total_estimated_weeks', 0)} weeks

## Investment Analysis
- Level: {explainability.get('investment_summary', {}).get('investment_level', 'N/A')}
- Break-even: {explainability.get('investment_summary', {}).get('roi_analysis', {}).get('break_even_point', 'N/A')}
"""
        return md
    
    return None


def create_explainability_sidebar_options():
    """Create sidebar options for explainability display"""
    
    with st.sidebar:
        st.markdown("---")
        st.subheader("⚙️ Explainability Options")
        
        show_recruiter = st.checkbox(
            "Show Recruiter Analysis",
            value=True,
            help="Display detailed recruiter-focused explanation"
        )
        
        show_training = st.checkbox(
            "Show Training Plan",
            value=True,
            help="Display skill training requirements"
        )
        
        show_investment = st.checkbox(
            "Show Investment Analysis",
            value=True,
            help="Display ROI and time to productivity"
        )
        
        show_feedback = st.checkbox(
            "Show Candidate Feedback",
            value=False,
            help="Display growth-oriented candidate feedback"
        )
        
        export_format = st.selectbox(
            "Export Format",
            ["json", "text", "markdown"],
            help="Choose format for exporting reports"
        )
        
        return {
            "recruiter": show_recruiter,
            "training": show_training,
            "investment": show_investment,
            "feedback": show_feedback,
            "export_format": export_format
        }
