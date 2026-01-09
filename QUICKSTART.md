# Quick Start Guide: Running the AI Hiring Agent

## Prerequisites

1. ✅ Python 3.9+
2. ✅ Virtual environment activated (`.venv`)
3. ✅ Dependencies installed (`pip install -r requirements.txt`)
4. ✅ Port 8000 is free (for backend)
5. ✅ Port 8501 is free (for frontend)

## Option 1: Run Both Backend and Frontend (Recommended)

### Terminal 1: Start Backend
```bash
cd /Users/parth/Projects/ai-hiring-agent
python backend/main.py
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000 (Press CTRL+C to quit)
```

### Terminal 2: Start Frontend
```bash
cd /Users/parth/Projects/ai-hiring-agent
streamlit run frontend/app.py
```

You should see:
```
Local URL: http://localhost:8501
Network URL: http://192.168.x.x:8501
```

## Option 2: Using Bash from Root Directory

### From the project root:
```bash
# Terminal 1
python backend/main.py

# Terminal 2
cd frontend && streamlit run app.py
```

## Troubleshooting

### Issue: `ModuleNotFoundError: No module named 'frontend'`
**Solution**: Run streamlit from the project root directory:
```bash
cd /Users/parth/Projects/ai-hiring-agent
streamlit run frontend/app.py
```

### Issue: Port 8000 already in use
**Solution**: Kill the process using port 8000:
```bash
lsof -i :8000  # Find what's using it
kill -9 <PID>  # Kill the process
```

### Issue: Backend returns connection error
**Solution**: Make sure backend is running:
1. Check terminal 1 is still running
2. Verify http://localhost:8000/health returns `{"status": "ok"}`

### Issue: Streamlit won't start
**Solution**: Make sure port 8501 is free:
```bash
lsof -i :8501  # Check what's using it
kill -9 <PID>  # Kill if needed
```

## Testing the Application

### 1. Upload Resumes & Job Description
- Paste a job description
- Upload 1-3 resume files (PDF or TXT)

### 2. Click "Evaluate Candidates"
- Wait for evaluation to complete
- Should see candidate scores and analysis

### 3. See Explainability Artifacts
- View hiring recommendation (🟢🟡🔴)
- See training plan with costs
- Check investment analysis with ROI
- Download reports (JSON, Text, Markdown)

## Environment Variables

Create a `.env` file in project root if needed:

```bash
# Backend
BACKEND_URL=http://localhost:8000
GROQ_API_KEY=your_groq_key_here

# Frontend
STREAMLIT_CLIENT_LOGGER_LEVEL=warning
```

## What to Expect

### Initial Load
- ~5-10 seconds for frontend to initialize
- Backend should respond immediately

### Evaluation Process
- For 3 candidates: ~30-60 seconds
- Shows progress bar and status messages
- Results with explainability artifacts

### Explainability Display
For each candidate:
```
🟡 HIRE_WITH_TRAINING (87% confidence)

Training Plan:
- Kubernetes: 100 hrs (~10 wks, $1,500)
- AWS: 120 hrs (~12 wks, $1,800)
- Total: 250 hrs (~25 wks, $3,450)

Investment Analysis:
- Break-even: 25 weeks
- Month 1: 45% productivity
- Month 6: 95% productivity

[📥 JSON] [📝 Text] [📋 Markdown]
```

## Project Structure

```
ai-hiring-agent/
├── backend/              # FastAPI backend
│   └── main.py          # Backend entry point (python backend/main.py)
├── frontend/            # Streamlit frontend
│   ├── app.py           # Frontend entry point (streamlit run frontend/app.py)
│   └── services/
│       ├── api.py       # API service layer
│       └── explainability.py  # Explainability service
└── requirements.txt     # Python dependencies
```

## Getting Help

- **Backend Docs**: See `EXPLAINABILITY_IMPLEMENTATION.md`
- **Frontend Docs**: See `FRONTEND_INTEGRATION.md`
- **Architecture**: See `EXPLAINABILITY_ARCHITECTURE.md`
- **Examples**: See `EXPLAINABILITY_QUICKSTART.md`

## Common Commands

```bash
# Check if backend is running
curl http://localhost:8000/health

# Check if frontend is running
curl http://localhost:8501

# Kill process on port 8000
lsof -i :8000 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Kill process on port 8501
lsof -i :8501 | grep -v COMMAND | awk '{print $2}' | xargs kill -9

# Reinstall dependencies
pip install -r requirements.txt --force-reinstall

# View backend logs
tail -f backend/logs/app.log
```

## Performance Tips

1. **Use 2-3 resumes** for testing (faster evaluation)
2. **Use specific job descriptions** (better results)
3. **Wait for backend to fully start** before opening frontend
4. **Close other browsers tabs** to reduce memory usage

## Success Indicators

✅ Backend running: Terminal 1 shows `Uvicorn running on http://127.0.0.1:8000`  
✅ Frontend running: Terminal 2 shows `Local URL: http://localhost:8501`  
✅ App loaded: Browser shows "AI Hiring Agent" title  
✅ Evaluation works: Upload files and click evaluate  
✅ Explainability shows: See hiring decisions, training plans, ROI

---

**Ready to go! Start both terminals and open http://localhost:8501 in your browser.** 🚀
