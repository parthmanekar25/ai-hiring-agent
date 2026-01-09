# CONDITIONAL_HIRE Investment Analysis - Troubleshooting Guide

## What Was the Problem?

For candidates with **CONDITIONAL_HIRE** recommendation (score 60-69), the Investment Analysis was showing **default values** instead of calculated values based on missing skills:

```
❌ BEFORE (Wrong):
- Investment Level: LOW
- Training Hours: 0
- Ramp-up Weeks: 2
- Time to Productivity: 2 weeks
- Month 1: 30% → Month 3: 70% → Month 6: 90%
```

## Root Cause

The LLM response for CONDITIONAL_HIRE candidates sometimes didn't explicitly mention missing skills, or the extraction didn't work properly. This caused:

1. `missing_skills[]` to be empty
2. `training_plan` to have 0 hours
3. `investment_summary` to default to LOW investment level with generic ROI

## The Fix - Multi-Layer Detection

### Layer 1: Backend - Scorer Agent (scorer.py)
- **Added:** `_infer_missing_skills()` method
- **Does:** Looks at skill_matches marked as `present: false` to identify gaps
- **Fallback:** If score < 75 but no gaps found, extracts from response text

### Layer 2: Backend - Integration Layer (integration.py)
- **Added:** Debug logging to trace gaps through pipeline
- **Does:** Ensures gaps dict always has all required fields
- **Logs:** Prints missing_skills count and names during processing

### Layer 3: Frontend - App (app.py)  
- **Added:** Frontend gap inference when score < 75
- **Does:** Checks skill_matches for skills marked as NOT present
- **Warning:** Shows `⚠️ Inferred missing skills:` when using fallback
- **Updates:** `interview_data['skill_analysis']['gaps']` with inferred skills

## How It Works Now

### For CONDITIONAL_HIRE (60-69) with Missing Skills:

```
1. LLM analyzes resume → Response identifies gaps
   ↓
2. Scorer extracts missing skills from response
   - If found: Returns extracted list
   - If not found: Uses _infer_missing_skills() fallback
   ↓
3. Training plan generates with actual hours
   - Example: 190 hours for 4 missing skills
   ↓
4. Investment summary calculates ROI
   - Break-even: 28 weeks (not default 2)
   - Month 1: 3% (not default 30%)
   ↓
5. Frontend receives calculated investment_summary
   ✅ Displays: "190 hours", "28 weeks", "3% → 59% → 95%"
```

### For CONDITIONAL_HIRE with No Clear Gaps:

```
If LLM truly found no gaps AND skill_matches are all present:
→ Investment Analysis correctly shows defaults (LOW, 2 weeks, 30%-70%-90%)
→ This is correct behavior when candidate has all required skills
```

## What to Look For

### ✅ Correct Behavior (After Fix)

**CONDITIONAL_HIRE with gaps:**
- Investment Level: MEDIUM/HIGH/VERY_HIGH (not LOW)
- Training Hours: > 0 (actual value calculated)
- Ramp-up Weeks: > 2 (based on hours)
- Time to Productivity: e.g., "28 weeks" (not "2 weeks")
- Month 1: < 30% (based on training burden)
- Month 3: > 70% (productivity curve)
- Month 6: > 90% (approaching full productivity)

**Visual indicator in Training Plan:**
- Should list actual skills needing training
- Should show hours for each skill
- Example: "Python: 80 hours", "Docker: 30 hours", etc.

**Console warnings (if inferred):**
- May see: `⚠️ Inferred missing skills: Docker, Kubernetes, PostgreSQL`
- This means fallback inference worked

### ❌ Problem Indicators

If you still see defaults with CONDITIONAL_HIRE score:
- Training Hours: 0
- Ramp-up Weeks: 2
- Month 1: 30%
- Month 3: 70%
- Month 6: 90%

**Then check:**
1. Is the candidate's score actually 60-69? (CONDITIONAL_HIRE range)
2. Do the skill_matches show any `present: false`?
3. Check backend logs for extracted missing_skills

## How to Test the Fix

### Test Case 1: CONDITIONAL_HIRE with Clear Gaps

**Resume:** Missing Docker, Kubernetes, FastAPI, PostgreSQL
**Score:** 65/100 (CONDITIONAL_HIRE)
**Expected Result:**
- Training Hours: ~190
- Ramp-up Weeks: ~9  
- Time to Productivity: ~28 weeks
- Month 1: ~3%
- Month 3: ~59%
- Month 6: ~95%

### Test Case 2: CONDITIONAL_HIRE No Clear Gaps

**Resume:** Has all mentioned skills
**Score:** 65/100 (experience/education fit issues, not technical)
**Expected Result:**
- Training Hours: 0
- Ramp-up Weeks: 2
- Time to Productivity: 2 weeks
- Month 1: 30%
- Investment Level: LOW (correctly)

### Test Case 3: STRONG_HIRE

**Resume:** Excellent fit, >75 score
**Expected Result:**
- Investment Level: LOW
- Training Hours: 0
- Time to Productivity: 2 weeks (correct, no training needed)

## Debugging Steps

If Investment Analysis still shows defaults for CONDITIONAL_HIRE:

### Step 1: Check Backend Logs
Look for these debug lines:
```
📊 DEBUG: Processing [Candidate Name]
   Overall Score: 65
   Missing Skills Count: 4
   Missing Skills: ['Docker', 'Kubernetes', 'FastAPI', 'PostgreSQL']
```

If Missing Skills Count is 0 → Gap extraction failed

### Step 2: Check Skill Matches
In the UI, look at "⚠️ Gaps & Concerns" section:
- Should show missing skills if any
- If empty, candidate may have all skills

### Step 3: Check Training Plan
If it shows "No specific skill matches analyzed":
- Skill matching failed
- This might be causing gap detection to fail too

## Code Changes Made

**File: `/backend/agents/scorer.py`**
- Added `_infer_missing_skills()` method (25 lines)
- Enhanced gap handling in `score()` method (10 lines)

**File: `/backend/explainability/integration.py`**
- Added debug logging (8 lines)
- Enhanced gaps structure validation (7 lines)

**File: `/frontend/app.py`**
- Added frontend gap inference (15 lines)
- Added warning for inferred gaps (3 lines)

## Expected Outcomes

After this fix, **CONDITIONAL_HIRE candidates should**:

✅ Show calculated investment values when they have missing skills
✅ Show default investment values only when they have no real gaps
✅ Have accurate ROI projections based on training needs
✅ Display training plans with actual skill requirements
✅ Have explainability data that matches their actual needs

## Next Steps if Still Not Working

1. **Restart backend:**
   ```bash
   Ctrl+C (stop current)
   uvicorn backend.main:app --reload
   ```

2. **Clear frontend cache:**
   - Refresh browser (Cmd+R or Ctrl+R)

3. **Re-run evaluation:**
   - Upload resume again
   - Observe debug output

4. **Check specific score range:**
   - CONDITIONAL_HIRE is 60-69
   - Check that your score is in this range
   - If > 69 → HIRE_WITH_TRAINING (different rules)
   - If < 60 → RECONSIDER (different rules)

---

**Fix Version:** Commit 5dfc831
**Date:** January 9, 2026
**Status:** Active (multi-layer detection enabled)
