from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
import json
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from backend.prompts import get_prompt_manager, PromptVersion


class QuestionGeneratorAgent:
    def __init__(self, api_key: str, model: str = "llama-3.3-70b-versatile", use_cot: bool = True):
        self.llm = ChatGroq(
            api_key=api_key,
            model=model,
            temperature=0.7
        )
        self.prompt_manager = get_prompt_manager()
        self.use_cot = use_cot
        self.model = model
    
    async def generate_questions(
        self, 
        job_description: str, 
        analysis: dict, 
        gaps: dict
    ) -> list:
        """Generate targeted interview questions using advanced prompting"""
        
        # Compose full prompt with examples and instructions
        full_prompt = self.prompt_manager.compose_full_prompt(
            "question_generator",
            job_description=job_description,
            analysis=json.dumps(analysis, indent=2),
            gaps=json.dumps(gaps, indent=2)
        )
        
        # Create message and invoke LLM directly
        message = HumanMessage(content=full_prompt)
        response = await self.llm.ainvoke([message])
        
        try:
            content = response.content
            # Try to extract JSON from code blocks first
            if "```json" in content:
                content = content.split("```json")[1].split("```")[0]
            elif "```" in content:
                try:
                    content = content.split("```")[1].split("```")[0]
                except:
                    pass
            
            # Look for JSON object pattern - use find() for first occurrence
            if "{" in content and "}" in content:
                start_idx = content.find("{")
                end_idx = content.rfind("}") + 1
                if start_idx >= 0 and end_idx > start_idx:
                    content = content[start_idx:end_idx]
            
            result = json.loads(content.strip())
            
            # Handle both V1/V2 simple format and V3 complex format
            questions = result.get("questions", [])
            
            # If questions array is empty, try alternative formats
            if not questions and "vague_claims_identified" in result:
                # This is V3 format with more fields
                questions = result.get("questions", [])
            
            # If still empty, try looking for questions nested differently
            if not questions:
                for key in result.keys():
                    if isinstance(result[key], list) and key != "vague_claims_identified":
                        # Check if it looks like questions
                        if result[key] and isinstance(result[key][0], dict) and "question" in result[key][0]:
                            questions = result[key]
                            break
            
            # Ensure all questions have required fields and minimum quantity
            validated_questions = []
            for q in questions:
                if isinstance(q, dict) and 'question' in q:
                    q.setdefault('category', 'Technical')
                    q.setdefault('reasoning', '')
                    validated_questions.append(q)
            
            # If we got questions, return them; otherwise use fallback with 5 questions
            if validated_questions:
                return validated_questions
            else:
                # Generate default questions if parsing failed
                return self._get_default_questions()
                
        except Exception as e:
            print(f"Question generator parsing error: {str(e)}")
            print(f"Response content: {response.content[:500]}")  # Debug info
            return self._get_default_questions()
    
    def _get_default_questions(self) -> list:
        """Generate default fallback questions"""
        return [
            {
                "question": "Can you walk us through your most significant project that used the key technologies mentioned in this job description?",
                "category": "Technical",
                "reasoning": "Tests practical experience with required tech stack"
            },
            {
                "question": "Tell us about a time when you had to learn a new technology quickly. How did you approach it and what was the outcome?",
                "category": "Problem-Solving",
                "reasoning": "Assesses learning ability and initiative"
            },
            {
                "question": "What aspects of your previous role prepared you best for this position, and what areas are you looking to develop further?",
                "category": "Experience",
                "reasoning": "Evaluates self-awareness and career progression"
            },
            {
                "question": "Describe a situation where you had to work with a team member you initially didn't see eye-to-eye with. How did you handle it?",
                "category": "Soft Skills",
                "reasoning": "Tests collaboration and conflict resolution"
            },
            {
                "question": "If you could redesign your most recent project from scratch, what would you do differently and why?",
                "category": "Technical",
                "reasoning": "Assesses depth of understanding and critical thinking"
            }
        ]