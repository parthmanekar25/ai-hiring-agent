import streamlit as st
import requests
import json
import time
from typing import List
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configuration
BACKEND_URL = os.getenv("BACKEND_URL", "http://localhost:8000")

# Page configuration
st.set_page_config(
    page_title="AI Hiring Agent",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 1rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        margin-bottom: 2rem;
    }
    .candidate-card {
        background-color: #f8f9fa;
        padding: 1.5rem;
        border-radius: 10px;
        margin-bottom: 1.5rem;
        border-left: 5px solid #1f77b4;
    }
    .score-badge {
        display: inline-block;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: bold;
        margin: 0.25rem;
    }
    .score-high {
        background-color: #d4edda;
        color: #155724;
    }
    .score-medium {
        background-color: #fff3cd;
        color: #856404;
    }
    .score-low {
        background-color: #f8d7da;
        color: #721c24;
    }
    .skill-present {
        background-color: #d4edda;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        margin: 0.25rem;
        display: inline-block;
    }
    .skill-missing {
        background-color: #f8d7da;
        padding: 0.25rem 0.5rem;
        border-radius: 5px;
        margin: 0.25rem;
        display: inline-block;
    }
    .stButton>button {
        width: 100%;
        background-color: #1f77b4;
        color: white;
        font-weight: bold;
        padding: 0.75rem;
        border-radius: 5px;
        border: none;
    }
    .stButton>button:hover {
        background-color: #155a8a;
    }
</style>
""", unsafe_allow_html=True)


def get_score_class(score: float) -> str:
    """Return CSS class based on score"""
    if score >= 75:
        return "score-high"
    elif score >= 60:
        return "score-medium"
    else:
        return "score-low"


def check_backend_health() -> bool:
    """Check if backend is running"""
    try:
        response = requests.get(f"{BACKEND_URL}/health", timeout=5)
        return response.status_code == 200
    except:
        return False


def evaluate_candidates(job_description: str, resume_files: List) -> dict:
    """Send evaluation request to backend"""
    files = []
    form_data = {"job_description": job_description}
    
    try:
        # Prepare files for upload
        for resume_file in resume_files:
            files.append(
                ("resumes", (resume_file.name, resume_file.getvalue(), resume_file.type))
            )
        
        # Make request to backend
        response = requests.post(
            f"{BACKEND_URL}/api/evaluate",
            data=form_data,
            files=files,
            timeout=120  # 2 minutes timeout for processing
        )
        
        if response.status_code == 200:
            return {"success": True, "data": response.json()}
        else:
            return {
                "success": False,
                "error": f"Backend error: {response.status_code} - {response.text}"
            }
    
    except requests.exceptions.Timeout:
        return {"success": False, "error": "Request timed out. Please try with fewer resumes."}
    except requests.exceptions.ConnectionError:
        return {"success": False, "error": "Cannot connect to backend. Make sure it's running on port 8000."}
    except Exception as e:
        return {"success": False, "error": f"Error: {str(e)}"}


def display_candidate_evaluation(evaluation: dict, rank: int):
    """Display individual candidate evaluation"""
    with st.container():
        st.markdown(f"""
        <div class="candidate-card">
            <h2>🏆 Rank #{rank} - {evaluation['candidate_name']}</h2>
            <p style="color: #666;"><i>{evaluation['filename']}</i></p>
        </div>
        """, unsafe_allow_html=True)
        
        # Scores section
        col1, col2, col3, col4 = st.columns(4)
        
        score = evaluation['score']
        with col1:
            st.metric("Overall Score", f"{score['overall_score']:.0f}/100")
        with col2:
            st.metric("Technical Fit", f"{score['technical_fit']:.0f}/100")
        with col3:
            st.metric("Experience Fit", f"{score['experience_fit']:.0f}/100")
        with col4:
            st.metric("Education Fit", f"{score['education_fit']:.0f}/100")
        
        # Reasoning
        with st.expander("📝 Evaluation Reasoning", expanded=True):
            st.write(score['reasoning'])
        
        # Summary
        if evaluation.get('summary'):
            with st.expander("📄 Executive Summary"):
                st.write(evaluation['summary'])
        
        # Skill Matches
        with st.expander("💡 Skill Analysis"):
            if evaluation['skill_matches']:
                for skill in evaluation['skill_matches']:
                    if skill['present']:
                        st.markdown(f"""
                        <span class="skill-present">✓ {skill['skill']}</span>
                        """, unsafe_allow_html=True)
                        if skill.get('evidence'):
                            st.caption(f"Evidence: {skill['evidence']}")
                    else:
                        st.markdown(f"""
                        <span class="skill-missing">✗ {skill['skill']}</span>
                        """, unsafe_allow_html=True)
            else:
                st.info("No specific skill matches analyzed")
        
        # Gaps and Concerns
        gaps = evaluation['gaps']
        if any([gaps['missing_skills'], gaps['unclear_sections'], gaps['inconsistencies']]):
            with st.expander("⚠️ Gaps & Concerns"):
                if gaps['missing_skills']:
                    st.subheader("Missing Skills")
                    for skill in gaps['missing_skills']:
                        st.markdown(f"- {skill}")
                
                if gaps['unclear_sections']:
                    st.subheader("Unclear Sections")
                    for section in gaps['unclear_sections']:
                        st.markdown(f"- {section}")
                
                if gaps['inconsistencies']:
                    st.subheader("Inconsistencies")
                    for inconsistency in gaps['inconsistencies']:
                        st.markdown(f"- {inconsistency}")
        
        # Interview Questions
        if evaluation['interview_questions']:
            with st.expander("❓ Suggested Interview Questions"):
                for i, question in enumerate(evaluation['interview_questions'], 1):
                    st.markdown(f"**Q{i}:** {question['question']}")
                    st.caption(f"Category: {question['category']}")
                    st.caption(f"Purpose: {question['reasoning']}")
                    st.divider()
        
        st.divider()


def main():
    # Header
    st.markdown('<h1 class="main-header">🤖 AI Hiring Agent</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Intelligent candidate evaluation powered by AI agents</p>',
        unsafe_allow_html=True
    )
    
    # Sidebar
    with st.sidebar:
        st.header("ℹ️ About")
        st.info("""
        This AI-powered hiring assistant helps you:
        - Analyze resumes against job requirements
        - Score candidates consistently
        - Identify skill gaps and concerns
        - Generate targeted interview questions
        - Detect keyword stuffing and inconsistencies
        """)
        
        st.header("🔧 Backend Status")
        if check_backend_health():
            st.success("✅ Backend Connected")
        else:
            st.error("❌ Backend Offline")
            st.warning("Make sure FastAPI backend is running on port 8000")
        
        st.header("📊 How It Works")
        st.markdown("""
        1. **Resume Analyzer Agent**: Deep analysis of qualifications
        2. **Scorer Agent**: Consistent scoring with reasoning
        3. **Question Generator**: Targeted interview questions
        """)
    
    # Main content
    tab1, tab2 = st.tabs(["📝 Evaluate Candidates", "📖 Instructions"])
    
    with tab1:
        # Job Description Input
        st.subheader("1️⃣ Job Description")
        job_description = st.text_area(
            "Paste the job description here",
            height=250,
            placeholder="Enter the complete job description including requirements, responsibilities, and qualifications...",
            help="Be specific and detailed for better candidate evaluation"
        )
        
        # Resume Upload
        st.subheader("2️⃣ Upload Candidate Resumes")
        uploaded_files = st.file_uploader(
            "Upload resumes (PDF or TXT format)",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            help="You can upload multiple resumes at once"
        )
        
        if uploaded_files:
            st.success(f"✅ {len(uploaded_files)} resume(s) uploaded")
            with st.expander("View uploaded files"):
                for file in uploaded_files:
                    st.write(f"- {file.name} ({file.size / 1024:.1f} KB)")
        
        # Evaluate Button
        st.subheader("3️⃣ Evaluate")
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            evaluate_btn = st.button("🚀 Evaluate Candidates", use_container_width=True)
        
        # Process evaluation
        if evaluate_btn:
            if not job_description.strip():
                st.error("⚠️ Please enter a job description")
            elif not uploaded_files:
                st.error("⚠️ Please upload at least one resume")
            else:
                with st.spinner("🔄 Analyzing candidates... This may take a minute..."):
                    progress_bar = st.progress(0)
                    status_text = st.empty()
                    
                    # Simulate progress (actual processing happens in backend)
                    for i in range(100):
                        time.sleep(0.05)
                        progress_bar.progress(i + 1)
                        if i < 30:
                            status_text.text("Parsing resumes...")
                        elif i < 60:
                            status_text.text("Analyzing qualifications...")
                        elif i < 90:
                            status_text.text("Scoring candidates...")
                        else:
                            status_text.text("Generating questions...")
                    
                    # Make actual API call
                    result = evaluate_candidates(job_description, uploaded_files)
                    
                    progress_bar.empty()
                    status_text.empty()
                
                if result['success']:
                    data = result['data']
                    st.success(f"✅ Evaluation complete! Processed in {data['processing_time']:.1f}s")
                    
                    # Display results
                    st.header("📊 Evaluation Results")
                    st.markdown("---")
                    
                    # Check if we have evaluations
                    if not data['evaluations']:
                        st.warning("⚠️ No candidates were successfully evaluated. Please check your uploads and try again.")
                    else:
                        # Summary metrics
                        col1, col2, col3 = st.columns(3)
                        with col1:
                            st.metric("Total Candidates", len(data['evaluations']))
                        with col2:
                            if len(data['evaluations']) > 0:
                                avg_score = sum(e['score']['overall_score'] for e in data['evaluations']) / len(data['evaluations'])
                                st.metric("Average Score", f"{avg_score:.1f}/100")
                            else:
                                st.metric("Average Score", "N/A")
                        with col3:
                            st.metric("Processing Time", f"{data['processing_time']:.1f}s")
                        
                        st.markdown("---")
                        
                        # Display each candidate
                        for rank, evaluation in enumerate(data['evaluations'], 1):
                            display_candidate_evaluation(evaluation, rank)
                        
                        # Download results
                        st.subheader("💾 Download Results")
                        json_str = json.dumps(data, indent=2)
                        st.download_button(
                            label="📥 Download JSON Results",
                            data=json_str,
                            file_name="candidate_evaluations.json",
                            mime="application/json"
                        )
                
                else:
                    st.error(f"❌ Evaluation failed: {result['error']}")
    
    with tab2:
        st.header("📖 How to Use")
        
        st.markdown("""
        ### Setup Requirements
        1. Ensure the FastAPI backend is running (`python backend/main.py`)
        2. Backend should be accessible at `http://localhost:8000`
        3. You need a valid OpenAI API key configured in the backend
        
        ### Evaluation Process
        1. **Paste Job Description**: Include all requirements, responsibilities, and qualifications
        2. **Upload Resumes**: PDF or TXT format, multiple files supported
        3. **Click Evaluate**: The AI agents will analyze each candidate
        
        ### What You Get
        - **Overall Score**: 0-100 rating based on job fit
        - **Skill Analysis**: Which required skills are present/missing
        - **Gap Analysis**: Missing skills, unclear sections, inconsistencies
        - **Interview Questions**: Targeted questions based on candidate's profile
        - **Detailed Reasoning**: Transparent explanation of scores
        
        ### Tips for Best Results
        - Be specific in job descriptions
        - Include all must-have and nice-to-have skills
        - Upload clean, well-formatted resumes
        - Review the reasoning behind scores
        - Use generated questions as interview starting points
        
        ### Anti-Keyword-Stuffing
        The AI agents are trained to:
        - Look for concrete examples and achievements
        - Identify vague or unsubstantiated claims
        - Detect inconsistencies in experience
        - Value quality over quantity of keywords
        
        ### Scoring Scale
        - **90-100**: Exceptional fit (rare)
        - **75-89**: Strong fit
        - **60-74**: Good fit with some gaps
        - **40-59**: Marginal fit
        - **Below 40**: Poor fit
        """)
        
        st.header("⚡ Sample Data")
        st.info("Sample job descriptions and resumes are available in the `samples/` directory for testing.")


if __name__ == "__main__":
    main()