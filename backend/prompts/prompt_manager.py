"""
Centralized Prompt Manager for AI Hiring Agent
Handles prompt versioning, composition, and management
"""

from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from enum import Enum
import json


class PromptVersion(str, Enum):
    """Prompt versions for A/B testing and iteration"""
    V1 = "v1"  # Initial version
    V2 = "v2"  # Enhanced with few-shot examples
    V3 = "v3"  # Chain-of-thought reasoning


@dataclass
class PromptTemplate:
    """Structured prompt template"""
    name: str
    version: PromptVersion
    system_prompt: str
    task_prompt: str
    few_shot_examples: List[Dict[str, Any]]
    output_format: str
    constraints: List[str]
    temperature: float
    description: str


class PromptManager:
    """Manages all prompts with versioning and composition"""
    
    def __init__(self):
        self.prompts: Dict[str, Dict[str, PromptTemplate]] = {}
        self._load_all_prompts()
    
    def _load_all_prompts(self):
        """Load all prompt templates"""
        self.prompts["resume_analyzer"] = self._get_resume_analyzer_prompts()
        self.prompts["scorer"] = self._get_scorer_prompts()
        self.prompts["question_generator"] = self._get_question_generator_prompts()
    
    def get_prompt(
        self,
        agent_name: str,
        version: PromptVersion = PromptVersion.V3
    ) -> PromptTemplate:
        """Get a specific prompt template"""
        if agent_name not in self.prompts:
            raise ValueError(f"Unknown agent: {agent_name}")
        
        if version not in self.prompts[agent_name]:
            # Fallback to latest version
            versions = list(self.prompts[agent_name].keys())
            latest = sorted(versions, reverse=True)[0]
            return self.prompts[agent_name][latest]
        
        return self.prompts[agent_name][version]
    
    def compose_full_prompt(
        self,
        agent_name: str,
        **kwargs
    ) -> str:
        """Compose full prompt from template"""
        prompt = self.get_prompt(agent_name)
        
        full_prompt = f"{prompt.system_prompt}\n\n"
        
        # Add few-shot examples if using V2+
        if prompt.version in [PromptVersion.V2, PromptVersion.V3]:
            full_prompt += self._format_few_shot_examples(
                prompt.few_shot_examples
            ) + "\n\n"
        
        # Add task-specific prompt
        full_prompt += prompt.task_prompt.format(**kwargs) + "\n\n"
        
        # Add output format instructions
        full_prompt += f"Output Format:\n{prompt.output_format}\n\n"
        
        # Add constraints
        full_prompt += "Constraints:\n"
        for constraint in prompt.constraints:
            full_prompt += f"- {constraint}\n"
        
        return full_prompt
    
    def _format_few_shot_examples(
        self,
        examples: List[Dict[str, Any]]
    ) -> str:
        """Format few-shot examples for prompt"""
        formatted = "## Few-Shot Examples:\n\n"
        
        for i, example in enumerate(examples, 1):
            formatted += f"### Example {i}:\n"
            formatted += f"Input:\n{json.dumps(example.get('input', {}), indent=2)}\n\n"
            formatted += f"Output:\n{json.dumps(example.get('output', {}), indent=2)}\n\n"
        
        return formatted
    
    def _get_resume_analyzer_prompts(self) -> Dict[str, PromptTemplate]:
        """Resume Analyzer prompts"""
        return {
            PromptVersion.V1: PromptTemplate(
                name="resume_analyzer_v1",
                version=PromptVersion.V1,
                system_prompt="""You are an expert technical recruiter with 15+ years of experience.
Your role is to analyze resumes with extreme attention to detail.
Focus on concrete achievements and demonstrated experience, not buzzwords.
Identify red flags, inconsistencies, and keyword stuffing attempts.""",
                task_prompt="""Analyze this resume against the job description.

Job Description:
{job_description}

Resume Text:
{resume_text}

Provide a detailed analysis.""",
                few_shot_examples=[],
                output_format="""{
    "candidate_name": "string",
    "skills_found": ["skill1", "skill2"],
    "experience_summary": "string",
    "education": "string",
    "strengths": ["strength1", "strength2"],
    "concerns": ["concern1", "concern2"],
    "keyword_stuffing_detected": boolean,
    "overall_impression": "string"
}""",
                constraints=[
                    "Be critical and thorough",
                    "Look for concrete examples, not just keywords",
                    "Note any vague or unsubstantiated claims",
                    "Identify inconsistencies in timeline or experience",
                    "Flag overly generic language",
                ],
                temperature=0.3,
                description="Basic resume analysis"
            ),
            PromptVersion.V3: PromptTemplate(
                name="resume_analyzer_v3",
                version=PromptVersion.V3,
                system_prompt="""You are an expert technical recruiter with 15+ years of experience.
Your role is to analyze resumes with extreme attention to detail.
Focus on concrete achievements and demonstrated experience, not buzzwords.
Identify red flags, inconsistencies, and keyword stuffing attempts.

Your analysis process:
1. Extract basic info (name, contact, education)
2. Map skills to job requirements
3. Assess experience depth and relevance
4. Identify gaps and red flags
5. Synthesize overall impression""",
                task_prompt="""Analyze this resume against the job description using structured reasoning.

Job Description:
{job_description}

Resume Text:
{resume_text}

Follow this step-by-step process:
1. EXTRACTION: List all skills, experiences, and education
2. MAPPING: Match against job requirements
3. DEPTH_ASSESSMENT: Evaluate demonstrated expertise
4. RED_FLAG_ANALYSIS: Identify concerns and inconsistencies
5. SYNTHESIS: Provide overall impression""",
                few_shot_examples=[
                    {
                        "input": {
                            "job_description": "Senior Python Developer with 5+ years experience, AWS knowledge required",
                            "resume": "Python Expert. 3 years as Python Developer. AWS certified. Developed scalable systems."
                        },
                        "output": {
                            "candidate_name": "Unknown",
                            "skills_found": ["Python", "AWS"],
                            "experience_summary": "3 years Python development, AWS certified",
                            "education": "Not mentioned",
                            "strengths": ["AWS certification", "Python experience"],
                            "concerns": ["3 years vs 5+ years required", "Vague system details", "No specific projects mentioned"],
                            "keyword_stuffing_detected": True,
                            "overall_impression": "Appears to be mid-level developer, below senior requirement. Language is generic."
                        }
                    },
                    {
                        "input": {
                            "job_description": "Full Stack Engineer: React, Node.js, PostgreSQL",
                            "resume": "Architect at TechCorp: Led React migration (50k LOC), Node.js backend with PostgreSQL. 7 years experience."
                        },
                        "output": {
                            "candidate_name": "Unknown",
                            "skills_found": ["React", "Node.js", "PostgreSQL", "System Architecture"],
                            "experience_summary": "7 years with 2+ years architectural work, direct experience with required stack",
                            "education": "Not mentioned",
                            "strengths": ["All required skills", "Clear scale of projects", "Architectural background"],
                            "concerns": ["Education background missing", "Only one company listed"],
                            "keyword_stuffing_detected": False,
                            "overall_impression": "Strong fit. Demonstrates deep expertise with concrete project examples."
                        }
                    }
                ],
                output_format="""{
    "candidate_name": "string",
    "extraction": {
        "skills": ["skill1", "skill2"],
        "years_total_experience": number,
        "education": "string"
    },
    "mapping": {
        "matched_requirements": ["req1", "req2"],
        "missing_requirements": ["req1"]
    },
    "depth_assessment": {
        "demonstrated_expertise_level": "junior|mid|senior|expert",
        "evidence": "string"
    },
    "red_flags": {
        "concerns": ["concern1"],
        "inconsistencies": ["inconsistency1"],
        "keyword_stuffing_detected": boolean
    },
    "overall_impression": "string",
    "confidence_score": 0.0-1.0
}""",
                constraints=[
                    "Provide step-by-step reasoning",
                    "Support conclusions with evidence from resume",
                    "Be skeptical of vague language",
                    "Note timeline inconsistencies",
                    "Include confidence score (0-1)"
                ],
                temperature=0.3,
                description="Advanced resume analysis with chain-of-thought reasoning"
            )
        }
    
    def _get_scorer_prompts(self) -> Dict[str, PromptTemplate]:
        """Scorer Agent prompts"""
        return {
            PromptVersion.V1: PromptTemplate(
                name="scorer_v1",
                version=PromptVersion.V1,
                system_prompt="""You are an expert hiring manager responsible for scoring candidates fairly and consistently.
Your scores should reflect realistic job fit, not perfection.
Consider both strengths and gaps in your assessment.""",
                task_prompt="""Score this candidate for the job position.

Job Description:
{job_description}

Candidate Analysis:
{analysis}

Provide fair, consistent scores with clear reasoning.""",
                few_shot_examples=[],
                output_format="""{
    "overall_score": 0-100,
    "technical_fit": 0-100,
    "experience_fit": 0-100,
    "education_fit": 0-100,
    "reasoning": "string"
}""",
                constraints=[
                    "90-100: Exceptional fit (rare)",
                    "75-89: Strong fit",
                    "60-74: Good fit with gaps",
                    "40-59: Marginal fit",
                    "Below 40: Poor fit",
                    "Be consistent across candidates"
                ],
                temperature=0.2,
                description="Basic candidate scoring"
            ),
            PromptVersion.V3: PromptTemplate(
                name="scorer_v3",
                version=PromptVersion.V3,
                system_prompt="""You are an expert hiring manager responsible for scoring candidates fairly and consistently.
Your scores should reflect realistic job fit, not perfection.
Consider both strengths and gaps in your assessment.

Scoring Methodology:
1. Assess requirement coverage (what % of must-haves are met)
2. Evaluate experience quality and depth
3. Identify growth potential and gaps
4. Consider risk factors
5. Synthesize overall fit""",
                task_prompt="""Score this candidate using structured assessment.

Job Description:
{job_description}

Candidate Analysis:
{analysis}

Follow this process:
1. REQUIREMENT_COVERAGE: What % of requirements are met?
2. SKILL_MATCHING: For each key skill, indicate if present/absent with evidence
3. EXPERIENCE_DEPTH: How deep is their experience?
4. GROWTH_POTENTIAL: Can they grow into gaps?
5. RISK_ASSESSMENT: Any red flags?
6. FINAL_SCORE: Calculate overall fit

IMPORTANT: End your response with ONLY a valid JSON object (no additional text after the JSON).
The JSON should match the Output Format specification exactly.""",
                few_shot_examples=[
                    {
                        "input": {
                            "job_description": "Senior Python Developer, 5+ years, AWS, Django",
                            "analysis": {
                                "experience_summary": "3 years Python, some AWS, no Django",
                                "strengths": ["Strong Python skills"],
                                "concerns": ["Below required experience", "No Django"]
                            }
                        },
                        "output": {
                            "overall_score": 58,
                            "technical_fit": 70,
                            "experience_fit": 45,
                            "education_fit": 65,
                            "reasoning": "Candidate has strong Python but lacks 2 years experience and Django expertise. Mid-level seeking senior role. Could grow but needs mentoring.",
                            "requirement_coverage": "60%",
                            "risk_assessment": "Learning curve required",
                            "skill_matches": [
                                {"skill": "Python", "present": True, "evidence": "3 years professional experience", "confidence": 0.95},
                                {"skill": "AWS", "present": True, "evidence": "Some experience mentioned", "confidence": 0.6},
                                {"skill": "Django", "present": False, "evidence": "Not mentioned in resume", "confidence": 0.9}
                            ],
                            "gaps": {
                                "missing_skills": ["Django", "Advanced AWS"],
                                "unclear_sections": [],
                                "inconsistencies": []
                            }
                        }
                    },
                    {
                        "input": {
                            "job_description": "Full Stack: React, Node.js, PostgreSQL, 7+ years",
                            "analysis": {
                                "experience_summary": "8 years full stack, direct React/Node/PG experience, architectural background",
                                "strengths": ["All required skills", "Experience exceeds requirement"],
                                "concerns": ["Only one company"]
                            }
                        },
                        "output": {
                            "overall_score": 85,
                            "technical_fit": 90,
                            "experience_fit": 85,
                            "education_fit": 80,
                            "reasoning": "Excellent technical fit with all required skills. Experience level matches/exceeds requirement. Single employer is minor concern but depth suggests strong performer.",
                            "requirement_coverage": "100%",
                            "risk_assessment": "Low risk, high confidence",
                            "skill_matches": [
                                {"skill": "React", "present": True, "evidence": "Led React migration (50k LOC)", "confidence": 0.99},
                                {"skill": "Node.js", "present": True, "evidence": "Node.js backend architecture", "confidence": 0.99},
                                {"skill": "PostgreSQL", "present": True, "evidence": "Direct PostgreSQL experience", "confidence": 0.98}
                            ],
                            "gaps": {
                                "missing_skills": [],
                                "unclear_sections": [],
                                "inconsistencies": []
                            }
                        }
                    }
                ],
                output_format="""{
    "requirement_coverage": "X%",
    "experience_depth_assessment": "junior|mid|senior|expert",
    "technical_scores": {
        "technical_fit": 0-100,
        "experience_fit": 0-100,
        "education_fit": 0-100
    },
    "skill_matches": [
        {
            "skill": "skill_name",
            "present": true/false,
            "evidence": "brief evidence from resume",
            "confidence": 0.0-1.0
        }
    ],
    "growth_potential": "high|medium|low",
    "risk_assessment": "string",
    "overall_score": 0-100,
    "reasoning": "string",
    "recommendation": "strong_hire|hire|maybe|pass",
    "technical_fit": 0-100,
    "experience_fit": 0-100,
    "education_fit": 0-100,
    "gaps": {
        "missing_skills": ["skill1"],
        "unclear_sections": ["section1"],
        "inconsistencies": ["inconsistency1"]
    }
}""",
                constraints=[
                    "Show calculation logic",
                    "Be honest about gaps",
                    "Consider growth potential, not just current fit",
                    "Maintain consistency across candidates",
                    "Support each score with evidence",
                    "CRITICAL: Output ONLY valid JSON at the end, no text after JSON",
                    "Ensure overall_score is the average or weighted score of component fits",
                    "Ensure skill_matches array is always populated with at least top 5 skills",
                    "Ensure gaps object has all three fields populated"
                ],
                temperature=0.2,
                description="Advanced scoring with structured assessment"
            )
        }
    
    def _get_question_generator_prompts(self) -> Dict[str, PromptTemplate]:
        """Question Generator prompts"""
        return {
            PromptVersion.V1: PromptTemplate(
                name="question_generator_v1",
                version=PromptVersion.V1,
                system_prompt="""You are an expert interviewer skilled at asking targeted questions.
Create questions that probe specific skills, validate claims, and assess depth of knowledge.
Avoid generic questions.""",
                task_prompt="""Generate targeted interview questions for this candidate.

Job Description:
{job_description}

Candidate Analysis:
{analysis}

Gaps Identified:
{gaps}

IMPORTANT: You MUST generate exactly 5-7 interview questions. Do not generate just one question.

Generate 5-7 specific, targeted questions based on the analysis and gaps.""",
                few_shot_examples=[],
                output_format="""{
    "questions": [
        {
            "question": "string",
            "category": "Technical|Experience|Soft Skills",
            "reasoning": "string"
        }
    ]
}""",
                constraints=[
                    "Probe vague claims",
                    "Test depth of stated skills",
                    "Address identified gaps",
                    "Clarify inconsistencies",
                    "Assess problem-solving",
                    "Avoid yes/no questions"
                ],
                temperature=0.7,
                description="Basic question generation"
            ),
            PromptVersion.V3: PromptTemplate(
                name="question_generator_v3",
                version=PromptVersion.V3,
                system_prompt="""You are an expert interviewer skilled at asking targeted questions.
Create questions that probe specific skills, validate claims, and assess depth of knowledge.
Avoid generic questions.

Your question design process:
1. Identify ambiguous or vague claims
2. Design questions to test depth
3. Target specific gaps
4. Create follow-up paths
5. Balance technical and soft skills""",
                task_prompt="""Generate targeted interview questions using structured approach.

Job Description:
{job_description}

Candidate Analysis:
{analysis}

Gaps Identified:
{gaps}

IMPORTANT: You MUST generate exactly 5-7 interview questions. Do not generate just one question.

Process:
1. VAGUE_CLAIMS: Identify unclear statements to probe
2. DEPTH_TESTING: Design questions for claimed expertise
3. GAP_ADDRESSING: Create questions targeting missing skills
4. FOLLOW_UP_PATHS: Note expected answers and follow-ups
5. QUESTION_SET: Generate 5-7 strategic questions (REQUIRED: at least 5 questions)""",
                few_shot_examples=[
                    {
                        "input": {
                            "analysis": "Claims 5 years Python experience, but no specific projects mentioned",
                            "gap": "Experience depth unclear"
                        },
                        "output": {
                            "questions": [
                                {
                                    "question": "Can you walk me through the largest Python project you've led from architecture to deployment? What were the most complex challenges?",
                                    "category": "Technical",
                                    "reasoning": "Tests actual depth and leadership in Python. Follow-ups can probe architecture decisions and problem-solving.",
                                    "target": "Experience depth",
                                    "follow_up_path": "Ask about specific libraries used, performance optimization, team coordination"
                                }
                            ]
                        }
                    },
                    {
                        "input": {
                            "analysis": "Resume shows 3 years but job requires 5+",
                            "gap": "Experience shortfall"
                        },
                        "output": {
                            "questions": [
                                {
                                    "question": "Despite having 3 years of direct experience vs. the 5+ we're seeking, your role at [Company] involved architectural decisions. Tell us about a time you had to design a system at the scale of what we handle here—what did you learn?",
                                    "category": "Experience",
                                    "reasoning": "Acknowledges gap while assessing ability to handle senior-level complexity. Tests growth and confidence.",
                                    "target": "Gap bridging",
                                    "follow_up_path": "Ask about mentorship received, impact, and learning velocity"
                                }
                            ]
                        }
                    }
                ],
                output_format="""{
    "vague_claims_identified": ["claim1"],
    "questions": [
        {
            "question": "string",
            "category": "Technical|Experience|Problem-Solving|Leadership|Soft Skills",
            "reasoning": "string",
            "target": "string (what this probes)",
            "follow_up_path": "string (expected answer and follow-ups)",
            "red_flag_indicators": ["indicator1"]
        }
    ],
    "interview_strategy": "string (overall approach)"
}""",
                constraints=[
                    "Base questions on specific resume details",
                    "Avoid generic behavioral questions",
                    "Include follow-up strategy",
                    "Flag potential red flag responses",
                    "Target both strengths and gaps",
                    "Test actual depth, not just keywords"
                ],
                temperature=0.7,
                description="Advanced question generation with strategic interview planning"
            )
        }
    
    def get_all_versions(self, agent_name: str) -> List[PromptVersion]:
        """Get all available versions for an agent"""
        if agent_name not in self.prompts:
            return []
        return list(self.prompts[agent_name].keys())
    
    def list_prompts(self) -> Dict[str, List[str]]:
        """List all available prompts and versions"""
        result = {}
        for agent_name, versions in self.prompts.items():
            result[agent_name] = [v.value for v in versions.keys()]
        return result


# Singleton instance
_prompt_manager = None


def get_prompt_manager() -> PromptManager:
    """Get singleton instance of prompt manager"""
    global _prompt_manager
    if _prompt_manager is None:
        _prompt_manager = PromptManager()
    return _prompt_manager
