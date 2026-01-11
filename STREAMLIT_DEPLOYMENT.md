# 🚀 Streamlit Deployment Guide

## Quick Start - Streamlit Cloud

### Prerequisites
- GitHub repository: https://github.com/parthmanekar25/ai-hiring-agent
- Streamlit Cloud account: https://share.streamlit.io
- Groq API key: https://console.groq.com

### Step 1: Prepare the Repository
```bash
git add .
git commit -m "fix: streamlit deployment configuration"
git push origin main
```

### Step 2: Deploy to Streamlit Cloud
1. Go to https://share.streamlit.io
2. Click "New app"
3. Connect GitHub account
4. Select repository: `parthmanekar25/ai-hiring-agent`
5. Main file path: `streamlit_app.py`
6. Python version: 3.11
7. Click "Deploy"

### Step 3: Add Secrets (After Deployment)
1. Wait for app to finish deploying
2. Click the menu (≡) in top right
3. Select "Settings"
4. Click "Secrets" tab
5. Add the following:
   ```
   GROQ_API_KEY = "your-actual-groq-api-key"
   BACKEND_URL = "your-backend-url-here"
   ```
6. Save

## Architecture

### Frontend (Streamlit) - Streamlit Cloud
- **Location:** `streamlit_app.py` (entry point)
- **Config:** `.streamlit/config.toml`
- **URL:** Will be assigned by Streamlit Cloud

### Backend (FastAPI) - Separate Hosting Required
The backend needs to be deployed separately since Streamlit Cloud doesn't support long-running processes like FastAPI.

**Deploy backend to:**
- **Render:** https://render.com (free tier available)
- **Railway:** https://railway.app
- **Heroku:** https://heroku.com
- **AWS:** EC2, Lambda, or Lightsail
- **Digital Ocean:** App Platform or Droplets

**Example: Deploy to Render**

1. Create account at https://render.com
2. Create new "Web Service"
3. Connect GitHub repository
4. Settings:
   - Name: `ai-hiring-agent-backend`
   - Root Directory: `/`
   - Build Command: `pip install -r requirements.txt`
   - Start Command: `uvicorn backend.main:app --host 0.0.0.0 --port 8000`
   - Environment: Add `GROQ_API_KEY`
5. Create Service

5. Get the deployed backend URL (e.g., https://ai-hiring-agent-backend.onrender.com)
6. Add this URL to Streamlit Secrets as `BACKEND_URL`

## Environment Variables

### Streamlit Cloud Secrets
Add to `.streamlit/secrets.toml` (via Streamlit UI):
```
GROQ_API_KEY = "your-key"
BACKEND_URL = "https://your-backend-url.onrender.com"
```

### Local Development
Create `.env` file:
```
GROQ_API_KEY=your-key
BACKEND_URL=http://localhost:8000
```

## Troubleshooting

### Issue: "ModuleNotFoundError: No module named 'frontend'"
**Solution:** Ensure `streamlit_app.py` is in project root and imports are correct

### Issue: Backend connection timeout
**Solution:** 
1. Check BACKEND_URL is correct in secrets
2. Verify backend is running and deployed
3. Check firewall/CORS settings

### Issue: File upload limit exceeded
**Solution:** Set `maxUploadSize` in `.streamlit/config.toml` (default is 200MB)

### Issue: GROQ API key not working
**Solution:**
1. Get fresh key from https://console.groq.com
2. Update in Streamlit Cloud secrets
3. Wait for app to restart

## Local Development

### Run Locally Before Deploying
```bash
# Terminal 1: Backend
python backend/main.py

# Terminal 2: Frontend
streamlit run streamlit_app.py
```

Access at: http://localhost:8501

## Files Added/Modified

### New Files
- `streamlit_app.py` - Streamlit entry point
- `.streamlit/config.toml` - Streamlit configuration
- `.streamlit/secrets.toml.example` - Secrets template
- `STREAMLIT_DEPLOYMENT.md` - This guide

### Modified Files
- `requirements.txt` - Updated versions for compatibility
  - pandas: 2.1.3 → >=2.2.0 (Python 3.13 compatibility)
  - streamlit: 1.29.0 → 1.31.1
  - Removed: psycopg2-binary, sqlalchemy, pymongo

## Performance Tips

1. **Cache agent responses** to reduce API calls
2. **Lazy load components** for faster initial load
3. **Use session state** to maintain data between reruns
4. **Optimize prompts** for faster LLM responses
5. **Consider rate limiting** for Groq API

## Monitoring

### Streamlit Cloud Logs
- Access via app menu → "Manage App" → terminal output

### Backend Logs (Render example)
- Go to service dashboard → "Logs" tab

### Common Issues to Monitor
- Rate limiting: "429 Too Many Requests"
- API key invalid: "401 Unauthorized"
- Backend down: "Connection refused"

## Next Steps

1. ✅ Update requirements.txt
2. ✅ Create Streamlit config
3. ✅ Create entry point
4. ✅ Deploy to Streamlit Cloud
5. Deploy backend separately
6. Add secrets to Streamlit Cloud
7. Test end-to-end
8. Share with team!

---

**Need Help?**
- Streamlit Docs: https://docs.streamlit.io
- Groq Docs: https://console.groq.com/docs
- Community: https://discuss.streamlit.io
