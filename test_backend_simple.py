#!/usr/bin/env python3
"""
Simple test script to debug backend issues
"""

import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Add project to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.agents.resume_analyzer import ResumeAnalyzerAgent
from backend.agents.scorer import ScorerAgent
from backend.agents.question_generator import QuestionGeneratorAgent

async def test_pipeline():
    """Test the full pipeline"""
    
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    
    if not GROQ_API_KEY:
        print("❌ ERROR: GROQ_API_KEY not set in .env")
        return
    
    print("✅ GROQ_API_KEY found")
    
    # Test data
    job_description = """
    Senior Python Developer
    - 5+ years Python experience
    - FastAPI/Django
    - PostgreSQL
    - AWS
    """
    
    resume_text = """
    John Smith
    john@example.com
    
    Experience:
    - 6 years Python developer at TechCorp
    - Built FastAPI microservices
    - PostgreSQL database design
    - AWS deployment
    
    Skills: Python, FastAPI, PostgreSQL, AWS, Docker
    Education: B.S. Computer Science
    """
    
    # Initialize agents
    print("\n📌 Initializing agents...")
    try:
        analyzer = ResumeAnalyzerAgent(GROQ_API_KEY)
        scorer = ScorerAgent(GROQ_API_KEY)
        question_gen = QuestionGeneratorAgent(GROQ_API_KEY)
        print("✅ Agents initialized")
    except Exception as e:
        print(f"❌ Failed to initialize agents: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test analyzer
    print("\n📌 Testing Resume Analyzer...")
    try:
        analysis = await analyzer.analyze(job_description, resume_text)
        print(f"✅ Analysis complete")
        print(f"   Fields: {list(analysis.keys())}")
        print(f"   Candidate: {analysis.get('candidate_name', 'Unknown')}")
    except Exception as e:
        print(f"❌ Analyzer failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test scorer
    print("\n📌 Testing Scorer...")
    try:
        scoring_result = await scorer.score(job_description, analysis)
        print(f"✅ Scoring complete")
        print(f"   Fields: {list(scoring_result.keys())}")
        print(f"   Score: {scoring_result.get('overall_score', 'N/A')}")
    except Exception as e:
        print(f"❌ Scorer failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    # Test question generator
    print("\n📌 Testing Question Generator...")
    try:
        questions = await question_gen.generate_questions(
            job_description,
            analysis,
            scoring_result.get('gaps', {})
        )
        print(f"✅ Questions generated")
        print(f"   Count: {len(questions)}")
        if questions:
            print(f"   Sample: {questions[0].get('question', 'N/A')}")
    except Exception as e:
        print(f"❌ Question Generator failed: {e}")
        import traceback
        traceback.print_exc()
        return
    
    print("\n✅ All tests passed!")
    
    # Print complete results
    print("\n" + "="*60)
    print("COMPLETE RESULTS:")
    print("="*60)
    print(f"\nAnalysis keys: {list(analysis.keys())}")
    print(f"Scoring keys: {list(scoring_result.keys())}")
    print(f"Questions: {len(questions)}")

if __name__ == "__main__":
    asyncio.run(test_pipeline())
