"""
API Service Layer for Frontend
Handles all communication with FastAPI backend
"""

import requests
from typing import List, Dict, Any, Optional
import os
from dotenv import load_dotenv

load_dotenv()

class APIService:
    """Service class for backend API communication"""
    
    def __init__(self, base_url: str = None):
        self.base_url = base_url or os.getenv("BACKEND_URL", "http://localhost:8000")
        self.timeout = 120  # 2 minutes for LLM processing
    
    def health_check(self) -> Dict[str, Any]:
        """Check backend health status"""
        try:
            response = requests.get(
                f"{self.base_url}/health",
                timeout=5
            )
            return {
                "status": "healthy" if response.status_code == 200 else "unhealthy",
                "code": response.status_code
            }
        except requests.exceptions.ConnectionError:
            return {"status": "offline", "code": None}
        except Exception as e:
            return {"status": "error", "code": None, "message": str(e)}
    
    def evaluate_candidates(
        self,
        job_description: str,
        resume_files: List[tuple]
    ) -> Dict[str, Any]:
        """
        Evaluate candidates against job description
        
        Args:
            job_description: Job description text
            resume_files: List of (filename, file_content, mime_type) tuples
        
        Returns:
            Dictionary with evaluation results or error
        """
        try:
            # Prepare form data
            form_data = {"job_description": job_description}
            
            # Prepare files
            files = [
                ("resumes", (filename, content, mime_type))
                for filename, content, mime_type in resume_files
            ]
            
            # Make request
            response = requests.post(
                f"{self.base_url}/api/evaluate",
                data=form_data,
                files=files,
                timeout=self.timeout
            )
            
            if response.status_code == 200:
                return {
                    "success": True,
                    "data": response.json()
                }
            else:
                return {
                    "success": False,
                    "error": f"Backend returned {response.status_code}: {response.text}"
                }
        
        except requests.exceptions.Timeout:
            return {
                "success": False,
                "error": "Request timed out. Try with fewer resumes or simpler job description."
            }
        except requests.exceptions.ConnectionError:
            return {
                "success": False,
                "error": "Cannot connect to backend. Ensure it's running on the correct port."
            }
        except Exception as e:
            return {
                "success": False,
                "error": f"Unexpected error: {str(e)}"
            }
    
    def get_api_docs_url(self) -> str:
        """Get URL for API documentation"""
        return f"{self.base_url}/docs"


# Singleton instance
api_service = APIService()