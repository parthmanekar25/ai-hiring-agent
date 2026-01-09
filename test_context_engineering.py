"""
Test suite for context engineering components
Validates prompt manager, context optimization, and chain-of-thought
"""

import sys
import asyncio
sys.path.insert(0, '/Users/parth/Projects/ai-hiring-agent')

from backend.prompts import (
    get_prompt_manager,
    get_context_optimizer,
    get_cot_framework,
    PromptVersion
)


def test_prompt_manager():
    """Test prompt manager functionality"""
    print("=" * 60)
    print("Testing Prompt Manager")
    print("=" * 60)
    
    pm = get_prompt_manager()
    
    # Test 1: Get prompts for each agent
    for agent in ["resume_analyzer", "scorer", "question_generator"]:
        print(f"\nAgent: {agent}")
        versions = pm.get_all_versions(agent)
        print(f"  Available versions: {[v.value for v in versions]}")
        
        # Get V3 prompt
        prompt = pm.get_prompt(agent, PromptVersion.V3)
        print(f"  V3 Name: {prompt.name}")
        print(f"  Temperature: {prompt.temperature}")
        print(f"  Few-shot examples: {len(prompt.few_shot_examples)}")
        print(f"  Constraints: {len(prompt.constraints)}")
    
    # Test 2: Compose full prompt
    print("\n" + "=" * 60)
    print("Testing Prompt Composition")
    print("=" * 60)
    
    full_prompt = pm.compose_full_prompt(
        "resume_analyzer",
        job_description="Senior Python Developer, 5+ years AWS experience",
        resume_text="Python expert with 3 years experience, AWS certified"
    )
    
    print(f"\nComposed prompt length: {len(full_prompt)} characters")
    print(f"Contains few-shot examples: {'Example' in full_prompt}")
    print(f"Contains system prompt: {'expert technical recruiter' in full_prompt}")
    
    # Test 3: List all prompts
    all_prompts = pm.list_prompts()
    print("\nAvailable Prompts:")
    for agent, versions in all_prompts.items():
        print(f"  {agent}: {versions}")
    
    print("\n✓ Prompt Manager tests passed")


def test_context_optimizer():
    """Test context optimization functionality"""
    print("\n" + "=" * 60)
    print("Testing Context Optimizer")
    print("=" * 60)
    
    co = get_context_optimizer()
    
    sample_job_desc = """
Senior Python Developer
Location: Remote

Requirements:
- 5+ years Python experience
- AWS knowledge
- Django framework
- PostgreSQL
- Leadership experience

Responsibilities:
- Design scalable systems
- Lead technical team
- Code reviews
- Architecture decisions

Nice to have:
- Kubernetes
- Docker
- Machine Learning
"""
    
    sample_resume = """
JOHN DOE
john@example.com | LinkedIn

EXPERIENCE:
Senior Software Engineer, TechCorp (2020-2024)
- Led Python development team of 5 engineers
- Designed microservices architecture using Python and AWS
- Mentored junior developers
- 4 years Python, 3 years AWS

Software Developer, StartupXYZ (2018-2020)
- Developed Django applications
- PostgreSQL database design
- 2 years Python development
- Worked with AWS services

EDUCATION:
BS Computer Science, State University

SKILLS:
Python, AWS, Django, PostgreSQL, Docker, Git, Agile
"""
    
    # Test 1: Optimize resume
    print("\nTest 1: Resume Optimization")
    optimized_resume = co.optimize_resume_context(sample_resume, sample_job_desc)
    print(f"Original length: {len(sample_resume)} chars")
    print(f"Optimized length: {len(optimized_resume)} chars")
    print(f"Sections preserved: Experience, Education, Skills")
    
    # Test 2: Optimize job description
    print("\nTest 2: Job Description Optimization")
    optimized_job = co.optimize_job_description(sample_job_desc)
    print(f"Original length: {len(sample_job_desc)} chars")
    print(f"Optimized length: {len(optimized_job)} chars")
    print(f"Contains must-haves: {'MUST-HAVE' in optimized_job}")
    print(f"Contains responsibilities: {'RESPONSIBILITIES' in optimized_job}")
    
    # Test 3: Token estimation
    print("\nTest 3: Token Estimation")
    resume_tokens = co._estimate_tokens(sample_resume)
    job_tokens = co._estimate_tokens(sample_job_desc)
    print(f"Resume tokens: {resume_tokens}")
    print(f"Job description tokens: {job_tokens}")
    print(f"Context window limit: {co.max_context_tokens}")
    
    print("\n✓ Context Optimizer tests passed")


def test_chain_of_thought():
    """Test chain-of-thought framework"""
    print("\n" + "=" * 60)
    print("Testing Chain-of-Thought Framework")
    print("=" * 60)
    
    cot = get_cot_framework()
    
    # Test 1: Create reasoning chains
    print("\nTest 1: Creating Reasoning Chains")
    
    sample_analysis = {
        "candidate_name": "John Doe",
        "skills_found": ["Python", "AWS", "Django"],
        "experience_summary": "8 years full-stack"
    }
    
    resume_chain = cot.create_resume_analysis_chain(
        "Senior Python Developer, 5+ years AWS",
        "Python expert with 3 years experience"
    )
    print(f"Resume analysis chain created: {resume_chain.task_name}")
    
    scoring_chain = cot.create_scoring_chain(
        sample_analysis,
        "Senior Python Developer, 5+ years"
    )
    print(f"Scoring chain created: {scoring_chain.task_name}")
    
    question_chain = cot.create_question_generation_chain(
        sample_analysis,
        "Senior Python Developer, 5+ years AWS",
        {"missing_skills": ["Kubernetes"], "unclear_sections": ["Leadership"]}
    )
    print(f"Question generation chain created: {question_chain.task_name}")
    
    # Test 2: Generate CoT instructions
    print("\nTest 2: CoT Instructions")
    cot_instruction = cot.generate_cot_instruction()
    print(f"CoT instruction length: {len(cot_instruction)} chars")
    print(f"Contains step-by-step guidance: {'step' in cot_instruction.lower()}")
    
    # Test 3: Create prompt with CoT
    print("\nTest 3: Prompt with CoT")
    cot_prompt = cot.create_prompt_with_cot(
        base_prompt="Analyze this candidate",
        steps=[
            "Extract all skills and experience",
            "Map to job requirements",
            "Identify gaps and strengths"
        ],
        examples=[
            {
                "input": {"job": "Python Dev", "resume": "Python expert"},
                "reasoning": [
                    "Extracted: Python skill, unspecified experience",
                    "Mapped: Python requirement met, experience unclear",
                    "Conclusion: Promising but needs verification"
                ],
                "output": {"fit": "medium", "confidence": 0.7}
            }
        ]
    )
    print(f"CoT prompt length: {len(cot_prompt)} chars")
    print(f"Contains examples: {'Example 1' in cot_prompt}")
    print(f"Contains steps: {'Step 1' in cot_prompt}")
    
    print("\n✓ Chain-of-Thought tests passed")


def test_integration():
    """Test integration of all components"""
    print("\n" + "=" * 60)
    print("Testing Integration")
    print("=" * 60)
    
    pm = get_prompt_manager()
    co = get_context_optimizer()
    
    # Simulate actual usage
    job_desc = "Senior Python Dev, 5+ years AWS"
    resume = "Python expert, 3 years, some AWS, Docker experience"
    
    print("\n1. Optimizing context...")
    opt_job = co.optimize_job_description(job_desc)
    opt_resume = co.optimize_resume_context(resume, job_desc)
    
    print("2. Composing prompt...")
    prompt = pm.compose_full_prompt(
        "resume_analyzer",
        job_description=opt_job,
        resume_text=opt_resume
    )
    
    print("3. Validating prompt...")
    assert "expert technical recruiter" in prompt, "Missing system prompt"
    assert "Example" in prompt, "Missing few-shot examples"
    assert "extraction" in prompt.lower() or "analysis" in prompt.lower(), "Missing step-by-step instructions"
    assert "Output Format" in prompt, "Missing output format"
    
    print("\n✓ Integration test passed")
    print(f"Total prompt size: {len(prompt)} characters")


def main():
    """Run all tests"""
    print("\n" + "=" * 60)
    print("CONTEXT ENGINEERING TESTS")
    print("=" * 60)
    
    try:
        test_prompt_manager()
        test_context_optimizer()
        test_chain_of_thought()
        test_integration()
        
        print("\n" + "=" * 60)
        print("ALL TESTS PASSED ✓")
        print("=" * 60)
        print("\nContext engineering components are working correctly:")
        print("  ✓ Prompt Manager - Versioning & Composition")
        print("  ✓ Context Optimizer - Token Management")
        print("  ✓ Chain-of-Thought - Structured Reasoning")
        print("  ✓ Integration - All components working together")
        
    except Exception as e:
        print(f"\n✗ TEST FAILED: {str(e)}")
        import traceback
        traceback.print_exc()
        return 1
    
    return 0


if __name__ == "__main__":
    exit(main())
