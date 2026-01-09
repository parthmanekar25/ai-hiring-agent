#!/usr/bin/env python3
"""
Validation script to verify the investment analysis fix is working correctly
Run this to ensure missing_skills are properly extracted and investment summary is calculated
"""

import sys
import os
import json

# Add backend to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def validate_extraction():
    """Validate that gap extraction is working"""
    print("=" * 80)
    print("🔍 VALIDATION 1: Gap Extraction from LLM Response")
    print("=" * 80 + "\n")
    
    from backend.agents.scorer import ScorerAgent
    
    scorer = ScorerAgent(api_key="test")
    
    # Test with sample LLM response
    llm_response = """
    The candidate has Python experience but is missing critical skills in Docker, Kubernetes, 
    and PostgreSQL. They lack AWS expertise and no mention of FastAPI in their resume.
    Overall technical fit is 68/100 due to these gaps.
    """
    
    extracted = scorer._extract_missing_skills(llm_response)
    
    print(f"LLM Response: {llm_response.strip()}\n")
    print(f"Extracted Missing Skills: {extracted}\n")
    
    expected = ["Docker", "Kubernetes", "PostgreSQL", "AWS", "FastAPI"]
    if all(skill in extracted for skill in expected):
        print("✅ PASS: All expected skills were extracted\n")
        return True
    else:
        print(f"❌ FAIL: Expected {expected}, got {extracted}\n")
        return False

def validate_investment_calculation():
    """Validate that investment summary calculates correctly with gaps"""
    print("=" * 80)
    print("📊 VALIDATION 2: Investment Summary Calculation with Gaps")
    print("=" * 80 + "\n")
    
    from backend.explainability.explainability_generator import ExplainabilityGenerator
    
    generator = ExplainabilityGenerator()
    
    # Test with gaps
    gaps = {
        "missing_skills": ["Docker", "Kubernetes", "PostgreSQL"],
        "unclear_sections": [],
        "inconsistencies": []
    }
    
    training_plan = generator.generate_training_plan(gaps=gaps, experience_level="mid")
    investment = generator.generate_investment_summary(
        overall_score=75,
        training_plan=training_plan,
        experience_fit=0.8,
        technical_fit=0.7
    )
    
    total_hours = training_plan['summary']['total_estimated_hours']
    training_hours = investment['breakdown']['training_hours']
    ramp_weeks = investment['breakdown']['ramp_up_weeks']
    
    print(f"Input Gaps: {gaps['missing_skills']}")
    print(f"Total Training Hours Calculated: {total_hours}\n")
    print(f"Investment Summary Breakdown:")
    print(f"  - Training Hours: {training_hours}")
    print(f"  - Ramp-up Weeks: {ramp_weeks}")
    print(f"  - Time to Productivity: {investment['breakdown']['time_to_productivity']}")
    print(f"  - Investment Level: {investment['investment_level']}\n")
    
    # Validate
    if total_hours > 0 and training_hours == total_hours and ramp_weeks > 2:
        print("✅ PASS: Investment summary correctly calculated from gaps\n")
        return True
    else:
        print(f"❌ FAIL: Investment not calculated correctly\n")
        return False

def validate_empty_gaps():
    """Validate that default values appear when no gaps"""
    print("=" * 80)
    print("📊 VALIDATION 3: Default Values When No Gaps")
    print("=" * 80 + "\n")
    
    from backend.explainability.explainability_generator import ExplainabilityGenerator
    
    generator = ExplainabilityGenerator()
    
    # Test without gaps
    gaps = {
        "missing_skills": [],
        "unclear_sections": [],
        "inconsistencies": []
    }
    
    training_plan = generator.generate_training_plan(gaps=gaps, experience_level="mid")
    investment = generator.generate_investment_summary(
        overall_score=90,
        training_plan=training_plan,
        experience_fit=0.9,
        technical_fit=0.85
    )
    
    total_hours = training_plan['summary']['total_estimated_hours']
    ramp_weeks = investment['breakdown']['ramp_up_weeks']
    month_1_productivity = investment['roi_analysis']['productivity_by_month']['month_1']
    
    print(f"Input Gaps: {gaps['missing_skills']} (empty)")
    print(f"Total Training Hours: {total_hours}\n")
    print(f"Investment Summary with No Gaps:")
    print(f"  - Training Hours: {total_hours}")
    print(f"  - Ramp-up Weeks: {ramp_weeks} (default)")
    print(f"  - Month 1 Productivity: {month_1_productivity}")
    print(f"  - Investment Level: {investment['investment_level']}\n")
    
    if total_hours == 0 and ramp_weeks == 2 and month_1_productivity == "30%":
        print("✅ PASS: Default values shown when no gaps\n")
        return True
    else:
        print(f"❌ FAIL: Default values not correct\n")
        return False

def main():
    """Run all validation checks"""
    print("\n")
    print("█" * 80)
    print("█" + " " * 78 + "█")
    print("█" + "  AI HIRING AGENT - INVESTMENT ANALYSIS FIX VALIDATION".center(78) + "█")
    print("█" + " " * 78 + "█")
    print("█" * 80)
    print()
    
    results = []
    
    try:
        results.append(("Gap Extraction", validate_extraction()))
    except Exception as e:
        print(f"❌ ERROR in gap extraction: {e}\n")
        results.append(("Gap Extraction", False))
    
    try:
        results.append(("Investment Calculation (with gaps)", validate_investment_calculation()))
    except Exception as e:
        print(f"❌ ERROR in investment calculation: {e}\n")
        results.append(("Investment Calculation (with gaps)", False))
    
    try:
        results.append(("Default Values (no gaps)", validate_empty_gaps()))
    except Exception as e:
        print(f"❌ ERROR in default values: {e}\n")
        results.append(("Default Values (no gaps)", False))
    
    # Summary
    print("=" * 80)
    print("📋 VALIDATION SUMMARY")
    print("=" * 80 + "\n")
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    print()
    print(f"Total: {passed}/{total} validations passed\n")
    
    if passed == total:
        print("█" * 80)
        print("█" + "✅ ALL VALIDATIONS PASSED - FIX IS WORKING CORRECTLY".center(78) + "█")
        print("█" * 80)
        return 0
    else:
        print("█" * 80)
        print("█" + "❌ SOME VALIDATIONS FAILED - REVIEW ERROR MESSAGES".center(78) + "█")
        print("█" * 80)
        return 1

if __name__ == "__main__":
    sys.exit(main())
