"""
Context Optimization Module
Handles smart chunking, prioritization, and context window management
"""

from typing import List, Dict, Any, Tuple, Optional
from dataclasses import dataclass
import re


@dataclass
class ContextChunk:
    """A chunk of context with priority"""
    content: str
    priority: float  # 0-1, higher = more important
    section_type: str  # "experience", "education", "skills", etc.
    tokens_estimate: int


class ContextOptimizer:
    """Optimizes context for LLM consumption"""
    
    CONTEXT_WINDOW_LIMIT = 8000  # Conservative limit for Mixtral
    AVERAGE_TOKENS_PER_WORD = 1.3  # Rough estimate
    
    # Priority weights for different section types
    SECTION_PRIORITIES = {
        "experience": 1.0,
        "skills": 0.95,
        "education": 0.85,
        "certifications": 0.8,
        "projects": 0.9,
        "summary": 0.7,
        "other": 0.5,
    }
    
    def __init__(self):
        self.max_context_tokens = self.CONTEXT_WINDOW_LIMIT
    
    def optimize_resume_context(
        self,
        resume_text: str,
        job_description: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Optimize resume text for LLM processing by:
        1. Chunking into sections
        2. Prioritizing relevant information
        3. Removing redundancy
        4. Staying within token limits
        """
        max_tokens = max_tokens or self.max_context_tokens
        
        # Step 1: Parse resume into sections
        sections = self._parse_resume_sections(resume_text)
        
        # Step 2: Score relevance to job description
        for section in sections:
            section.priority = self._score_relevance(
                section.content,
                job_description
            )
        
        # Step 3: Sort by priority
        sections.sort(key=lambda x: x.priority, reverse=True)
        
        # Step 4: Build optimized context within token limit
        optimized = self._build_context_within_limit(
            sections,
            max_tokens
        )
        
        return optimized
    
    def optimize_job_description(
        self,
        job_description: str,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Compress job description while preserving critical information:
        1. Extract requirements
        2. Identify must-haves vs nice-to-haves
        3. Summarize key responsibilities
        """
        max_tokens = max_tokens or (self.max_context_tokens // 3)
        
        # Extract key sections
        must_haves = self._extract_must_haves(job_description)
        responsibilities = self._extract_responsibilities(job_description)
        nice_to_haves = self._extract_nice_to_haves(job_description)
        
        # Build optimized version prioritizing requirements
        optimized = "MUST-HAVE REQUIREMENTS:\n"
        optimized += self._format_list(must_haves)
        optimized += "\n\nKEY RESPONSIBILITIES:\n"
        optimized += self._format_list(responsibilities[:5])  # Top 5
        
        if nice_to_haves:
            optimized += "\n\nNICE-TO-HAVE SKILLS:\n"
            optimized += self._format_list(nice_to_haves[:5])  # Top 5
        
        # Ensure within token limit
        while self._estimate_tokens(optimized) > max_tokens:
            optimized = self._truncate_at_limit(optimized, max_tokens)
        
        return optimized
    
    def _parse_resume_sections(self, resume_text: str) -> List[ContextChunk]:
        """Parse resume into logical sections"""
        sections = []
        
        # Define common section patterns
        section_patterns = {
            "experience": r"(?:experience|work history|employment)",
            "education": r"(?:education|academic|degree)",
            "skills": r"(?:skills|technical|competencies)",
            "projects": r"(?:projects|portfolio|works?)",
            "certifications": r"(?:certifications?|licenses?)",
            "summary": r"(?:summary|objective|profile)",
        }
        
        # Split by section headers
        current_section_type = "other"
        current_content = ""
        
        for line in resume_text.split('\n'):
            # Check if this is a section header
            matched_section = False
            for section_type, pattern in section_patterns.items():
                if re.search(pattern, line, re.IGNORECASE) and len(line) < 100:
                    # Save previous section
                    if current_content.strip():
                        sections.append(ContextChunk(
                            content=current_content.strip(),
                            priority=self.SECTION_PRIORITIES.get(
                                current_section_type,
                                0.5
                            ),
                            section_type=current_section_type,
                            tokens_estimate=self._estimate_tokens(current_content)
                        ))
                    current_section_type = section_type
                    current_content = line + "\n"
                    matched_section = True
                    break
            
            if not matched_section:
                current_content += line + "\n"
        
        # Add final section
        if current_content.strip():
            sections.append(ContextChunk(
                content=current_content.strip(),
                priority=self.SECTION_PRIORITIES.get(current_section_type, 0.5),
                section_type=current_section_type,
                tokens_estimate=self._estimate_tokens(current_content)
            ))
        
        return sections if sections else [ContextChunk(
            content=resume_text,
            priority=0.5,
            section_type="full_resume",
            tokens_estimate=self._estimate_tokens(resume_text)
        )]
    
    def _score_relevance(self, text: str, job_description: str) -> float:
        """
        Score how relevant a section is to the job description.
        Higher score = more relevant.
        """
        score = 0.0
        
        # Extract key terms from job description
        job_terms = self._extract_key_terms(job_description)
        
        # Count matches in section
        text_lower = text.lower()
        match_count = sum(
            text_lower.count(term.lower())
            for term in job_terms
        )
        
        # Normalize score (0-1)
        score = min(1.0, match_count / (len(job_terms) + 1))
        
        # Boost score based on section type
        if any(keyword in text_lower for keyword in ["achievement", "delivered", "led", "built", "created"]):
            score = min(1.0, score + 0.2)
        
        return score
    
    def _extract_key_terms(self, text: str) -> List[str]:
        """Extract important technical terms from job description"""
        # This is simplified; in production, use NER or TF-IDF
        terms = re.findall(r'\b[A-Z][a-z]+(?:\.[A-Z][a-z]+)?\b', text)
        # Filter out common words
        common = {'The', 'This', 'And', 'You', 'Your', 'Have', 'Will', 'Can'}
        return [t for t in terms if t not in common][:20]  # Top 20 terms
    
    def _build_context_within_limit(
        self,
        sections: List[ContextChunk],
        max_tokens: int
    ) -> str:
        """Build optimized context within token limit"""
        result = ""
        current_tokens = 0
        
        for section in sections:
            if current_tokens + section.tokens_estimate <= max_tokens:
                result += f"\n{section.section_type.upper()}:\n"
                result += section.content + "\n"
                current_tokens += section.tokens_estimate + 10
            elif current_tokens < max_tokens * 0.8:
                # Include partial section if we have room
                truncated = self._truncate_to_tokens(
                    section.content,
                    max_tokens - current_tokens
                )
                if truncated.strip():
                    result += f"\n{section.section_type.upper()} (PARTIAL):\n"
                    result += truncated + "\n"
                    current_tokens = max_tokens
                break
        
        return result if result else "Resume content too long for context window"
    
    def _estimate_tokens(self, text: str) -> int:
        """Estimate tokens using word count"""
        word_count = len(text.split())
        return int(word_count * self.AVERAGE_TOKENS_PER_WORD)
    
    def _truncate_to_tokens(self, text: str, max_tokens: int) -> str:
        """Truncate text to fit within token limit"""
        max_words = int(max_tokens / self.AVERAGE_TOKENS_PER_WORD)
        words = text.split()
        return " ".join(words[:max_words])
    
    def _truncate_at_limit(self, text: str, max_tokens: int) -> str:
        """Truncate text intelligently at token limit"""
        return self._truncate_to_tokens(text, int(max_tokens * 0.9))
    
    def _extract_must_haves(self, job_desc: str) -> List[str]:
        """Extract must-have requirements"""
        items = []
        
        # Look for explicit must-haves
        patterns = [
            r"must have.*?(?:\n|$)",
            r"required:.*?(?:\n\n|$)",
            r"\d+\+\s+years?.*?(?:\n|$)",
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, job_desc, re.IGNORECASE | re.DOTALL)
            items.extend(matches)
        
        # If no explicit must-haves found, use first few lines
        if not items:
            lines = job_desc.split('\n')[:10]
            items = [line.strip() for line in lines if len(line.strip()) > 20]
        
        return list(set(items))[:10]  # Top 10 unique items
    
    def _extract_responsibilities(self, job_desc: str) -> List[str]:
        """Extract key responsibilities"""
        items = []
        
        # Look for responsibility sections
        resp_patterns = [
            r"responsibilities?:.*?(?:\n\n|$)",
            r"will:.*?(?:\n\n|$)",
            r"you will:.*?(?:\n\n|$)",
        ]
        
        for pattern in resp_patterns:
            match = re.search(pattern, job_desc, re.IGNORECASE | re.DOTALL)
            if match:
                # Extract bullet points
                bullets = re.findall(r"[-•]\s+(.*?)(?:\n|$)", match.group(0))
                items.extend(bullets)
        
        return items[:10]  # Top 10
    
    def _extract_nice_to_haves(self, job_desc: str) -> List[str]:
        """Extract nice-to-have requirements"""
        items = []
        
        patterns = [
            r"nice to have.*?(?:\n\n|$)",
            r"preferred.*?(?:\n\n|$)",
            r"bonus.*?(?:\n\n|$)",
        ]
        
        for pattern in patterns:
            match = re.search(pattern, job_desc, re.IGNORECASE | re.DOTALL)
            if match:
                bullets = re.findall(r"[-•]\s+(.*?)(?:\n|$)", match.group(0))
                items.extend(bullets)
        
        return items[:5]  # Top 5
    
    def _format_list(self, items: List[str]) -> str:
        """Format list as readable text"""
        return "\n".join(f"• {item.strip()}" for item in items if item.strip())


# Singleton instance
_optimizer = None


def get_context_optimizer() -> ContextOptimizer:
    """Get singleton instance of context optimizer"""
    global _optimizer
    if _optimizer is None:
        _optimizer = ContextOptimizer()
    return _optimizer
