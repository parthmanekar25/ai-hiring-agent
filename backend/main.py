from fastapi import FastAPI, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import time
import os
import sys
from dotenv import load_dotenv

# Add backend directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from models.schemas import (
    CandidateEvaluation, EvaluationResponse,
    CandidateScore, SkillMatch, GapAnalysis, InterviewQuestion
)
from agents.resume_analyzer import ResumeAnalyzerAgent
from agents.scorer import ScorerAgent
from agents.question_generator import QuestionGeneratorAgent
from utils.pdf_parser import extract_text_from_pdf, clean_text
from api.routes.explainability_routes import router as explainability_router

load_dotenv()

app = FastAPI(title="AI Hiring Agent API")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include explainability routes
app.include_router(explainability_router, prefix="/api/v1/explainability", tags=["explainability"])

# Configure Groq API
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

# Initialize agents (will fail gracefully if API key is missing)
analyzer = None
scorer = None
question_gen = None

if GROQ_API_KEY:
    try:
        analyzer = ResumeAnalyzerAgent(GROQ_API_KEY)
        scorer = ScorerAgent(GROQ_API_KEY)
        question_gen = QuestionGeneratorAgent(GROQ_API_KEY)
    except Exception as e:
        print(f"⚠️ Warning: Failed to initialize agents: {str(e)}")
else:
    print("⚠️ Warning: GROQ_API_KEY not found in environment variables")

@app.post("/api/evaluate", response_model=EvaluationResponse)
async def evaluate_candidates(
    job_description: str = Form(...),
    resumes: List[UploadFile] = File(...)
):
    """Evaluate candidates against job description"""
    start_time = time.time()
    
    # Validate inputs
    if not job_description or not job_description.strip():
        raise HTTPException(status_code=400, detail="Job description cannot be empty")
    
    if not resumes:
        raise HTTPException(status_code=400, detail="No resumes provided")
    
    if not GROQ_API_KEY:
        raise HTTPException(
            status_code=500, 
            detail="GROQ_API_KEY not configured. Please set GROQ_API_KEY in .env file. Get your key at https://console.groq.com"
        )
    
    if not analyzer or not scorer or not question_gen:
        raise HTTPException(
            status_code=500,
            detail="AI agents not initialized. Check backend logs for initialization errors."
        )
    
    evaluations = []
    errors = []
    total_files = len(resumes)
    
    for resume_file in resumes:
        try:
            # Extract text from resume
            content = await resume_file.read()
            
            if not content:
                errors.append({
                    "filename": resume_file.filename,
                    "error": "File is empty",
                    "type": "empty_file"
                })
                continue
            
            if resume_file.filename.endswith('.pdf'):
                try:
                    resume_text = extract_text_from_pdf(content)
                except Exception as pdf_error:
                    errors.append({
                        "filename": resume_file.filename,
                        "error": f"Failed to parse PDF: {str(pdf_error)}",
                        "type": "pdf_parse_error"
                    })
                    continue
            else:
                try:
                    resume_text = content.decode('utf-8')
                except UnicodeDecodeError:
                    errors.append({
                        "filename": resume_file.filename,
                        "error": "File encoding not supported (must be UTF-8)",
                        "type": "encoding_error"
                    })
                    continue
            
            if not resume_text or not resume_text.strip():
                errors.append({
                    "filename": resume_file.filename,
                    "error": "No text content extracted from file",
                    "type": "empty_content"
                })
                continue
            
            resume_text = clean_text(resume_text)
            
            # Step 1: Analyze resume
            try:
                analysis = await analyzer.analyze(job_description, resume_text)
            except Exception as e:
                errors.append({
                    "filename": resume_file.filename,
                    "error": f"Resume analysis failed: {str(e)}",
                    "type": "analysis_error"
                })
                continue
            
            # Step 2: Score candidate
            try:
                scoring_result = await scorer.score(job_description, analysis)
            except Exception as e:
                errors.append({
                    "filename": resume_file.filename,
                    "error": f"Scoring failed: {str(e)}",
                    "type": "scoring_error"
                })
                continue
            
            # Step 3: Generate questions
            try:
                questions = await question_gen.generate_questions(
                    job_description,
                    analysis,
                    scoring_result.get('gaps', {})
                )
            except Exception as e:
                # Questions are optional, so we'll continue with empty list
                questions = []
                print(f"Warning: Question generation failed for {resume_file.filename}: {str(e)}")
            
            # Build evaluation
            try:
                evaluation = CandidateEvaluation(
                    candidate_name=analysis.get('candidate_name', 'Unknown'),
                    filename=resume_file.filename,
                    score=CandidateScore(
                        overall_score=float(scoring_result.get('overall_score', 50)),
                        technical_fit=float(scoring_result.get('technical_fit', 50)),
                        experience_fit=float(scoring_result.get('experience_fit', 50)),
                        education_fit=float(scoring_result.get('education_fit', 50)),
                        reasoning=str(scoring_result.get('reasoning', ''))
                    ),
                    skill_matches=[
                        SkillMatch(
                            skill=skill.get('skill', 'Unknown'),
                            present=skill.get('present', False),
                            evidence=skill.get('evidence'),
                            confidence=float(skill.get('confidence', 0.5))
                        )
                        for skill in scoring_result.get('skill_matches', [])
                        if isinstance(skill, dict)
                    ],
                    gaps=GapAnalysis(
                        missing_skills=scoring_result.get('gaps', {}).get('missing_skills', []),
                        unclear_sections=scoring_result.get('gaps', {}).get('unclear_sections', []),
                        inconsistencies=scoring_result.get('gaps', {}).get('inconsistencies', [])
                    ),
                    interview_questions=[
                        InterviewQuestion(
                            question=q.get('question', ''),
                            category=q.get('category', 'General'),
                            reasoning=q.get('reasoning', '')
                        ) for q in questions
                        if isinstance(q, dict) and 'question' in q
                    ],
                    summary=str(analysis.get('overall_impression', ''))
                )
                
                evaluations.append(evaluation)
            except Exception as e:
                errors.append({
                    "filename": resume_file.filename,
                    "error": f"Failed to build evaluation: {str(e)}",
                    "type": "evaluation_build_error"
                })
                continue
            
        except Exception as e:
            import traceback
            error_msg = f"Unexpected error processing {resume_file.filename}: {str(e)}"
            print(f"❌ {error_msg}")
            traceback.print_exc()
            errors.append({
                "filename": resume_file.filename,
                "error": error_msg,
                "type": "unexpected_error",
                "traceback": traceback.format_exc()
            })
            continue
    
    processing_time = time.time() - start_time
    
    # Sort by overall score
    evaluations.sort(key=lambda x: x.score.overall_score, reverse=True)
    
    return EvaluationResponse(
        evaluations=evaluations,
        processing_time=processing_time,
        errors=errors,
        total_files=total_files,
        successful=len(evaluations),
        failed=len(errors)
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
    