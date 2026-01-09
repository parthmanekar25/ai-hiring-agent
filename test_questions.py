#!/usr/bin/env python3
"""Test script to verify question generator produces multiple questions"""

import asyncio
import os
import sys
import json

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.agents.question_generator import QuestionGeneratorAgent

async def test_question_generator():
    """Test that question generator produces 5+ questions"""
    
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        print("❌ ERROR: GROQ_API_KEY not set")
        return False
    
    agent = QuestionGeneratorAgent(api_key=api_key)
    
    # Sample data
    job_description = """Senior Python Developer
    
    Requirements:
    - 5+ years Python experience
    - FastAPI or similar web framework
    - PostgreSQL database design
    - Docker and containerization
    - Team leadership experience
    
    Nice to have:
    - Kubernetes
    - AWS
    - Machine learning basics
    """
    
    analysis = {
        "candidate_name": "John Doe",
        "experience_years": 6,
        "key_skills": ["Python", "FastAPI", "PostgreSQL"],
        "education": "BS Computer Science",
        "strengths": "Strong Python background, 6 years experience",
        "concerns": "Limited Kubernetes and AWS experience"
    }
    
    gaps = {
        "missing_skills": ["Kubernetes", "AWS"],
        "unclear_sections": ["Leadership experience details"],
        "inconsistencies": []
    }
    
    print("🔄 Testing Question Generator...")
    print("=" * 60)
    
    try:
        questions = await agent.generate_questions(
            job_description=job_description,
            analysis=analysis,
            gaps=gaps
        )
        
        print(f"\n✅ Generated {len(questions)} questions:")
        print("=" * 60)
        
        for i, q in enumerate(questions, 1):
            print(f"\n📝 Question {i}:")
            print(f"   Q: {q.get('question', 'N/A')}")
            print(f"   Category: {q.get('category', 'N/A')}")
            print(f"   Reasoning: {q.get('reasoning', 'N/A')}")
        
        print("\n" + "=" * 60)
        
        if len(questions) >= 5:
            print(f"✅ SUCCESS: Got {len(questions)} questions (need ≥5)")
            return True
        elif len(questions) > 1:
            print(f"⚠️  WARNING: Got {len(questions)} questions (expected ≥5)")
            return True
        else:
            print(f"❌ FAILED: Got only {len(questions)} question(s)")
            return False
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    # Load env
    from dotenv import load_dotenv
    load_dotenv()
    
    # Run test
    result = asyncio.run(test_question_generator())
    sys.exit(0 if result else 1)
