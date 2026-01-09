"""
Chain-of-Thought Reasoning Framework
Implements step-by-step reasoning and structured decomposition for LLM tasks
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field, asdict
from enum import Enum
import json


class ReasoningStep(str, Enum):
    """Standard reasoning steps"""
    EXTRACTION = "extraction"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    VALIDATION = "validation"
    CONCLUSION = "conclusion"


@dataclass
class ReasoningChain:
    """Structured chain of reasoning"""
    task_name: str
    steps: List[Dict[str, Any]] = field(default_factory=list)
    final_conclusion: Optional[Dict[str, Any]] = None
    confidence_score: float = 0.0
    
    def add_step(
        self,
        step_type: ReasoningStep,
        input_data: Any,
        output_data: Any,
        reasoning: str
    ):
        """Add a reasoning step"""
        self.steps.append({
            "step": step_type.value,
            "input": input_data,
            "output": output_data,
            "reasoning": reasoning
        })
    
    def to_json(self) -> str:
        """Convert to JSON for logging/debugging"""
        return json.dumps(asdict(self), indent=2)


class ChainOfThoughtFramework:
    """Framework for implementing chain-of-thought reasoning"""
    
    def __init__(self):
        self.chains: Dict[str, ReasoningChain] = {}
    
    def create_resume_analysis_chain(
        self,
        resume_text: str,
        job_description: str
    ) -> ReasoningChain:
        """
        Create chain of thought for resume analysis
        Steps: Extraction → Analysis → Synthesis
        """
        chain = ReasoningChain(task_name="resume_analysis")
        
        # Step 1: EXTRACTION
        extraction_prompt = self._create_extraction_prompt(
            resume_text,
            job_description
        )
        
        # Step 2: ANALYSIS
        analysis_prompt = self._create_analysis_prompt(
            resume_text,
            job_description
        )
        
        # Step 3: SYNTHESIS
        synthesis_prompt = self._create_synthesis_prompt(
            resume_text,
            job_description
        )
        
        return chain
    
    def create_scoring_chain(
        self,
        candidate_analysis: Dict[str, Any],
        job_description: str
    ) -> ReasoningChain:
        """
        Create chain of thought for candidate scoring
        Steps: Coverage → Depth → Risk → Synthesis
        """
        chain = ReasoningChain(task_name="candidate_scoring")
        
        # Step 1: REQUIREMENT COVERAGE
        coverage_analysis = f"""
Step 1: Analyze Requirement Coverage

Analyze how many must-have requirements the candidate meets:
1. Extract all must-have requirements from job description
2. Map candidate's skills to these requirements
3. Calculate coverage percentage
4. Identify critical gaps

Input: {json.dumps(candidate_analysis, indent=2)}
"""
        
        # Step 2: EXPERIENCE DEPTH
        depth_analysis = f"""
Step 2: Assess Experience Depth

Evaluate quality and depth of experience:
1. Identify years of direct experience
2. Assess seniority level progression
3. Evaluate project complexity
4. Consider breadth vs. depth

Context: {json.dumps(candidate_analysis, indent=2)}
"""
        
        # Step 3: GROWTH POTENTIAL
        growth_analysis = f"""
Step 3: Assess Growth Potential

Consider ability to grow into gaps:
1. Learning velocity indicators
2. Related skill transferability
3. Career progression pattern
4. Motivation indicators
"""
        
        # Step 4: RISK ASSESSMENT
        risk_analysis = f"""
Step 4: Risk Assessment

Identify red flags and risks:
1. Resume inconsistencies
2. Employment gaps
3. Keyword stuffing indicators
4. Overstatement of skills

Known concerns: {json.dumps(candidate_analysis.get('gaps', {}), indent=2)}
"""
        
        return chain
    
    def create_question_generation_chain(
        self,
        candidate_analysis: Dict[str, Any],
        job_description: str,
        gaps: Dict[str, Any]
    ) -> ReasoningChain:
        """
        Create chain of thought for interview question generation
        Steps: Identify Claims → Design Probes → Plan Follow-ups
        """
        chain = ReasoningChain(task_name="question_generation")
        
        # Step 1: IDENTIFY VAGUE CLAIMS
        vague_claims = f"""
Step 1: Identify Vague/Unclear Claims in Resume

Look for statements that need probing:
1. Generic skills without context ("expert in Python")
2. Vague achievement statements ("delivered value")
3. Unclear timelines or responsibilities
4. Potential exaggerations

Resume context: {json.dumps(candidate_analysis, indent=2)}
"""
        
        # Step 2: DESIGN DEPTH TESTS
        depth_tests = f"""
Step 2: Design Questions to Test Depth

For each claimed skill, design a question to validate depth:
1. Ask for specific project examples
2. Request decision-making rationale
3. Explore technology choices
4. Evaluate problem-solving approach

Claimed skills: {json.dumps(candidate_analysis.get('skills_found', []))}
"""
        
        # Step 3: TARGET GAPS
        gap_targeting = f"""
Step 3: Target Experience Gaps

Create questions addressing identified gaps:
1. Acknowledge gap respectfully
2. Assess learning ability
3. Identify transferable skills
4. Gauge confidence in learning curve

Identified gaps: {json.dumps(gaps, indent=2)}
"""
        
        # Step 4: PLAN FOLLOW-UPS
        followup_planning = f"""
Step 4: Plan Follow-up Paths

For each question, identify:
1. Expected answer patterns
2. Red flag responses
3. Follow-up questions
4. What would impress you

This allows adaptive interviewing based on responses.
"""
        
        return chain
    
    def create_prompt_with_cot(
        self,
        base_prompt: str,
        steps: List[str],
        examples: Optional[List[Dict[str, Any]]] = None
    ) -> str:
        """
        Create prompt with chain-of-thought instruction
        
        Args:
            base_prompt: Base instruction
            steps: Ordered steps to follow
            examples: Few-shot examples showing step-by-step reasoning
        """
        cot_prompt = base_prompt + "\n\n"
        
        # Add step-by-step instructions
        cot_prompt += "REASONING APPROACH:\n"
        cot_prompt += "Follow these steps in order:\n\n"
        
        for i, step in enumerate(steps, 1):
            cot_prompt += f"Step {i}: {step}\n"
        
        # Add examples if provided
        if examples:
            cot_prompt += "\n\nEXAMPLES OF STEP-BY-STEP REASONING:\n\n"
            
            for i, example in enumerate(examples, 1):
                cot_prompt += f"Example {i}:\n"
                cot_prompt += f"Input: {json.dumps(example.get('input', {}), indent=2)}\n\n"
                cot_prompt += f"Step-by-Step Reasoning:\n"
                
                for step_num, reasoning in enumerate(example.get('reasoning', []), 1):
                    cot_prompt += f"  Step {step_num}: {reasoning}\n"
                
                cot_prompt += f"\nFinal Output:\n{json.dumps(example.get('output', {}), indent=2)}\n\n"
        
        cot_prompt += "\nNow apply this step-by-step approach to the current task:"
        
        return cot_prompt
    
    def _create_extraction_prompt(
        self,
        resume_text: str,
        job_description: str
    ) -> str:
        """Create extraction step prompt"""
        return f"""
STEP 1: EXTRACTION
Extract raw information from resume without interpretation.

Resume:
{resume_text}

Job Description:
{job_description}

Extract:
1. All mentioned skills
2. Work experience timeline
3. Education details
4. Certifications/achievements
5. Any dates or numbers

Output format: Structured list of extracted items
"""
    
    def _create_analysis_prompt(
        self,
        resume_text: str,
        job_description: str
    ) -> str:
        """Create analysis step prompt"""
        return f"""
STEP 2: ANALYSIS
Analyze the extracted information.

Map extracted skills to job requirements:
1. Match rate: What % of requirements are present?
2. Experience relevance: How relevant is their experience?
3. Depth indicators: Are there signs of deep expertise?
4. Concerns: Any red flags or inconsistencies?

Provide analysis with evidence.
"""
    
    def _create_synthesis_prompt(
        self,
        resume_text: str,
        job_description: str
    ) -> str:
        """Create synthesis step prompt"""
        return f"""
STEP 3: SYNTHESIS
Synthesize analysis into conclusions.

Based on extraction and analysis:
1. Overall impression: How well does this candidate fit?
2. Strengths: What are their biggest advantages?
3. Concerns: What are the main weaknesses?
4. Questions: What needs clarification?
5. Confidence: How confident are you in this assessment?

Provide a cohesive assessment.
"""
    
    @staticmethod
    def generate_cot_instruction() -> str:
        """Generate standard chain-of-thought instruction"""
        return """
CHAIN-OF-THOUGHT REASONING:
Think step-by-step. Break down the problem into logical steps.
For each step, show your reasoning before proceeding to the next.
Explain your logic clearly so others can follow your thinking.

Format your response:
1. Step 1: [What you're doing] → [Your reasoning] → [Conclusion]
2. Step 2: [What you're doing] → [Your reasoning] → [Conclusion]
...
Final: [Synthesize conclusions into final answer]
"""


# Singleton instance
_cot_framework = None


def get_cot_framework() -> ChainOfThoughtFramework:
    """Get singleton instance of COT framework"""
    global _cot_framework
    if _cot_framework is None:
        _cot_framework = ChainOfThoughtFramework()
    return _cot_framework
