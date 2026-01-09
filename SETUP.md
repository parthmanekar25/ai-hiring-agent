# Setup Guide

Complete installation and running instructions for the AI Hiring Agent.

## Prerequisites

- **Python:** 3.8 or higher
- **API Key:** Groq account (free tier at https://console.groq.com)
- **Disk Space:** ~500MB for dependencies
- **Internet:** Required for Groq API calls

## Step 1: Get Groq API Key

1. Visit https://console.groq.com
2. Sign up (free)
3. Navigate to API Keys section
4. Create new API key
5. Copy the key (you'll need it in Step 3)

> **Note:** Free tier includes generous rate limits (~100 requests/hour). Perfect for testing.

## Step 2: Install Dependencies

### macOS/Linux

```bash
# Navigate to project
cd ai-hiring-agent

# Create virtual environment
python3 -m venv .venv

# Activate virtual environment
source .venv/bin/activate

# Install Python packages
pip install -r requirements.txt
```

### Windows

```bash
# Navigate to project
cd ai-hiring-agent

# Create virtual environment
python -m venv .venv

# Activate virtual environment (choose one)
.venv\Scripts\activate          # Command Prompt
.venv\Scripts\Activate.ps1      # PowerShell

# Install Python packages
pip install -r requirements.txt
```

### Verify Installation

```bash
# Check Python version
python --version

# Check packages installed
pip list | grep -E "fastapi|streamlit|langchain"
```

Expected output:
```
fastapi               0.104.1
streamlit             1.29.0
langchain             0.1.x
langchain-groq        0.x.x
```

## Step 3: Configure Environment

### Create .env File

Create a file named `.env` in the project root:

```bash
# macOS/Linux
echo "GROQ_API_KEY=your_actual_api_key_here" > .env

# Windows (Command Prompt)
echo GROQ_API_KEY=your_actual_api_key_here > .env

# Or manually create .env with these contents:
GROQ_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

> **Important:** Never commit `.env` to version control. It's already in `.gitignore`.

### Verify Configuration

```bash
# Check .env exists
cat .env  # macOS/Linux
type .env  # Windows

# Should output:
# GROQ_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## Step 4: Run the Application

### Option A: Automated (Recommended)

```bash
# macOS/Linux
chmod +x start.sh
./start.sh

# Windows
start.bat
```

The scripts will:
1. Activate virtual environment
2. Start FastAPI backend (http://localhost:8000)
3. Start Streamlit frontend (http://localhost:8501)
4. Display URLs in terminal

### Option B: Manual

**Terminal 1 - Backend Server:**
```bash
source .venv/bin/activate  # Activate venv
python backend/main.py
```

Output should show:
```
Uvicorn running on http://0.0.0.0:8000
Press CTRL+C to quit
```

**Terminal 2 - Frontend UI:**
```bash
source .venv/bin/activate  # Activate venv
streamlit run frontend/app.py
```

Output should show:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

### Option C: Docker (Advanced)

```bash
docker build -t ai-hiring-agent .
docker run -p 8000:8000 -p 8501:8501 -e GROQ_API_KEY=your_key ai-hiring-agent
```

## Step 5: Access the Application

Open your browser and navigate to:

```
http://localhost:8501
```

You should see:
- Job description input field
- Resume upload area
- "Evaluate Candidates" button
- Sample results section

## Common Setup Issues

### Issue: "ModuleNotFoundError: No module named 'fastapi'"

**Solution:** Virtual environment not activated
```bash
source .venv/bin/activate  # macOS/Linux
.venv\Scripts\activate     # Windows
pip install -r requirements.txt
```

### Issue: "Address already in use :8000"

**Solution:** Kill existing process
```bash
# macOS/Linux
lsof -ti:8000 | xargs kill -9

# Windows (PowerShell)
netstat -ano | findstr :8000
taskkill /PID <PID> /F
```

Then restart: `python backend/main.py`

### Issue: "GROQ_API_KEY not found"

**Solution:** Create/verify .env file
```bash
# Check if .env exists
ls -la .env  # macOS/Linux
dir .env    # Windows

# If missing, create it:
echo "GROQ_API_KEY=your_key" > .env
```

### Issue: "Authentication error from Groq"

**Solution:** Verify API key
1. Check .env file has correct key
2. Visit https://console.groq.com to verify key is still valid
3. Try regenerating API key if needed
4. Restart backend: `python backend/main.py`

### Issue: PDF upload fails with "Error parsing PDF"

**Solution:** Try alternative formats
1. Try uploading as `.txt` instead of PDF
2. Ensure PDF is not encrypted/password-protected
3. Check file is not corrupted (try opening in reader first)
4. If all else fails, copy-paste resume text into TXT file

### Issue: "Connection refused" when accessing frontend

**Solution:** Ensure backend is running
```bash
# Check backend health
curl http://localhost:8000/health

# Expected output:
# {"status":"healthy"}

# If not running, start it:
python backend/main.py
```

## Testing the Setup

### 1. Backend Health Check

```bash
curl http://localhost:8000/health
```

Expected response:
```json
{"status": "healthy"}
```

### 2. Test with Sample Resume

Use the Streamlit UI:
1. Paste sample job description:
   ```
   Senior Python Developer
   Required: Python, FastAPI, PostgreSQL
   Experience: 5+ years
   ```

2. Create sample resume as .txt:
   ```
   John Doe
   Python Developer with 6 years of experience
   Skills: Python, FastAPI, PostgreSQL, Docker
   ```

3. Click "Evaluate Candidates"

Expected result: Score ~85, multiple skill matches

### 3. Direct API Test

```bash
# Create test files
echo "Senior Python Developer\nRequired: Python, FastAPI" > job.txt
echo "John Doe\nPython Developer, 6 years\nSkills: Python, FastAPI" > resume.txt

# Send to API
curl -X POST http://localhost:8000/api/evaluate \
  -F "job_description=Senior Python Developer" \
  -F "resumes=@resume.txt"
```

## Next Steps

1. ✅ Complete setup (you are here)
2. 📖 Read [ARCHITECTURE.md](ARCHITECTURE.md) to understand how it works
3. 🔌 Check [API.md](API.md) for API documentation
4. 🎯 Review [DECISIONS.md](DECISIONS.md) for design choices
5. 🚀 Start using: Upload real resumes and job descriptions

## Environment Variables Reference

| Variable | Required | Default | Purpose |
|----------|----------|---------|---------|
| `GROQ_API_KEY` | Yes | - | Groq API authentication key |
| `BACKEND_HOST` | No | 0.0.0.0 | Backend server host |
| `BACKEND_PORT` | No | 8000 | Backend server port |
| `STREAMLIT_SERVER_PORT` | No | 8501 | Streamlit UI port |
| `LOG_LEVEL` | No | INFO | Logging verbosity (DEBUG, INFO, WARNING, ERROR) |
| `DEBUG` | No | true | Enable debug mode |

To override defaults, add to `.env`:
```bash
GROQ_API_KEY=your_key
BACKEND_PORT=9000
DEBUG=false
```

## System Requirements

### Minimum
- **RAM:** 2GB
- **CPU:** 2 cores
- **Network:** 5 Mbps (for Groq API)
- **Python:** 3.8+

### Recommended
- **RAM:** 4GB
- **CPU:** 4+ cores
- **Network:** 10+ Mbps
- **Python:** 3.10+

## Performance

Typical processing times:
- Single resume: 45-70 seconds
- 5 resumes: 5-8 minutes
- API response time: 50-80 seconds

> Slower on first run due to model loading. Subsequent requests are faster.

## Deactivating Virtual Environment

When done working:

```bash
# macOS/Linux & Windows
deactivate

# Or exit the terminal
```

---

Need help? Check the troubleshooting section above or review [README.md](README.md) for overview.
