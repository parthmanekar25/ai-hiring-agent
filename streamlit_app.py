"""
AI Hiring Agent - Streamlit Entry Point
Main application file for Streamlit Cloud deployment
"""

import sys
import os

# Add project root to Python path
project_root = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, project_root)

# Import and run the frontend app
from frontend.app import main

if __name__ == "__main__":
    main()
