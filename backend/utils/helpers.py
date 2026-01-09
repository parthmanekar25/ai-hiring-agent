"""
Utility functions for Streamlit frontend
"""

import json
import pandas as pd
from typing import List, Dict, Any
import plotly.graph_objects as go
import plotly.express as px


def format_score(score: float) -> str:
    """Format score with color indicator"""
    if score >= 75:
        return f"🟢 {score:.0f}"
    elif score >= 60:
        return f"🟡 {score:.0f}"
    else:
        return f"🔴 {score:.0f}"


def get_score_category(score: float) -> str:
    """Get category label for score"""
    if score >= 90:
        return "Exceptional"
    elif score >= 75:
        return "Strong"
    elif score >= 60:
        return "Good"
    elif score >= 40:
        return "Marginal"
    else:
        return "Poor"


def create_score_chart(evaluations: List[Dict[str, Any]]) -> go.Figure:
    """Create radar chart comparing candidates"""
    categories = ['Overall', 'Technical', 'Experience', 'Education']
    
    fig = go.Figure()
    
    for eval in evaluations:
        score = eval['score']
        values = [
            score['overall_score'],
            score['technical_fit'],
            score['experience_fit'],
            score['education_fit']
        ]
        
        fig.add_trace(go.Scatterpolar(
            r=values,
            theta=categories,
            fill='toself',
            name=eval['candidate_name']
        ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=True,
        title="Candidate Score Comparison"
    )
    
    return fig


def create_skills_comparison(evaluations: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create dataframe for skills comparison"""
    data = []
    
    for eval in evaluations:
        for skill in eval['skill_matches']:
            data.append({
                'Candidate': eval['candidate_name'],
                'Skill': skill['skill'],
                'Present': '✓' if skill['present'] else '✗',
                'Confidence': skill.get('confidence', 0) * 100
            })
    
    return pd.DataFrame(data)


def export_to_markdown(evaluations: List[Dict[str, Any]]) -> str:
    """Export evaluation results to markdown format"""
    md = "# Candidate Evaluation Report\n\n"
    
    for rank, eval in enumerate(evaluations, 1):
        md += f"## Rank #{rank}: {eval['candidate_name']}\n\n"
        md += f"**File:** {eval['filename']}\n\n"
        
        # Scores
        score = eval['score']
        md += "### Scores\n\n"
        md += f"- Overall: {score['overall_score']:.0f}/100\n"
        md += f"- Technical Fit: {score['technical_fit']:.0f}/100\n"
        md += f"- Experience Fit: {score['experience_fit']:.0f}/100\n"
        md += f"- Education Fit: {score['education_fit']:.0f}/100\n\n"
        
        # Reasoning
        md += "### Evaluation Reasoning\n\n"
        md += f"{score['reasoning']}\n\n"
        
        # Skills
        md += "### Skill Matches\n\n"
        for skill in eval['skill_matches']:
            status = "✓" if skill['present'] else "✗"
            md += f"- {status} {skill['skill']}\n"
            if skill.get('evidence'):
                md += f"  - Evidence: {skill['evidence']}\n"
        md += "\n"
        
        # Gaps
        gaps = eval['gaps']
        if gaps['missing_skills'] or gaps['unclear_sections']:
            md += "### Gaps & Concerns\n\n"
            
            if gaps['missing_skills']:
                md += "**Missing Skills:**\n"
                for skill in gaps['missing_skills']:
                    md += f"- {skill}\n"
                md += "\n"
            
            if gaps['unclear_sections']:
                md += "**Unclear Sections:**\n"
                for section in gaps['unclear_sections']:
                    md += f"- {section}\n"
                md += "\n"
        
        # Questions
        md += "### Interview Questions\n\n"
        for i, q in enumerate(eval['interview_questions'], 1):
            md += f"{i}. **{q['question']}**\n"
            md += f"   - Category: {q['category']}\n"
            md += f"   - Purpose: {q['reasoning']}\n\n"
        
        md += "---\n\n"
    
    return md


def validate_job_description(text: str) -> Dict[str, Any]:
    """Validate job description quality"""
    issues = []
    suggestions = []
    
    if len(text.strip()) < 100:
        issues.append("Job description is too short")
        suggestions.append("Add more details about requirements and responsibilities")
    
    keywords = ['requirement', 'skill', 'experience', 'education', 'responsibility']
    found_keywords = sum(1 for kw in keywords if kw in text.lower())
    
    if found_keywords < 2:
        issues.append("Job description lacks structure")
        suggestions.append("Include clear sections for requirements and responsibilities")
    
    if not any(char.isdigit() for char in text):
        suggestions.append("Consider adding experience requirements (e.g., '5+ years')")
    
    return {
        "valid": len(issues) == 0,
        "issues": issues,
        "suggestions": suggestions,
        "quality_score": max(0, 100 - len(issues) * 20 - len(suggestions) * 10)
    }


def analyze_resume_quality(file_size: int, filename: str) -> Dict[str, str]:
    """Provide basic quality check for uploaded resumes"""
    warnings = []
    
    if file_size < 1024:  # Less than 1KB
        warnings.append("File seems very small - may not contain enough information")
    elif file_size > 5 * 1024 * 1024:  # More than 5MB
        warnings.append("File is very large - may take longer to process")
    
    if not any(ext in filename.lower() for ext in ['.pdf', '.txt', '.doc']):
        warnings.append("Unusual file format - PDF or TXT recommended")
    
    return {
        "size_mb": file_size / (1024 * 1024),
        "warnings": warnings
    }


def calculate_statistics(evaluations: List[Dict[str, Any]]) -> Dict[str, Any]:
    """Calculate aggregate statistics from evaluations"""
    if not evaluations:
        return {}
    
    scores = [e['score']['overall_score'] for e in evaluations]
    
    return {
        "total_candidates": len(evaluations),
        "average_score": sum(scores) / len(scores),
        "highest_score": max(scores),
        "lowest_score": min(scores),
        "strong_fits": sum(1 for s in scores if s >= 75),
        "good_fits": sum(1 for s in scores if 60 <= s < 75),
        "poor_fits": sum(1 for s in scores if s < 60)
    }


def create_comparison_table(evaluations: List[Dict[str, Any]]) -> pd.DataFrame:
    """Create comparison table for all candidates"""
    data = []
    
    for rank, eval in enumerate(evaluations, 1):
        score = eval['score']
        data.append({
            "Rank": rank,
            "Candidate": eval['candidate_name'],
            "Overall": f"{score['overall_score']:.0f}",
            "Technical": f"{score['technical_fit']:.0f}",
            "Experience": f"{score['experience_fit']:.0f}",
            "Education": f"{score['education_fit']:.0f}",
            "Missing Skills": len(eval['gaps']['missing_skills']),
            "Concerns": len(eval['gaps']['unclear_sections']) + len(eval['gaps']['inconsistencies'])
        })
    
    return pd.DataFrame(data)