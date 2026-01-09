# API Reference

Complete documentation of the AI Hiring Agent REST API endpoints.

## Base URL

```
http://localhost:8000
```

## Endpoints

### 1. POST /api/evaluate

Evaluates candidates against a job description.

#### Request

**URL:** `POST /api/evaluate`

**Content-Type:** `multipart/form-data`

**Parameters:**

| Name | Type | Required | Description | Example |
|------|------|----------|-------------|---------|
| `job_description` | String | Yes | Job requirements and description | "Senior Python Developer with 5+ years..." |
| `resumes` | File(s) | Yes | Resume files (PDF or TXT), multiple allowed | resume1.pdf, resume2.txt |

#### Examples

**cURL:**
```bash
curl -X POST http://localhost:8000/api/evaluate \
  -F "job_description=Senior Python Developer" \
  -F "resumes=@resume1.pdf" \
  -F "resumes=@resume2.txt"
```

**Python:**
```python
import requests

files = [
    ("resumes", open("resume1.pdf", "rb")),
    ("resumes", open("resume2.txt", "rb"))
]
data = {
    "job_description": "Senior Python Developer with 5+ years experience"
}

response = requests.post(
    "http://localhost:8000/api/evaluate",
    data=data,
    files=files
)

results = response.json()
```

**JavaScript (Fetch):**
```javascript
const formData = new FormData();
formData.append("job_description", "Senior Python Developer");
formData.append("resumes", resumeFile1);
formData.append("resumes", resumeFile2);

fetch("http://localhost:8000/api/evaluate", {
  method: "POST",
  body: formData
})
.then(r => r.json())
.then(data => console.log(data));
```

#### Response (200 OK)

**Format:** JSON

**Example Response:**
```json
{
  "evaluations": [
    {
      "candidate_name": "John Doe",
      "filename": "john_doe_resume.pdf",
      "score": {
        "overall_score": 87.5,
        "technical_fit": 92.0,
        "experience_fit": 87.0,
        "education_fit": 83.0,
        "reasoning": "Strong fit with excellent Python skills and relevant experience in FastAPI and database design. Has all required technical skills and exceeds experience requirements."
      },
      "skill_matches": [
        {
          "skill": "Python",
          "present": true,
          "evidence": "7 years of professional Python development experience mentioned in resume",
          "confidence": 0.98
        },
        {
          "skill": "FastAPI",
          "present": true,
          "evidence": "Worked on FastAPI-based microservices project for 2 years",
          "confidence": 0.95
        },
        {
          "skill": "PostgreSQL",
          "present": true,
          "evidence": "Database design and optimization experience with PostgreSQL",
          "confidence": 0.90
        },
        {
          "skill": "Docker",
          "present": true,
          "evidence": "Docker containerization experience mentioned",
          "confidence": 0.85
        },
        {
          "skill": "Kubernetes",
          "present": false,
          "evidence": "Kubernetes not mentioned in resume",
          "confidence": 0.92
        },
        {
          "skill": "AWS",
          "present": true,
          "evidence": "AWS certification and 2 years of AWS experience",
          "confidence": 0.88
        }
      ],
      "gaps": {
        "missing_skills": [
          "Kubernetes",
          "Advanced AWS DevOps",
          "Machine Learning"
        ],
        "unclear_sections": [
          "Leadership experience limited to brief team lead mention",
          "Mentoring examples not provided"
        ],
        "inconsistencies": []
      },
      "interview_questions": [
        {
          "question": "Can you describe your experience with container orchestration and Kubernetes?",
          "category": "Technical",
          "reasoning": "Kubernetes is a critical requirement but not mentioned in your resume. This question will help us understand if you have hands-on experience or knowledge in this area."
        },
        {
          "question": "Tell us about your largest scale AWS deployment and the infrastructure decisions you made.",
          "category": "Technical",
          "reasoning": "AWS is mentioned but details are limited. We need to understand the scope and complexity of your AWS experience."
        },
        {
          "question": "Describe a time when you led a technical team through a major system redesign. What were the challenges?",
          "category": "Behavioral",
          "reasoning": "Leadership is an expectation but your resume shows limited team leadership experience. This explores your ability to lead technically."
        },
        {
          "question": "What's your approach to designing highly scalable microservices?",
          "category": "Technical",
          "reasoning": "Understanding your approach to scalability will help us assess if your experience aligns with our needs."
        }
      ],
      "summary": "John Doe is a strong candidate with 7+ years of Python experience and solid FastAPI/database knowledge. Exceeds minimum requirements in technical skills. Primary gaps are Kubernetes experience and leadership breadth. Recommend technical and behavioral interviews to assess gap areas."
    },
    {
      "candidate_name": "Jane Smith",
      "filename": "jane_smith.txt",
      "score": {
        "overall_score": 72.0,
        "technical_fit": 78.0,
        "experience_fit": 70.0,
        "education_fit": 68.0,
        "reasoning": "Moderate fit with good Python fundamentals but limited FastAPI experience. Has database knowledge but AWS/DevOps experience is minimal."
      },
      "skill_matches": [
        {
          "skill": "Python",
          "present": true,
          "evidence": "5 years Python experience with focus on data science",
          "confidence": 0.92
        },
        {
          "skill": "FastAPI",
          "present": false,
          "evidence": "Resume shows Django and Flask but not FastAPI",
          "confidence": 0.88
        },
        {
          "skill": "PostgreSQL",
          "present": true,
          "evidence": "SQL and database optimization mentioned",
          "confidence": 0.85
        },
        {
          "skill": "Docker",
          "present": false,
          "evidence": "No containerization experience mentioned",
          "confidence": 0.90
        },
        {
          "skill": "Kubernetes",
          "present": false,
          "evidence": "No Kubernetes experience mentioned",
          "confidence": 0.95
        },
        {
          "skill": "AWS",
          "present": false,
          "evidence": "No AWS experience mentioned",
          "confidence": 0.93
        }
      ],
      "gaps": {
        "missing_skills": [
          "FastAPI framework",
          "Docker and containerization",
          "Kubernetes",
          "AWS platform",
          "DevOps practices"
        ],
        "unclear_sections": [
          "Scalability experience not documented",
          "Deployment processes not explained"
        ],
        "inconsistencies": []
      },
      "interview_questions": [
        {
          "question": "While your background is in Django and Flask, what's your experience with fast, modern async frameworks like FastAPI?",
          "category": "Technical",
          "reasoning": "FastAPI is the primary framework requirement, but your experience is with older frameworks. This assesses willingness to learn."
        },
        {
          "question": "Tell us about your experience with containerization and DevOps practices.",
          "category": "Technical",
          "reasoning": "Docker and containerization are critical requirements with zero experience shown."
        },
        {
          "question": "What would be your learning plan to get up to speed with our tech stack (FastAPI, Kubernetes, AWS)?",
          "category": "Behavioral",
          "reasoning": "Significant learning curve required. Assesses approach to professional development."
        }
      ],
      "summary": "Jane Smith has solid Python fundamentals but is a junior fit for this role due to lack of modern framework, DevOps, and cloud platform experience. May be suitable for junior positions or with 3-6 months ramp-up time. Recommend skills assessment interview."
    }
  ],
  "processing_time": 128.45
}
```

#### Response Fields

**Top Level:**

| Field | Type | Description |
|-------|------|-------------|
| `evaluations` | Array | List of evaluated candidates |
| `processing_time` | Number | Total processing time in seconds |

**Evaluation Object:**

| Field | Type | Description |
|-------|------|-------------|
| `candidate_name` | String | Name extracted from resume |
| `filename` | String | Original filename uploaded |
| `score` | Object | Scoring details |
| `skill_matches` | Array | Individual skill assessments |
| `gaps` | Object | Identified gaps and concerns |
| `interview_questions` | Array | Suggested interview questions |
| `summary` | String | High-level summary of fit |

**Score Object:**

| Field | Type | Range | Description |
|-------|------|-------|-------------|
| `overall_score` | Number | 0-100 | Final fit score (weighted) |
| `technical_fit` | Number | 0-100 | Technical skills match |
| `experience_fit` | Number | 0-100 | Experience level match |
| `education_fit` | Number | 0-100 | Education relevance |
| `reasoning` | String | - | Explanation of scoring |

**Skill Match Object:**

| Field | Type | Description |
|-------|------|-------------|
| `skill` | String | Required skill name |
| `present` | Boolean | Whether skill found in resume |
| `evidence` | String | Quote or reference from resume |
| `confidence` | Number (0-1) | Confidence level in assessment |

**Gaps Object:**

| Field | Type | Description |
|-------|------|-------------|
| `missing_skills` | Array | Required skills not mentioned |
| `unclear_sections` | Array | Areas needing clarification |
| `inconsistencies` | Array | Conflicting information |

**Interview Question Object:**

| Field | Type | Description |
|-------|------|-------------|
| `question` | String | The interview question |
| `category` | String | Type (Technical, Behavioral, Scenario) |
| `reasoning` | String | Why this question was chosen |

#### Error Responses

**400 Bad Request - Missing field:**
```json
{
  "detail": "job_description and resumes are required"
}
```

**400 Bad Request - No resumes uploaded:**
```json
{
  "detail": "At least one resume file is required"
}
```

**400 Bad Request - Invalid file type:**
```json
{
  "detail": "Only PDF and TXT files are supported. Got: .doc"
}
```

**413 Payload Too Large:**
```json
{
  "detail": "File too large. Maximum: 10MB"
}
```

**500 Internal Server Error:**
```json
{
  "detail": "Error processing resumes. Please try again.",
  "error": "Specific error message"
}
```

#### Status Codes

| Code | Meaning | Cause |
|------|---------|-------|
| 200 | Success | All candidates evaluated successfully |
| 400 | Bad Request | Missing fields, invalid files, wrong format |
| 413 | Payload Too Large | File size exceeds 10MB limit |
| 422 | Unprocessable Entity | Invalid data format |
| 500 | Server Error | Backend processing failed |
| 503 | Service Unavailable | Groq API unreachable |

---

### 2. GET /health

Simple health check to verify backend is running.

#### Request

**URL:** `GET /health`

**Headers:** None required

**Example:**
```bash
curl http://localhost:8000/health
```

#### Response (200 OK)

```json
{
  "status": "healthy"
}
```

#### Use Case

Test if backend is running before attempting evaluation:

```python
import requests

try:
    response = requests.get("http://localhost:8000/health", timeout=5)
    if response.status_code == 200:
        print("Backend is running")
except:
    print("Backend is not reachable")
```

---

## Practical Examples

### Full Evaluation Flow

**1. Check backend health:**
```bash
curl http://localhost:8000/health
```

**2. Prepare files:**
```bash
# Create job description
echo "Senior Python Developer
Required: 5+ years Python, FastAPI, PostgreSQL
Nice-to-have: AWS, Docker, Kubernetes" > job.txt

# Resume is already in resume1.pdf
```

**3. Send evaluation request:**
```bash
curl -X POST http://localhost:8000/api/evaluate \
  -F "job_description=Senior Python Developer, 5+ years" \
  -F "resumes=@resume1.pdf"
```

**4. Parse response:**
```bash
# Save to file
curl -X POST http://localhost:8000/api/evaluate \
  -F "job_description=Senior Python Developer" \
  -F "resumes=@resume.pdf" > results.json

# Extract scores
cat results.json | jq '.evaluations[0].score.overall_score'

# Extract candidate names
cat results.json | jq '.evaluations[].candidate_name'
```

### Batch Processing Multiple Resumes

```python
import requests
import json
from pathlib import Path

job_description = "Senior Python Developer with 5+ years experience"
resume_files = list(Path(".").glob("*.pdf")) + list(Path(".").glob("*.txt"))

# Prepare files for upload
files = []
for resume in resume_files:
    files.append(("resumes", open(resume, "rb")))

# Send request
response = requests.post(
    "http://localhost:8000/api/evaluate",
    data={"job_description": job_description},
    files=files
)

# Process results
results = response.json()

# Sort by score
sorted_candidates = sorted(
    results["evaluations"],
    key=lambda x: x["score"]["overall_score"],
    reverse=True
)

# Print summary
for i, candidate in enumerate(sorted_candidates, 1):
    print(f"{i}. {candidate['candidate_name']}: {candidate['score']['overall_score']:.1f}/100")
```

### Exporting Results to CSV

```python
import requests
import csv

response = requests.post(
    "http://localhost:8000/api/evaluate",
    data={"job_description": job_desc},
    files=files
)

# Export to CSV
with open("results.csv", "w") as f:
    writer = csv.DictWriter(f, fieldnames=[
        "Name", "Overall Score", "Technical Fit", 
        "Experience Fit", "Education Fit", "Missing Skills"
    ])
    writer.writeheader()
    
    for eval in response.json()["evaluations"]:
        writer.writerow({
            "Name": eval["candidate_name"],
            "Overall Score": eval["score"]["overall_score"],
            "Technical Fit": eval["score"]["technical_fit"],
            "Experience Fit": eval["score"]["experience_fit"],
            "Education Fit": eval["score"]["education_fit"],
            "Missing Skills": "; ".join(eval["gaps"]["missing_skills"])
        })
```

---

## Performance & Limits

### Rate Limiting

- **Requests per minute:** 60 (limited by Groq free tier)
- **Concurrent requests:** 1 (sequential processing)
- **File size limit:** 10MB per file
- **Total files per request:** Unlimited (but practical limit ~10)

### Processing Time

| Scenario | Time | Cost |
|----------|------|------|
| 1 resume | 45-70s | ~$0.01 |
| 5 resumes | 5-8 min | ~$0.05 |
| 10 resumes | 10-15 min | ~$0.10 |

### Timeout

- **Request timeout:** 120 seconds per request
- **Individual agent timeout:** 40 seconds
- **If exceeded:** Returns partial results or error

---

## Error Handling

### Common Error Scenarios

**Resume parsing fails:**
- Try uploading as `.txt` instead of `.pdf`
- Check PDF isn't encrypted or password-protected
- Verify file isn't corrupted

**API timeout:**
- Try with fewer resumes
- Check Groq API status
- Increase timeout in your client

**Low scores for good candidates:**
- Ensure job description has key skills
- Make sure resume format is standard
- Check that keywords match job description

---

## CORS & Requests from Frontend

CORS is enabled for:
- **Origins:** `http://localhost:*`, `http://127.0.0.1:*`
- **Methods:** GET, POST
- **Headers:** Content-Type, Accept
- **Credentials:** Not required

Frontend can directly call API:
```javascript
fetch("http://localhost:8000/api/evaluate", {
  method: "POST",
  body: formData,
  headers: {
    "Accept": "application/json"
  }
})
```

---

## Integration Tips

### With Excel/Sheets

1. Evaluate candidates via API
2. Export results as JSON
3. Import JSON into Excel with `Power Query`
4. Create pivot tables and charts

### With ATS (Applicant Tracking Systems)

Most ATS systems can integrate via:
1. REST API webhook
2. CSV import
3. Custom integration

Contact your ATS provider for integration support.

### With Slack/Teams

Get notifications when evaluation completes:
```python
import requests

response = requests.post("http://localhost:8000/api/evaluate", ...)
results = response.json()

# Send to Slack
for eval in results["evaluations"]:
    requests.post(
        "https://hooks.slack.com/services/YOUR_WEBHOOK",
        json={
            "text": f"{eval['candidate_name']}: {eval['score']['overall_score']}/100"
        }
    )
```

---

## Authentication

The current API has **no authentication**. For production:

```python
# Add to main.py
from fastapi.security import HTTPBearer

security = HTTPBearer()

@app.post("/api/evaluate")
async def evaluate(job_description: str, credentials: HTTPAuthCredentials = Depends(security)):
    token = credentials.credentials
    # Verify token
    ...
```

---

## Rate Limiting (Production)

Add to `main.py`:

```python
from slowapi import Limiter
from slowapi.util import get_remote_address

limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter

@app.post("/api/evaluate")
@limiter.limit("60/minute")
async def evaluate(request: Request, ...):
    ...
```

---

Next: Check [DECISIONS.md](DECISIONS.md) for technical design decisions.
