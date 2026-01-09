# Investment Analysis ROI Data Fix - Summary

## Problem Identified
The Investment Analysis & ROI section in the frontend was displaying **static/default values** instead of calculated values based on the candidate's missing skills:

### Before Fix:
- Training Hours: 0
- Ramp-up Weeks: 2 (default)
- Time to Productivity: "2 weeks"
- Month 1: 30% (default)
- Month 3: 70% (default)
- Month 6: 90% (default)

### After Fix:
- Training Hours: 230 (calculated from missing skills)
- Ramp-up Weeks: 11 (calculated)
- Time to Productivity: "34 weeks"
- Month 1: 2% (calculated)
- Month 3: 56% (calculated)
- Month 6: 96% (calculated)

## Root Cause
The scorer agent's fallback JSON parsing logic was returning **empty `missing_skills` arrays** when:
1. JSON parsing from LLM response failed
2. Gaps field was missing from the JSON response
3. Missing_skills array was empty or null

This caused the training plan generator to receive empty gaps, resulting in `total_estimated_hours = 0`, which triggered the default ROI calculations.

## Solution Implemented

### File: `/backend/agents/scorer.py`

**Added method: `_extract_missing_skills()`**
- Extracts missing skills from LLM responses using multiple regex patterns
- Handles both natural language mentions (e.g., "missing: FastAPI") and JSON format
- Searches for common patterns: `missing`, `lack`, `no experience`, `needs`, etc.
- Supports 40+ common tech skills in pattern matching

**Modified method: `score()`**
- Enhanced fallback logic to always extract missing skills from LLM response text
- Even when JSON parsing fails, missing skills are extracted and populated
- When gaps exist in JSON but missing_skills is empty, extraction fills in the data

### Regex Patterns Added
```python
r'missing(?:\s+skills?)?:\s*([^.\n]*)'           # missing: FastAPI, Docker
r'not mentioned:\s*([^.\n]*)'                     # not mentioned: PostgreSQL
r'no(?:\s+\w+)?\s+(?:experience|expertise|background)?\s+(?:in|with):\s*([^.\n]*)'
r'lacks?(?:\s+(?:experience|expertise|background|knowledge))?(?:\s+(?:in|with))?\s*:?\s*([^.\n]*)'
r'needs?(?:\s+(?:experience|expertise|background|knowledge))?(?:\s+(?:in|with))?\s*:?\s*([^.\n]*)'
r'required\s+(?:but\s+)?(?:missing|absent):\s*([^.\n]*)'
r'lack(?:s|ing)?\s+(?:experience|expertise|background|knowledge)?\s+(?:in|with)?\s*([^.\n]*)'
```

## Data Flow Fix
```
Resume Evaluation
    ↓
Scorer Agent analyzes gaps
    ↓
LLM returns response with missing skills mentioned
    ↓
⭐ NEW: _extract_missing_skills() extracts skills from response text
    ↓
Gaps dict populated with actual missing_skills array
    ↓
Training Plan Generator receives populated gaps
    ↓
Creates training requirements with estimated hours
    ↓
Investment Summary uses actual hours to calculate ROI
    ↓
Frontend displays calculated Investment Analysis ✅
```

## Testing

Verified with end-to-end test:
- Input: Candidate with missing skills: ["FastAPI", "Docker", "Kubernetes", "PostgreSQL"]
- Training Plan: Correctly identifies 4 skills needing 230 hours total
- Investment Summary: Calculates ROI showing "34 weeks" break-even vs default "2 weeks"
- Productivity Projections: Month 1 = 2% (from missing skills) vs default 30%

## Impact
✅ Investment Analysis now shows dynamic, calculated ROI values
✅ Training hours, weeks, and costs accurately reflect missing skills
✅ Productivity projections adjust based on actual training burden
✅ Hiring recommendations better informed by realistic training investment
✅ Frontend displays accurate explainability data to users

## Files Modified
- `backend/agents/scorer.py` - Added gap extraction logic (+78 lines)

## Commit
`f3a59d6` - fix: Improve gap extraction to populate missing_skills for investment analysis
