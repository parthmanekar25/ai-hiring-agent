from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import json
import re
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.prompts import get_prompt_manager, PromptVersion


class ScorerAgent:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile", use_cot: bool = True):
        self.llm = ChatGroq(
            api_key=api_key,
            model=model,
            temperature=0.2  # Lower temp for consistency
        )
        self.prompt_manager = get_prompt_manager()
        self.use_cot = use_cot
        self.model = model
    
    async def score(self, job_description: str, analysis: dict) -> dict:
        """Score candidate based on analysis using advanced prompting"""
        
        # Compose full prompt with examples and instructions
        full_prompt = self.prompt_manager.compose_full_prompt(
            "scorer",
            job_description=job_description,
            analysis=json.dumps(analysis, indent=2)
        )
        
        # Create message and invoke LLM directly
        message = HumanMessage(content=full_prompt)
        response = await self.llm.ainvoke([message])
        
        try:
            content = response.content
            
            # Try multiple extraction strategies
            json_content = None
            
            # Strategy 1: Look for ```json blocks first
            if "```json" in content:
                try:
                    json_content = content.split("```json")[1].split("```")[0].strip()
                except:
                    pass
            
            # Strategy 2: Find the FIRST occurrence of "{" and corresponding "}"
            # This gets the top-level JSON object
            if not json_content:
                start_idx = content.find("{")  # Use find for FIRST occurrence
                if start_idx >= 0:
                    brace_count = 0
                    for i in range(start_idx, len(content)):
                        if content[i] == "{":
                            brace_count += 1
                        elif content[i] == "}":
                            brace_count -= 1
                            if brace_count == 0:
                                json_content = content[start_idx:i+1]
                                break
            
            if json_content:
                result = json.loads(json_content)
            else:
                raise ValueError("Could not extract JSON from response")
            
            # Ensure all required fields exist with proper types
            result['overall_score'] = float(result.get('overall_score', 50))
            result['technical_fit'] = float(result.get('technical_fit', 50))
            result['experience_fit'] = float(result.get('experience_fit', 50))
            result['education_fit'] = float(result.get('education_fit', 50))
            result.setdefault('reasoning', '')
            
            # Handle skill_matches - could be nested in technical_scores
            if 'skill_matches' not in result or not result['skill_matches']:
                result['skill_matches'] = []
            
            # Handle gaps
            if 'gaps' not in result or not result['gaps']:
                result['gaps'] = {
                    'missing_skills': [],
                    'unclear_sections': [],
                    'inconsistencies': []
                }
            
            return result
        except Exception as e:
            print(f"\n❌ Scorer parsing error: {str(e)}")
            print(f"Response length: {len(response.content)} chars")
            
            # Check what's in the response
            if "overall_score" in response.content:
                print("✓ Response contains 'overall_score'")
            if "technical_fit" in response.content:
                print("✓ Response contains 'technical_fit'")
            if "{" in response.content:
                print("✓ Response contains JSON markers")
            
            print(f"\nFirst 1000 chars:\n{response.content[:1000]}\n")
            
            # Try to extract just the scores from the response if JSON parsing fails
            # This is a fallback to at least get something useful
            try:
                # Look for key patterns
                overall = re.search(r'"overall_score"\s*:\s*(\d+\.?\d*)', response.content)
                tech = re.search(r'"technical_fit"\s*:\s*(\d+\.?\d*)', response.content)
                exp = re.search(r'"experience_fit"\s*:\s*(\d+\.?\d*)', response.content)
                edu = re.search(r'"education_fit"\s*:\s*(\d+\.?\d*)', response.content)
                
                if overall:
                    return {
                        "overall_score": float(overall.group(1)),
                        "technical_fit": float(tech.group(1)) if tech else 50,
                        "experience_fit": float(exp.group(1)) if exp else 50,
                        "education_fit": float(edu.group(1)) if edu else 50,
                        "reasoning": response.content,
                        "skill_matches": [],
                        "gaps": {
                            'missing_skills': [],
                            'unclear_sections': [],
                            'inconsistencies': []
                        }
                    }
            except:
                pass
            
            # Return defaults with raw reasoning
            return {
                "overall_score": 50,
                "technical_fit": 50,
                "experience_fit": 50,
                "education_fit": 50,
                "reasoning": response.content,
                "skill_matches": [],
                "gaps": {
                    'missing_skills': [],
                    'unclear_sections': [],
                    'inconsistencies': []
                }
            }