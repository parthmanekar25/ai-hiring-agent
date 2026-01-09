# Frontend Integration Guide: Explainability Artifacts

## Overview

The Streamlit frontend has been fully integrated with the explainability backend. Users can now see comprehensive explainability artifacts for each candidate evaluation, including hiring recommendations, training plans, and ROI analysis.

## Architecture

### Service Layer: `frontend/services/explainability.py`

The `ExplainabilityService` class handles all communication with the explainability API:

```python
from frontend.services.explainability import ExplainabilityService

service = ExplainabilityService(base_url="http://localhost:8000")

# Call any explainability endpoint
result = service.generate_hiring_decision(interview_data={
    "candidate_name": "John Doe",
    "overall_score": 85,
    "technical_score": 82,
    # ... other fields
})
```

### Display Components

The service layer provides 8 reusable display functions:

#### 1. **display_hiring_decision(hiring_decision)**
Renders a color-coded hiring recommendation card:
- 🟢 STRONG_HIRE
- 🟡 HIRE_WITH_TRAINING
- 🟠 CONDITIONAL_HIRE
- 🔴 RECONSIDER

```python
from frontend.services.explainability import display_hiring_decision

hiring_decision = {
    "recommendation": "HIRE_WITH_TRAINING",
    "confidence": 0.87,
    "rationale": "Strong technical foundation with some skill gaps..."
}

display_hiring_decision(hiring_decision)
```

#### 2. **display_recruiter_explanation(explanation)**
Shows recruiter-focused analysis with formatted text and bullet points:

```python
from frontend.services.explainability import display_recruiter_explanation

explanation = {
    "summary": "Candidate is a good fit...",
    "key_strengths": ["Python expert", "AWS certified"],
    "concerns": ["No Kubernetes experience"]
}

display_recruiter_explanation(explanation)
```

#### 3. **display_training_plan(training_plan)**
Renders interactive training plan with progress bars:

```python
from frontend.services.explainability import display_training_plan

training_plan = {
    "skills": [
        {
            "name": "Kubernetes",
            "hours_required": 100,
            "weeks_required": 10,
            "estimated_cost": 1500,
            "difficulty": "Hard",
            "resources_needed": 2
        },
        # ... more skills
    ],
    "total_hours": 250,
    "total_weeks": 25,
    "total_cost": 3450
}

display_training_plan(training_plan)
```

#### 4. **display_investment_analysis(investment_summary)**
Shows ROI metrics and productivity projections:

```python
from frontend.services.explainability import display_investment_analysis

investment_summary = {
    "investment_level": "HIGH",
    "total_hours": 250,
    "total_cost": 3450,
    "break_even_weeks": 25,
    "mentoring_hours": 50,
    "productivity_timeline": {
        "month_1": 0.45,
        "month_3": 0.75,
        "month_6": 0.95
    }
}

display_investment_analysis(investment_summary)
```

#### 5. **display_role_fit_analysis(role_fit)**
Shows role-specific assessment with readiness levels:

```python
from frontend.services.explainability import display_role_fit_analysis

role_fit = {
    "role_match_score": 82,
    "readiness_level": "READY_WITH_SUPPORT",
    "must_have_skills_met": 8,
    "total_must_have_skills": 10,
    "nice_to_have_skills_met": 3,
    "total_nice_to_have_skills": 5
}

display_role_fit_analysis(role_fit)
```

#### 6. **display_score_rationale(score_rationale)**
Breaks down scoring components:

```python
from frontend.services.explainability import display_score_rationale

score_rationale = {
    "overall_score": 82,
    "technical_fit": 85,
    "experience_fit": 78,
    "education_fit": 82,
    "score_breakdown": {
        "python": 90,
        "docker": 70,
        "kubernetes": 40
    }
}

display_score_rationale(score_rationale)
```

#### 7. **export_explainability_report(explainability, format='json')**
Exports reports in multiple formats:

```python
from frontend.services.explainability import export_explainability_report

# Export as JSON
json_report = export_explainability_report(explainability, format='json')

# Export as Markdown
md_report = export_explainability_report(explainability, format='markdown')

# Export as Text
txt_report = export_explainability_report(explainability, format='text')
```

#### 8. **create_explainability_sidebar_options()**
Renders display preference controls:

```python
from frontend.services.explainability import create_explainability_sidebar_options

options = create_explainability_sidebar_options()
# Returns dict with user preferences for display
```

## Frontend Integration Points

### 1. Main Application (`frontend/app.py`)

The main Streamlit app integrates explainability in the following locations:

#### Tab 1: Evaluation Results
- **Enhanced display_candidate_evaluation()**: Now calls the explainability API for each candidate
- Shows hiring decision, training plan, investment analysis
- Provides export options

```python
# In display_candidate_evaluation():
if 'explainability' in evaluation:
    st.subheader("✨ Explainability")
    
    explainability = evaluation['explainability']
    
    # Show decision
    display_hiring_decision(explainability['hiring_decision'])
    
    # Show explanation
    display_recruiter_explanation(explainability['recruiter_explanation'])
    
    # Show training plan
    display_training_plan(explainability['training_plan'])
    
    # Show investment analysis
    display_investment_analysis(explainability['investment_summary'])
    
    # Export options
    st.write("**Export Report:**")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        json_data = export_explainability_report(explainability, 'json')
        st.download_button("📄 JSON", json_data, "report.json", "application/json")
    
    with col2:
        txt_data = export_explainability_report(explainability, 'text')
        st.download_button("📝 Text", txt_data, "report.txt", "text/plain")
    
    with col3:
        md_data = export_explainability_report(explainability, 'markdown')
        st.download_button("📋 Markdown", md_data, "report.md", "text/markdown")
```

#### Summary Metrics
- Added explainability metrics to results summary:
  - Strong hire count
  - Hiring recommendation distribution
  - Total training investment and hours

```python
# In results summary section:
decision_counts = {}
for e in data['evaluations']:
    exp = e.get('explainability', {})
    if exp:
        decision = exp.get('hiring_decision', {}).get('recommendation')
        decision_counts[decision] = decision_counts.get(decision, 0) + 1

st.metric("Strong Hires", decision_counts.get('STRONG_HIRE', 0))
```

#### Tab 2: Instructions
- Updated documentation to explain new explainability features
- Added examples of training plans and ROI analysis
- Added tips for using explainability artifacts

### 2. Service Configuration

The `ExplainabilityService` is initialized with the backend URL:

```python
from frontend.services.explainability import ExplainabilityService

# Uses environment variable or defaults to localhost
BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")
explainability_service = ExplainabilityService(base_url=BASE_URL)
```

## Data Flow

### Request Flow

1. **User evaluates candidates** → Tab 1: Evaluate Candidates
2. **Backend evaluates** → Returns basic evaluation scores
3. **Frontend calls explainability API** → For each candidate
4. **ExplainabilityService sends**:
   ```python
   {
       "candidate_name": str,
       "overall_score": float,
       "technical_score": float,
       "experience_score": float,
       "education_score": float,
       "skill_analysis": dict,
       "reasoning": str,
       "strengths": str,
       "areas_for_growth": str
   }
   ```
5. **Backend generates** explainability artifacts
6. **Frontend displays** all components with proper formatting
7. **User can export** reports in multiple formats

### Response Structure

```python
{
    "success": True,
    "data": {
        "hiring_decision": {
            "recommendation": "HIRE_WITH_TRAINING",
            "confidence": 0.87,
            "rationale": "..."
        },
        "recruiter_explanation": {
            "summary": "...",
            "key_strengths": [...],
            "concerns": [...]
        },
        "candidate_explanation": {
            "greeting": "...",
            "strengths": [...],
            "growth_areas": [...],
            "next_steps": [...]
        },
        "training_plan": {
            "skills": [...],
            "total_hours": 250,
            "total_weeks": 25,
            "total_cost": 3450
        },
        "investment_summary": {
            "investment_level": "HIGH",
            "break_even_weeks": 25,
            "productivity_timeline": {...}
        },
        "role_fit_analysis": {
            "role_match_score": 82,
            "readiness_level": "READY_WITH_SUPPORT",
            "must_have_skills_met": 8
        }
    }
}
```

## Features

### 1. Color-Coded Decisions
- 🟢 STRONG_HIRE - Immediately hire
- 🟡 HIRE_WITH_TRAINING - Hire and provide training
- 🟠 CONDITIONAL_HIRE - Hire based on conditions
- 🔴 RECONSIDER - Not recommended

### 2. Training Plan Display
- Skill-by-skill breakdown
- Estimated hours and weeks
- Cost calculations
- Difficulty levels
- Resource requirements

### 3. Investment Analysis
- Total investment calculation
- ROI projections
- Break-even analysis
- Productivity timeline (months 1, 3, 6)
- Mentoring hours

### 4. Multi-Format Export
- **JSON**: Structured data for integration
- **Markdown**: Formatted for sharing
- **Text**: Plain text for emails

### 5. Role-Fit Analysis
- Must-have skills coverage
- Nice-to-have skills coverage
- Overall role match score
- Readiness assessment

## Usage Example

### Complete Flow

```python
import streamlit as st
from frontend.services.explainability import (
    ExplainabilityService,
    display_hiring_decision,
    display_training_plan,
    display_investment_analysis,
    export_explainability_report
)

# Initialize service
service = ExplainabilityService()

# Prepare interview data
interview_data = {
    "candidate_name": "Jane Smith",
    "overall_score": 82,
    "technical_score": 85,
    "experience_score": 78,
    "education_score": 82,
    "skill_analysis": {
        "python": 90,
        "docker": 70,
        "kubernetes": 40
    },
    "reasoning": "Strong Python skills...",
    "strengths": "Excellent foundation",
    "areas_for_growth": "Kubernetes experience"
}

# Generate hiring decision package
result = service.generate_hiring_decision(interview_data)

if result['success']:
    explainability = result['data']
    
    # Display components
    col1, col2 = st.columns(2)
    
    with col1:
        display_hiring_decision(explainability['hiring_decision'])
        display_training_plan(explainability['training_plan'])
    
    with col2:
        display_investment_analysis(explainability['investment_summary'])
    
    # Export options
    st.subheader("Export Report")
    
    json_data = export_explainability_report(explainability, 'json')
    st.download_button(
        "📥 Download JSON",
        json_data,
        "report.json",
        "application/json"
    )
```

## API Requirements

The frontend requires the following backend endpoints:

1. `POST /api/v1/explainability/generate` - Basic explainability
2. `POST /api/v1/explainability/generate/role-fit` - Role-specific analysis
3. `POST /api/v1/explainability/generate/hiring-decision` - Complete package
4. `GET /api/v1/explainability/training-resources/{skill}` - Skill resources
5. `GET /api/v1/explainability/available-skills` - Skills catalog

All endpoints are implemented in `backend/api/routes/explainability_routes.py`.

## Configuration

### Environment Variables

```bash
# Backend URL
API_BASE_URL=http://localhost:8000

# Optional: API timeout (seconds)
API_TIMEOUT=30
```

### Streamlit Configuration

No special Streamlit configuration is required. The app works with standard Streamlit settings.

## Troubleshooting

### Issue: "API connection failed"
- Ensure backend is running: `python backend/main.py`
- Check API_BASE_URL environment variable
- Verify backend is accessible at `http://localhost:8000`

### Issue: "Missing explainability data"
- Check if API endpoint is properly configured
- Verify Groq API key is set in backend
- Check backend logs for errors

### Issue: "Export button not working"
- Ensure explainability data was generated successfully
- Check browser console for JavaScript errors
- Try different export format

## Testing

To test the integration end-to-end:

```bash
# 1. Start backend
cd backend
python main.py

# 2. In another terminal, start frontend
cd frontend
streamlit run app.py

# 3. Upload sample resumes and evaluate
# 4. Verify explainability artifacts appear
# 5. Test export functionality
```

## Performance Considerations

- **API calls are async** - Frontend remains responsive
- **Caching**: Consider caching explainability results for repeated evaluations
- **Batch processing**: For multiple candidates, explainability generation happens sequentially

## Future Enhancements

1. **Caching**: Cache explainability results to reduce API calls
2. **Batch generation**: Generate explainability for all candidates in parallel
3. **Custom templates**: Allow users to customize explainability reports
4. **Visualization**: Add charts for training timelines and ROI projections
5. **Feedback loop**: Allow users to rate explainability quality

## Summary

The frontend is now fully integrated with the explainability backend, providing users with:

✅ Color-coded hiring recommendations  
✅ Detailed training plans with costs  
✅ ROI analysis and productivity projections  
✅ Role-fit assessment  
✅ Multi-format report exports  
✅ Seamless integration with existing evaluation workflow  

All components are production-ready and fully tested.
