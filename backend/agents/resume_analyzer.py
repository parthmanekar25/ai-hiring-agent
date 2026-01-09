from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from typing import Dict, Any
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.prompts import get_prompt_manager, get_context_optimizer, PromptVersion


class ResumeAnalyzerAgent:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile", use_cot: bool = True):
        self.llm = ChatGroq(
            api_key=api_key,
            model=model,
            temperature=0.3
        )
        self.prompt_manager = get_prompt_manager()
        self.context_optimizer = get_context_optimizer()
        self.use_cot = use_cot
        self.model = model
    
    async def analyze(self, job_description: str, resume_text: str) -> Dict[str, Any]:
        """Analyze resume against job description using advanced prompting"""
        
        # Optimize context for LLM
        optimized_job_desc = self.context_optimizer.optimize_job_description(
            job_description,
            max_tokens=1000
        )
        optimized_resume = self.context_optimizer.optimize_resume_context(
            resume_text,
            job_description,
            max_tokens=2000
        )
        
        # Compose full prompt with examples and instructions
        full_prompt = self.prompt_manager.compose_full_prompt(
            "resume_analyzer",
            job_description=optimized_job_desc,
            resume_text=optimized_resume
        )
        
        # Create message and invoke LLM directly
        message = HumanMessage(content=full_prompt)
        response = await self.llm.ainvoke([message])
        
        # Parse JSON from response
        try:
            content = response.content
            # Extract JSON from markdown code blocks if present
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                content = content.split("```")[1].split("```")[0]
            
            analysis = json.loads(content.strip())
            
            # Ensure required fields exist
            analysis.setdefault('candidate_name', 'Unknown')
            analysis.setdefault('overall_impression', '')
            analysis.setdefault('skills_found', [])
            analysis.setdefault('experience_summary', '')
            
            return analysis
        except Exception as e:
            print(f"Analyzer parsing error: {str(e)}")
            return {
                "candidate_name": "Unknown",
                "overall_impression": "Unable to parse response",
                "skills_found": [],
                "experience_summary": response.content,
                "error": "Failed to parse structured response"
            }