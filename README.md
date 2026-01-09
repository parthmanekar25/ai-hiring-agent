# AI Hiring Agent - Full Stack Application

## 🎯 Overview

A production-ready full-stack application for intelligent candidate evaluation using AI. Accepts job descriptions and candidate resumes (PDF/TXT), and provides:

- ✅ **Deep Resume Analysis** - Detailed assessment against job requirements
- ✅ **Fair Candidate Scoring** - 0-100 scores with transparent reasoning
- ✅ **Interview Question Generation** - Strategic, targeted questions
- ✅ **Skill Gap Analysis** - Missing skills and concerns identification
- ✅ **Functional UI** - Streamlit frontend with charts and visualizations

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Groq API Key (free at https://console.groq.com)

### Installation (5 minutes)

#### macOS/Linux
```bash
# Clone or navigate to project
cd ai-hiring-agent

# Create and activate virtual environment
python3 -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo "GROQ_API_KEY=your_actual_api_key" > .env
```

#### Windows
```bash
# Clone or navigate to project
cd ai-hiring-agent

# Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
echo GROQ_API_KEY=your_actual_api_key > .env
```

### Running the Application

#### Option A: Automated (Easiest)

**macOS/Linux:**
```bash
chmod +x start.sh
./start.sh
```

**Windows:**
```bash
start.bat
```

#### Option B: Manual (Separate Terminals)

**Terminal 1 - Backend:**
```bash
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python backend/main.py
```

Output should show:
```
Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
source .venv/bin/activate  # Windows: .venv\Scripts\activate
streamlit run frontend/app.py
```

Output should show:
```
You can now view your Streamlit app in your browser at:
  http://localhost:8501
```

### Using the Application

1. **Open browser:** http://localhost:8501
2. **Enter job description** - Paste the job requirements
3. **Upload resumes** - Select PDF or TXT files
4. **Click "Evaluate Candidates"** - Wait 45-70 seconds
5. **Review results:**
   - Candidates ranked by overall score
   - Detailed analysis for each candidate
   - Identified skill gaps and concerns
   - Suggested interview questions
6. **Download results** - Export as JSON for further analysis

## 📁 Project Structure

```
ai-hiring-agent/
├── backend/
│   ├── main.py                 # FastAPI server
│   ├── agents/                 # AI agents (Groq-based)
│   │   ├── resume_analyzer.py
│   │   ├── scorer.py
│   │   └── question_generator.py
│   ├── prompts/                # Advanced prompt engineering
│   │   ├── prompt_manager.py
│   │   ├── context_optimizer.py
│   │   └── chain_of_thought.py
│   ├── models/
│   │   └── schemas.py          # Data validation
│   └── utils/
│       ├── pdf_parser.py       # PDF extraction
│       └── helpers.py          # Utilities
│
├── frontend/
│   ├── app.py                  # Streamlit UI
│   └── services/
│       └── api.py              # API client
│
├── requirements.txt            # Dependencies
├── .env                        # Configuration (GROQ_API_KEY)
├── start.sh                    # Startup script (macOS/Linux)
├── start.bat                   # Startup script (Windows)
└── test_context_engineering.py # Test suite
```

## 🏗️ Architecture

### Data Flow
```
User Input (Frontend)
    ↓
Job Description + Resumes
    ↓
FastAPI Backend
    ↓
Resume Analysis → Scoring → Question Generation
    ↓
(All using Groq LLM + Advanced Context Engineering)
    ↓
Structured JSON Response
    ↓
Results Display (Frontend)
```

### Tech Stack
- **Frontend:** Streamlit (Python)
- **Backend:** FastAPI (Python)
- **LLM:** Groq (Mixtral 8x7b)
- **AI Framework:** LangChain
- **File Processing:** PyPDF2
- **Validation:** Pydantic

## ⚙️ Configuration

### Environment Variables (.env)
```
# Required
GROQ_API_KEY=your_groq_api_key

# Optional (defaults shown)
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
STREAMLIT_SERVER_PORT=8501
LOG_LEVEL=INFO
DEBUG=true
```

Get your Groq API key:
1. Visit https://console.groq.com
2. Create account (free)
3. Generate API key
4. Add to `.env` file

## 🧪 Testing

Run the test suite to verify everything is working:

```bash
python test_context_engineering.py
```

Expected output:
```
✓ Prompt Manager tests passed
✓ Context Optimizer tests passed
✓ Chain-of-Thought tests passed
✓ Integration test passed

ALL TESTS PASSED ✓
```

## 📊 Features & Capabilities

### Resume Analysis
- Extracts skills, experience, education
- Compares against job requirements
- Identifies keyword stuffing and red flags
- Assesses experience depth
- Notes inconsistencies and gaps

### Candidate Scoring
- Overall fit score (0-100)
- Technical skill match
- Experience relevance
- Education fit
- Reasoning and confidence

### Interview Questions
- Targeted, specific questions
- Addresses identified gaps
- Tests depth of knowledge
- Covers both technical and soft skills
- Includes follow-up strategies

### Results Export
- Download as JSON
- Share with team
- Track over time
- Integrate with HRIS

## 🎓 Understanding the Results

### Score Ranges
- **90-100**: Exceptional fit (rare)
- **75-89**: Strong fit
- **60-74**: Good fit with some gaps
- **40-59**: Marginal fit
- **Below 40**: Poor fit

### Confidence Indicators
- **Green badge**: High confidence (>0.85)
- **Yellow badge**: Medium confidence (0.6-0.85)
- **Red badge**: Low confidence (<0.6)

### Red Flags
- ⚠️ Keyword stuffing detected
- ⚠️ Inconsistent dates/timeline
- ⚠️ Exaggerated claims
- ⚠️ Gaps in employment
- ⚠️ Vague descriptions

## 🔧 Troubleshooting

### Backend Won't Start
```
❌ Error: "Address already in use :8000"
→ Kill existing process: lsof -ti:8000 | xargs kill -9
→ Or change port in backend/main.py

❌ Error: "GROQ_API_KEY not found"
→ Check .env file exists
→ Verify GROQ_API_KEY=your_key is set
→ Restart terminal/IDE
```

### Frontend Won't Connect
```
❌ Error: "Cannot connect to backend"
→ Ensure backend is running (python backend/main.py)
→ Check health: curl http://localhost:8000/health
→ Should return: {"status":"healthy"}
```

### PDF Upload Fails
```
❌ Error: "Error parsing PDF"
→ Try uploading as TXT instead
→ Ensure PDF is not encrypted
→ Check file isn't corrupted
```

### Slow Processing
```
⏱️ Normal: 45-70 seconds per candidate batch
→ Check Groq API status at console.groq.com
→ Verify internet connection
→ Reduce batch size (fewer resumes)
```

## 📚 Advanced Configuration

### Switching LLM Models
Edit `backend/agents/resume_analyzer.py`:
```python
self.llm = ChatGroq(
    api_key=api_key,
    model="mixtral-8x7b-32768",  # or "llama2-70b", etc.
    temperature=0.3
)
```

### Adjusting Prompt Versions
The system uses V3 prompts by default (includes few-shot + chain-of-thought).

To use V1 (basic):
```python
prompt = pm.get_prompt("resume_analyzer", PromptVersion.V1)
```

### Adding Custom Few-Shot Examples
Edit `backend/prompts/prompt_manager.py`:
```python
few_shot_examples=[
    {
        "input": {"job_description": "...", "resume": "..."},
        "output": {"analysis": "...", "reasoning": "..."}
    }
]
```

## 📖 Documentation

- **FULL_STACK_IMPLEMENTATION.md** - Complete architecture and flow
- **CONTEXT_ENGINEERING.md** - Advanced prompt engineering details
- **LLM_ARCHITECTURE.md** - System design and diagrams
- **QUICK_REFERENCE.md** - Quick lookup guide
- **PATH_FIX_SUMMARY.md** - Import path explanations

## 🚀 Deployment

### Local Network
```bash
# Change BACKEND_HOST in backend/main.py to your IP
# e.g., 192.168.1.100:8000

# Frontend clients can access:
# http://192.168.1.100:8501
```

### Docker (Optional)
```dockerfile
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
ENV GROQ_API_KEY=your_key
CMD ["sh", "-c", "python backend/main.py & streamlit run frontend/app.py"]
```

### Cloud Deployment
- **Heroku:** Add Procfile and deploy
- **AWS:** Use EC2 with Docker
- **GCP:** Deploy to Cloud Run
- **Azure:** Use App Service

## 📊 Performance Metrics

### Processing Time
- Resume Analysis: 20-30 seconds
- Scoring: 10-15 seconds
- Question Generation: 15-25 seconds
- **Total per candidate: 45-70 seconds**

### Context Efficiency
- System Prompt: 200 tokens (2.5%)
- Few-shot Examples: 1000 tokens (12.5%)
- Job + Resume: 3000 tokens (37.5%)
- Output Space: 3800 tokens (47.5%)
- **Efficiency: 95%**

### Scalability
- Single candidate: <2 minutes
- 5 candidates: 5-6 minutes
- 10 candidates: 10-12 minutes
- Batch processing available

## 🤝 Contributing

To improve the system:

1. **Test new prompts** - Update few-shot examples
2. **Adjust temperatures** - Fine-tune for your domain
3. **Add metrics** - Track hiring success
4. **Integrate feedback** - Learn from outcomes
5. **A/B test** - Compare prompt versions

## ❓ FAQ

**Q: Can I use a different LLM?**
A: Yes! Replace `ChatGroq` with any LangChain provider (OpenAI, Anthropic, etc.)

**Q: Does it support other file formats?**
A: Currently PDF and TXT. DOCX support can be added via `python-docx`

**Q: Can I run this offline?**
A: No, Groq API requires internet connection. But you can use local LLMs.

**Q: How accurate is the scoring?**
A: Depends on prompt quality. V3 prompts (default) are highly consistent.

**Q: Can I customize the questions?**
A: Yes, edit the question generation prompts in `prompt_manager.py`

## 📞 Support

For issues:
1. Check the **Troubleshooting** section above
2. Review **Documentation** files
3. Check test output: `python test_context_engineering.py`
4. Verify `.env` configuration

## 📄 License

This project is provided as-is for recruitment purposes.

## 🎉 Ready to Use!

Your application is **fully functional and ready for immediate use**.

**Start using it now:**
```bash
# macOS/Linux
./start.sh

# Windows
start.bat
```

Then open: **http://localhost:8501**

---

**Questions?** See the documentation files in the project root.

**Happy hiring! 🚀**
