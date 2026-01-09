# Testing CONDITIONAL_HIRE Investment Analysis Fix

## Quick Start

### 1. Start the Backend
```bash
cd /Users/parth/Projects/ai-hiring-agent
uvicorn backend.main:app --reload
```
**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 2. Start the Frontend
```bash
cd /Users/parth/Projects/ai-hiring-agent
streamlit run frontend/app.py
```
**Expected output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### 3. Keep Backend Terminal Open
You'll see debug output here during evaluation:
```
📊 DEBUG: Processing [Candidate Name]
   Overall Score: 65
   Missing Skills Count: 4
   Missing Skills: ['Docker', 'Kubernetes', 'FastAPI', 'PostgreSQL']
```

---

## Test Case 1: CONDITIONAL_HIRE with Clear Skill Gaps

### Candidate Profile
- **Title:** Mid-level Python Developer
- **Experience:** 4 years Python
- **Missing:** Docker, Kubernetes, CI/CD, React
- **Expected Score:** 62-68 (CONDITIONAL_HIRE)

### Test Resume Text
```
SOFTWARE ENGINEER
Experience: 4 years

Technologies: Python, Django, PostgreSQL, Git, Linux, AWS S3

Projects:
- Built REST APIs with Django and PostgreSQL
- Deployed on AWS using Elastic Beanstalk
- Wrote unit tests and integration tests
- Created data processing scripts

Skills: Python (expert), Django (advanced), PostgreSQL (advanced)
```

### What Should Happen

**Backend Terminal (Watch for this):**
```
📊 DEBUG: Processing [Test Candidate]
   Overall Score: 64
   Missing Skills Count: 4
   Missing Skills: ['Docker', 'Kubernetes', 'React', 'CI/CD']
```

**Frontend - Investment Analysis Section:**

✅ **CORRECT** (After Fix):
```
Investment Level: MEDIUM
Training Hours: 160 hours
Ramp-up Weeks: 8 weeks
Time to Productivity: 24 weeks

Training Plan:
├─ Docker: 40 hours
├─ Kubernetes: 50 hours  
├─ React: 40 hours
└─ CI/CD: 30 hours

ROI Projection:
├─ Month 1: 5% → productivity
├─ Month 3: 62% → productivity
└─ Month 6: 92% → productivity
```

❌ **WRONG** (Before Fix):
```
Investment Level: LOW
Training Hours: 0 hours
Ramp-up Weeks: 2 weeks
Time to Productivity: 2 weeks
Month 1: 30% / Month 3: 70% / Month 6: 90%
```

---

## Test Case 2: CONDITIONAL_HIRE with No Clear Gaps

### Candidate Profile
- **Title:** Senior Python Developer
- **Experience:** 8 years with all key skills
- **Issue:** Education background not typical (bootcamp instead of CS degree)
- **Expected Score:** 65-68 (still CONDITIONAL_HIRE but for non-technical reasons)

### Test Resume Text
```
SENIOR SOFTWARE ENGINEER
Experience: 8 years

Technologies: Python, FastAPI, Docker, Kubernetes, PostgreSQL, 
React, CI/CD (Jenkins, GitLab CI), AWS, Microservices

Key Achievements:
- Architected microservices system with 50+ Docker containers
- Implemented Kubernetes orchestration for 99.9% uptime
- Led team of 5 engineers
- Mentored junior developers

Certifications: AWS Solutions Architect, Kubernetes Administration
Education: Coding Bootcamp (not traditional CS degree)
```

### What Should Happen

**Backend Terminal:**
```
📊 DEBUG: Processing [Senior Candidate]
   Overall Score: 67
   Missing Skills Count: 0
   Missing Skills: []
```

**Frontend - Investment Analysis:**

✅ **CORRECT** (This is fine):
```
Investment Level: LOW
Training Hours: 0 hours
Ramp-up Weeks: 2 weeks
Time to Productivity: 2 weeks (no training needed)

ROI Projection:
├─ Month 1: 30% → productivity
├─ Month 3: 70% → productivity
└─ Month 6: 90% → productivity
```

This is **correct** because the candidate has all technical skills. The CONDITIONAL_HIRE score is due to education/background, not skills.

---

## Test Case 3: STRONG_HIRE (Baseline)

### Expected Behavior
- Score: > 75
- Investment Level: LOW (always, no training needed)
- Training Hours: 0
- Should NOT trigger inference logic

---

## What to Verify After Running Tests

### ✅ Fix Verification Checklist

1. **Backend Inference Working:**
   - [ ] Backend terminal shows debug output with Missing Skills
   - [ ] Count > 0 when candidate missing skills
   - [ ] Count = 0 when candidate has all skills

2. **Investment Summary Calculated:**
   - [ ] Training Hours > 0 when gaps exist
   - [ ] Investment Level not always "LOW"
   - [ ] Ramp-up weeks calculated based on hours
   - [ ] Break-even weeks calculated correctly

3. **ROI Projection Reasonable:**
   - [ ] Month 1 < 30% when training needed (not default 30%)
   - [ ] Month 3 > 50% when training needed (not default 70%)
   - [ ] Month 6 > 85% when training needed (not default 90%)

4. **Frontend Inference Warning:**
   - [ ] See `⚠️ Inferred missing skills: [list]` when fallback used
   - [ ] Warning only appears for score < 75
   - [ ] Warning doesn't appear for STRONG_HIRE

5. **Training Plan Details:**
   - [ ] Shows individual skills with hours
   - [ ] Total hours matches investment summary
   - [ ] Only appears when gaps exist

---

## Debugging Output Examples

### Example 1: Good Gap Extraction
```
Backend terminal shows:
📊 DEBUG: Processing Jane Doe
   Overall Score: 64
   Missing Skills Count: 3
   Missing Skills: ['Docker', 'Kubernetes', 'PostgreSQL']

Frontend shows:
✅ Investment Level: MEDIUM
✅ Training Hours: 120
✅ Training Plan lists skills with hours
✅ ROI projection curves show training impact
```

### Example 2: Inference Working (Fallback)
```
Backend terminal shows:
📊 DEBUG: Processing John Smith
   Overall Score: 62
   Missing Skills Count: 0
   Missing Skills: []

Frontend shows:
⚠️ Inferred missing skills: React, TypeScript
✅ Investment Level: MEDIUM (inferred)
✅ Training Hours: 100 (inferred)
```

### Example 3: Problem Indicator
```
Backend shows:
📊 DEBUG: Processing Bob Wilson
   Overall Score: 64  ← Should have training
   Missing Skills Count: 0
   Missing Skills: []

Frontend shows:
❌ Investment Level: LOW ← Should be MEDIUM
❌ Training Hours: 0 ← Should be > 0
❌ No ⚠️ warning about inference
```
**If you see this: Check if skill_matches in evaluation have `present: true/false` data**

---

## Common Issues & Solutions

### Issue 1: Still Seeing Defaults for CONDITIONAL_HIRE

**Symptom:**
- Score: 64 (CONDITIONAL_HIRE)
- Training Hours: 0
- Investment Level: LOW

**Check:**
1. Restart backend: `Ctrl+C` then `uvicorn backend.main:app --reload`
2. Refresh frontend: `Cmd+R`
3. Re-upload resume
4. Check backend terminal for debug output

### Issue 2: Backend Terminal Empty

**Symptom:**
- No debug output in backend terminal
- Can't see what skills were extracted

**Check:**
1. Confirm backend still running
2. Check for error messages in backend
3. Try simpler test resume
4. Check if API is receiving requests

### Issue 3: Frontend Warning Doesn't Appear

**Symptom:**
- No `⚠️ Inferred missing skills:` warning
- But Investment Level shows correct value

**Note:**
- This is OK. Warning is optional indicator.
- Backend inference might have worked (don't need frontend fallback)
- Or all skills were present (no inference needed)

### Issue 4: Investment Hours Too High

**Symptom:**
- Training Hours: 500+ (seems unrealistic)
- Ramp-up Weeks: 25+ (seems very long)

**Check:**
1. How many skills are truly missing?
2. Are some skills marked multiple times?
3. Is estimate per-skill reasonable (20-50 hours typical)?

---

## Success Criteria

The fix is **working correctly** if:

✅ CONDITIONAL_HIRE candidates with gaps show **Investment Level ≥ MEDIUM**
✅ Training Hours are **> 0** when gaps exist
✅ ROI curves show **realistic training impact** (Month 1 low, ramping up)
✅ Backend debug logs show **extracted or inferred skills**
✅ Defaults are only used when **genuinely no gaps exist**

---

## After Testing

If all tests pass:
1. Test with real resume samples
2. Monitor a few live evaluations
3. Verify explainability messages align with investment data
4. Confirm hiring team sees accurate metrics

If issues persist:
1. Note the exact score and skills shown
2. Check backend debug output
3. Verify skill_matches structure in response
4. Review CONDITIONAL_HIRE_FIX.md troubleshooting section

---

**Last Updated:** January 9, 2026
**Fix Status:** Active (Commit 5dfc831)
**Testing Guide Version:** 1.0
