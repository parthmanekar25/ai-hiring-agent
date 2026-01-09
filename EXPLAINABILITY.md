# Explainability Artifact Generator

## Overview

The Explainability Artifact Generator creates **post-hoc justifications** for hiring decisions that are safe, transparent, and actionable. This is NOT chain-of-thought leakage — it's principled explanation generation based on evaluation results.

**Key Features:**
- ✅ Recruiter-friendly explanations with hiring recommendations
- ✅ Candidate-friendly feedback (optional) for transparent communication
- ✅ Detailed training plans with time and resource estimates
- ✅ Investment analysis with ROI projections
- ✅ Role-specific fit analysis
- ✅ Hiring decision recommendations

## Architecture

```
explainability/
├── explainability_generator.py    # Core explanation generation
├── integration.py                  # Workflow integration layer
├── __init__.py                     # Module exports
└── test_explainability.py          # Test suite

api/routes/
└── explainability_routes.py        # FastAPI endpoints
```

## Core Components

### 1. ExplainabilityGenerator

Generates explanations and training requirements.

```python
from backend.explainability import ExplainabilityGenerator

generator = ExplainabilityGenerator()

artifact = generator.generate_complete_artifact(
    candidate_name="Alice Johnson",
    overall_score=72,
    technical_fit=75,
    experience_fit=68,
    education_fit=70,
    skill_matches=[...],
    gaps={...},
    reasoning="Strong Python background with gaps in deployment",
    strengths="Excellent problem solver",
    areas_for_growth="Cloud technologies",
    experience_level="mid",
    learning_velocity=1.2,
    include_candidate_feedback=True
)

# Access components
print(artifact.recruiter_explanation)
print(artifact.candidate_explanation)
print(artifact.training_plan)
print(artifact.investment_summary)
```

### 2. ExplainabilityIntegration

Integration layer for scoring workflow.

```python
from backend.explainability import ExplainabilityIntegration

integration = ExplainabilityIntegration()

# Generate from interview data
result = integration.generate_from_interview(interview_data)

# Analyze for specific role
result = integration.generate_for_job_role(interview_data, job_requirements)

# Complete hiring package
package = integration.generate_hiring_decision_package(interview_data, job_requirements)
```

## Output Components

### 1. Recruiter Explanation

**Purpose:** Help hiring teams understand evaluation results and make decisions.

**Content:**
- Overall assessment summary
- Score breakdown (Technical, Experience, Education)
- Key strengths (top 5)
- Critical gaps with trainability assessment
- Areas for clarification
- Hiring recommendation
- Next steps

**Example:**
```
RECRUITER SUMMARY FOR ALICE JOHNSON
============================================================

OVERALL ASSESSMENT: 72/100
Strong Python developer with solid FastAPI experience. Good problem-solving skills 
and ability to learn quickly. Score reduced by 12 points due to missing Docker and 
Kubernetes experience; however, growth potential remains high based on learning velocity 
indicators.

SCORE BREAKDOWN:
  • Technical Fit:    75/100 - Strong fit
  • Experience Fit:   68/100 - Moderate fit
  • Education Fit:    70/100 - Strong fit

STRENGTHS:
  ✓ Python: 5+ years production experience (Confidence: 95%)
  ✓ FastAPI: 2 major projects built (Confidence: 85%)
  ✓ PostgreSQL: Strong SQL knowledge demonstrated (Confidence: 80%)

CRITICAL GAPS (3 areas):
  ✗ Docker - Can be trained (see training plan below)
  ✗ Kubernetes - Can be trained
  ✗ AWS - Can be trained

HIRING RECOMMENDATION:
🟡 RECOMMEND WITH TRAINING - Good foundation, invest in skill development

NEXT STEPS:
  1. If score > 75: Proceed to technical interview
  2. If score 60-75: Conduct skills assessment on key gaps
  3. If score < 60: Consider for junior/entry-level roles
```

### 2. Candidate Explanation

**Purpose:** Provide transparent feedback to candidates (optional).

**Content:**
- What we liked
- Key strengths identified
- Areas for growth with actionable advice
- Next steps in process
- Encouragement to develop skills

### 3. Training Plan

**Components:**
- Individual skill training requirements
- Estimated hours per skill
- Recommended resources
- Difficulty level
- Priority ranking

**Example:**
```python
{
  "training_requirements": [
    {
      "skill": "Docker",
      "priority": "high",
      "estimated_hours": 30,
      "estimated_weeks": 3,
      "resources": ["Docker documentation", "Play with Docker", "Udemy course"],
      "difficulty": "easy",
      "estimated_cost": "$150"
    },
    {
      "skill": "Kubernetes",
      "priority": "high",
      "estimated_hours": 100,
      "estimated_weeks": 10,
      "resources": ["K8s docs", "Linux Academy", "CKA courses"],
      "difficulty": "hard",
      "estimated_cost": "$500"
    }
  ],
  "summary": {
    "total_skills_to_develop": 3,
    "total_estimated_hours": 170,
    "total_estimated_weeks": 17,
    "estimated_cost_range": "$500 - $1,000",
    "recommended_pace": "Part-time (10 hrs/week) or Full-time (40 hrs/week)"
  }
}
```

### 4. Investment Summary

**Includes:**
- Investment level classification (LOW / MEDIUM / HIGH / VERY_HIGH)
- Breakdown of training components
- Resource requirements
- ROI analysis with productivity projections

**Example:**
```python
{
  "investment_level": "MEDIUM",
  "breakdown": {
    "training_hours": 170,
    "training_weeks": 17,
    "ramp_up_weeks": 8,
    "time_to_productivity": "25 weeks",
    "mentor_hours_needed": 51,
    "team_support_hours": 34
  },
  "resources_required": {
    "training_budget": "$500 - $1,000",
    "mentorship": "Recommended",
    "tools_and_subscriptions": [
      "Online Learning Platform ($10-30/month)",
      "Kaggle/Fast.ai (Free)"
    ],
    "team_time": "~34 hours for onboarding/mentoring"
  },
  "roi_analysis": {
    "break_even_point": "25 weeks",
    "productivity_by_month": {
      "month_1": "45%",
      "month_3": "75%",
      "month_6": "95%"
    },
    "recommendation": "Good investment - structured training will yield productive team member"
  }
}
```

## API Endpoints

### 1. Generate Basic Explainability

**Endpoint:** `POST /api/v1/explainability/generate`

**Purpose:** Generate recruiter and candidate-friendly explanations with training requirements.

**Request:**
```json
{
  "candidate_name": "Alice Johnson",
  "overall_score": 72,
  "technical_score": 75,
  "experience_score": 68,
  "education_score": 70,
  "skill_analysis": {
    "matched_skills": [
      {
        "skill": "Python",
        "present": true,
        "confidence": 0.95,
        "evidence": "5+ years production experience"
      }
    ],
    "gaps": {
      "missing_skills": ["Docker", "Kubernetes", "AWS"],
      "unclear_sections": []
    }
  },
  "reasoning": "Strong Python background with gaps in deployment technologies",
  "strengths": "Excellent problem solver with strong fundamentals",
  "areas_for_growth": "Cloud and containerization technologies",
  "experience_level": "mid",
  "learning_velocity": 1.2,
  "include_candidate_feedback": true
}
```

**Response:**
```json
{
  "candidate_name": "Alice Johnson",
  "overall_score": 72,
  "recruiter_explanation": "...",
  "candidate_explanation": "...",
  "score_rationale": {
    "technical_fit": "75/100 - Strong fit",
    "experience_fit": "68/100 - Moderate fit",
    "education_fit": "70/100 - Strong fit"
  },
  "training_plan": {...},
  "investment_summary": {...}
}
```

### 2. Role-Specific Analysis

**Endpoint:** `POST /api/v1/explainability/generate/role-fit`

**Purpose:** Analyze candidate fit for a specific job role.

**Request:**
```json
{
  "interview_request": {...},
  "job_requirements": {
    "title": "Senior Backend Engineer",
    "level": "senior",
    "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
    "nice_to_have": ["Kubernetes", "AWS"]
  }
}
```

**Response:**
```json
{
  "candidate_name": "Alice Johnson",
  "overall_score": 72,
  "job_role": "Senior Backend Engineer",
  "role_fit_analysis": {
    "required_skills_met": "3/4",
    "required_percentage": "75%",
    "readiness_level": "TRAINABLE - Can reach full productivity with training",
    "trainable_skills": 1
  },
  "training_plan": {...},
  "investment_summary": {...}
}
```

### 3. Hiring Decision Package

**Endpoint:** `POST /api/v1/explainability/generate/hiring-decision`

**Purpose:** Generate complete hiring decision package with recommendation.

**Response:**
```json
{
  "candidate_name": "Alice Johnson",
  "overall_score": 72,
  "hiring_decision": {
    "recommendation": "HIRE_WITH_TRAINING",
    "confidence": "80%",
    "time_to_productivity": "25 weeks",
    "justification": "Good foundation (72/100) with 3 skill gaps. Training plan will result in productive team member."
  },
  "training_plan": {...},
  "investment_summary": {...}
}
```

### 4. Training Resources

**Endpoint:** `GET /api/v1/explainability/training-resources/{skill}`

**Purpose:** Get training resources for a specific skill.

**Response:**
```json
{
  "skill": "Docker",
  "estimated_hours": 30,
  "estimated_weeks": 3,
  "difficulty": "easy",
  "priority": "high",
  "resources": [
    "Docker documentation",
    "Play with Docker",
    "Udemy Docker course"
  ],
  "estimated_cost": "$150",
  "breakdown": {
    "self_study": "18 hours",
    "projects": "9 hours",
    "review": "3 hours"
  }
}
```

### 5. Available Skills

**Endpoint:** `GET /api/v1/explainability/available-skills`

**Purpose:** List all available skills with training information.

**Response:**
```json
{
  "total_skills": 11,
  "skills": [
    {"skill": "Python", "hours": 80, "weeks": 8, "difficulty": "medium", "priority": "critical"},
    {"skill": "FastAPI", "hours": 40, "weeks": 4, "difficulty": "medium", "priority": "high"}
  ],
  "difficulty_breakdown": {
    "easy": 2,
    "medium": 5,
    "hard": 4
  }
}
```

## Integration with Scoring System

### Step 1: Add to Main Pipeline

```python
# backend/main.py or scoring workflow

from backend.explainability import ExplainabilityIntegration

explainability = ExplainabilityIntegration()

# After scoring is complete:
result = explainability.generate_hiring_decision_package(
    interview_data=interview_results,
    job_requirements=job_role
)

# Return in evaluation response
return {
    "score": interview_results["overall_score"],
    "evaluation": interview_results,
    "explainability": result
}
```

### Step 2: Register API Routes

```python
# backend/api/main.py or app initialization

from backend.api.routes import explainability_routes

app.include_router(explainability_routes.router)
```

## Design Principles

### 1. Post-hoc Justification, Not Chain-of-Thought

- ❌ NOT leaking intermediate LLM reasoning
- ✅ ONLY exposing evaluation-based explanations
- ✅ Safe for candidate communication

### 2. Actionable & Concrete

- ✅ Specific skill gaps (not vague)
- ✅ Training time estimates (not "needs improvement")
- ✅ Resource recommendations (actionable next steps)

### 3. Recruiter-Focused

- ✅ Hiring decision guidance
- ✅ Investment/ROI analysis
- ✅ Role-specific fit analysis
- ✅ Confidence scoring

### 4. Candidate-Friendly Option

- ✅ Encouraging tone
- ✅ Growth-oriented feedback
- ✅ Clear next steps
- ✅ Optional (not mandatory)

## Training Skill Map

Currently supports:
- **Backend:** Python, FastAPI, PostgreSQL
- **DevOps:** Docker, Kubernetes, AWS
- **Frontend:** React, Vue.js
- **Soft Skills:** Leadership
- **ML:** Machine Learning

Can be extended with new skills in `explainability_generator.py`.

## Cost Estimation

Cost estimates are based on:
- Skill difficulty level
- Training platform pricing
- Resource availability (free vs. paid)

Formula: `hours × difficulty_factor × platform_cost`

## Security & Privacy

- ✅ No raw interview data exposure
- ✅ Post-hoc explanations only
- ✅ Score-based reasoning
- ✅ No model internals leakage
- ✅ Candidate feedback optional

## Testing

Run the test suite:

```bash
python -m pytest backend/explainability/test_explainability.py -v

# Or run directly:
python backend/explainability/test_explainability.py
```

## Example Workflow

```python
# 1. Get interview evaluation
interview_results = scoring_agent.evaluate_candidate(candidate_profile)

# 2. Get job requirements
job_role = {
    "title": "Senior Backend Engineer",
    "level": "senior",
    "required_skills": ["Python", "FastAPI", "PostgreSQL", "Docker"],
    "nice_to_have": ["Kubernetes"]
}

# 3. Generate explainability
integration = ExplainabilityIntegration()
package = integration.generate_hiring_decision_package(
    interview_results,
    job_role
)

# 4. Present to recruiter
print(package["hiring_decision"]["recommendation"])
print(package["training_plan"]["summary"])
print(package["investment_summary"]["roi_analysis"])

# 5. Optional: Send candidate feedback
if candidate_wants_feedback:
    print(package["candidate_explanation"])
```

## Future Enhancements

- [ ] Multi-language support for candidate feedback
- [ ] Integration with training platform APIs (Coursera, Udemy)
- [ ] Historical training effectiveness tracking
- [ ] Personalized learning path recommendations
- [ ] Team skill gap analysis (aggregate)
- [ ] Training budget optimization algorithms
- [ ] Candidate growth tracking over time
