RESUME_ANALYSIS_PROMPT = """You are an expert technical recruiter analyzing a candidate's resume.

Job Description:
{job_description}

Candidate Resume:
{resume_text}

Analyze this resume thoroughly and provide:

1. Extract the candidate's name (if present)
2. Identify all relevant skills mentioned
3. Assess experience level and relevance
4. Note education background
5. Identify any red flags, inconsistencies, or unclear sections
6. Look beyond keyword matching - assess actual demonstrated experience

Be critical and thorough. Don't be fooled by keyword stuffing. Look for concrete examples and achievements.

Provide your analysis in a structured format."""

SCORING_PROMPT = """You are scoring a candidate's fit for a position.

Job Description:
{job_description}

Resume Analysis:
{analysis}

Score the candidate on a 0-100 scale for:
1. Overall Fit
2. Technical Skills Match
3. Experience Relevance
4. Education Fit

For each score, provide clear reasoning. Be consistent - similar candidates should receive similar scores.

Consider:
- Actual demonstrated experience vs. just keywords
- Relevance and recency of experience
- Quality over quantity
- Red flags or inconsistencies

Return your scores with detailed reasoning."""

QUESTION_GENERATION_PROMPT = """You are preparing targeted interview questions for a candidate.

Job Description:
{job_description}

Resume Analysis:
{analysis}

Gaps and Concerns:
{gaps}

Generate 5-7 targeted interview questions that:
1. Probe unclear or vague claims on the resume
2. Test depth of knowledge in claimed skills
3. Address experience gaps
4. Clarify inconsistencies
5. Assess cultural fit for the role

Each question should have a clear purpose. Avoid generic questions."""