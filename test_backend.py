#!/usr/bin/env python3
"""Test backend API endpoints"""

import requests
import json
import time

BACKEND_URL = "http://localhost:8000"

def test_health():
    """Test health endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        if response.status_code == 200:
            print("✅ Backend is healthy:", response.json())
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Cannot connect to backend: {e}")
        return False

def test_evaluation():
    """Test evaluation endpoint with minimal data"""
    print("\n🔍 Testing evaluation endpoint...")
    
    job_description = """
    We are looking for a Python developer with:
    - 3+ years of Python experience
    - FastAPI knowledge
    - PostgreSQL experience
    - Docker/Kubernetes
    """
    
    # Create minimal test resume
    resume_text = """
    John Doe
    Senior Python Developer
    
    Experience:
    - 5 years Python development
    - FastAPI REST API development
    - PostgreSQL database management
    - AWS and Docker deployment
    
    Skills: Python, FastAPI, PostgreSQL, Docker, AWS, Git
    """
    
    files = [("resumes", ("test_resume.txt", resume_text.encode(), "text/plain"))]
    data = {"job_description": job_description}
    
    try:
        print("  Sending evaluation request...")
        response = requests.post(
            f"{BACKEND_URL}/api/evaluate",
            files=files,
            data=data,
            timeout=120
        )
        
        print(f"  Response status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            evals = result.get("evaluations", [])
            print(f"✅ Evaluation endpoint is working!")
            print(f"   - Evaluations returned: {len(evals)}")
            if evals:
                eval_data = evals[0]
                print(f"   - Candidate: {eval_data.get('candidate_name')}")
                score = eval_data.get('score', {})
                print(f"   - Overall Score: {score.get('overall_score')}/100")
                processing_time = result.get('processing_time', 0)
                print(f"   - Processing time: {processing_time:.1f}s")
            elif "Rate limit" in response.text or "rate_limit" in response.text:
                print(f"   ⚠️ Groq API rate limit exceeded!")
                print(f"      Your free tier (100,000 tokens/day) is exhausted.")
                print(f"      Please wait a few minutes or upgrade to Dev Tier at:")
                print(f"      https://console.groq.com/settings/billing")
                return False
            else:
                print(f"   ⚠️ No evaluations returned (check backend logs)")
            return len(evals) > 0
        else:
            print(f"❌ Evaluation failed: {response.status_code}")
            print(f"   Response: {response.text[:500]}")
            return False
            
    except requests.exceptions.Timeout:
        print("❌ Request timed out")
        return False
    except Exception as e:
        print(f"❌ Error during evaluation: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("AI HIRING AGENT - BACKEND TEST")
    print("=" * 60)
    
    # Test health
    if not test_health():
        print("\n❌ Backend is not running. Please start it with:")
        print("   cd /Users/parth/Projects/ai-hiring-agent")
        print("   source .venv/bin/activate")
        print("   uvicorn backend.main:app --reload")
        exit(1)
    
    # Test evaluation
    success = test_evaluation()
    
    print("\n" + "=" * 60)
    if success:
        print("✅ ALL TESTS PASSED")
    else:
        print("❌ TESTS FAILED - Check backend logs")
        print("   tail -50 /Users/parth/Projects/ai-hiring-agent/backend.log")
    print("=" * 60)
